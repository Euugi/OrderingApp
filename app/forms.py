from django.forms.widgets import Select
from app.models import Restaurant, Dish, Review
from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.forms import PasswordInput
from django.contrib.auth import get_user_model

User = get_user_model()


USER_ROLE = [
        ('customer', 'Klient', ),
        ('restaurant', 'Restaurator'),
        ('supplier', 'Dostawca'),
    ]

CUISINE_CATEGORY = [
    ('asian', 'Azjatycka'),
    ('european', 'Europejska', ),
    ('italian', 'Włoska'),
    ('japan', 'Japońska'),
]

REVIEW_RATE = [
    ('0', 'Wybierz ocenę'),
    ('1', 'Bardzo źle'),
    ('2', 'Źle'),
    ('3', 'Dostatecznie'),
    ('4', 'Dobrze'),
    ('5', 'Bardzo dobrze'),
]

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nazwa użytkownika'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    user_role = forms.CharField(label='Wybierz typ użytkownika', widget=forms.Select(choices=USER_ROLE))
    email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'placeholder': 'e-mail'}))
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'user_role', 'email', 'password1', 'password2', )


class SignInForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nazwa użytkownika'}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'category', 'address_city', 'address_street', 'address_postalcode', 'description']
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Nazwa'}))
    category = forms.CharField(max_length=30, widget=forms.Select(choices=CUISINE_CATEGORY))
    address_city = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Miasto'}))
    address_street = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Ulica'}))
    address_postalcode = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'placeholder': 'Kod pocztowy'}))
    description = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Opis'}))
    
    def clean_name(self):
        name = self.cleaned_data['name']
        restaurant_exists = Restaurant.objects.filter(name=self.cleaned_data['name']).exists()
        if restaurant_exists:
            raise forms.ValidationError("Wskazana restauracja już istnieje")
        return name

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'ingredients', 'alergens', 'price']
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Nazwa'}))
    price = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': 'Cena'}))
    description = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Opis'}))
    ingredients = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Składniki'}))
    alergens = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Alergeny'}))


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['restaurant_rate', 'restaurant_rate_desc', 'supplier_rate', 'supplier_rate_desc']
    restaurant_rate = forms.CharField(max_length=30, widget=forms.Select(choices=REVIEW_RATE))
    restaurant_rate_desc = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Oceń jedzenie'}))
    supplier_rate = forms.CharField(max_length=30, widget=forms.Select(choices=REVIEW_RATE))
    supplier_rate_desc = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Oceń dostawcę'}))