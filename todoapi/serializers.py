from rest_framework import serializers

from todoapi.models import Task, TaskHistory, User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields='__all__'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'task_title'}
        # }
    
class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=TaskHistory
        fields='__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','password2']
    def create(self,validated_data):
        user=User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    def validate(self,data):
        if data['password']!=data['password2']:
            raise serializers.ValidationError("Password 1 and Password 2 are not Same")
        return data
    def validate_password(self,value):
        if len(value)<8 or len(value)>51:
            raise serializers.ValidationError("Password Length Must be between 8 and 51")
        if value.isalnum() and value.isalpha():
            raise serializers.ValidationError("Password must be a Combination of Words and Numeric Digits")
        return value