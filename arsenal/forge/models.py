from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.html import format_html
from django.utils.timezone import datetime
from django.urls import reverse
import uuid


class ArmorType(models.Model):
    name = models.CharField(
        'name', 
        max_length=200, help_text='Enter name of armor type')

    def __str__(self) -> str:
        return self.name

    def link_filtered_armors(self):
        link = reverse('armors')+'?armor_type_id='+str(self.id)
        return format_html('<a class="armor_type" href="{link}">{name}</a>', link=link, name=self.name)


class Blacksmith(models.Model):
    first_name = models.CharField('first name', max_length=50)
    last_name = models.CharField('last name', max_length=50)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def display_armors(self) -> str:
        return ', '.join(armor.title for armor in self.armors.all())
    display_armors.short_description = 'armors'

    def link(self) -> str:
        link = reverse('blacksmith', kwargs={'blacksmith_id':self.id})
        return format_html(
            '<a href="{link}">{blacksmith}</a>', 
            link=link, blacksmith=self.__str__())

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "blacksmith"
        verbose_name_plural = "blacksmiths"


class Armor(models.Model):
    title = models.CharField('title', max_length=255)
    summary = models.TextField('summary')
    blacksmith = models.ForeignKey(
        Blacksmith, 
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='armors')
    armor_type = models.ManyToManyField(
        ArmorType, 
        help_text='Choose armor type for your armor', 
        verbose_name='armor_type(s)')
    photo = models.ImageField("photo", upload_to='photos', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.blacksmith} - {self.title}"

    def display_armor_type(self) -> str:
        return ', '.join(armor_type.name for armor_type in self.armor_type.all()[:3])
    display_armor_type.short_description = 'armor_type(s)'


class ArmorOrder(models.Model):
    unique_id = models.UUIDField('unique ID', default=uuid.uuid4, editable=False)
    armor = models.ForeignKey(Armor, verbose_name="armor", on_delete=models.CASCADE)
    due_back = models.DateField('due back', null=True, blank=True)

    ORDER_CHOICES = (
        ('m', "manufacturing"),
        ('r', "repairing"),
        ('a', "assembled"),
        ('n', "no materials"),
    )

    status = models.CharField(
        'status', max_length=1, choices=ORDER_CHOICES, default='m')
    client = models.ForeignKey(
        get_user_model(), 
        verbose_name="client", 
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='ordered_armors',
    )

    @property
    def is_overdue(self):
        if self.due_back and self.due_back < datetime.date(datetime.now()):
            return True
        return False
    blacksmith = models.ForeignKey(
        Blacksmith, 
        verbose_name=_('blacksmith'), 
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='taken_armors')
    due_back = models.DateField(_('due_back'))
    price = models.DecimalField(
        _('price'), 
        max_digits=18, decimal_places=2, 
        default=0)

    def __str__(self) -> str:
        return f"{self.unique_id}: {self.armor.title}"

    class Meta:
        ordering = ['due_back']
