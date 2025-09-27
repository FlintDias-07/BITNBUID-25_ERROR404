from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Bid
from .forms import ProjectForm, BidForm
from payments.models import Escrow

@login_required
def post_project(request):
    if request.user.profile.role != 'client':
        messages.error(request, 'Only clients can post projects.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.posted_by = request.user
            project.save()
            messages.success(request, 'Project posted successfully!')
            return redirect('dashboard')
    else:
        form = ProjectForm()
    
    return render(request, 'projects/post_project.html', {'form': form})

def project_list(request):
    projects = Project.objects.filter(status='open').order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    bids = project.bids.all().order_by('-created_at')
    user_bid = None
    
    if request.user.profile.role == 'freelancer':
        user_bid = bids.filter(freelancer=request.user).first()
    
    if request.method == 'POST' and request.user.profile.role == 'freelancer':
        if not user_bid:
            form = BidForm(request.POST)
            if form.is_valid():
                bid = form.save(commit=False)
                bid.project = project
                bid.freelancer = request.user
                bid.save()
                messages.success(request, 'Bid submitted successfully!')
                return redirect('project_detail', project_id=project.id)
        else:
            messages.warning(request, 'You have already bid on this project.')
    
    form = BidForm() if request.user.profile.role == 'freelancer' and not user_bid else None
    
    context = {
        'project': project,
        'bids': bids,
        'form': form,
        'user_bid': user_bid,
    }
    
    return render(request, 'projects/project_detail.html', context)

@login_required
def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    
    if bid.project.posted_by != request.user:
        messages.error(request, 'You can only accept bids on your own projects.')
        return redirect('project_detail', project_id=bid.project.id)
    
    # Update bid status
    bid.status = 'accepted'
    bid.save()
    
    # Close project
    bid.project.status = 'closed'
    bid.project.save()
    
    # Create escrow
    Escrow.objects.create(bid=bid, amount=bid.amount)
    
    messages.success(request, 'Bid accepted! Escrow created.')
    return redirect('project_detail', project_id=bid.project.id)