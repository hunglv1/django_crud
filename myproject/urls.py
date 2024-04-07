"""
URL configuration for st_report project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.urls import path
# from myapp.views import CustomerList, CustomerListCreate
#
# urlpatterns = [
#     path('customers/', CustomerList.as_view(), name='customer-list'),
#     path('customers/create/', CustomerListCreate.as_view(), name='customer-create'),
# ]




# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from myapp.views import CustomerViewSet, PlanViewSet, CustomerPlanViewSet, PaymentViewSet, CustomerTokenViewSet

# router = DefaultRouter()
# router.register(r'customers', CustomerViewSet)
# router.register(r'plans', PlanViewSet)
# router.register(r'customer-plans', CustomerPlanViewSet)
# router.register(r'payments', PaymentViewSet)
# router.register(r'customer-tokens', CustomerTokenViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.urls import path
from myapp.views import (
    CustomerCreateView,
    MyAPIView,
    CustomerListView,
    CustomerDetailView,
    CustomerUpdateView,
    CustomerDeleteView,
    PlanCreateView,
    PlanListView,
    CustomerPlanCreateView,
    CustomerPlanListView,
    CustomerPlanHighestPriceView
)


urlpatterns = [
    path('create-customer/', CustomerCreateView.as_view(), name='create-customer'),
    path('my-api/', MyAPIView.as_view(), name='my-api'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customers/<str:email>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('customers/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer-update'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete'),

    path('createPlan/', PlanCreateView.as_view(), name='create-plan'),
    path('plans/', PlanListView.as_view(), name='plan-list'),

    path('createCustomerPlan/', CustomerPlanCreateView.as_view(), name='create-customer-plan'),
    path('customerPlan/', CustomerPlanListView.as_view(), name='customer-plan-list'),
    path('highestCustomerPlan/', CustomerPlanHighestPriceView.as_view(), name='highest-customer-plan'),
]
