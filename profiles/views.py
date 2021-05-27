from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import forms, models
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, UpdateView, CreateView

from profiles.forms import RegisterForm, AddUserForm
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


def check_admin(user):
    return user.is_superuser


@user_passes_test(check_admin)
def user_management_view(request):
    if request.method == "GET":
        try:
            cid = request.GET.get('cid')
            action = request.GET.get('action')
            user = User.objects.get(id=cid)
            if action == 'delete':
                user.delete()
                messages.success(request, "Delete user successfully!")
            elif action == 'activate':
                user.is_staff = True
                user.save()
                messages.success(request, "Activate staff successfully!")
        except:
            pass
    admin = User.objects.filter(username='admin').only('id')
    users = User.objects.all().exclude(id__in=admin).order_by('id')
    data = {'users': users, 'nav': 'user'}
    return render(request, 'user_management.html', data)


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


# class AddUser(SuccessMessageMixin, CreateView, AdminStaffRequiredMixin):
#     template_name = 'add_user.html'
#     model = User
#     fields = ['']
#     success_url = reverse_lazy('user_management')
#     success_message = "Create new user successfully!"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
class AddUser(CreateView, SuccessMessageMixin):
    template_name = 'add_user.html'
    # form_class = AddUserForm
    model = User
    # fields = '__all__'
    fields = ['username', 'password', 'email', 'first_name', 'last_name']
    success_url = reverse_lazy('user_management')
    success_message = "Create new user successfully!"

    # def form_valid(self, form):
    #     data = form.cleaned_data
    #     new_user = User.objects.create_user(
    #         username=data['username'],
    #         password=data['password1'],
    #         email=data['email'],
    #         first_name=data['first_name'],
    #         last_name=data['last_name']
    #     )
    #     return redirect('user_management')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    # def get_queryset(self):
    #     pass
