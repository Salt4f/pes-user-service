from django import urls
from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from django.urls import path, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="User Service API",
        default_version='v1',
        description="User Api for greenshare project",
        terms_of_service="https://www.greensharebcn.com",
        contact=openapi.Contact(email="@greensharebcn.com"),
        license=openapi.License(name="GreenshareBcn"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('users/', views.all_users_api_view, name = 'Users'),
    path('users/<int:pk>/', views.user_detail_api_view, name = 'Concrete user'),
    path('users/verify/',views.user_verification, name = 'User verificatio'),
    path('users/<int:pk>/password/', views.user_change_pass_api_view, name = 'Update password'),
    path('users/<int:pk>/PasswordIdToken/', views.user_change_pass_id_api_view, name = 'Update password by id and token'),
    path('auth/login/', views.user_login, name = 'Login'),
    path('auth/login-id/', views.user_login_id_token, name = 'Login id user'),
    url(r'.*', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')    
]
