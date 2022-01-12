from django.http.response import Http404
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from boards.models import Board, Post, Topic
from .forms import NewTopicForm

# Create your views here.
def home(request):
    boards = Board.objects.all()
    boards_names = list()
    for board in boards:
        boards_names.append(board.name)
    return render(request,'home.html',{'boards':boards})

def board_topics(request,pk):
    board = get_object_or_404(Board,pk=pk)
    return render(request,'topics.html',{'board':board})

@login_required
def new_topic(request,pk):
    board = get_object_or_404(Board,pk=pk)
    user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = user
            )
            return redirect('board_topics',pk=board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html',{'board':board,'form':form})
        
