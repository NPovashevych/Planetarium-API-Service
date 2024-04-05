from rest_framework import routers

from planetarium.views import (
    AstronomyShowViewSet,
    ReservationViewSet,
    ShowSessionViewSet,
    ShowThemeViewSet,
    PlanetariumDomeViewSet
)

app_name = "planetarium"

router = routers.DefaultRouter()
router.register("astronomy_shows", AstronomyShowViewSet)
router.register("reservations", ReservationViewSet)
router.register("show_sessions", ShowSessionViewSet)
router.register("show_themes", ShowThemeViewSet)
router.register("planetarium_domes", PlanetariumDomeViewSet)

urlpatterns = router.urls
