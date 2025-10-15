from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import Dish, DishType, Ingredient


class ModelsTests(TestCase):
    def setUp(self):
        self.password = "Test12!@#"
        self.cook = get_user_model().objects.create_user(username="cook_test",
                                                         password=self.password,
                                                         last_name="Smith",
                                                         first_name="Bob",
                                                         years_of_experience=10)
        self.dish_type = DishType.objects.create(name="bread")
        self.ingredient = Ingredient.objects.create(name="tomato")

    def test_create_cook_with_years_of_experience(self):
        self.assertEqual(self.cook.years_of_experience, 10)
        self.assertEqual(self.cook.username, "cook_test")
        self.assertTrue(self.cook.check_password(self.password))

    def test_cook_str(self):
        self.assertEqual(str(self.cook),
                         f"{self.cook.username},"
                         f" {self.cook.years_of_experience} "
                         f"({self.cook.first_name} {self.cook.last_name})")

    def test_dish_type_str(self):
        self.assertEqual(str(self.dish_type), self.dish_type.name)

    def test_ingredient_str(self):
        self.assertEqual(str(self.ingredient), self.ingredient.name)

    def test_dish_str(self):
        dish = Dish(name="Tomato soup",
                    description="Creamy tomato soup",
                    price=5.50,
                    dish_type=self.dish_type,
                    id=0
                    )
        dish.cooks.add(self.cook)
        dish.ingredients.add(self.ingredient)
        dish.save()
        self.assertEqual(str(dish), f"{dish.name}, price: {dish.price}")
