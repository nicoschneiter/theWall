from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

from .models import User, Message, Comment
import bcrypt

# Create your views here.
def index(request):
    if 'id' in request.session.keys():
        request.session.clear()
    if 'first_name' not in request.session.keys():
        request.session['first_name'] = ''
        request.session['last_name'] = ''
        request.session['email'] = ''
        request.session['lemail'] = ''
    return render(request,"the_wall/index.html")
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if request.method == 'POST':
        if len(errors):
            for key, value in errors.items():
                messages.error(request,value, extra_tags = key)
            return redirect('/')
        else:
            User.objects.create(first_name=request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
            request.session['id'] = User.objects.last().id
            request.session['first_name'] = User.objects.last().first_name
            return redirect('/wall')
    return redirect('/')
def login(request):
    errors = User.objects.login_validator(request.POST)
    if request.method == 'POST':
        if len(errors):
            for key, value in errors.items():
                messages.error(request,value, extra_tags = key)
            return redirect('/')
        request.session['id'] = User.objects.get(email=request.POST['lemail']).id
        request.session['first_name'] = User.objects.get(email=request.POST['lemail']).first_name
        return redirect('/wall')
def wall(request):
    selected_m = Message.objects.all()
    selected_c = Comment.objects.all()
    context = {
            'selected_m':selected_m,
            'selected_c':selected_c
            }
    return render(request,"the_wall/wall.html", context)

def create(request):
    Message.objects.create(message = request.POST['posting'], user = User.objects.get(id=request.session['id']))
    return redirect('/wall')
def create_comment(request):
    Comment.objects.create(comment = request.POST['posting'], user = User.objects.get(id=request.session['id']), message = Message.objects.get(id=request.POST['mid']))
    return redirect('/wall')
def delete(request):
    Message.objects.get(id = request.POST['mid']).delete()
    return redirect('/wall')
def delete_comment(request):
    Comment.objects.get(id = request.POST['cid']).delete()
    return redirect('/wall')
def logout(request):
    request.session.clear()
    return redirect('/')
