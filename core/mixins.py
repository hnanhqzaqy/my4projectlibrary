from django.contrib.auth.mixins import UserPassesTestMixin


class SuperUserRequiredMixin(UserPassesTestMixin):
    """
    فقط مدیر سیستم (Superuser)
    اجازه دسترسی دارد.
    """

    def test_func(self):
        return self.request.user.is_superuser