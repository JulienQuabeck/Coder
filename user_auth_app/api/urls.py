from django.urls import path
from .views import RegistraionView, LoginView, GetAllUsers, GetDetailUser, getBusinessUsers, getBusinessUsersDetail, getCustomerUsers, getCustomerUsersDetail

from .views import FileUploadView


urlpatterns = [
    # path('', include(router.urls)),
    path('registration/', RegistraionView.as_view(), name='registraion'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('profile/<int:pk>/', GetDetailUser.as_view(), name='GetDetailUser'),





    path('profiles/', GetAllUsers.as_view(), name='getuser'),
    path('profiles/business/', getBusinessUsers.as_view(), name='GetBusinessUser'),
    path('profiles/business/<int:pk>/', getBusinessUsersDetail.as_view(), name='GetBusinessUserDetail'),
    path('profiles/customer/', getCustomerUsers.as_view(), name='GetCustomerUser'),
    path('profiles/customer/<int:pk>/', getCustomerUsersDetail.as_view(), name='GetCustomerUserDetail'),
]

