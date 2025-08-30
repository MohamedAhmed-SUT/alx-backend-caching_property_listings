from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .utils import get_all_properties

@cache_page(60 * 15)  # كاش 15 دقيقة للـ response
def property_list(request):
    properties = get_all_properties()  # بدل ما نجيب من ORM مباشرة
    return JsonResponse({"data": properties})
