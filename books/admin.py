from django.contrib import admin
from .models import Borrow



@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):

    list_display = (
        "book",
        "user",
        "borrow_date",
        "due_date",
        "return_date",
    )

    list_filter = (
        "borrow_date",
        "due_date",
    )

    search_fields = (
        "book__title",
        "user__username",
    )