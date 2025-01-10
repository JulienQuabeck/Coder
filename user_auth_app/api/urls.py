from django.urls import path
from .views import RegistraionView, LoginView, GetAllUsers, GetDetailUser, getBusinessUsers, getCustomerUsers

from .views import FileUploadView


urlpatterns = [
    # path('', include(router.urls)),
    path('registration/', RegistraionView.as_view(), name='registraion'),
    path('login/', LoginView.as_view(), name='login'),
    path('profiles/', GetAllUsers.as_view(), name='getuser'),
    path('profiles/business/', getBusinessUsers.as_view(), name='GetBusinessUser'),
    path('profiles/customer/', getCustomerUsers.as_view(), name='GetCustomerUser'),
    path('profile/<int:pk>/', GetDetailUser.as_view(), name='GetDetailUser'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
]

