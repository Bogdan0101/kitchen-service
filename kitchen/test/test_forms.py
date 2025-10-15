from django.test import TestCase
from kitchen.forms import CookCreationForm


class FormsTests(TestCase):
  def test_cook_creation_form_is_valid(self):
    form_data = {
      "username": "cook",
      "password1": "Qweasd123!@",
      "password2": "Qweasd123!@",
      "first_name": "Test first",
      "last_name": "Test last",
      "years_of_experience": 10,
    }
    form = CookCreationForm(data=form_data)
    self.assertTrue(form.is_valid())
    self.assertEqual(form.cleaned_data, form_data)
