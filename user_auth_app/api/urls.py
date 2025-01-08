from django.urls import path, include
from .views import RegistraionView, LoginView, GetAllUsers, GetDetailUser
from rest_framework.authtoken.views import obtain_auth_token

# router = DefaultRouter()
# router.register(r'users', UsersViewSet, basename='question')

urlpatterns = [
    # path('', include(router.urls)),
    path('registration/', RegistraionView.as_view(), name='registraion'),
    path('login/', LoginView.as_view(), name='login'),
    path('getuser/', GetAllUsers.as_view(), name='getuser'),
    path('profile/<int:pk>/', GetDetailUser.as_view(), name='GetDetailUser')
]
