from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import views
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, authentication_classes, permission_classes
from django.contrib.auth import logout 

from .models import * 
from .serializers import *


# class DynamicSearchFilter(filters.SearchFilter):
#     '''This function is used to create Dynamic Search Filter'''
    
#     def get_search_fields(self, view, request):
#         return request.GET.getlist('search_fields', [])


class TaskViewSet(viewsets.ModelViewSet):
    '''This is a ViewSet for Model Task'''
    
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    
    search_fields=['task_title','task_description']
    filter_fields=['task_title','task_description']
    filter_backends=[filters.SearchFilter,]
    # search_fields=['task_title','task_description']
    # filter_backends=(DynamicSearchFilter,)
    # lookup_field='task_title'
    
 
class TaskHistoryViewSet(viewsets.ModelViewSet):
    '''This is a ViewSet for Model TaskHistory'''
    
    queryset=TaskHistory.objects.all()
    serializer_class=TaskHistorySerializer
    
    search_fields=['task',]
    filter_fields=['task',]
    filter_backends=[filters.SearchFilter,]
    
 
class RegisterUser(views.APIView):
    '''
        This is a APIView to Register a new User and Generate a Token for that 
        particular User
    '''
    
    def post(self,request):
        '''This method Registers a User and Generates Token for it'''
        
        # import  pdb; pdb.set_trace()
        serializer=UserSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
        # user=serializer.validated_data['user']
        user=User.objects.get(username=serializer.data['username'])
        token,created=Token.objects.get_or_create(user=user)
        return Response({'status':200,'payload':serializer.data,'token':str(token),'msg':'Success Message'})

class CustomAuthToken(ObtainAuthToken):
    '''
        This Class is used to get the Token when a User provides valid
        username and password.
        This is Overriding the inbuilt rest framework method "views.obtain_auth_token"
        which returns only the token's key.
        With this method we can return more details about the User
    '''
    
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
    '''
        This Class will Log the User out and will delete the Authentication Token
    '''
    
    authentication_classes=[authentication.TokenAuthentication,]
    permission_classes=[permissions.IsAuthenticated,]
    
    def post(self,request):
        try:
            request.user.auth_token.delete()
        except Exception as e:
            pass
        logout(request)
        return Response({'msg':"You have been logged out"})
    