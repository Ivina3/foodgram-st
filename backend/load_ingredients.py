import json
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from ingredient.models import Ingredient  # noqa: E402

with open("data/ingredients.json", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    Ingredient.objects.get_or_create(
        name=item["name"], measurement_unit=item["measurement_unit"]
    )
print(f"Loaded {len(data)} ingredients.")
