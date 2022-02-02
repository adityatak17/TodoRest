from django.db import models
# from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.conf import settings


DESIGNATION=(
    ("manager","MANAGER"),
    ("employee","EMPLOYEE")
)
class User(AbstractUser):
    '''This is a User Model which extends the built-in User Model'''
    
    phone=models.CharField(max_length=10)
    designation=models.CharField(max_length=20,choices=DESIGNATION,default="employee")
    password=models.CharField(max_length=51)


TASK_STATUS=(
    ('done',"DONE"),
    ('pending','PENDING'),
    ('ongoing',"ONGOING"),
    ('paused','PAUSED')
)
class Task(models.Model):
    '''This Model gives information about the Task'''
    
    task_title=models.CharField(max_length=251)
    task_description=models.TextField()
    task_status=models.CharField(max_length=21,choices=TASK_STATUS,default='pending')
    is_archived=models.BooleanField(_('Archive This Record'),default=False)
    
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_title
  
    
class TaskHistory(models.Model):
    '''This Model gives information about the History of a particular Task'''
    
    task_history=models.TextField()
    changes_made=models.TextField()
    
    task=models.ForeignKey(Task,on_delete=models.CASCADE)
    
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural='Task Histories'
        default_permissions=('view',)
        # permissions=[('view', 'Can See')]
        # ordering=['-task__created_on','-task__updated_on']
    
    def __str__(self):
        return (f"{self.task.task_title}'s History ")
    
    

