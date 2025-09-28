from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
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
@require_POST
def release_escrow(request, escrow_id):
    escrow = get_object_or_404(Escrow, id=escrow_id)
    project = escrow.bid.project
    if request.user != project.posted_by:
        messages.error(request, "You are not authorized to release this payment.")
        return redirect('escrow_status', escrow.id)
    if escrow.status != 'held':
        messages.warning(request, "Escrow is not held.")
        return redirect('escrow_status', escrow.id)

    # mark released (extend with real payment transfer logic as needed)
    escrow.status = 'released'
    escrow.released_at = timezone.now()
    escrow.save()

    messages.success(request, "Payment released to freelancer.")
    return redirect('escrow_status', escrow.id)

{
  "python.analysis.extraPaths": [
    "C:/Users/Admin/AppData/Roaming/Python/Python311/site-packages"
  ],
  "python.pythonPath": "C:/Users/Admin/AppData/Roaming/Python/Python311/python.exe"
}