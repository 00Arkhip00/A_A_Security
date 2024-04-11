from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from test_site.models import Message
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

chat_login = ''


def index_page(request):
    context = {}
    return render(request, "index.html", context)


@login_required
def chats(request):
    global chat_login
    u = User.objects.all()
    sp_people = []
    for i in u:
        sp_people.append(str(request.user) + '-' + i.username)
        sp_people.append(i.username + '-' + str(request.user))
    ob = Message.objects.filter(name__in=sp_people)
    if request.method == 'POST':
        chat_login = request.POST.get('name')
        new_chat = request.POST.get('new_chat')
        old_chat = request.POST.get('old_chat')
        if chat_login is not None:
            return redirect('/chat/')
        elif new_chat is not None:
            if new_chat in sp_people and str(request.user) in new_chat:
                ch1 = Message(name=f"{str(request.user)}-{new_chat}", sms={})
                ch1.save()
            else:
                return HttpResponse('Пользователя с таким именем не существует!/У вас нет доступа к этому чату!')
        else:
            if str(request.user) in old_chat:
                ch1 = Message.objects.filter(name__in=[str(request.user) + '-' + old_chat, old_chat + '-' + str(request.user)])
                ch1.delete()
            else:
                return HttpResponse('У вас нет доступа к этому чату!')
    context = {'db': ob}
    return render(request, "chats.html", context)


@login_required
def chat(request):
    global chat_login
    n1, n2 = chat_login, chat_login[::-1]
    ob = Message.objects.filter(name__in=[n1, n2])
    if request.method == 'POST':
        sms = request.POST.get('message')
        s = ob[0].sms
        s[f"{datetime.datetime.now().strftime('%H:%M:%S')}-{str(request.user)}"] = sms
        ob.update(sms=s)
    context = {'db': []}
    for k, v in ob[0].sms.items():
        context['db'].append([k, v])

    return render(request, "chat.html", context)


def registration(request):
    context = dict()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/chats/')
    else:
        form = UserCreationForm()
    context['form'] = form
    return render(request, "registration/registration.html", context)
