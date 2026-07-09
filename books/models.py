from django.db import models
from core.models import BaseModel
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
 
 


class Category(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="نام دسته‌بندی"
    )

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Author(BaseModel):
    full_name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="نام نویسنده"
    )

    class Meta:
        verbose_name = "نویسنده"
        verbose_name_plural = "نویسندگان"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class Publisher(BaseModel):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="نام ناشر"
    )

    class Meta:
        verbose_name = "ناشر"
        verbose_name_plural = "ناشران"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(BaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="books",
        verbose_name="دسته‌بندی"
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name="books",
        verbose_name="نویسنده"
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.PROTECT,
        related_name="books",
        verbose_name="ناشر"
    )

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان کتاب"
    )

    isbn = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="ISBN"
    )

    publish_year = models.PositiveIntegerField(
        verbose_name="سال انتشار",
    )

    pages = models.PositiveIntegerField(
        verbose_name="تعداد صفحات"
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )
    summary = models.TextField(
    blank=True,
    verbose_name="خلاصه کتاب"
    )

    language = models.CharField(
    max_length=50,
    default="فارسی",
    verbose_name="زبان"
    )

    copies = models.PositiveIntegerField(
    default=1,
    verbose_name="تعداد نسخه"
    )

    image = models.ImageField(
        upload_to="books/",
        blank=True,
        null=True,
        verbose_name="تصویر جلد"
    )

    is_available = models.BooleanField(
        default=True,
        verbose_name="موجود"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )
    
    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب‌ها"
        ordering = ["title"]

    def __str__(self):
        return self.title
    
    
    
class Borrow(BaseModel):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_RETURNED = "returned"

    STATUS_CHOICES = (
        (STATUS_PENDING, "در انتظار تأیید"),
        (STATUS_APPROVED, "تأیید شده"),
        (STATUS_REJECTED, "رد شده"),
        (STATUS_RETURNED, "تحویل داده شده"),
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="borrows",
        verbose_name="کتاب",
    )
    book_title = models.CharField(
    max_length=255,
    blank=True,
    verbose_name="عنوان کتاب"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="borrows",
        verbose_name="کاربر",
    )

    request_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان ثبت درخواست",
    )

    borrow_date = models.DateField(
    null=True,
    blank=True,
    verbose_name="تاریخ امانت",
    )

    due_date = models.DateField(
    null=True,
    blank=True,
    verbose_name="تاریخ تحویل",
    )
    
    return_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="تاریخ بازگشت"
    )

    class Meta:
        verbose_name = "امانت"
        verbose_name_plural = "امانت‌ها"
        ordering = ["-borrow_date"]

    def __str__(self):
        return f"{self.book} - {self.user}"
    
    
    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default=STATUS_PENDING,
    verbose_name="وضعیت درخواست",
)
    
    
    reject_reason = models.TextField(
    blank=True,
    verbose_name="دلیل رد درخواست",
)
    
    
    approved_at = models.DateTimeField(
    null=True,
    blank=True,
    verbose_name="زمان تأیید",
)
    
    
    edit_deadline = models.DateTimeField(
    null=True,
    blank=True,
    verbose_name="مهلت ویرایش",
)