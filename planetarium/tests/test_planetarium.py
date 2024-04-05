from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from planetarium.models import AstronomyShow, ShowSession, PlanetariumDome, ShowTheme
from planetarium.serializers import AstronomyShowListSerializer, AstronomyShowDetailSerializer

ASTRONOMY_SHOW_URL = reverse("planetarium:astronomyshow-list")
SHOW_SESSION_URL = reverse("planetarium:showsession-list")


def sample_astronomy_show(**params):
    defaults = {
        "title": "Sample show",
        "description": "Sample description",
        "image": None
    }
    defaults.update(params)

    return AstronomyShow.objects.create(**defaults)


def sample_theme(**params):
    defaults = {
        "name": "Tale",
    }
    defaults.update(params)

    return ShowTheme.objects.create(**defaults)


def sample_show_session(**params):
    dome = PlanetariumDome.objects.create(
        name="Big", rows=20, seats_in_row=20
    )
    show = AstronomyShow.objects.create(
        title="Sample title",
        description="Sample description",
    )

    defaults = {
        "show_time": "2024-04-02 14:00:00",
        "astronomy_show": show,
        "planetarium_dome": dome,
    }
    defaults.update(params)

    return ShowSession.objects.create(**defaults)


def detail_url(astronomy_show_id):
    return reverse("planetarium:astronomyshow-detail", args=[astronomy_show_id])


class UnauthenticatedShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_unauthenticated_(self):
        self.assertEqual(self.client.get(ASTRONOMY_SHOW_URL).status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@planetarium.com",
            password="user_password"
        )
        self.client.force_authenticate(self.user)

    def test_user_authenticated_list_shows(self):
        sample_astronomy_show()
        sample_astronomy_show()
        response = self.client.get(ASTRONOMY_SHOW_URL)
        astronomy_shows = AstronomyShow.objects.all()
        serializer = AstronomyShowListSerializer(astronomy_shows, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_authenticated_detail_show(self):
        show = sample_astronomy_show()
        url = detail_url(show.id)
        response = self.client.get(url)
        serializer = AstronomyShowDetailSerializer(show)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_authenticated_created_show(self):
        payload = {
            "title": "Test title",
            "description": "Test description",
        }
        response = self.client.post(ASTRONOMY_SHOW_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_authenticated_filter_by_title(self):
        astronomy_show1 = sample_astronomy_show(title="Test title1")
        astronomy_show2 = sample_astronomy_show(title="Test title2")

        response = self.client.get(ASTRONOMY_SHOW_URL, {"title": f"{astronomy_show1.title}"})

        serializer1 = AstronomyShowListSerializer(astronomy_show1)
        serializer2 = AstronomyShowListSerializer(astronomy_show2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_user_authenticated_filter_by_theme(self):
        astronomy_show1 = sample_astronomy_show(title="Test title1")
        astronomy_show2 = sample_astronomy_show(title="Test title2")
        astronomy_show3 = sample_astronomy_show()

        theme1 = sample_theme(name="Test theme1")
        theme2 = sample_theme(name="Test theme2")

        astronomy_show1.themes.add(theme1)
        astronomy_show2.themes.add(theme2)

        response = self.client.get(ASTRONOMY_SHOW_URL, {"themes": f"{theme1.id},{theme2.id}"})

        serializer1 = AstronomyShowListSerializer(astronomy_show1)
        serializer2 = AstronomyShowListSerializer(astronomy_show2)
        serializer3 = AstronomyShowListSerializer(astronomy_show3)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)
        self.assertNotIn(serializer3.data, response.data)


class AdminShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@cinema.com",
            password="admin_password",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_admin_user_create_show(self):
        theme = sample_theme()
        payload = {
            "title": "Test title",
            "description": "Test description",
            "themes": [theme.id]
        }
        self.client.post(ASTRONOMY_SHOW_URL, payload)
        self.assertTrue(AstronomyShow.objects.filter(title="Test title").exists())