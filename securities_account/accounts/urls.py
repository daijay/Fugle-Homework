from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.views.generic import RedirectView

from .views import (apply_account, approved_page, register, supplement_info,
                    view_my_applications)

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('register/', register, name='register'),
    path('superuser-register/', lambda request: register(request, is_superuser=True), name='superuser_register'),
    path('apply/', apply_account, name='apply_account'),
    path('my-applications/', view_my_applications, name='view_my_applications'),
    path('supplement/<int:app_id>/', supplement_info, name='supplement_info'),
    path('approved/', approved_page, name='approved_page'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
]