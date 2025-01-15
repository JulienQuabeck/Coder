from django.urls import path
from .views import RegistraionView, LoginView, RetrievUpdateDestroyDetailUser, ListBusinessUsers, ListCustomerUsers

from .views import FileUploadView


urlpatterns = [
    path('registration/', RegistraionView.as_view(), name='registraion'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('profile/<int:pk>/', RetrievUpdateDestroyDetailUser.as_view(), name='GetDetailUser'),
    path('profiles/business/', ListBusinessUsers.as_view(), name='GetBusinessUser'),
    path('profiles/customer/', ListCustomerUsers.as_view(), name='GetCustomerUser'),
]