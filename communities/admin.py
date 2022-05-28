from django.contrib import admin
from .models import Community


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'creator', 'members_count')
    list_filter = ('creator',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def members_count(self, obj):
        return obj.members.count()
