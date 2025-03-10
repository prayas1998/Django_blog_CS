# from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from helper import check_image_nsfw


def register(request):
    if request.method == "POST":
        # request.POST contains all the data submitted via the POST request, which includes the values entered by the user in the registration form.
        form = UserRegisterForm(request.POST)
        if form.is_valid():  # Here django does the backend checks
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account has been successfully created. You can now login!"
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(request, "users/logout.html")


@login_required()
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            if "image" in request.FILES:
                uploaded_image = request.FILES["image"]
                is_nsfw = check_image_nsfw(uploaded_image)
                if is_nsfw is None:
                    messages.error(
                        request,
                        "An error occurred while processing the image. Please try again.",
                        extra_tags="danger",
                    )
                    return redirect("profile")
                elif is_nsfw:
                    messages.error(
                        request,
                        "The uploaded image contains inappropriate content. Please choose another image.",
                        extra_tags="danger",
                    )
                    return redirect("profile")

            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile.html", context)
