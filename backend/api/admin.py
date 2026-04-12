from django.contrib import admin

from api.models import CustomUser, PurchaseIntention, ReflectionQuestion, AppFeedback, ErrorLog

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(PurchaseIntention)
admin.site.register(ReflectionQuestion)
admin.site.register(AppFeedback)
admin.site.register(ErrorLog)