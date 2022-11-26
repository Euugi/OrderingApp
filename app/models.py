from django.db import models, reset_queries
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils.text import slugify


CUISINE_CATEGORY = [
    ('asian', 'Azjatycka'),
    ('european', 'Europejska', ),
    ('italian', 'Włoska'),
    ('japan', 'Japońska'),
]


class CustomUser(AbstractUser):
    USER_ROLE = [
        ('customer', 'klient', ),
        ('restaurant', 'restaurator'),
        ('supplier', 'dostawca'),
    ]
    user_role = models.CharField(max_length=30, choices=USER_ROLE)

    def get_role(self):
        return self.user_role


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=30, choices=CUISINE_CATEGORY)
    address_city = models.CharField(max_length=30)
    address_street = models.CharField(max_length=30)
    address_postalcode = models.CharField(max_length=6)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    slug = models.SlugField(max_length=255, unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            val = self.slug
        return super(Restaurant, self).save(*args, **kwargs)

class Supplier(models.Model):
    name = models.CharField(max_length=50)


class Dish(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(max_length=6)
    description = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=150, null=True)
    alergens = models.CharField(max_length=50)
    restaurant_id = models.ForeignKey('Restaurant', null=True, on_delete=models.DO_NOTHING)

ORDER_STATUS = [
    ('awaiting', 'Oczekujące na zatwierdzenie'),
    ('accepted_restaurant', 'Zatwierdzone przez restaurację', ),
    ('in_progress', 'Realizowane'),
    ('finished', 'Zakończone'),
    ('aborted', 'Anulowane'),
]

ACCEPTANCE_DECISION = [
    ('awaiting', 'Oczekujące'),
    ('accepted', 'Zaakceptowane'),
    ('aborted', 'Odrzucone'),
]

class Order(models.Model):
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='awaiting')
    restaurant_acceptance = models.CharField(max_length=30, choices=ACCEPTANCE_DECISION, default='awaiting')
    supplier_acceptance = models.CharField(max_length=30, choices=ACCEPTANCE_DECISION, default='awaiting')
    ordered_user = models.ForeignKey('CustomUser', null=True, related_name="ordered_user", on_delete=models.DO_NOTHING)
    delivery_address = models.CharField(max_length=60, null=True)
    restaurant = models.ForeignKey('Restaurant', null=True, on_delete=models.DO_NOTHING)
    supplier = models.ForeignKey('CustomUser', null=True, related_name='supplier', on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('Dish', related_name='order', blank=True)
    review = models.ForeignKey('Review', null=True, on_delete=models.DO_NOTHING)


class ChatGroup(Group):
    description = models.TextField(blank=True)
    mute_notifications = models.BooleanField(default=False)
    icon = models.ImageField(help_text="Group icon", blank=True, upload_to="chartgroup")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dashboard/order:room', args=[str(self.id)])

class Message(models.Model):
    user = models.CharField(max_length=250)
    room = models.CharField(max_length=250)
    date = models.CharField(max_length=250)
    message = models.TextField()
    objects = models.Manager

    def __str__(self):
        return self.user + ' ' + self.room + ' ' + self.date + ' ' + self.message

REVIEW_STATUS = [
    ('awaiting', 'Oczekująca na wystawienie'),
    ('issued', 'Wystawiona'),
]

REVIEW_RATE = [
    ('0', 'Wybierz ocenę'),
    ('1', 'Bardzo źle'),
    ('2', 'Źle'),
    ('3', 'Dostatecznie'),
    ('4', 'Dobrze'),
    ('5', 'Bardzo dobrze'),
]


class Review(models.Model):
    #order = models.ForeignKey('Order', null=True, on_delete=models.DO_NOTHING)
    review_status = models.CharField(max_length=30, choices=REVIEW_STATUS, default='awaiting')
    restaurant_rate = models.CharField(max_length=30, choices=REVIEW_RATE, default='')
    restaurant_rate_desc = models.CharField(max_length=200)
    supplier_rate = models.CharField(max_length=30, choices=REVIEW_RATE, default='')
    supplier_rate_desc = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)