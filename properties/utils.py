from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

def get_all_properties():
    """Get all properties with low-level Redis caching (1 hour)."""
    properties = cache.get("all_properties")
    if properties is None:
        properties = list(Property.objects.all())
        cache.set("all_properties", properties, 3600)  # Cache for 1 hour
    return properties


def get_redis_cache_metrics():
    """Retrieve Redis cache hit/miss metrics and calculate hit ratio."""
    conn = get_redis_connection("default")
    info = conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    # تقدر تطبعها للـ logs كمان
    print(f"Cache Metrics: {metrics}")

    return metrics
