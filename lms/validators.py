from rest_framework.serializers import ValidationError


def validate_links(value):
    if "http" in value and "youtube.com" not in value:
        raise ValidationError("Материалы могут содержать ссылки только на youtube.com")