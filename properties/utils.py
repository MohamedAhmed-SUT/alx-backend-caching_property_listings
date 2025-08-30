from django.core.cache import cache
from .models import Property

def get_all_properties():
    # جرب تجيب البيانات من الكاش
    properties = cache.get("all_properties")

    if properties is None:
        # لو مش موجودة في الكاش، هات من الداتابيز
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        ))
        # خزّن البيانات في الكاش لمدة ساعة (3600 ثانية)
        cache.set("all_properties", properties, 3600)

    return properties
