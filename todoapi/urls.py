from django.http import HttpResponse
from django.urls import path,include
from rest_framework import routers 
from rest_framework.authtoken import views

from .views import RegisterUser,CustomAuthToken,LogoutUser
from . import views

router=routers.DefaultRouter()
router.register(r'task',views.TaskViewSet)
router.register(r'taskhistory',views.TaskHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('register/',RegisterUser.as_view()),
    path('custom/',CustomAuthToken.as_view()),
    path('logout/', LogoutUser.as_view()),
]

