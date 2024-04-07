from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        db_table = 'customer'


class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    class Meta:
        db_table = 'plan'


class CustomerPlan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    using_status = models.CharField(max_length=100)

    class Meta:
        db_table = 'customer_plan'


class Payment(models.Model):
    customer_plan = models.ForeignKey(CustomerPlan, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_date = models.DateField()

    class Meta:
        db_table = 'payment'


class CustomerToken(models.Model):
    token = models.CharField(max_length=600)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'customer_token'
