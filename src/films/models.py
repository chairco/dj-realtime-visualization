# films/models.py
import uuid

from django.db import models
from django.db.models import Count, Q

from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.core.validators import (
    MaxValueValidator, MinValueValidator, RegexValidator
)


class Message(models.Model):
    """
    Save user submitted
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_name = models.TextField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class FilmType(models.Model):
    """
    Film's type
    """
    content_type = models.CharField(
        max_length=20,
        verbose_name=_('content_type')
    )

    class Meta:
        verbose_name = _('FilmType')
        verbose_name_plural = _('FilmTypes')

    def __str__(self):
        return self.content_type


class FilmSeq(models.Model):
    """
    Assembly pair
    """
    seqid = models.UUIDField(
        default=uuid.uuid1
    )
    create_time = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

    class Meta:
        verbose_name = _('FilmSeq')
        verbose_name_plural = _('FilmSeqs')
        ordering = ('create_time',)

    def __str__(self):
        return str(self.id)


class FilmQueryset(models.QuerySet):

    def yields(self, start, end):
        yields = self.filter(Q(rs232_time__gte=start),
                             Q(rs232_time__lte=end)).count()
        return yields

    def interval(self, start, end, cam):
        if cam == None:
            datas = self.filter(Q(rs232_time__gte=start), Q(
                rs232_time__lte=end)).order_by('-rs232_time')
        else:
            datas = self.filter(Q(rs232_time__gte=start), Q(
                rs232_time__lte=end), Q(cam=cam)).order_by('-rs232_time')
        
        return datas

    def gte(self, dt, cam):
        if cam == None:
            datas = self.filter(Q(rs232_time__gte=dt)).order_by('-rs232_time')
        else:
            datas = self.filter(Q(rs232_time__gte=dt), Q(
                cam=cam)).order_by('-rs232_time')

        return datas

    def gapfail(self, dt, cam):
        datas = self.filter(Q(rs232_time__gte=dt), Q(
            cam=cam), Q(gap_ret=0)).order_by('-rs232_time')

        return datas

    def lenfail(self, dt, cam):
        datas = self.filter(Q(rs232_time__gte=dt), Q(
            cam=cam), Q(len_ret=0)).order_by('-rs232_time')

        return datas


class FilmManager(models.Manager):

    def get_queryset(self):
        return FilmQueryset(self.model, using=self._db)

    def yields(self, start, end):
        return self.get_queryset().yields(start, end)

    def interval(self, start, end, cam):
        return self.get_queryset().interval(start, end, cam)

    def gte(self, dt, cam):
        return self.get_queryset().gte(dt, cam)

    def gapfail(self, dt, cam):
        return self.get_queryset().gapfail(dt, cam)

    def lenfail(self, dt, cam):
        return self.get_queryset().lenfail(dt, cam)


class Film(models.Model):
    """
    each film data
    """
    filmid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    pic = models.CharField(
        max_length=30,
        verbose_name=_('pic')
    )
    pic_url = models.CharField(
        max_length=30,
        blank=True, null=True,
        verbose_name=_('pic_url')
    )
    content_type = models.ForeignKey(
        'FilmType',
        related_name='film_types',
        verbose_name=_('FilmType'),
        on_delete=models.CASCADE,
    )
    seq = models.ForeignKey(
        'FilmSeq',
        related_name='film_seqs',
        verbose_name=_('FilmSeqs'),
        on_delete=models.CASCADE,
    )
    CAM_CHOICES = (
        (0, _('CAM0')),
        (1, _('CAM1')),
    )
    cam = models.IntegerField(
        choices=CAM_CHOICES,
        verbose_name=_('CAM NO.'),
    )
    rs232_time = models.DateTimeField(
        blank=True, null=True,
        verbose_name=_('rs232_time')
    )

    DISAS_CHOICES = (
        ('0', _('FAIL')),
        ('1', _('PASS')),
    )
    len_ret = models.CharField(
        max_length=4,
        blank=False,
        choices=DISAS_CHOICES,
        verbose_name=_('間距檢驗')
    )
    gap_ret = models.CharField(
        max_length=4,
        blank=False,
        choices=DISAS_CHOICES,
        verbose_name=_('長度檢驗')
    )
    create_time = models.DateTimeField(
        default=timezone.now,
        editable=False
    )
    objects = FilmManager()

    class Meta:
        verbose_name = _('Film')
        verbose_name_plural = _('Films')
        ordering = ('create_time',)

    def __str__(self):
        return str(self.pic)


class FilmGap(models.Model):

    film = models.OneToOneField(
        'Film',
        related_name='film_gaps',
        verbose_name=_('FilmGaps'),
        on_delete=models.CASCADE,
    )
    gap0 = models.FloatField(null=True, blank=True, verbose_name="左邊|粉色")
    gap1 = models.FloatField(null=True, blank=True, verbose_name="粉色|橘色")
    gap2 = models.FloatField(null=True, blank=True, verbose_name="橘色|黃色")
    gap3 = models.FloatField(null=True, blank=True, verbose_name="黃色|綠色")
    gap4 = models.FloatField(null=True, blank=True, verbose_name="綠色|藍色")
    gap5 = models.FloatField(null=True, blank=True, verbose_name="藍色|右邊")

    class Meta:
        verbose_name = _('FilmGap')
        verbose_name_plural = _('FilmGaps')

    def __str__(self):
        return str(self.film)


class FilmLen(models.Model):
    """
    """
    film = models.OneToOneField(
        'Film',
        related_name='film_lens',
        verbose_name=_('FilmLens'),
        on_delete=models.CASCADE,
    )
    pink = models.FloatField(null=True, blank=True, verbose_name="粉色")
    orange = models.FloatField(null=True, blank=True, verbose_name="橘色")
    yellow = models.FloatField(null=True, blank=True, verbose_name="黃色")
    green = models.FloatField(null=True, blank=True, verbose_name="綠色")
    blue = models.FloatField(null=True, blank=True, verbose_name="藍色")

    class Meta:
        verbose_name = _('FilmLen')
        verbose_name_plural = _('FilmLens')

    def __str__(self):
        return str(self.film)


class FilmWidth(models.Model):

    film = models.OneToOneField(
        'Film',
        related_name='film_widths',
        verbose_name=_('FilmWidth'),
        on_delete=models.CASCADE,
    )
    pink = models.FloatField(null=True, blank=True, verbose_name="粉色")
    orange = models.FloatField(null=True, blank=True, verbose_name="橘色")
    yellow = models.FloatField(null=True, blank=True, verbose_name="黃色")
    green = models.FloatField(null=True, blank=True, verbose_name="綠色")
    blue = models.FloatField(null=True, blank=True, verbose_name="藍色")

    class Meta:
        verbose_name = _('FilmWidth')
        verbose_name_plural = _('FilmWidths')

    def __str__(self):
        return str(self.film)

