from django.views.generic import TemplateView

from books.models import (
    Book,
    Category,
    Author,
    Publisher,
)


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["books_count"] = Book.objects.count()
        context["categories_count"] = Category.objects.count()
        context["authors_count"] = Author.objects.count()
        context["publishers_count"] = Publisher.objects.count()
        return context
    
    
    
    
class AboutView(TemplateView):
    template_name = "core/about.html"
    
    
    
class ContactView(TemplateView):
    template_name = "core/contact.html"   