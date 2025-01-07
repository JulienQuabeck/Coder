from django.urls import path, include
from .views import RegistraionView, GetAllUsers, GetDetailUser

# router = DefaultRouter()
# router.register(r'users', UsersViewSet, basename='question')

urlpatterns = [
    # path('', include(router.urls)),
    path('registration/', RegistraionView.as_view(), name='registraion'),
    path('getuser/', GetAllUsers.as_view(), name='getuser'),
    path('getuser/<int:pk>/', GetDetailUser.as_view(), name='GetDetailUser')
]
