from django.shortcuts import render
from .models import s3objects
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    object_list = None
    if request.user.is_authenticated:
        object_list = s3objects.objects.all()
    return render(request, 's3objects/home.html', {'object_list': object_list})


def account(request):
    user_list = UserSocialAuth.objects.all()
    return render(request, 's3objects/account.html', {'sau': user_list})


from django import forms
from django.http import HttpResponseRedirect


class s3objectForm(forms.ModelForm):
    class Meta:
        model = s3objects
        fields = ['file', 'description']
        exclude = ('owner',)


def upload_file(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = s3objectForm(request.POST, request.FILES)
            if form.is_valid():
                new_s3object = form.save(commit=False)
                new_s3object.owner = request.user
                new_s3object = form.save()
                return HttpResponseRedirect('/')
        else:
            form = s3objectForm()
        return render(request, 's3objects/upload.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def update_file(request, id):
    if request.user.is_authenticated and s3objects.objects.get(pk=id).owner == request.user:
        old_file = s3objects.objects.get(pk=id)
        form = s3objectForm(request.POST or None, request.FILES, instance=old_file)
        if request.POST and form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

        return render(request, 's3objects/upload.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def delete_file(request, id):
    if request.user.is_authenticated and s3objects.objects.get(pk=id).owner == request.user:
        sel_file = s3objects.objects.get(pk=id)
        if request.method == 'POST':
            sel_file.delete()
            return HttpResponseRedirect('/')

        return render(request, 's3objects/delete.html', {'sel_file': sel_file})
    else:
        return HttpResponseRedirect('/login/')


from django.contrib.auth.forms import UserCreationForm


class registrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = registrationForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                return HttpResponseRedirect('/')
        else:
            form = registrationForm()
        return render(request, 's3objects/registration/register.html', {'form': form})
