from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket,
)


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class AstronomyShowImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "image")


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "themes",)


class AstronomyShowListSerializer(AstronomyShowSerializer):
    themes = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "themes")


class AstronomyShowDetailSerializer(AstronomyShowSerializer):
    themes = ShowThemeSerializer(many=True, read_only=True)
    images = AstronomyShowImageSerializer

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "themes", "image")


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionListSerializer(ShowSessionSerializer):
    planetarium_dome = serializers.CharField(
        source="planetarium_dome.name", read_only=True)
    astronomy_show = serializers.CharField(
        source="astronomy_show.title", read_only=True)
    astronomy_show_image = serializers.ImageField(
        source="astronomy_show.image", read_only=True)
    planetarium_dome_capacity = serializers.IntegerField(
        source="planetarium_dome.capacity", read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "show_time",
            "astronomy_show",
            "astronomy_show_image",
            "planetarium_dome",
            "planetarium_dome_capacity",
            "tickets_available",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["show_session"].planetarium_dome,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session")


class TicketListSerializer(TicketSerializer):
    show_session = ShowSessionListSerializer(many=False, read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class ShowSessionDetailSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowListSerializer(many=False, read_only=True)
    planetarium_dome = PlanetariumDomeSerializer(many=False, read_only=True)
    taken_places = TicketSeatsSerializer(
        source="tickets", many=True, read_only=True
    )

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "show_time",
            "astronomy_show",
            "planetarium_dome",
            "taken_places"
        )


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=reservation, **ticket_data)
            return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
