from datetime import datetime

from django.db import models

from profiles.admin import User


class Room(models.Model):
    NUM_PERSON = (
        ('single', 'single'),
        ('double', 'double'),
        ('family', 'family')
    )
    room_type = models.CharField(max_length=200)
    price = models.PositiveSmallIntegerField(default=0)
    num_person = models.CharField(choices=NUM_PERSON, max_length=50)
    num_room = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()
    picture = models.ImageField(upload_to='room_pictures')

    def __str__(self):
        return self.room_type


class HotelInfo(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Blog(models.Model):
    blog_name = models.CharField(max_length=1000)
    type = models.CharField(max_length=200)
    post_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    picture = models.ImageField(upload_to='other')
    content = models.TextField()
    author = models.CharField(max_length=200)

    def __str__(self):
        return self.blog_name


class RoomDetail(models.Model):
    type = models.ForeignKey(Room, on_delete=models.CASCADE)
    ROOM_STATUS = (
        ('available', 'available'),
        ('unavailable', 'unavailable'),
        ('checkedIn', 'checkedIn')
    )
    status = models.CharField(choices=ROOM_STATUS, max_length=50)

    def __str__(self):
        return self.type.room_type


class Reservation(models.Model):
    check_in = models.DateField(auto_now=False)
    check_out = models.DateField()
    room = models.ForeignKey(RoomDetail, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.PositiveSmallIntegerField(default=0)
    transaction_date = models.DateTimeField(default=datetime.now())
    RESERVATION_STATUS = (
        ('confirmed', 'confirmed'),
        ('checkedIn', 'checkedIn'),
        ('checkedOut', 'checkedOut'),
        ('pending', 'pending')
    )

    reservation_status = models.CharField(choices=RESERVATION_STATUS, max_length=50, default='pending')

    def __str__(self):
        return self.guest.username
