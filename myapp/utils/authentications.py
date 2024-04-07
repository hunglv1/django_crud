# myapp/utils/authentications.py

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from myapp.models import CustomerToken


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization', '').split('Bearer ')[-1]

        if not token:
            return None

        try:
            customer_token = CustomerToken.objects.get(token=token)
        except CustomerToken.DoesNotExist:
            raise AuthenticationFailed('Unauthorized')

        return (customer_token.customer, None)
