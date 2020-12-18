from datetime import datetime, date
import django_filters
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView

from hotel.models import Room, Blog, Reservation, RoomDetail
from profiles.models import User, MyBooking

from .filters import RoomFilter
from .forms import CategoryForm, BlogForm


def home_view(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {
        'rooms_list': rooms,
        'nav': 'home'
    })


class SiteRoomView(TemplateView):
    template_name = 'room.html'

    def get_context_data(self, **kwargs):
        rooms = Room.objects.all()
        context = super().get_context_data(**kwargs)
        context['nav'] = 'room'
        context['rooms_list'] = rooms
        return context


def about_view(request):
    return render(request, 'about.html', {
        'nav': 'about'
    })


class SiteBlogView(TemplateView):
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        blogs = Blog.objects.all()
        context = super().get_context_data(**kwargs)
        context['nav'] = 'blog'
        context['blogs_list'] = blogs
        return context


def booking_view(request):
    if request.method == "POST":
        room_reserved = []
        for each_reservation in Reservation.objects.all():
            if str(each_reservation.check_in) > str(request.POST['cout']):
                pass
            elif str(each_reservation.check_out) < str(request.POST['cin']):
                pass
            else:
                room_reserved.append(each_reservation.room.id)

        check_in = request.POST.get('cin')
        check_out = request.POST.get('cout')

        room_available = RoomDetail.objects.all().exclude(id__in=room_reserved).filter(
            type__num_person=str(request.POST['capacity']), status='available')
        room_list = Room.objects.all().filter(id__in=room_available.values('type_id'))
        print(room_available)
        data = {'room_list': room_list, 'rr_list': room_reserved, 'room_available': room_available,
                'check_in': check_in,
                'check_out': check_out, 'check': 'already'}

        ra_id = [item.id for item in room_available]
        request.session['room_show'] = ra_id
        request.session['check_in'] = check_in
        request.session['check_out'] = check_out
        if len(room_available) == 0:
            messages.warning(request, "Sorry No Rooms Are Available on this time period")
        response = render(request, 'booking.html', data)
    else:
        rooms = Room.objects.all()
        data = {'room_list': rooms, }
        response = render(request, 'booking.html', data)
    return HttpResponse(response)


def check_guest(user):
    return not user.is_superuser


@login_required()
# @user_passes_test(check_guest)
def payment(request):
    check_in = parse_date(request.session['check_in'])
    check_out = parse_date(request.session['check_out'])
    nights = (check_out - check_in).days
    room_type_id = int(request.GET['room_id'])
    price = Room.objects.all().filter(id=room_type_id)[0].price
    total = nights * price
    # rooms = [RoomDetail.objects.get(id=room_id) for room_id in request.session['room_show']]
    room = RoomDetail.objects.filter(id__in=request.session['room_show'], type_id=room_type_id)[0]
    room_name = room.type
    data = {'room_select': room, 'check_in': check_in, 'check_out': check_out, 'nights': nights, 'price': price,
            'total': total, 'room_name': room_name}
    print(request.user)
    if request.method == "POST":
        current_user = request.user
        reservation = Reservation()
        # user_object = User.objects.all().get(username=current_user)
        reservation.guest = current_user
        reservation.room = room
        reservation.check_in = request.session['check_in']
        reservation.check_out = request.session['check_out']
        reservation.total_price = total
        reservation.save()
        messages.success(request, "Congratulations! Booking Successfull")
        return redirect('booking')

    return render(request, 'payment.html', data)


def check_admin(user):
    return user.is_superuser


@user_passes_test(check_admin)
def reservation_management_view(request):
    if request.method == "GET":
        reservation_id = request.GET.get('id')
        status = request.GET.get('status')
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            room = RoomDetail.objects.get(id=reservation.room_id)
            if status == 'confirmed':
                nights = (reservation.check_out - reservation.check_in).days
                total = nights * reservation.room.type.price
                my_booking = MyBooking()
                my_booking.guest = reservation.guest
                my_booking.room = reservation.room.type
                my_booking.check_in = reservation.check_in
                my_booking.check_out = reservation.check_out
                my_booking.price = reservation.room.type.price
                my_booking.nights = nights
                my_booking.amount = total
                my_booking.save()
            if status == 'checkedIn':
                if reservation.check_in <= date.today():
                    room.status = 'checkedIn'
                    reservation.reservation_status = status
                else:
                    messages.warning(request, "Check In isn't ready!")
            else:
                if status == 'checkedOut':
                    room.status = 'unavailable'
                # elif status == 'delete':
                #     room.status = 'available'
                reservation.reservation_status = status
            room.save()
            if status == 'delete':
                reservation.delete()
            else:
                reservation.save()
        except:
            pass
    reservations = Reservation.objects.all()
    data = {'reservations': reservations, 'nav': 'reservation'}
    return render(request, 'reservation_management.html', data)


@user_passes_test(check_admin)
def room_detail_view(request):
    r_id = request.GET.get('room_id')
    room_status = request.GET.get('status')
    rooms = RoomDetail.objects.all().order_by('id')
    myFilter = RoomFilter(request.GET, queryset=rooms)
    if r_id:
        myFilter = RoomFilter({}, queryset=rooms)
        try:
            room = RoomDetail.objects.get(id=r_id)
            if room_status == 'ready':
                room.status = 'available'
                room.save()
            elif room_status == 'unavailable':
                room.status = 'unavailable'
                room.save()
        except:
            pass
    rooms = myFilter.qs
    total_rooms = len(RoomDetail.objects.all())
    rooms_available = len(RoomDetail.objects.filter(status='available'))
    rooms_unavailable = len(RoomDetail.objects.filter(status='unavailable'))
    rooms_checked_in = len(RoomDetail.objects.filter(status='checkedIn'))

    data = {'checkedIn': rooms_checked_in, 'total_rooms': total_rooms, 'unavailable': rooms_unavailable,
            'available': rooms_available, 'rooms': rooms, 'myFilter': myFilter, 'nav': 'room detail'}
    return render(request, 'room_detail.html', data)


class AddRoom(SuccessMessageMixin, CreateView):
    template_name = 'add_room.html'
    model = RoomDetail
    fields = '__all__'
    success_url = reverse_lazy('room_detail')
    success_message = "Create new room successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@user_passes_test(check_admin)
def room_category_view(request):
    if request.method == "GET":
        try:
            cid = request.GET.get('cid')
            category = Room.objects.get(id=cid)
            category.delete()
            messages.success(request, "Delete category successfully!")
        except:
            pass
    rooms = Room.objects.all().order_by('id')
    data = {'rooms': rooms, 'nav': 'room category'}
    return render(request, 'room_category.html', data)


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class AddCategory(SuccessMessageMixin, CreateView, AdminStaffRequiredMixin):
    template_name = 'add_category.html'
    model = Room
    fields = '__all__'
    success_url = reverse_lazy('room_category')
    success_message = "Create new category successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# class EditCategory(SuccessMessageMixin, UpdateView):
#     template_name = 'edit_category.html'
#     model = Room
#     fields = '__all__'
#     success_url = reverse_lazy('room_category')
#     success_message = "Update category successfully!"
#     slug_field = 'url'
#     slug_url_kwarg = 'url'
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(self.model, pk=self.request.user.pk)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


def edit_category_view(request, pk):
    room = Room.objects.get(id=pk)
    form = CategoryForm(instance=room)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Update category successfully!")
            return redirect('room_category')

    data = {'form': form}
    return render(request, 'edit_category.html', data)


@user_passes_test(check_admin)
def blog_management_view(request):
    if request.method == "GET":
        try:
            cid = request.GET.get('cid')
            blog = Blog.objects.get(id=cid)
            blog.delete()
            messages.success(request, "Delete blog successfully!")
        except:
            pass
    blogs = Blog.objects.all().order_by('id')
    data = {'blogs': blogs, 'nav': 'blog'}
    return render(request, 'blog_management.html', data)


def edit_blog_view(request, pk):
    blog = Blog.objects.get(id=pk)
    form = BlogForm(instance=blog)

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Update blog successfully!")
            return redirect('blog_management')

    data = {'form': form}
    return render(request, 'edit_blog.html', data)


class AddBlog(SuccessMessageMixin, CreateView, AdminStaffRequiredMixin):
    template_name = 'add_blog.html'
    model = Blog
    fields = '__all__'
    success_url = reverse_lazy('blog_management')
    success_message = "Create new blog successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
