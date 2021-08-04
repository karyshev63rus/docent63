from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UpdateUserForm, UpdateProfileForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def profile(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        if user is None or user.id == request.user.id:
            user_form = UpdateUserForm(
                instance=request.user,
                data=request.POST
            )
            profile_form = UpdateProfileForm(
                instance=request.user.profile,
                data=request.POST
            )
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Профиль успешно обновлен')
        else:
            messages.error(request, 'Пользователь с данным e-mail уже существует')
        return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request,
                  'account/profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
