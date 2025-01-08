from django.urls import path
from .views import RegistraionView, LoginView, GetAllUsers, GetDetailUser

from .views import FileUploadView


urlpatterns = [
    # path('', include(router.urls)),
    path('registration/', RegistraionView.as_view(), name='registraion'),
    path('login/', LoginView.as_view(), name='login'),
    path('profiles/', GetAllUsers.as_view(), name='getuser'),
    path('profile/<int:pk>/', GetDetailUser.as_view(), name='GetDetailUser'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
]

