"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .forms import AnketaForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Comment     #Использование модели комментариев
from .forms import CommentForm      #Использование формы ввода комментариев
from .forms import BlogForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас',
            'year':datetime.now().year,
        }
    )
def links (request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'message':'Партнеры',
            'year':datetime.now().year,
        }
    )
def pool(request):
        assert isinstance(request, HttpRequest)
        data = None
        gender = {'1':'Мужчина','2':'Женщина'}
        trial = {'1':'Да, я ваш постоянный клиент',
                 '2':'Собираюсь обратиться',
                 '3':'Нет',
                 '4':'Да, но мне не понравилось'}
        if request.method == 'POST':
            form = AnketaForm(request.POST)
            if form.is_valid():
                data = dict()
                data['name'] = form.cleaned_data['name']
                data['city'] = form.cleaned_data['city']
                data['job'] = form.cleaned_data['job']
                data['gender'] = gender[ form.cleaned_data['gender'] ]
                data['trial'] = trial[ form.cleaned_data['trial'] ]
                if(form.cleaned_data['notice'] == True):
                   data['notice'] = 'Да'
                else:
                   data['notice'] = 'Нет' 
                data['email'] = form.cleaned_data['email']
                data['message'] = form.cleaned_data['message']
                form = None
        else:
            form = AnketaForm()
        return render(
            request,
            'app/pool.html',
            {
                'title':'Анкета',
                'message':'Заполните все поля анкеты.',
                'form':form,
                'data':data
            }
        )

def registration(request):
    """Renders the registration page."""
    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
             reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
             reg_f.is_staff = False # запрещен вход в административный раздел
             reg_f.is_active = True # активный пользователь
             reg_f.is_superuser = False # не является суперпользователем
             reg_f.date_joined = datetime.now() # дата регистрации
             reg_f.last_login = datetime.now() # дата последней авторизации
             reg_f.save() # сохраняем изменения после добавления данных
             return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
        assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
        'regform': regform, # передача формы в шаблон веб-страницы
        'year':datetime.now().year,
        }
        )
def blog(request):
    """Renders the blog page"""
    posts = Blog.objects.all()       #Запрос на выбор всех статей из модели

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts':posts,          #Передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )
def blogpost (request, parametr):
    """Renders the blogpost page"""
    post_1 = Blog.objects.get(id=parametr)      #Запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)    #Запрос на выбор всех комментариев статьи
   
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
        else:
            form = CommentForm() # создание формы для ввода комментария

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1':post_1,        #Передача конкретной статьи в шаблон веб-страницы
            'comments': comments,   #передача всех комментариев к данной статье в шаблон веб-сайта
            'form': CommentForm(),           #передача формы добавления комментария в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def newpost(request):
    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()

            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/newpost.html',
        {
            'blogform':blogform,
            'year':datetime.now().year,
        }
)

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Выберите видео для просмотра.',
            'year':datetime.now().year,
        }
    )