from django import forms

from .models import (
    Category,
    Author,
    Publisher,
    Book,
    Borrow,
)


class BootstrapFormMixin:

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():

            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):

                widget.attrs["class"] = "form-check-input"

            elif isinstance(
                widget,
                (
                    forms.Select,
                    forms.SelectMultiple,
                ),
            ):

                widget.attrs["class"] = "form-select"

            elif isinstance(
                widget,
                forms.FileInput,
            ):

                widget.attrs["class"] = "form-control"

            else:

                widget.attrs["class"] = "form-control"


class CategoryForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            "name",
        ]


class AuthorForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = Author
        fields = [
            "full_name",
        ]


class PublisherForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = Publisher
        fields = [
            "name",
        ]


class BookForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = Book
        fields = [
        "category",
        "author",
        "publisher",
        "title",
        "isbn",
        "publish_year",
        "pages",
        "summary",
        "description",
        "language",
        "copies",
        "image",
        "is_available",
]
        
        
        widgets = {
            "summary": forms.Textarea(
                attrs={
                    "rows": 3,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                }
            ),
        }



class BorrowForm(BootstrapFormMixin, forms.ModelForm):
    def clean_book(self):
        book = self.cleaned_data["book"]
        if self.instance.pk:
            return book
        if not book.is_available:
            raise forms.ValidationError("این کتاب در حال حاضر قابل امانت نیست.")
        return book
    

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        book = cleaned_data.get("book")
        if user and book:
            if self.instance.pk:
                return cleaned_data
            if Borrow.objects.filter(
                user=user,
                book=book,
                status__in=[
                    Borrow.STATUS_PENDING,
                    Borrow.STATUS_APPROVED,
                ],
            ).exists():
                raise forms.ValidationError("برای این کتاب قبلاً یک درخواست فعال ثبت کرده‌اید.")
        return cleaned_data
       
    class Meta:
        model = Borrow

        fields = [
            "book",
        ]

        widgets = {

            "borrow_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "due_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "return_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }
        
        


class BorrowApprovalForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:

        model = Borrow

        fields = [
            "status",
            "reject_reason",
        ]