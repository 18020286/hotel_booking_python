from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from hotel.models import Room, Blog, Reservation, RoomDetail
from profiles.models import User, MyBooking


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

        room_available = RoomDetail.objects.all().exclude(id__in=room_reserved).filter(type__num_person=str(request.POST['capacity']))
        room_list = Room.objects.all().filter(id__in=room_available.values('type_id'))
        print(room_available)
        data = {'room_list': room_list, 'rr_list': room_reserved, 'room_available': room_available, 'check_in': check_in,
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


@login_required()
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
        my_booking = MyBooking()
        my_booking.guest = current_user
        my_booking.room = room_name
        my_booking.check_in = request.session['check_in']
        my_booking.check_out = request.session['check_out']
        my_booking.price = price
        my_booking.nights = nights
        my_booking.amount = total
        my_booking.save()
        return redirect('booking')

    return render(request, 'payment.html', data)


def reservation_management_view(request):
    reservations = Reservation.objects.all()
    data = {'reservations': reservations}
    return render(request, 'reservation_management.html', data)
