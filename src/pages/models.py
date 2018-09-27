#pages/models
from django.conf import settings
from django.db import models
from django.db.models import F

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.urls import reverse
from django.contrib.auth import get_user_model

from django_echarts.datasets.managers import AxisValuesQuerySet


class BlogQuerySet(models.QuerySet):
    def update_counter(self, pk):
        return self.filter(id=pk)


class BlogManager(models.Manager):
    def get_queryset(self):
        return BlogQuerySet(self.model, using=self._db)

    def update_counter(self, pk):
        #self.filter(id=pk).update(read_count=F('read_count')+1)
        self.get_queryset().update_counter(pk).update(read_count=F('read_count')+1)


class Blog(models.Model):
    
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name='owned_blogs',
        on_delete=models.CASCADE
    )
    post_time = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    read_count = models.PositiveIntegerField(default=0)
    objects = BlogManager()
    
    class Meta:
        ordering = ['-post_time']
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'pk': self.pk})

    def can_user_delete(self, user):
        if not self.owner or self.owner == user:
            return True
        if user.has_perm('pages.delete_blog'):
            return True
        return False

    def update_counter(self):
        self.read_count = self.read_count + 1
        self.save(update_fields=['read_count'])

