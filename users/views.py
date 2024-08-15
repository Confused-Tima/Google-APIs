from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from google_apis.mixins import (
    AjaxFormMixin,
    reCAPTCHAValidation,
    FormErrors,
)

from .forms import (
    UserForm,
    UserProfileForm,
    AuthForm,
)

result = "Error"
message = "There was an error, please try again"


class AccountView(TemplateView):
    """
    Generic FormView with our mixin to display user account page
    """

    template_name = "users/account.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def profile_view(request):
    """
    function view to allow users to update their profile
    """
    user = request.user
    up = user.userprofile

    form = UserProfileForm(instance=up)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = UserProfileForm(data=request.POST, instance=up)
        if form.is_valid():
            obj = form.save()
            obj.has_profile = True
            obj.save()
            result = "Success"
            message = "Your profile has been updated"
        else:
            message = FormErrors(form)
        data = {"result": result, "message": message}
        return JsonResponse(data)
    else:
        context = {"form": form}
        context["google_api_key"] = settings.GOOGLE_API_KEY
        context["base_country"] = settings.BASE_COUNTRY

        return render(request, "users/profile.html", context)


class SignUpView(AjaxFormMixin):
    """
    Generic FormView with our mixin for user sign-up with reCAPTURE security
    """

    template_name = "users/sign_up.html"
    form_class = UserForm
    success_url = "/"

    # reCAPTURE key required in context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recaptcha_site_key"] = settings.CAPTACHA_KEY
        return context

    # over write the mixin logic to get, check and save reCAPTURE score
    def form_valid(self, form: UserForm):
        resp = super(FormView, self).form_valid(form)
        if resp is not None:
            return resp
        if self.request.headers.get('x-requested-with') != 'XMLHttpRequest':
            return HttpResponseBadRequest("Invalid request")

        token = form.cleaned_data.get("token")
        captcha = reCAPTCHAValidation(token)
        if captcha["success"]:
            form.instance.email = form.username
            obj = form.save()
            up = obj.userprofile
            up.captcha_score = float(captcha["score"])
            up.save()

            login(
                self.request,
                obj,
                backend="django.contrib.auth.backends.ModelBackend",
            )

            # change result & message on success
            result = "Success"
            message = "Thank you for signing up"

        data = {"result": result, "message": message}
        return JsonResponse(data)


class SignInView(AjaxFormMixin):
    """
    Generic FormView with our mixin for user sign-in
    """

    template_name = "users/sign_in.html"
    form_class = AuthForm
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form, save=False)
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # attempt to authenticate user
            user = authenticate(self.request, username=username, password=password)
            if user is not None:
                login(
                    self.request,
                    user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                result = "Success"
                message = "You are now logged in"
            else:
                message = FormErrors(form)
            data = {"result": result, "message": message}
            return JsonResponse(data)
        return response


def sign_out(request):
    """
    Basic view for user sign out
    """
    logout(request)
    return redirect(reverse("users:sign-in"))
