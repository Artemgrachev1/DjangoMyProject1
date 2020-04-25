"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from.models import Comment
from.models import Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))
class AnketaForm(forms.Form):
    name = forms.CharField(label='Имя',min_length=2,max_length=100)
    city = forms.CharField(label='Город',min_length=2,max_length=100)
    job = forms.CharField(label='Род занятий',min_length=2,max_length=100)
    gender = forms.ChoiceField(label='Пол',
                                choices=[('1','Мужской'),('2','Женский')],
                                widget=forms.RadioSelect,initial=1)
    trial = forms.ChoiceField(label='Посещали ли Вы наш автосервис?',
                              choices=(
                                  ('1','Да, я ваш постоянный клиент'),
                                  ('2','Собираюсь обратиться'),
                                  ('3','Нет'),
                                  ('4','Да, но мне не понравилось')),initial=1)
    notice = forms.BooleanField(label = 'Хотите получать интересные предложения по E-mail?',
                                required=False)
    email = forms.EmailField(label='Ваш E-mail',min_length=7)
    message = forms.CharField(label='Напишите мнение о нас',
                              widget=forms.Textarea(attrs={'rows':8,'cols':40}))

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment     #Используемая модель
        fields = ('text',)  #Требуется заполнить только поле текст
        labels = {'text':"Комментарий"} #Метка к полю формы text
        widgets = {
            'text':forms.Textarea(attrs={'rows': 10,'class': 'form-control'})
            }

class BlogForm (forms.ModelForm):
    class Meta:
        model=Blog      #Используемая модель
        fields = ('title','description','content','posted','author','image',)
        labels = {'title':"Заголовок",'description':"Краткое описание",'content':"Содержание",'posted':"Дата",'author':"Автор",'image':"Изображение"}
