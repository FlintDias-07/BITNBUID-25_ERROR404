from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Escrow
from portfolio.models import Review

@login_required
def escrow_status(request, escrow_id):
    escrow = get_object_or_404(Escrow, id=escrow_id)
    
    # Check if user is authorized to view this escrow
    if request.user != escrow.bid.project.posted_by and request.user != escrow.bid.freelancer:
        messages.error(request, 'You are not authorized to view this escrow.')
        return redirect('dashboard')
    
    return render(request, 'payments/escrow_status.html', {'escrow': escrow})

@login_required
def release_escrow(request, escrow_id):
    escrow = get_object_or_404(Escrow, id=escrow_id)
    
    if request.user != escrow.bid.project.posted_by:
        messages.error(request, 'Only the client can release escrow.')
        return redirect('escrow_status', escrow_id=escrow.id)
    
    if escrow.status == 'held':
        escrow.status = 'released'
        escrow.released_at = timezone.now()
        escrow.save()
        
        # Mark project as completed
        escrow.bid.project.status = 'completed'
        escrow.bid.project.save()
        
        messages.success(request, 'Escrow released! Project marked as completed.')
    
    return redirect('escrow_status', escrow_id=escrow.id)