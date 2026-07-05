from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
)
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, ProfileUpdateForm
from core.mixins import SuperUserRequiredMixin
from django.views.generic import TemplateView
from books.models import Borrow
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login
from .forms import RegisterForm
from django.shortcuts import render, redirect





class UserListView(LoginRequiredMixin,ListView):
    model = CustomUser
    template_name = "accounts/user_list.html"
    context_object_name = "users"
    paginate_by = 10
    ordering = ["username"]

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email__icontains=search)
            )
        return queryset


class AdminUserListView(
    SuperUserRequiredMixin,
    ListView,):
    model = CustomUser
    template_name = "accounts/admin/user_list.html"
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        queryset = CustomUser.objects.order_by("-date_joined")
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(username__icontains=search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "user"
        return context



 
    
    
    
class UserDeleteView(SuperUserRequiredMixin,LoginRequiredMixin,DeleteView):
    model = CustomUser
    template_name = "accounts/user_delete.html"
    success_url = reverse_lazy("user-list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "کاربر با موفقیت حذف شد."
        )
        return super().form_valid(form)
    
    
    
    
    
class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy("dashboard")
        return reverse_lazy("book-list")


class UserLogoutView(LogoutView):
    """
    خروج کاربران
    """

    next_page = "login"
    
    
    
    

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["active_borrows"] = Borrow.objects.filter(
            user=user,
            status=Borrow.STATUS_APPROVED,
        ).count()
        context["pending_borrows"] = Borrow.objects.filter(
            user=user,
            status=Borrow.STATUS_PENDING,
        ).count()
        context["total_borrows"] = Borrow.objects.filter(
            user=user,
        ).count()
        return context
    
    def get_template_names(self):
        if self.request.user.is_superuser:
            return ["accounts/admin/profile.html"]
        return ["accounts/profile.html"]
        
    
    
class ProfileUpdateView(
    LoginRequiredMixin,
    UpdateView,):
    form_class = ProfileUpdateForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user
    
    def get_template_names(self):
        if self.request.user.is_superuser:
            return ["accounts/admin/profile_edit.html"]
        return ["accounts/profile_edit.html"]
        
    
    
class UserPasswordChangeView(
    LoginRequiredMixin,
    PasswordChangeView,):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        messages.success(self.request, "رمز عبور با موفقیت تغییر کرد.",)
        return super().form_valid(form)
    
    def get_template_names(self):
        if self.request.user.is_superuser:
            return ["accounts/admin/change_password.html"]
        return ["accounts/change_password.html"]
    
    
    


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("book-list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("book-list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(
            self.request,
            self.object,
        )
        messages.success(self.request, "ثبت‌نام با موفقیت انجام شد.", )
        return response