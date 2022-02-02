from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import * 
from rest_framework import filters
from django.http import HttpResponse
from django.contrib.auth import logout 
from rest_framework import views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, authentication_classes, permission_classes
# from django.contrib.auth.decorators import login_required
# Create your views here.


class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

# @login_required
class TaskViewSet(viewsets.ModelViewSet):
    
    # search_fields=['task_title','task_description']
    # filter_backends=(filters.SearchFilter,)
    
    # search_fields=['task_title','task_description']
    # filter_backends=(DynamicSearchFilter,)
    
    search_fields=['task_title','task_description']
    filter_fields=['task_title','task_description']
    filter_backends=[filters.SearchFilter,]
    
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    # lookup_field='task_title'
    
# @login_required   
class TaskHistoryViewSet(viewsets.ModelViewSet):
    queryset=TaskHistory.objects.all()
    serializer_class=TaskHistorySerializer
    
    search_fields=['task']
    filter_fields=['task']
    filter_backends=[filters.SearchFilter,]
    
 
class RegisterUser(views.APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        # user=serializer.validated_data['user']
        user=User.objects.get(username=serializer.data['username'])
        token,created=Token.objects.get_or_create(user=user)
        return Response({'status':200,'payload':serializer.data,'token':str(token),'msg':'Success Message'})

class CustomAuthToken(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token,created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'email':user.email
        })
        
class LogoutUser(views.APIView):
    authentication_classes=[authentication.TokenAuthentication,]
    permission_classes=[permissions.IsAuthenticated,]
    def post(self,request):
        try:
            request.user.auth_token.delete()
        except Exception as e:
            pass
        logout(request)
        return Response({'msg':"You have been logged out"})
    
    
def logout_page(request):
    logout(request)
    return HttpResponse("You Have been Logged Out")


    

