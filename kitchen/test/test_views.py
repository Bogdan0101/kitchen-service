from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from kitchen.models import DishType, Dish, Ingredient, Cook

COOK_LIST_URL = reverse("kitchen:cook-list")
INGREDIENT_LIST_URL = reverse("kitchen:ingredient-list")
DISH_LIST_URL = reverse("kitchen:dish-list")
DISH_TYPE_LIST_URL = reverse("kitchen:dish-type-list")


class PublicListTests(TestCase):
    def test_login_required_cook(self):
        res = self.client.get(COOK_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_ingredient(self):
        res = self.client.get(INGREDIENT_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_dish(self):
        res = self.client.get(DISH_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_dish_type(self):
        res = self.client.get(DISH_TYPE_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateListAndSearchTests(TestCase):
    def setUp(self) -> None:
        self.cook_one = get_user_model().objects.create_user(
            username="cook_one",
            password="sdsdgfg@!$123",
            years_of_experience=5,
        )
        self.client.force_login(self.cook_one)
        self.cook_two = get_user_model().objects.create_user(
            username="cook_two",
            password="sdsg@!$123",
            years_of_experience=10,
        )
        self.dist_type_one = DishType.objects.create(name="Cakes")
        self.dist_type_two = DishType.objects.create(name="Bread")
        self.ingredient_one = Ingredient.objects.create(name="Milk")
        self.ingredient_two = Ingredient.objects.create(name="Flour")
        self.dish_one = Dish(
            id=0,
            name="Napoleon",
            description="Layered cake with custard",
            price=7.50,
            dish_type=self.dist_type_one,
        )
        self.dish_two = Dish(
            id=1,
            name="Garlic Bread",
            description="Toasted bread with garlic butter",
            price=3.50,
            dish_type=self.dist_type_one,
        )
        self.dish_one.cooks.add(self.cook_one)
        self.dish_one.ingredients.add(self.ingredient_one)
        self.dish_one.save()
        self.dish_two.cooks.add(self.cook_two)
        self.dish_two.ingredients.add(self.ingredient_two)
        self.dish_two.save()

    def test_create_cook(self):
        form_data = {
            "username": "cook",
            "password1": "Qweasd123!@",
            "password2": "Qweasd123!@",
            "first_name": "Test first",
            "last_name": "Test last",
            "years_of_experience": 10,
        }
        self.client.post(reverse("kitchen:cook-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.username, form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.years_of_experience,
                         form_data["years_of_experience"])

    def test_search_cooks(self):
        res = self.client.get(COOK_LIST_URL, {"username": "o"})
        self.assertContains(res, "cook_one")
        self.assertContains(res, "cook_two")
        self.assertEqual(len(res.context["cook_list"]), 2)

    def test_search_dish_types(self):
        res = self.client.get(DISH_TYPE_LIST_URL, {"name": "e"})
        self.assertContains(res, "Cakes")
        self.assertContains(res, "Bread")
        self.assertEqual(len(res.context["dish_type_list"]), 2)

    def test_search_ingredients(self):
        res = self.client.get(INGREDIENT_LIST_URL, {"name": "l"})
        self.assertContains(res, "Milk")
        self.assertContains(res, "Flour")
        self.assertEqual(len(res.context["ingredient_list"]), 2)

    def test_search_dishes(self):
        res = self.client.get(DISH_LIST_URL, {"name": "a"})
        self.assertContains(res, "Garlic Bread")
        self.assertContains(res, "Napoleon")
        self.assertEqual(len(res.context["dish_list"]), 2)

    def test_private_cooks_list(self):
        res = self.client.get(COOK_LIST_URL)
        self.assertEqual(res.status_code, 200)
        cooks = Cook.objects.all()
        self.assertEqual(list(res.context["cook_list"]), list(cooks))

    def test_private_dish_types_list(self):
        res = self.client.get(DISH_TYPE_LIST_URL)
        self.assertEqual(res.status_code, 200)
        dish_types = DishType.objects.all()
        self.assertEqual(list(res.context["dish_type_list"]), list(dish_types))

    def test_private_ingredients_list(self):
        res = self.client.get(INGREDIENT_LIST_URL)
        self.assertEqual(res.status_code, 200)
        ingredients = Ingredient.objects.all()
        self.assertEqual(list(res.context["ingredient_list"]),
                         list(ingredients))

    def test_private_dishes_list(self):
        res = self.client.get(DISH_LIST_URL)
        self.assertEqual(res.status_code, 200)
        dishes = Dish.objects.all()
        self.assertEqual(list(res.context["dish_list"]), list(dishes))
