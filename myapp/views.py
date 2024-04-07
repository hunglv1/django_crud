import jwt
import bcrypt
import logging
from django.db.models import Max, Min
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer, CustomerToken, Plan, CustomerPlan
from .serializers import CustomerSerializer, PlanSerializer, CustomerPlanSerializer

logger = logging.getLogger(__name__)


def encrypt_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


class CustomerCreateView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            # Encrypt password before saving
            serializer.validated_data['password'] = encrypt_password(serializer.validated_data['password'])

            # Create customer
            customer = serializer.save()

            # Generate token
            token = jwt.encode({'customer_id': customer.id}, settings.JWT_SECRET_KEY, algorithm='HS256')

            # Save token to customer_token table
            CustomerToken.objects.create(token=token, customer=customer)

            # Prepare response data
            response_data = {
                'status': 'success',
                'message': 'Customer created successfully',
                'token': token
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyAPIView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info("Received request for MyAPIView")

        # Get token from request body
        token = request.data.get('token')

        try:
            # Verify token
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])

            # Get customer_id from token payload
            customer_id = payload['customer_id']

            # Fetch customer from database
            customer = Customer.objects.get(id=customer_id)

            logger.info(f"Action performed successfully for customer: {customer}")

            return Response({'status': 'success', 'message': 'Action performed successfully'},
                            status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            return Response({'status': 'error', 'message': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            return Response({'status': 'error', 'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except Customer.DoesNotExist:
            logger.error("Customer not found")
            return Response({'status': 'error', 'message': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)


class CustomerListView(APIView):
    def get(self, request, format=None):
        logger.info("Received request for customer list")

        # Get the Bearer token from the request headers
        token = request.headers.get('Authorization', '').split('Bearer ')[-1]

        # Check if the token exists in the CustomerToken table
        # try:
        #     customer_token = CustomerToken.objects.get(token=token)
        # except CustomerToken.DoesNotExist:
        #     return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        # If token is valid, proceed to fetch and return all customers
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class CustomerDetailView(APIView):
    def get(self, request, email, format=None):
        try:
            customer = Customer.objects.get(email=email)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)


class CustomerUpdateView(APIView):
    def put(self, request, pk, format=None):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({'message': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDeleteView(APIView):
    def delete(self, request, pk, format=None):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({'message': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlanCreateView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            # Create plan
            plan = serializer.save()

            # Prepare response data
            response_data = {
                'status': 'success',
                'message': 'Plan created successfully',
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanListView(APIView):
    def get(self, request, format=None):
        logger.info("Received request for plan list")

        # Get the Bearer token from the request headers
        token = request.headers.get('Authorization', '').split('Bearer ')[-1]

        # Check if the token exists in the CustomerToken table
        # try:
        #     customer_token = CustomerToken.objects.get(token=token)
        # except CustomerToken.DoesNotExist:
        #     return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        # If token is valid, proceed to fetch and return all customers
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)


class CustomerPlanCreateView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = CustomerPlanSerializer(data=request.data)
        if serializer.is_valid():
            # Create CustomerPlan
            customer_plan = serializer.save()

            # Prepare response data
            response_data = {
                'status': 'success',
                'message': 'CustomerPlan created successfully',
                'customer_plan_id': customer_plan.id
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerPlanListView(APIView):
    def get(self, request, format=None):
        logger.info("Received request for CustomerPlan list")

        # Get the Bearer token from the request headers
        token = request.headers.get('Authorization', '').split('Bearer ')[-1]

        # Check if the token exists in the CustomerToken table
        # try:
        #     customer_token = CustomerToken.objects.get(token=token)
        # except CustomerToken.DoesNotExist:
        #     return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        # If token is valid, proceed to fetch and return all customers
        customerPlan = CustomerPlan.objects.all()
        serializer = CustomerPlanSerializer(customerPlan, many=True)
        return Response(serializer.data)


"""
function to get max CustomerPlan which has the highest Plan price
"""


class CustomerPlanHighestPriceView(APIView):
    def get(self, request, format=None):
        logger.info("Received request for CustomerPlan with the highest priced Plan")

        # Get the ID of the Plan with the highest price
        highest_price = Plan.objects.aggregate(max_price=Max('price'))['max_price']

        # Get the CustomerPlan associated with the Plan having the highest price
        customer_plan = CustomerPlan.objects.filter(plan__price=highest_price).first()

        if customer_plan:
            serializer = CustomerPlanSerializer(customer_plan)
            return Response(serializer.data)
        else:
            return Response({"message": "No CustomerPlan found with the highest priced Plan"},
                            status=status.HTTP_404_NOT_FOUND)
