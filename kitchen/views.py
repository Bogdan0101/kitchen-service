from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic

from .forms import (CookCreationForm,
                    CookUpdateYearsForm,
                    DishForm,
                    DishTypeForm,
                    IngredientForm,
                    CookSearchForm,
                    IngredientSearchForm,
                    DishSearchForm,
                    DishTypeSearchForm, )
from .models import Cook, Dish, DishType, Ingredient


@login_required
def index(request):
  count_cook = Cook.objects.count()
  count_dish = Dish.objects.count()
  count_ingredient = Ingredient.objects.count()
  count_dish_type = DishType.objects.count()
  count_visits = request.session.get("count_visits", 0)
  request.session["count_visits"] = count_visits + 1

  context = {
    "count_cook": count_cook,
    "count_dish": count_dish,
    "count_ingredient": count_ingredient,
    "count_dish_type": count_dish_type,
    "count_visits": count_visits + 1,
  }

  return render(request, "kitchen/index.html", context=context)


class CookListView(LoginRequiredMixin, generic.ListView):
  model = get_user_model()
  context_object_name = "cook_list"
  template_name = "kitchen/cook_list.html"
  paginate_by = 5

  def get_context_data(
      self, *, object_list=None, **kwargs
  ):
    context = super(CookListView, self).get_context_data(**kwargs)
    username = self.request.GET.get("username")
    context["search_form"] = CookSearchForm(
      initial={"username": username}
    )
    return context

  def get_queryset(self):
    form = CookSearchForm(self.request.GET)
    if form.is_valid():
      return (Cook.objects.
              filter(username__icontains=form.cleaned_data["username"]))
    return Cook.objects.all()


class CookDetailView(LoginRequiredMixin, generic.DetailView):
  model = get_user_model()
  queryset = Cook.objects.all().prefetch_related("dishes__dish_type")
  template_name = "kitchen/cook_detail.html"


class CookCreateView(LoginRequiredMixin, generic.CreateView):
  model = get_user_model()
  form_class = CookCreationForm


class CookUpdateYearsView(LoginRequiredMixin, generic.UpdateView):
  model = get_user_model()
  form_class = CookUpdateYearsForm
  success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
  model = get_user_model()
  success_url = reverse_lazy("kitchen:cook-list")


class DishListView(LoginRequiredMixin, generic.ListView):
  model = Dish
  paginate_by = 5
  context_object_name = "dish_list"
  template_name = "kitchen/dish_list.html"

  def get_context_data(
      self, *, object_list=None, **kwargs
  ):
    context = super(DishListView, self).get_context_data(**kwargs)
    name = self.request.GET.get("model")
    context["search_form"] = DishSearchForm(
      initial={"name": name}
    )
    return context

  def get_queryset(self):
    form = DishSearchForm(self.request.GET)
    if form.is_valid():
      return (Dish.objects.
              filter(name__icontains=form.cleaned_data["name"]))
    return Dish.objects.all()


class DishDetailView(LoginRequiredMixin, generic.DetailView):
  model = Dish
  queryset = Dish.objects.select_related("dish_type").prefetch_related("ingredients")
  template_name = "kitchen/dish_detail.html"


class DishCreateView(LoginRequiredMixin, generic.CreateView):
  model = Dish
  form_class = DishForm
  success_url = reverse_lazy("kitchen:dish-list")
  template_name = "kitchen/dish_form.html"


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
  model = Dish
  form_class = DishForm
  success_url = reverse_lazy("kitchen:dish-list")
  template_name = "kitchen/dish_form.html"


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
  model = Dish
  success_url = reverse_lazy("kitchen:dish-list")


@login_required
def toggle_assign_to_dish(request, pk):
  cook = Cook.objects.get(pk=request.user.id)
  if Dish.objects.get(id=pk) in cook.dishes.all():
    cook.dishes.remove(pk)
  else:
    cook.dishes.add(pk)
  return HttpResponseRedirect(reverse_lazy("kitchen:dish-detail", args=[pk]))


class DishTypeListView(LoginRequiredMixin, generic.ListView):
  model = DishType
  paginate_by = 5
  context_object_name = "dish_type_list"
  template_name = "kitchen/dish_type_list.html"
  queryset = DishType.objects.all().prefetch_related("dishes")

  def get_context_data(
      self, *, object_list=None, **kwargs
  ):
    context = super(DishTypeListView, self).get_context_data(**kwargs)
    name = self.request.GET.get("name")
    context["search_form"] = DishTypeSearchForm(
      initial={"name": name}
    )
    return context

  def get_queryset(self):
    form = DishTypeSearchForm(self.request.GET)
    if form.is_valid():
      return (DishType.objects
              .filter(name__icontains=form.cleaned_data["name"]))
    return DishType.objects.all()


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
  model = DishType
  queryset = DishType.objects.all().prefetch_related("dishes")
  template_name = "kitchen/dish_type_detail.html"


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
  model = DishType
  form_class = DishTypeForm
  success_url = reverse_lazy("kitchen:dish-type-list")
  template_name = "kitchen/dish_type_form.html"


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
  model = DishType
  form_class = DishTypeForm
  success_url = reverse_lazy("kitchen:dish-type-list")
  template_name = "kitchen/dish_type_form.html"


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
  model = DishType
  success_url = reverse_lazy("kitchen:dish-type-list")


class IngredientListView(LoginRequiredMixin, generic.ListView):
  model = Ingredient
  paginate_by = 5
  context_object_name = "ingredient_list"
  template_name = "kitchen/ingredient_list.html"
  queryset = Ingredient.objects.all().prefetch_related("dishes")

  def get_context_data(
      self, *, object_list=None, **kwargs
  ):
    context = super(IngredientListView, self).get_context_data(**kwargs)
    name = self.request.GET.get("name")
    context["search_form"] = IngredientSearchForm(
      initial={"name": name}
    )
    return context

  def get_queryset(self):
    form = IngredientSearchForm(self.request.GET)
    if form.is_valid():
      return (Ingredient.objects
              .filter(name__icontains=form.cleaned_data["name"]))
    return Ingredient.objects.all()


class IngredientDetailView(LoginRequiredMixin, generic.DetailView):
  model = Ingredient
  queryset = Ingredient.objects.all().prefetch_related("dishes")
  template_name = "kitchen/ingredient_detail.html"


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
  model = Ingredient
  form_class = IngredientForm
  success_url = reverse_lazy("kitchen:ingredient-list")
  template_name = "kitchen/ingredient_form.html"


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
  model = Ingredient
  form_class = IngredientForm
  success_url = reverse_lazy("kitchen:ingredient-list")
  template_name = "kitchen/ingredient_form.html"


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
  model = Ingredient
  success_url = reverse_lazy("kitchen:ingredient-list")
