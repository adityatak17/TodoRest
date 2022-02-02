from django.db.models.signals import post_save,post_delete,pre_save
from django.dispatch import receiver
from .models import TaskHistory,Task
from datetime import datetime

# from collections import namedtuple

# @receiver(post_save,sender=Task)
# def save_task_history(sender,instance,created,raw,using,update_fields,**kwargs):
#     if created:
#         TaskHistory.objects.create()
        
    
@receiver(pre_save,sender=Task)
def pre_save_task_history(sender,instance,**kwargs):
    if instance.id is not None:
        old=Task.objects.get(id=instance.id)
        new=instance
        changes_all=''
        changes_heading=''
        
        if old.task_title!=new.task_title:
            changes_heading+='Task Title was Changed\n'
            changes_all+= f'Task Title was Changed from "{old.task_title}" to "{new.task_title}" '
        if old.task_description != new.task_description:
            changes_heading+='Task Description was Changed\n'
            changes_all+= f'Task Description was Changed from "{old.task_description}" to "{new.task_description}" '
        if old.task_status!=new.task_status:
            changes_heading+='Task Status was Changed\n'
            changes_all+= f'Task Status was Changed from "{old.task_status}" to "{new.task_status}" '  
        if old.is_archived!=new.is_archived:
            changes_heading+=f'''Task was {'Archived' if new.is_archived else 'Unarchived'}\n'''
            changes_all+= f'''Task with Title "{old.task_title}" was {'Archived' if new.is_archived else 'Unarchived'} '''
        
        if changes_all!='':
            TaskHistory.objects.create(
                task=instance,
                task_history=f'''Task {old.task_title} was Updated at {new.updated_on}\n {changes_all}''',
                changes_made=changes_heading
            )
        
        
        
        # Details=namedtuple('Details',['task_title','task_description','task_status','is_archived'])
        # details1=Details(old.task_title,old.task_description,old.task_status,old.is_archived)
        # details2=Details(new.task_title,new.task_description,new.task_status,new.is_archived)
        # details1._fields will return the keys i.e 'task_title','task_status' etc
        
        # if details1.task_title!=details2.task_title:
        #     changes_heading+="Task Title was changed\n"
        #     changes_all+=f'Task Title was Changed from "{}" to "{}"'
        # if details1.task_description!=details2.task_description:
        #     changes_heading+="Task Description was changed\n"
        # if details1.task_status!=details2.task_status:
        #     changes_heading+="Task Status was changed\n"
        # if details2.is_archived == False:
        #     changes_heading+="Task was Unarchived\n"
        # for i in range(4):
        #     if details1[i] != details2[i]:
        # changes_all=''
        # changes_heading=''                     
        # list1=[(old.task_title,new.task_title,0),(old.task_description,new.task_description,1),
        #        (old.task_status,new.task_status,2),(old.is_archived,new.is_archived,3)]
        # for i,j,k in list1:
        #     if i!=j:
        #         if k<=2:
        #             if k==0:
        #                 a='Title'
        #             elif k==1:
        #                 a='Description'
        #             elif k==2:
        #                 a='Status' 
        #             changes_all=changes_all+f'Task {a} was changed from "{i}" to "{j}"'+'\n'
        #             changes_heading+=f"Task {a} was Changed"+ '\n'
        #         else:
        #             changes_all+='Task was Unarchived'
        #             changes_heading+=f'Task "{new.task_title}" was Unarchived'
        # if changes_heading!='':
        #     TaskHistory.objects.create(
        #         task=instance,
        #         task_history=f'Task "{old.task_title}" was updated at {new.updated_on}.{changes_all}',
        #         changes_made=changes_heading
        #     )
        
        
@receiver(post_save,sender=Task)
def save_task_history(sender,instance,created,**kwargs):
    changes_heading='A New Task was Created\n'
    changes_all=''
    if created:
        changes_all+=f'Task with Title "{instance.task_title}" was Created at {instance.created_on}\n'
        if instance.is_archived:
            changes_heading+='Task was Archived\n'
            changes_all+=f'Task with Title "{instance.task_title}" was Archived'
        TaskHistory.objects.create(
            task=instance,
            task_history=changes_all,
            changes_made=changes_heading
        )
        
            
        # TaskHistory.objects.create(
        #     task=instance,
        #     task_history=f'Task "{instance.task_title}" was created on {instance.created_on}',
        #     changes_made=f'Task "{instance.task_title}" was Created'
        #     )   
    # else:
    #     if instance.is_archived:
    #         TaskHistory.objects.create(
    #             task=instance,
    #             task_history=f'Task "{instance.task_title}" was archived at {instance.updated_on}',
    #             changes_made=f'Task "{instance.task_title}" was Archived'
    #         )
      
# @receiver(post_delete,sender=Task)
# def delete_task_history(sender,instance,**kwargs):
#     TaskHistory.objects.create(
#         task_history=f"{instance.task_title} {instance.task_description} was deleted at {datetime.now()}"
#         )

