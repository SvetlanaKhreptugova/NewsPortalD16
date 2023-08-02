from django.urls import path
from .views import PostsList, PostDetail, PostSearch, NewsCreate, NewsUpdate, NewsDelete, upgrade_me, CategoryListView, \
    subscribe
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60*10)(PostsList.as_view()), name='posts_list'),
    path('<int:pk>', cache_page(60*10)(PostDetail.as_view()), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', NewsCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('articles/create/', NewsCreate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/edit/', NewsUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='articles_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),

]
