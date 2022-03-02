from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='Категория коммикса')
    slug = models.SlugField(max_length=200, db_index=True)

    def get_absolute_url(self):
        return reverse('comics_site:comics_list_by_category',
                       args=[self.slug])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Comic(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название комикса')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    grade = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Оценка')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    photo = models.ImageField(upload_to='img', blank=True)
    slug = models.SlugField(max_length=200, db_index=True)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True, verbose_name="Доступность")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_absolute_url(self):
        return reverse('comics_site:comics_detail',
                       args=[self.id, self.slug])

    class Meta:
        verbose_name = 'Комикс'
        verbose_name_plural = 'Комиксы'

    def __str__(self):
        return self.name


class Images(models.Model):
    product = models.ForeignKey(Comic, default=None, related_name='images', on_delete=models.PROTECT)
    image = models.ImageField(upload_to='img/%Y/%m/%d', blank=True)
