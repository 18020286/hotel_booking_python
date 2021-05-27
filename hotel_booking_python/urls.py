from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


from hotel import views
from profiles import views as profiles_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home_view, name='home'),
    path('room/', views.SiteRoomView.as_view(), name='room'),
    path('about/', views.about_view, name='about'),
    path('blog/', views.SiteBlogView.as_view(), name='blog'),

    # path('accounts/', include('django.contrib.auth.urls')),
    path('login/', profiles_views.SiteLoginView.as_view(), name='login'),
    path('logout/', profiles_views.SiteLogoutView.as_view(), name='logout'),

    path('guest', profiles_views.GuestView.as_view(), name='guest'),
    path('guest/profile/', profiles_views.ProfileEditView.as_view(), name='profile'),
    path('guest/my_booking', profiles_views.my_booking_view, name='my_booking'),
    path('register/', profiles_views.SiteRegisterView.as_view(), name='register'),
    path('register/ok/', profiles_views.SiteRegisterOkView.as_view(), name='register_ok'),

    path('booking/', views.booking_view, name="booking"),
    path('payment', views.payment, name='payment'),

    path('admin/reservation_management', views.reservation_management_view, name="reservation_management"),
    path('admin/room_detail', views.room_detail_view, name="room_detail"),

    path('admin/room_detail/add_room', views.AddRoom.as_view(), name='add_room'),
    path('admin/room_category', views.room_category_view, name="room_category"),
    path('admin/room_category/add_category', views.AddCategory.as_view(), name="add_category"),
    path('admin/room_category/edit_category/<str:pk>', views.edit_category_view, name="edit_category"),

    path('admin/blog', views.blog_management_view, name="blog_management"),
    path('admin/blog/add_blog', views.AddBlog.as_view(), name="add_blog"),
    path('admin/blog/edit_blog/<str:pk>', views.edit_blog_view, name="edit_blog"),

    path('admin/user', profiles_views.user_management_view, name="user_management"),
    path('admin/user/add', profiles_views.AddUser.as_view(), name="add_user"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

