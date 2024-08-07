# accounts/views.py
from django.contrib import auth, messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse

from django.contrib.auth.models import User

from mvw.settings import SYSTEM_NAME

from mvw.accounts.forms import LoginForm, UsersForm, UsersUpdateForm, SignupForm, ForgottenPasswordForm, \
    PasswordChangeForm
from mvw.accounts.tokens import account_activation_token

import base64
import qrcode
import io


def make_code(url):
    image = qrcode.make(url)
    return image


def get_redirect_path(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
        return redirect_path
    else:
        return "/walk/"


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = LoginForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            print(get_redirect_path(request))
            return redirect(get_redirect_path(request))
        else:
            return redirect('/')

    return render(request, 'accounts/login.html', {'form': form})


def sign_out(request):
    auth.logout(request)
    return redirect('/')


#def logout_view(request):
#    logout(request)
#    return redirect('/')


def build_message(request, template, user):
    current_site = get_current_site(request)
    message = render_to_string(template, {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    return message


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            from .tokens import account_activation_token as token

            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            # https://stackoverflow.com/questions/76580910/is-it-possible-to-create-a-qr-code-for-an-image-using-the-python-qrcode-library
            domain = request.META['HTTP_HOST']
            username = new_user.username
            url = f"http://{domain}/accounts/activate/{username}/{token.make_token(new_user)}"
            qr = make_code(url)
            #
            temp = io.BytesIO()
            qr.save(temp)
            temp.seek(0)
            b = temp.read()
            b64 = 'data:image/gif;base64,' + base64.standard_b64encode(b).decode()
            #
            return render(request, 'accounts/complete.html', {"qr64": b64, "url_complete": url})
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def activate(request, username, token):
    try:
        username = force_str(username)
        user = User.objects.get(username=username)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        print("here")
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request,  'core/index.html',
                      {'message': "Thank you for clicking on the link. Now you can start using the system."})
    else:
        return render(request, 'core/index.html', {'message': 'Activation link is invalid!'})


@sensitive_post_parameters()
@csrf_protect
@never_cache
def forgotten_password(request):
    if request.method == 'POST':
        form = ForgottenPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['email'])
            if user:
                user = user[0]  # first and only user
                #
                mail_subject = 'Password reset for your {0} account.'.format(SYSTEM_NAME)
                message = build_message(request, "accounts/acc_reset_password.html", user)
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                #
            return redirect('accounts:forgotten_password_done')
    else:
        form = ForgottenPasswordForm()
    return render(request, 'accounts/forgotten.html', {'form': form})


def profile(request, user_id):
    return update_user(request, user_id)


@user_passes_test(lambda u: u.is_superuser)
def list_users(request):
    users = User.objects.order_by('email')
    return render(request, 'accounts/users.html', {'users': users})


@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    form = UsersForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_users')
    return render(request, 'accounts/user-form.html', {'form': form})


@login_required()
def update_user(request):
    user = request.user
    form = UsersUpdateForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect(reverse('walk:home'))
    return render(request, 'accounts/user-form.html', {'form': form, 'user': user})


def password_change(request, user_id):
    if not request.user.is_superuser:
        if request.user.id != user_id:
            return redirect(reverse('base:index'))
    user = User.objects.get(id=user_id)
    form = PasswordChangeForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        login(request, user)
        return render(request,  'core/index.html', {'message': "Password was set!"})
    return render(request, 'accounts/password_change.html', {'form': form, 'user': user})


# @user_passes_test(lambda u: u.is_superuser)
def delete_user(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        auth.logout(request)
        return redirect(reverse('core:index'))
    return render(request, 'accounts/user-delete-confirm.html', {'user': user})
