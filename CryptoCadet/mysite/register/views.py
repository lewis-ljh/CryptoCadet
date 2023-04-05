from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, PersonalInfoForm, AddressForm
from main.models import Profile

from main.models import Address


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(f"/FillPersonalInfo/{user.id}")
    else:
        form = RegisterForm()
    return render(request, "register/register.html", {"form": form})


def personal_info(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    try:
        address = Address.objects.get(user_id=user_id)
    except Address.DoesNotExist:
        address = None

    if request.method == "POST":
        personal_info_form = PersonalInfoForm(request.POST, instance=profile)
        address_form = AddressForm(request.POST, instance=address)
        if personal_info_form.is_valid() and address_form.is_valid():
            personal_info_form.save()
            address = address_form.save(commit=False)
            address.user_id = profile.user_id
            address.save()
            return redirect("/home")
    else:
        personal_info_form = PersonalInfoForm(instance=profile)
        address_form = AddressForm(instance=address)
    return render(request, "register/personal_info.html",
                  {"personal_info_form": personal_info_form, "address_form": address_form})


