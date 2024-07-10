from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages

from .forms import SignUpForm, UserprofileForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        userprofileform = UserprofileForm(request.POST)

        if form.is_valid() and userprofileform.is_valid():
            user = form.save()

            userprofile = userprofileform.save(commit=False)
            userprofile.user = user
            userprofile.save()

            login(request, user)

            return redirect('index')
    else:
        form = SignUpForm()
        userprofileform = UserprofileForm()
    
    return render(request, 'userprofile/signup.html', {'form': form, 'userprofileform': userprofileform})

@login_required
def myaccount(request):
    return render(request, 'userprofile/myaccount.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")