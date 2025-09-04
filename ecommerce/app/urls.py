from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import PasswordChangeView,LogoutView,PasswordResetCompleteView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetView
from .forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MyPasswordSetForm


urlpatterns = [
    path("",views.home ,name="home"),
    path("about",views.about ,name="about"),
    path("contact",views.contact,name="contact" ),
    path("category/<slug:val>",views.CategoryView.as_view(),name="category"),
    path("category-title/<str:val>",views.CategoryTitle.as_view(),name="category-title"),
    path("product-detail/<int:pk>",views.ProductDetails.as_view(),name="product-detail"),
    #registration
    path("registration/",views.CustomerRegistrationView.as_view(),name="customerregistration"),
    path("accounts/login/",auth_view.LoginView.as_view(template_name='app/login.html',form_class=LoginForm),name="login"),
    path("password_reset/",PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path("password_reset/done",PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path("password-reset-confirm/<uidb64>/<token>",PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MyPasswordSetForm),name='password_reset_confirm'),
    path("password-reset-complete/",PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),
    path("changepassword/",PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),
    name='changepassword'),
    path("passwordchangedone/",auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),
    name='passwordchangedone'),
    path("profile/",views.ProfileView.as_view(),name='profile'),
    path("address/",views.address,name='address'),
    path("updateAddress/<int:pk>",views.UpdateAddress.as_view(),name='updateAddress'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('cart/',views.show_cart,name='show_cart'),
    path('pluscart/',views.plus_cart,name="plus_cart"),
    path('minuscart/',views.minus_cart,name="minus_cart"),
    path('removecart/',views.remove_cart,name="remove_cart"),
    path('checkout/',views.Checkout.as_view(),name='checkout'),
    path('search/', views.search_products, name='search'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)