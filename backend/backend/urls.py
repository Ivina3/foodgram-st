from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from ingredient.views import IngredientViewSet
from recipe.views import RecipeViewSet
from user.views import UserViewSet, UserAvatarView
from .views import check_health

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("recipes", RecipeViewSet, basename="recipes")
router.register("ingredients", IngredientViewSet, basename="ingredients")

schema_view = get_schema_view(
    openapi.Info(
        title="Foodgram API",
        default_version="v1",
        description="API for Foodgram project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("djoser.urls.authtoken")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("api/users/me/avatar/", UserAvatarView.as_view(), name="user-avatar"),
    path("api/health/", check_health, name="health-check"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
