from django.urls import path
from . import views

from .views import (
    OrderView,
    CheckView,
    HomeView,
)
urlpatterns = [
    path("order/", OrderView.as_view(), name='order'),
    path("check/", CheckView.as_view(), name='check'),
    path("", HomeView.as_view(), name='home'),
]