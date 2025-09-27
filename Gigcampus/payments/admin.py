from django.contrib import admin
from .models import Escrow

@admin.register(Escrow)
class EscrowAdmin(admin.ModelAdmin):
    list_display = ('bid', 'amount', 'status', 'created_at', 'released_at')
    list_filter = ('status', 'created_at')
    search_fields = ('bid__project__title', 'bid__freelancer__username')
    readonly_fields = ('created_at', 'released_at')