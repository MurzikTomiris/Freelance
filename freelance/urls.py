from django.urls import path
from .views import (
    MainPageView,    
    ServiceListView,
    ServiceDetailView,
    OrderListView,
    OrderDetailView,
    ExecutorListView,
    ExecutorDetailView,
    CustomerListView,
    CustomerDetailView,
)

urlpatterns = [
    path("", MainPageView.as_view(), name="main_page"),
    path("executors/", ExecutorListView.as_view(), name="executor-list"),
    path("executors/<int:pk>/", ExecutorDetailView.as_view(), name="executor-detail"),
    path("customers/", CustomerListView.as_view(), name="customer-list"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("services/<int:pk>/", ServiceDetailView.as_view(), name="service-detail"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]
