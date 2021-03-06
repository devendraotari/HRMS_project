from django.urls import path, include
from management import views as user_view
from django.contrib.auth import views as auth
from . import views
from django.contrib.auth import authenticate, login, logout, get_user_model
urlpatterns = [
    # path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', user_view.register, name='register'),
    path('login/', user_view.CustomUserLoginView.as_view(), name='login'),
    path('login/success', user_view.login_success, name='login-success'),
    path('logout', user_view.logout_view, name="logout"),
    path('base/', user_view.base_view, name='base-view'),

    # path('logout/', auth.LogoutView.as_view(template_name='index.html'), name='logout'),
    # path('register', views.register, name="register"),
    # path('login', views.login, name="login"),
    # path('logout', views.logout, name="logout"),
    path('forgot_password', views.forgot_password, name="forgot_password"),
    path('AddEmployee', views.add_employee, name="AddEmployee"),
    path('addCat', views.add_categories),
    path('delete/<int:id>', views.delete),
    # path('edit/<int:id>', views.edit),
    path('Apply_leave', views.apply_leave, name="Apply_leave"),
    path('addleave', views.add_leave, name="addleave"),
    path('mailbox', views.mailbox, name="mailbox"),
    path('mail_detail', views.mail_detail, name="mail_detail"),
    path('mail_compose', views.mail_compose, name="mail_compose"),
    path('cardcustom', views.cardcustom, name="cardcustom"),
    path('widgets', views.widgets, name="widgets"),
    path('notifications', views.notifications, name="notifications"),
    path('addnotifications', views.addnotifications, name="addnotifications"),
    path('delete_N/<int:id>', views.delete_N, name="delete_N"),
    # path('edit_N/<int:id>', views.edit_N, name="edit_N"),
    path('contacts', views.contacts, name="contacts"),

]
