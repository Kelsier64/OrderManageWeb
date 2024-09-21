from django.contrib import admin
from django.urls import path,include
from base.views import (
    LoginView,LogoutView,IndexView
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('customer/', include('customer.urls')),
    path('op/', include('op.urls')),
    path('base/', include('base.urls')),
]
