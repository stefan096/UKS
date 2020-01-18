from django.contrib import admin

# Register your models here.
# from miniGithub.models import Project, Problem, Custom_Event, Comment, Change_State, Change_Assignee, \
#     Milestone, Change_Milestone, Change_Comment, Change_Code, Label, Profile


from miniGithub.models import Project, Profile, Custom_Event, Milestone, \
     Label

admin.site.register(Project)
# admin.site.register(Problem)
admin.site.register(Profile)
admin.site.register(Custom_Event)
# admin.site.register(Comment)
# admin.site.register(Change_State)
# admin.site.register(Change_Assignee)
admin.site.register(Milestone)
# admin.site.register(Change_Milestone)
# admin.site.register(Change_Comment)
# admin.site.register(Change_Code)
admin.site.register(Label)