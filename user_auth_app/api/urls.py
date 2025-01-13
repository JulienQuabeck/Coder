from django.urls import path
from .views import RegistraionView, LoginView, GetDetailUser, getBusinessUsers, getCustomerUsers

from .views import FileUploadView


urlpatterns = [
    path('registration/', RegistraionView.as_view(), name='registraion'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('profile/<int:pk>/', GetDetailUser.as_view(), name='GetDetailUser'),
    path('profiles/business/', getBusinessUsers.as_view(), name='GetBusinessUser'),
    path('profiles/customer/', getCustomerUsers.as_view(), name='GetCustomerUser'),
]

