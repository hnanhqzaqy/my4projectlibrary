from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (ListView,CreateView,UpdateView,DeleteView,DetailView,TemplateView,)
from .forms import (CategoryForm,AuthorForm,PublisherForm,BookForm,BorrowForm,)
from .models import (Category,Author,Publisher,Book,Borrow,)
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import SuperUserRequiredMixin
from .forms import BorrowApprovalForm
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import get_object_or_404
from accounts.models import CustomUser
from django.db.models import ProtectedError
from django.db.models.deletion import ProtectedError




# ==================================================
# Category Views
# ==================================================
class CategoryListView(LoginRequiredMixin,ListView):
    model = Category
    template_name = "books/category/category_list.html"
    context_object_name = "categories"
    paginate_by = 10

    def get_queryset(self):
        queryset = Category.objects.all()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        return queryset
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["sidebar"] = "category"
            return context




class AdminCategoryListView( SuperUserRequiredMixin, ListView,):
    model = Category
    template_name = "books/admin/category_list.html"
    context_object_name = "categories"
    paginate_by = 10

    def get_queryset(self):
        queryset = Category.objects.all()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search,)
        return queryset

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["sidebar"] = "category"
            return context




class CategoryDetailView(DetailView):
    model = Category
    template_name = "books/category/category_detail.html"
    context_object_name = "category"



class CategoryCreateView(SuperUserRequiredMixin,SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "books/category/category_create.html"
    success_url = reverse_lazy("admin-category-list")
    success_message = "دسته‌بندی با موفقیت ایجاد شد."
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "category"
        return context




class CategoryUpdateView(SuperUserRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "books/category/category_update.html"
    success_url = reverse_lazy("admin-category-list")
    success_message = "دسته‌بندی با موفقیت ویرایش شد."
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "category"
        return context







class CategoryDeleteView(SuperUserRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "books/category/category_delete.html"
    success_url = reverse_lazy("admin-category-list")
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.books.exists():
            messages.error(request,f"دسته‌بندی «{self.object.name}» دارای کتاب ثبت‌شده است و امکان حذف آن وجود ندارد.")
            return redirect("admin-category-list")
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        messages.success(self.request,"دسته‌بندی با موفقیت حذف شد.")
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "category"
        return context





# ==================================================
# Author Views
# ==================================================
class AuthorListView(LoginRequiredMixin,ListView):
    model = Author
    template_name = "books/author/author_list.html"
    context_object_name = "authors"
    paginate_by = 10

    def get_queryset(self):
        queryset = Author.objects.all()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter( Q(full_name__icontains=search) )
        return queryset
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["sidebar"] = "author"
            return context



class AdminAuthorListView(SuperUserRequiredMixin,ListView,):
    model = Author
    template_name = "books/admin/author_list.html"
    context_object_name = "authors"
    paginate_by = 10

    def get_queryset(self):
        queryset = Author.objects.all()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                full_name__icontains=search,)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "author"
        return context




class AuthorDetailView(DetailView):
    model = Author
    template_name = "books/author/author_detail.html"
    context_object_name = "author"



class AuthorCreateView(SuperUserRequiredMixin,SuccessMessageMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = "books/author/author_create.html"
    success_url = reverse_lazy("admin-author-list")
    success_message = "نویسنده با موفقیت ایجاد شد."
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "author"
        return context



class AuthorUpdateView(SuperUserRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = "books/author/author_update.html"
    success_url = reverse_lazy("admin-author-list")
    success_message = "نویسنده با موفقیت ویرایش شد."
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "author"
        return context



class AuthorDeleteView(SuperUserRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Author
    template_name = "books/author/author_delete.html"
    success_url = reverse_lazy("admin-author-list")
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.books.exists():
            messages.error(request,f"نویسنده «{self.object.full_name}» دارای کتاب ثبت‌شده است و امکان حذف آن وجود ندارد.")
            return redirect("admin-author-list")
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        messages.success(self.request, "نویسنده با موفقیت حذف شد.")
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "author"
        return context




# ==================================================
# Publisher Views
# ==================================================
class PublisherListView(LoginRequiredMixin,ListView):
    model = Publisher
    template_name = "books/publisher/publisher_list.html"
    context_object_name = "publishers"
    paginate_by = 10

    def get_queryset(self):
        queryset = Publisher.objects.all()
        search = self.request.GET.get("search")
        if search:queryset = queryset.filter(Q(name__icontains=search))
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "publisher"
        return context




class AdminPublisherListView(SuperUserRequiredMixin,ListView,):
    model = Publisher
    template_name = "books/admin/publisher_list.html"
    context_object_name = "publishers"
    paginate_by = 10

    def get_queryset(self):
        queryset = Publisher.objects.all()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                name__icontains=search, )
        return queryset

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["sidebar"] = "publisher"
            return context



class PublisherDetailView(DetailView):
    model = Publisher
    template_name = "books/publisher/publisher_detail.html"
    context_object_name = "publisher"



class PublisherCreateView(SuperUserRequiredMixin,SuccessMessageMixin, CreateView):
    model = Publisher
    form_class = PublisherForm
    template_name = "books/publisher/publisher_create.html"
    success_url = reverse_lazy("admin-publisher-list")
    success_message = "ناشر با موفقیت ایجاد شد."
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "publisher"
        return context




class PublisherUpdateView(SuperUserRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Publisher
    form_class = PublisherForm
    template_name = "books/publisher/publisher_update.html"
    success_url = reverse_lazy("admin-publisher-list")
    success_message = "ناشر با موفقیت ویرایش شد."
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "publisher"
        return context




class PublisherDeleteView(SuperUserRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Publisher
    template_name = "books/publisher/publisher_delete.html"
    success_url = reverse_lazy("admin-publisher-list")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.books.exists():
            messages.error(
                request,
                f"ناشر «{self.object.name}» دارای کتاب ثبت‌شده است و امکان حذف آن وجود ندارد."
            )
            return redirect("admin-publisher-list")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request,
            "ناشر با موفقیت حذف شد."
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "publisher"
        return context






# ==================================================
# Book Views
# ==================================================
class AdminBookListView(SuperUserRequiredMixin,ListView,):
    model = Book
    template_name = "books/admin/book_list.html"
    context_object_name = "books"
    paginate_by = 10
    def get_queryset(self):
        queryset = Book.objects.select_related(
            "category",
            "author",
            "publisher", )
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(isbn__icontains=search)
                | Q(author__full_name__icontains=search)
                | Q(publisher__name__icontains=search)
                | Q(category__name__icontains=search) )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "book"
        return context
    



class BookListView(ListView):
    model = Book
    template_name = "books/book/book_list.html"
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            queryset = Book.objects.select_related(
                "category",
                "author",
                "publisher",)
        else:
            queryset = Book.objects.filter(
                is_active=True
            ).select_related(
                "category",
                "author",
                "publisher",)
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(isbn__icontains=search) |
                Q(author__full_name__icontains=search) |
                Q(publisher__name__icontains=search) |
                Q(category__name__icontains=search) )
        return queryset




class BookDetailView(DetailView):
    model = Book
    context_object_name = "book"

    def get_queryset(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.is_superuser):
            return Book.objects.all()
        return Book.objects.filter(is_active=True)
    def get_template_names(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.is_superuser):
            return ["books/admin/book_detail.html"]
        return ["books/book/book_detail.html"]




class BookCreateView(SuperUserRequiredMixin,SuccessMessageMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book/book_create.html"
    success_url = reverse_lazy("admin-book-list")
    success_message = "کتاب با موفقیت ثبت شد."
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "book"
        return context



class BookUpdateView(SuperUserRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book/book_update.html"
    success_url = reverse_lazy("admin-book-list")
    success_message = "کتاب با موفقیت ویرایش شد."
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "book"
        return context



class BookDeleteView(SuperUserRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "books/book/book_delete.html"
    success_url = reverse_lazy("admin-book-list")

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        # اگر کتاب در امانت فعال باشد، اجازه بایگانی نده
        if Borrow.objects.filter(
            book=book,
            status=Borrow.STATUS_APPROVED,).exists():
            messages.error(request,"این کتاب در حال حاضر در امانت است و امکان بایگانی آن وجود ندارد.")
            return redirect("admin-book-list")
        # بایگانی کتاب
        book.is_active = False
        book.save()
        messages.success( request, "کتاب با موفقیت بایگانی شد.")
        return redirect("admin-book-list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "book"
        return context
    
    
class BookRestoreView(SuperUserRequiredMixin, LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.is_active = True
        book.save()
        messages.success(request, "کتاب با موفقیت بازیابی شد.")
        return redirect("admin-book-list")
    
    
    
    
class BookPermanentDeleteView(SuperUserRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "books/book/book_permanent_delete.html"
    success_url = reverse_lazy("admin-book-list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar"] = "book"
        return context
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # ابتدا باید کتاب بایگانی شده باشد
        if self.object.is_active:
            messages.error(request,"ابتدا کتاب را بایگانی کنید، سپس در صورت نیاز حذف دائمی انجام دهید.")
            return redirect("admin-book-list")
        # اگر کتاب در امانت فعال است
        if Borrow.objects.filter(
            book=self.object,
            status=Borrow.STATUS_APPROVED,).exists():
            messages.error(request,"❌ این کتاب در حال حاضر در امانت است و امکان حذف دائمی آن وجود ندارد.")
            return redirect("admin-book-list")
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request,"🗑 کتاب با موفقیت برای همیشه حذف شد.")
        return redirect("admin-book-list")
        
        
        
        
        
        
        
        

class BorrowListView(LoginRequiredMixin, ListView):
    model = Borrow
    template_name = "books/borrow/borrow_list.html"
    context_object_name = "borrows"
    paginate_by = 10
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Borrow.objects.select_related(
                "book",
                "user",
            ).order_by("-request_date")
        return Borrow.objects.filter(
            user=self.request.user
        ).select_related(
            "book",
            "user",
        ).order_by("-request_date")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["pending_count"] = queryset.filter(
            status=Borrow.STATUS_PENDING
        ).count()
        context["approved_count"] = queryset.filter(
            status=Borrow.STATUS_APPROVED
        ).count()
        context["returned_count"] = queryset.filter(
            status=Borrow.STATUS_RETURNED
        ).count()
        return context
    
    
    
class AdminBorrowListView(SuperUserRequiredMixin,ListView,):
    model = Borrow
    template_name = "books/admin/borrow_list.html"
    context_object_name = "borrows"
    paginate_by = 10

    def get_queryset(self):
        return Borrow.objects.select_related(
            "book",
            "user",
        ).order_by("-request_date")
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["pending_count"] = queryset.filter(
            status=Borrow.STATUS_PENDING
        ).count()
        context["approved_count"] = queryset.filter(
            status=Borrow.STATUS_APPROVED
        ).count()
        context["returned_count"] = queryset.filter(
            status=Borrow.STATUS_RETURNED
        ).count()
        context["sidebar"] = "borrow"
        return context
        
        
    
    
class BorrowCreateView(LoginRequiredMixin, CreateView):
    model = Borrow
    form_class = BorrowForm
    template_name = "books/borrow/borrow_create.html"
    success_url = reverse_lazy("my-borrows")
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            messages.error( request, "مدیر نمی‌تواند با حساب مدیریتی درخواست امانت ثبت کند.")
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        book = form.cleaned_data["book"]
        if Borrow.objects.filter(
            user=user,
            book=book,
            status__in=[
                Borrow.STATUS_PENDING,
                Borrow.STATUS_APPROVED,],).exists():
            form.add_error("book","شما قبلاً برای این کتاب یک درخواست فعال ثبت کرده‌اید.")
            return self.form_invalid(form)
        form.instance.user = user
        form.instance.book_title = book.title
        return super().form_valid(form)
    
    
    
# class BorrowUpdateView(UpdateView):
#     model = Borrow
#     form_class = BorrowForm
#     template_name = "books/borrow/borrow_update.html"
#     success_url = reverse_lazy("borrow-list")

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         if self.object.return_date:
#             self.object.book.is_available = True
#             self.object.book.save()
#         return response
    
    
    
    
class BorrowApproveView(SuperUserRequiredMixin, UpdateView):
    model = Borrow
    form_class = BorrowApprovalForm
    template_name = "books/borrow/borrow_approve.html"
    def dispatch(self, request, *args, **kwargs):
        borrow = self.get_object()
        if borrow.status != Borrow.STATUS_PENDING:
            messages.error(request, "این درخواست قبلاً بررسی شده است.")
            return redirect("admin-borrow-list")
        # کتاب حذف شده
        if borrow.book is None:
            messages.error(request,f"کتاب «{borrow.book_title}» حذف شده است و این درخواست دیگر قابل بررسی نیست.")
            return redirect("admin-borrow-list")
        # کتاب بایگانی شده
        if not borrow.book.is_active:
            messages.error(request,f"کتاب «{borrow.book.title}» بایگانی شده است و این درخواست دیگر قابل بررسی نیست.")
            return redirect("admin-borrow-list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        borrow = form.save(commit=False)
        # کتاب حذف شده
        if borrow.book is None:
            messages.error(self.request,f"کتاب «{borrow.book_title}» حذف شده است و امکان تأیید این درخواست وجود ندارد.")
            return redirect("admin-borrow-list")
        # کتاب بایگانی شده
        if not borrow.book.is_active:
            messages.error( self.request,f"کتاب «{borrow.book.title}» بایگانی شده است و امکان تأیید این درخواست وجود ندارد." )
            return redirect("admin-borrow-list")
        if borrow.status == Borrow.STATUS_APPROVED:
            now = timezone.now()
            borrow.approved_at = now
            borrow.edit_deadline = now + timedelta(hours=24)
            borrow.borrow_date = now.date()
            borrow.due_date = borrow.borrow_date + timedelta(days=14)
            borrow.book.is_available = False
            borrow.book.save()
        elif borrow.status == Borrow.STATUS_REJECTED:
            borrow.book.is_available = True
            borrow.book.save()
        borrow.save()
        return redirect("admin-borrow-list")
    
    
    
    
class BorrowReturnView(SuperUserRequiredMixin,View,):
    def post(self, request, pk):
        borrow = get_object_or_404(Borrow, pk=pk,)
        if borrow.return_date:
            messages.warning(request,"این کتاب قبلاً تحویل داده شده است.",)
            return redirect("borrow-list")
        borrow.return_date = timezone.now().date()
        borrow.status = Borrow.STATUS_RETURNED
        borrow.book.is_available = True
        borrow.book.save()
        borrow.save()
        messages.success(request,"کتاب با موفقیت بازگردانده شد.",)
        return redirect("admin-borrow-list")
    
    
    
    
class DashboardView(SuperUserRequiredMixin, TemplateView):
    template_name = "books/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books_count"] = Book.objects.count()
        context["available_books"] = Book.objects.filter(is_available=True).count()
        context["borrowed_books"] = Borrow.objects.filter(status=Borrow.STATUS_APPROVED).count()
        context["pending_requests"] = Borrow.objects.filter(status=Borrow.STATUS_PENDING).count()
        context["authors_count"] = Author.objects.count()
        context["publishers_count"] = Publisher.objects.count()
        context["categories_count"] = Category.objects.count()
        context["users_count"] = CustomUser.objects.count()
        context["sidebar"] = "dashboard"
        return context
    
    


class MyBorrowListView(LoginRequiredMixin, ListView):
    model = Borrow
    template_name = "books/borrow/my_borrow_list.html"
    context_object_name = "borrows"
    paginate_by = 10

    def get_queryset(self):
        return (
            Borrow.objects.filter(user=self.request.user)
            .select_related(
                "book",
                "user",)
            .order_by("-request_date"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["pending_count"] = queryset.filter(
            status=Borrow.STATUS_PENDING
        ).count()
        context["approved_count"] = queryset.filter(
            status=Borrow.STATUS_APPROVED
        ).count()
        context["returned_count"] = queryset.filter(
            status=Borrow.STATUS_RETURNED
        ).count()
        return context
    
    
    
    
class BorrowCancelView(LoginRequiredMixin, DeleteView):
    model = Borrow
    template_name = "books/borrow/borrow_cancel.html"
    success_url = reverse_lazy("my-borrows")
    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status != Borrow.STATUS_PENDING:
            messages.error(request,"فقط درخواست‌های در انتظار قابل لغو هستند.")
            return redirect("my-borrows")
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delete_message"] = (f"آیا از لغو درخواست امانت کتاب "f"«{self.object.book_title}» "f"مطمئن هستید؟")
        return context
    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request,"درخواست امانت با موفقیت لغو شد.")
        return redirect("my-borrows")
