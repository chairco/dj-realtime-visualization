# films/models.py
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


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
        verbose_name=_('rs232 time')
    )
    
    DISAS_CHOICES = (
        ('0', _('PASS')),
        ('1', _('FAIL')),
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

    class Meta:
        verbose_name = _('Film')
        verbose_name_plural = _('Films')
        ordering = ('create_time',)

    def __str__(self):
        return str(self.filmid)


class FilmGap(models.Model):
    """
    """
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
        return str(self.id)


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
    """
    """
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


