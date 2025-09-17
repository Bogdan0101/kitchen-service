from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
