from django.contrib import admin
from .models import Project, Bid

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'budget', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'posted_by__username')
    readonly_fields = ('created_at',)

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('project', 'freelancer', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('project__title', 'freelancer__username')
    readonly_fields = ('created_at',)