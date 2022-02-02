from django.contrib import admin
from .models import Task,TaskHistory,User
# Register your models here.      
from django.utils.translation import gettext_lazy as _

class ArchiveListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Archived Status') ## by ke sath aayega ki kis hisab se filter kar rahe vo title

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'is_archived' ## kis alue ke hisab se filter karna he vo

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('archived', _('Archived Tasks')),
            ('unarchived', _('Unarchived Tasks')),
        ) 
        ## do options banaye he mene pahli value variable he or dusri human readable form he

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either 'archived' or 'unarchived')
        # to decide how to filter the queryset.
        if self.value() == 'archived':
            return queryset.filter(is_archived=True)
        if self.value() == 'unarchived':
            return queryset.filter(is_archived=False)
        
        ## sidha yaha lookups vale kis option par kya show karna he vo likhdo 
  
        
class TaskStatusListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the right admin sidebar just above the filter options.
    title = _('Task Status') ## by ke sath aayega ki kis hisab se filter kar rahe vo title
    # Parameter for the filter that will be used in the URL query.
    
    parameter_name = 'task_status' ## kis value ke hisab se filter karna he vo

    def lookups(self, request, model_admin):
        return (
            ('done1', _('Status: Done')),
            ('pending1', _('Status: Pending')),
            ('ongoing1',_('Status: Ongoing')),
            ('paused1',_('Status: Paused'))
        ) 
        ## 4 options banaye he mene pahli value variable he or dusri human readable form he
        ## to jese agar me 'Status: Done' par click karunga to 'done1' variable iss choice ko show karega

    def queryset(self, request, queryset):
        # Compare the requested value (either 'done1','pending1','ongoing1' or 'paused1')
        # to decide how to filter the queryset.
        if self.value() == 'done1':
            return queryset.filter(task_status='done')
        if self.value() == 'pending1':
            return queryset.filter(task_status='pending')
        if self.value() == 'ongoing1':
            return queryset.filter(task_status='ongoing')
        if self.value() == 'paused1':
            return queryset.filter(task_status='paused')  
        ## fir yaha check hota he ki accha ye choice he to ispe ye show kardo
        ## done1 choice ko show karne vala variable he or done mere model me task_status batata he
        ## dono same naam ho sakte the par difference pata chal sake isiliye 1 laga rakha he  


# This Function will be called by actions attribute in the TaskAdmin class 
# Description Human Readable Name he jo vaha tum show karana chaho
# modeladmin= The current ModelAdmin
# request= An HttpRequest representing the current request,
# queryset=A QuerySet containing the set of objects selected by the user.
@admin.action(description='Unarchive Selected Tasks')
def unarchive_selected_tasks(modeladmin, request, queryset):
    queryset.update(is_archived=False)



class TaskHistoryAdmin(admin.ModelAdmin):
    list_display=('task','changes_made','task_history','created_on','updated_on')
    
    # isme jo bhi fields honge vo fir change nahi kar sakte sirf view kar sakte he
    readonly_fields=("task",'changes_made','task_history','created_on','updated_on')
    
    # ye delete karne ki permission revoke kar leta he
    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False
        
    
class TaskAdmin(admin.ModelAdmin):
    list_display = ("user",'task_title', 'task_description','task_status','created_on','is_archived')
    #admin interface sahi lagta he sab vertically dikh jata he acche se
    
    list_filter=(ArchiveListFilter,TaskStatusListFilter)
    # filters apply karne me kaam aata he
    
    
    actions=[unarchive_selected_tasks,'archive_selected_tasks']
    # Another way to implement actions
    @admin.action(description='Archive Selected Tasks')
    def archive_selected_tasks(self,request,queryset):
        queryset.update(is_archived=True)
        
    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False
    
    # actions_on_bottom=True # delete vgrh ka jo option hota he usko niche dikhane ke kaam aata
    # actions_on_top=False # by default True hota he
    # agar actions_on_bottom ko True kar rahe hoto actions_on_top ko False karna baki dono taraf dikhega action bar
    # actions_selection_counter=False # kitne select kiye out of esa option hota he action bar ke pass
    # date_hierarchy='created_on' # date or year type filter aa jayega action bar ke upar
    # empty_value_display='-Nothing-' # empty values ko override karna chahiye tha par meko diff nahi dikha
    # fields=('task','changes_made')  #kya kya fields show karna chahte admin panel par vo 
    # list_per_page=5
    # list_filter=('is_archived','task_status')
    # list_filter=(ArchiveListFilter,'task_status')
    # list_filter=(ArchiveListFilter,TaskStatusListFilter)
    
 
  
admin.site.register(Task,TaskAdmin)
admin.site.register(TaskHistory,TaskHistoryAdmin)
admin.site.register(User)


