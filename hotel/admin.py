from django.contrib import admin

from hotel.models import Room, HotelInfo, Blog, RoomDetail, Reservation


class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'price', 'num_person')
    search_fields = ('room_type',)


class Hotel(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')


class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_name', 'post_date')


class RoomDetailAdmin(admin.ModelAdmin):
    model = RoomDetail
    list_display = ('id', 'type', 'get_capacity', 'status')
    list_display_links = ('type',)

    def get_capacity(self, obj):
        return obj.type.num_person
    get_capacity.short_description = 'capacity'


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'get_num_person', 'guest')
    list_display_links = ('room',)

    def get_num_person(self, obj):
        return obj.room.type.num_person
    get_num_person.short_description = 'capacity'


admin.site.register(Room, RoomAdmin)
admin.site.register(HotelInfo, Hotel)
admin.site.register(Blog, BlogAdmin)

admin.site.register(RoomDetail, RoomDetailAdmin)
admin.site.register(Reservation, ReservationAdmin)
