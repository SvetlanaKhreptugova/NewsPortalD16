from django.contrib import admin
from .models import Post, Category


# напишем уже знакомую нам функцию обнуления товара на складе
def dellpost_text(modeladmin, request, queryset):
    queryset.update(text='Нет ничегошеньки')

dellpost_text.short_description = 'Обнулить'  # описание для более понятного представления в админ панеле задаётся, как будто это объект

class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('author', 'text', 'title')  # генерируем список имён всех полей для более красивого отображения
    list_filter = ('author', 'title', 'category')
    search_fields = 'text', 'title'
    actions = [dellpost_text]

# Register your models here.

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
