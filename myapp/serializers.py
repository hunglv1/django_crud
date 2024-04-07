from rest_framework import serializers
from .models import Customer, Plan, CustomerPlan, Payment, CustomerToken


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class CustomerPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPlan
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class CustomerTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerToken
        fields = '__all__'
