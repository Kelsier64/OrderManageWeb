from django.urls import path
from .views import (
    HomeView, RegistView, UserManageView,UserDelView, 
    UserEditView,CheckView,ProductView,CreateProductView,OrderDelView,
    ProductDelView,EditProductView,
)

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("userManage/regist/", RegistView.as_view(), name='regist'),
    path("userManage/", UserManageView.as_view(), name='userManage'),
    path("userManage/delete/", UserDelView.as_view(), name='userDel'),
    path("userManage/edit/", UserEditView.as_view(), name='edit'),
    path("check/", CheckView.as_view(), name='check'),
    path("productManage/", ProductView.as_view(), name='productManage'),
    path("productManage/create/", CreateProductView.as_view(), name='create'),
    path("check/delete/", OrderDelView.as_view(), name='delete'),
    path("productManage/delete/", ProductDelView.as_view(), name='delete'),
    path("productManage/edit/", EditProductView.as_view(), name='edit'),
    
]
