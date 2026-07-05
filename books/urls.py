from django.urls import path

from . import views

urlpatterns = [

    # ==========================
    # Category
    # ==========================

    path(
        "categories/",
        views.CategoryListView.as_view(),
        name="category-list",
    ),
    path(
    "categories/<int:pk>/",
    views.CategoryDetailView.as_view(),
    name="category-detail",
    ),
    path(
        "categories/create/",
        views.CategoryCreateView.as_view(),
        name="category-create",
    ),
    path(
        "categories/<int:pk>/update/",
        views.CategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "categories/<int:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category-delete",
    ),

    # ==========================
    # Author
    # ==========================

    path(
        "authors/",
        views.AuthorListView.as_view(),
        name="author-list",
    ),
    path(
    "authors/<int:pk>/",
    views.AuthorDetailView.as_view(),
    name="author-detail",
    ),
    path(
        "authors/create/",
        views.AuthorCreateView.as_view(),
        name="author-create",
    ),
    path(
        "authors/<int:pk>/update/",
        views.AuthorUpdateView.as_view(),
        name="author-update",
    ),
    path(
        "authors/<int:pk>/delete/",
        views.AuthorDeleteView.as_view(),
        name="author-delete",
    ),

    # ==========================
    # Publisher
    # ==========================

    path(
        "publishers/",
        views.PublisherListView.as_view(),
        name="publisher-list",
    ),
    path(
    "publishers/<int:pk>/",
    views.PublisherDetailView.as_view(),
    name="publisher-detail",
    ),
    path(
        "publishers/create/",
        views.PublisherCreateView.as_view(),
        name="publisher-create",
    ),
    path(
        "publishers/<int:pk>/update/",
        views.PublisherUpdateView.as_view(),
        name="publisher-update",
    ),
    path(
        "publishers/<int:pk>/delete/",
        views.PublisherDeleteView.as_view(),
        name="publisher-delete",
    ),

    # ==========================
    # Book
    # ==========================

   path(
    "books/",
    views.BookListView.as_view(),
    name="book-list",
    ),
   path(
    "<int:pk>/",
    views.BookDetailView.as_view(),
    name="book-detail",
    ),
    path(
        "books/create/",
        views.BookCreateView.as_view(),
        name="book-create",
    ),
    path(
        "books/<int:pk>/update/",
        views.BookUpdateView.as_view(),
        name="book-update",
    ),
    path(
        "books/<int:pk>/delete/",
        views.BookDeleteView.as_view(),
        name="book-delete",
    ),
    
    
    
    path(
    "borrows/",
    views.BorrowListView.as_view(),
    name="borrow-list",
    ),
    path(
    "borrows/create/",
    views.BorrowCreateView.as_view(),
    name="borrow-create",
    ),
    path(
    "borrows/<int:pk>/update/",
    views.BorrowUpdateView.as_view(),
    name="borrow-update",
    ),
    path(
    "borrows/<int:pk>/approve/",
    views.BorrowApproveView.as_view(),
    name="borrow-approve",
    ),
    path(
    "borrows/<int:pk>/return/",
    views.BorrowReturnView.as_view(),
    name="borrow-return",
    ),
    path(
    "dashboard/",
    views.DashboardView.as_view(),
    name="dashboard",
    ),
    path(
    "dashboard/books/",
    views.AdminBookListView.as_view(),
    name="admin-book-list",
    ),
    path(
    "dashboard/borrows/",
    views.AdminBorrowListView.as_view(),
    name="admin-borrow-list",
    ),
    path(
    "dashboard/authors/",
    views.AdminAuthorListView.as_view(),
    name="admin-author-list",
    ),
    path(
    "dashboard/publishers/",
    views.AdminPublisherListView.as_view(),
    name="admin-publisher-list",
    ),
    path(
    "dashboard/categories/",
    views.AdminCategoryListView.as_view(),
    name="admin-category-list",
    ),
    path(
    "my-borrows/",
    views.MyBorrowListView.as_view(),
    name="my-borrows",
    ),
]

