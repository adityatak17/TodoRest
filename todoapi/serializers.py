from rest_framework import serializers

from todoapi.models import Task, TaskHistory, User


class TaskSerializer(serializers.ModelSerializer):
    '''This is a Serializer for Task Model'''
    
    class Meta:
        model = Task
        fields = '__all__'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'task_title'}
        # }
    
class TaskHistorySerializer(serializers.ModelSerializer):
    '''This is a Serializer for TaskHistory Model'''
    
    class Meta:
        model = TaskHistory
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    '''This  is a Serializer for User Model'''
    
    class Meta:
        model = User
        fields = ['username','password','password2']
    
    def create(self,validated_data):
        '''This function creates a User with the given data and sets the Hashed Password'''
        
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate_password(self,value):
        '''
            This function applies Length and AlphaNumeric Validation on the 
            Password Field
        '''
        
        if len(value) < 8 or len(value) > 51:
            raise serializers.ValidationError("Password Length Must be between 8 and 51")
        
        if value.isalnum() and value.isalpha():
            raise serializers.ValidationError("Password must be a Combination of Words and Numeric Digits")
        
        return value
    
    def validate(self,data):
        '''This function applies Password Checking Validation '''
        
        if data['password']!=data['password2']:
            raise serializers.ValidationError("Password 1 and Password 2 are not Same")
        
        return data
    