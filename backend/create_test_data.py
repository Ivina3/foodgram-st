import os
from pathlib import Path

import django
from django.core.files import File
from django.core.exceptions import MultipleObjectsReturned

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from django.contrib.auth.hashers import make_password  # noqa: E402
from ingredient.models import Ingredient  # noqa: E402
from recipe.models import Recipe, RecipeIngredient  # noqa: E402
from user.models import User  # noqa: E402


def safe_get_ingredient(name):
    try:
        return Ingredient.objects.get(name=name)
    except MultipleObjectsReturned:
        print(
            f"[Warning] Несколько элементов с "
            f"одним name '{name}'. Выбирается первый!"
        )
        matches = Ingredient.objects.filter(name=name)
        print(f"ID элементов с одним name: {[i.id for i in matches]}")
        return matches.first()
    except Ingredient.DoesNotExist:
        print(f"[Error] Ингредиент '{name}' не найден в БД.")
        return None


def create_test_data():
    print("Создание тесовых данных...")

    user1, _ = User.objects.get_or_create(
        email="user1@example.com",
        defaults={
            "username": "admin_user",
            "first_name": "Admin",
            "last_name": "User",
            "password": make_password("password123"),
            "is_staff": True,
            "is_superuser": True,
        },
    )

    user2, _ = User.objects.get_or_create(
        email="user2@example.com",
        defaults={
            "username": "regular_user",
            "first_name": "Regular",
            "last_name": "User",
            "password": make_password("password123"),
            "is_staff": False,
            "is_superuser": False,
        },
    )

    user3, _ = User.objects.get_or_create(
        email="user3@example.com",
        defaults={
            "username": "no_avatar_user",
            "first_name": "User",
            "last_name": "3",
            "password": make_password("password123"),
            "is_staff": False,
            "is_superuser": False,
        },
    )

    ingredients = {
        "овсяные хлопья": "г",
        "молоко": "мл",
        "бананы": "г",
        "грецкие орехи": "г",
        "мед": "ст. л.",
        "авокадо": "г",
        "апельсины": "г",
        "мята": "г",
        "лимон": "шт",
        "оливковое масло": "ст. л.",
        "клубника": "г",
        "йогурт натуральный": "г",
    }

    for name, unit in ingredients.items():
        Ingredient.objects.get_or_create(name=name, measurement_unit=unit)

    oatmeal, created = Recipe.objects.get_or_create(
        name="Овсяная каша с бананом и орехами",
        defaults={
            "author": user1,
            "text": "Полезная и сытная каша с бананом,"
            " орехами и медом — отличный завтрак"
            " для бодрого начала дня.",
            "cooking_time": 10,
        },
    )

    if created:
        image_path = Path("data/oatmeal_banana_nuts.jpg")
        with open(image_path, "rb") as f:
            oatmeal.image.save("oatmeal_banana_nuts.jpg", File(f), save=True)

        ingredients_dict = {
            "овсяные хлопья": 50,
            "молоко": 200,
            "бананы": 80,
            "грецкие орехи": 20,
            "мед": 1,
        }

        for name, amount in ingredients_dict.items():
            ingredient = safe_get_ingredient(name)
            if ingredient:
                RecipeIngredient.objects.create(
                    recipe=oatmeal, ingredient=ingredient, amount=amount
                )

        print(f"Created recipe: {oatmeal.name}")

    salad, created = Recipe.objects.get_or_create(
        name="Салат с авокадо и апельсином",
        defaults={
            "author": user2,
            "text": "Свежий салат с авокадо,"
            " апельсином, мятой и легкой лимонной заправкой.",
            "cooking_time": 7,
        },
    )

    if created:
        image_path = Path("data/avocado_orange_salad.jpg")
        with open(image_path, "rb") as f:
            salad.image.save("avocado_orange_salad.jpg", File(f), save=True)

        ingredients_dict = {
            "авокадо": 100,
            "апельсины": 100,
            "мята": 5,
            "лимон": 0.5,
            "оливковое масло": 1,
        }

        for name, amount in ingredients_dict.items():
            ingredient = safe_get_ingredient(name)
            if ingredient:
                RecipeIngredient.objects.create(
                    recipe=salad, ingredient=ingredient, amount=amount
                )

        print(f"Created recipe: {salad.name}")

    smoothie, created = Recipe.objects.get_or_create(
        name="Смузи из клубники и банана",
        defaults={
            "author": user3,
            "text": "Освежающий смузи с клубникой,"
            " бананом и йогуртом. Идеален для лета и завтрака.",
            "cooking_time": 5,
        },
    )

    if created:
        image_path = Path("data/strawberry_banana_smoothie.jpg")
        with open(image_path, "rb") as f:
            smoothie.image.save(
                "strawberry_banana_smoothie.jpg", File(f), save=True
            )

        ingredients_dict = {
            "клубника": 100,
            "бананы": 80,
            "йогурт натуральный": 150,
            "мед": 1,
        }

        for name, amount in ingredients_dict.items():
            ingredient = safe_get_ingredient(name)
            if ingredient:
                RecipeIngredient.objects.create(
                    recipe=smoothie, ingredient=ingredient, amount=amount
                )

        print(f"Создан рецепт: {smoothie.name}")


if __name__ == "__main__":
    create_test_data()
