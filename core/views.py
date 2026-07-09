from django.views.generic import TemplateView
from books.models import (
    Book,
    Category,
    Borrow,
    Author,
    Publisher
)
from accounts.models import CustomUser





class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context["books_count"] = Book.objects.count()
        context["categories_count"] = Category.objects.count()
        context["users_count"] = CustomUser.objects.count()
        context["borrows_count"] = Borrow.objects.count()
        return context
    
    
    
    
class AboutView(TemplateView):
    template_name = "core/about.html"
    
    
    
class ContactView(TemplateView):
    template_name = "core/contact.html"   