from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from kitchen.models import Cook, Dish, DishType, Ingredient


class CookCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    model = get_user_model()
    fields = UserCreationForm.Meta.fields + (
      "first_name",
      "last_name",
      "years_of_experience",
    )


class CookUpdateYearsForm(forms.ModelForm):
  class Meta:
    model = get_user_model()
    fields = ["years_of_experience", ]


class DishForm(forms.ModelForm):
  cooks = forms.ModelMultipleChoiceField(
    queryset=get_user_model().objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )
  ingredients = forms.ModelMultipleChoiceField(
    queryset=Ingredient.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )

  class Meta:
    model = Dish
    fields = "__all__"


class DishTypeForm(forms.ModelForm):
  class Meta:
    model = DishType
    fields = "__all__"


class IngredientForm(forms.ModelForm):
  class Meta:
    model = Ingredient
    fields = "__all__"


class DishSearchForm(forms.Form):
  name = forms.CharField(
    max_length=255,
    required=False,
    label="",
    widget=forms.TextInput(attrs={
      "placeholder": "Search by name"}),
  )


class CookSearchForm(forms.Form):
  username = forms.CharField(
    max_length=255,
    required=False,
    label="",
    widget=forms.TextInput(attrs={
      "placeholder": "Search by username"}),
  )


class DishTypeSearchForm(forms.Form):
  name = forms.CharField(
    max_length=255,
    required=False,
    label="",
    widget=forms.TextInput(attrs={
      "placeholder": "Search by name"})
  )


class IngredientSearchForm(forms.Form):
  name = forms.CharField(
    max_length=255,
    required=False,
    label="",
    widget=forms.TextInput(attrs={
      "placeholder": "Search by name"})
  )
