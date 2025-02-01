from django.contrib import admin
from .models import FAQ


# Register your models here.
class FAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'question']
    search_fields = ['id', 'question']
    list_filter = ['id']


admin.site.site_header = 'FAQs Admin'
admin.site.site_title = 'FAQs Management Admin'
admin.site.index_title = 'Welcome to the FAQs Admin Area'
admin.site.register(FAQ, FAQAdmin)
