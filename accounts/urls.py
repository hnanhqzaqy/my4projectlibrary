from django.urls import path
from . import views




urlpatterns = [

    # ==========================
    # Authentication
    # ==========================
    path(
    "register/",
    views.RegisterView.as_view(),
    name="register",
    ),
    path(
        "login/",
        views.UserLoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        views.UserLogoutView.as_view(),
        name="logout",
    ),

    # ==========================
    # Users
    # ==========================

    path(
        "",
        views.UserListView.as_view(),
        name="user-list",
    ),
    path(
        "<int:pk>/delete/",
        views.UserDeleteView.as_view(),
        name="user-delete",
    ),
    
    path(
    "dashboard/users/",
    views.AdminUserListView.as_view(),
    name="admin-user-list",
    ),
    
    
    
    path(
        "profile/",
        views.ProfileView.as_view(),
        name="profile",
    ),
    path(
    "profile/edit/",
    views.ProfileUpdateView.as_view(),
    name="profile-edit",
    ),
    path(
    "profile/change-password/",
    views.UserPasswordChangeView.as_view(),
    name="change-password",
    ),

]