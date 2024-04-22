from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import BoardConfig
from .views import IndexView, AdvertisementListView, ReviewListView, ReviewDetailView, ReviewCreateView, \
    ReviewUpdateView, ReviewDeleteView

app_name = BoardConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('categories/', AdvertisementListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', ReviewListView.as_view(), name='product_list'),
    path('goods/<int:pk>/', cache_page(60)(ReviewDetailView.as_view()), name='product_detail'),
    path('goods/create', ReviewCreateView.as_view(), name='product_create'),
    path('goods/update/<int:pk>/', ReviewUpdateView.as_view(), name='product_update'),
    path('goods/delete/<int:pk>/', ReviewDeleteView.as_view(), name='product_delete'),
]
