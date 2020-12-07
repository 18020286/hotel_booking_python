from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    address = models.CharField(_('address'), max_length=500, blank=True)
    year_birth = models.PositiveSmallIntegerField(null=True, blank=True)
    phone_no = models.CharField(blank=True, max_length=20)
    bank_no = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.username


class MyBooking(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    room = models.CharField(max_length=200)
    check_in = models.DateField()
    check_out = models.DateField()
    price = models.PositiveSmallIntegerField(default=0)
    nights = models.PositiveSmallIntegerField(default=0)
    booking_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    amount = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.room
