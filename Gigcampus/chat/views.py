from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project
from .models import Message

@login_required
def chat_room(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Check if user is authorized to access this chat
    if (request.user != project.posted_by and 
        not project.bids.filter(freelancer=request.user, status='accepted').exists()):
        return render(request, 'chat/unauthorized.html')
    
    messages = Message.objects.filter(project=project).order_by('timestamp')
    
    context = {
        'project': project,
        'messages': messages,
        'project_id': project_id,
    }
    
    return render(request, 'chat/chat_room.html', context)