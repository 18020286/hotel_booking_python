from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import forms, models
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, UpdateView

from profiles.forms import RegisterForm
from profiles.models import MyBooking

User = get_user_model()


class SiteLoginView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = 'login'
        return context


# class EditProfileView(LoginRequiredMixin, TemplateView):
#     template_name = 'profile.html'
#
# # @login_required
# # def edit_profile_view(request):
# #     return render(request, 'profile.html', {})


class SiteRegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        data = form.cleaned_data
        new_user = User.objects.create_user(
            username=data['username'],
            password=data['password1'],
            email=data['email']
        )
        url = f"{reverse('register_ok')}?username={new_user.username}"
        return redirect(url)


class SiteRegisterOkView(TemplateView):
    template_name = 'register_ok.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.GET.get('username')
        return context


class SiteLogoutView(LogoutView):
    template_name = 'logout.html'


class ProfileEditView(LoginRequiredMixin, SuccessMessageMixin,  UpdateView):
    template_name = 'profile.html'
    model = User
    fields = ('first_name', 'last_name', 'address', 'year_birth', 'phone_no', 'bank_no')
    success_url = reverse_lazy('profile')
    success_message = "Changes successfully saved"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = 'profile'
        return context


class MyBookingView(LoginRequiredMixin, TemplateView):
    template_name = 'my_booking.html'


class GuestView(LoginRequiredMixin, TemplateView):
    template_name = 'guest.html'
    # success_url = reverse_lazy('guest')

    def get_object(self, queryset=None):
        return self.request.user


@login_required()
def my_booking_view(request):
    current_user = request.user
    my_bookings = MyBooking.objects.all().filter(guest_id=current_user.id)
    num_bookings = len(my_bookings)
    data = {'my_bookings': my_bookings, 'num_bookings': num_bookings}
    return render(request, 'my_booking.html', data)