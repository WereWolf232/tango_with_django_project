from django.contrib import admin
from .models import *

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category','url')
    
    
# This fills out the slug field in real time, and prompts if there's already a slug with the same name
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Page, PageAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(UserProfile)
