
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from projects.models import Project  # Change 'projects' to your real app name

@login_required
def analytics(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'client':
        return redirect('home')
    # Aggregate your real field data from Project or another model
    field_labels = ['Web Development', 'Design', 'Content Writing', 'Data Analysis', 'Others']
    field_counts = [
    Project.objects.filter(title__icontains='Web').count(),
    Project.objects.filter(title__icontains='Design').count(),
    Project.objects.filter(title__icontains='Content').count(),
    Project.objects.filter(title__icontains='Data').count(),
    Project.objects.exclude(
        title__icontains='Web'
    ).exclude(
        title__icontains='Design'
    ).exclude(
        title__icontains='Content'
    ).exclude(
        title__icontains='Data'
    ).count(),
]
    return render(request, 'analytics.html', {
        'field_labels': field_labels,
        'field_counts': field_counts
    })

@login_required
def field_demand(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'client':
        return redirect('home')
    return render(request, 'field_demand.html')   # Reuse the analytics view logic or make a separate one if you want

