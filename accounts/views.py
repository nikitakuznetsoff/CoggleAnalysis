from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from main_site.models import UserData


def registration(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        UserData.objects.create(user=user)
        return redirect('index')
    # else:
    #     form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})