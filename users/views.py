from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        # request.POST contains all the data submitted via the POST request, which includes the values entered by the user in the registration form.
        form = UserCreationForm(request.POST)
        if form.is_valid(): #Here django does the backend checks
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for '{username}'")
            return redirect('blog-home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
