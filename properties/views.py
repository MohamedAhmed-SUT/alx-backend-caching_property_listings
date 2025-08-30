from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property

@cache_page(60 * 15)  # كاش 15 دقيقة
def property_list(request):
    properties = Property.objects.all().values(
        "id", "title", "description", "price", "location", "created_at"
    )
    return JsonResponse({"data": list(properties)})
