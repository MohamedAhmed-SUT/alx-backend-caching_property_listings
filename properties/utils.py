import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)

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

    total_requests = hits + misses
    hit_ratio = hits / total_requests if total_requests > 0 else 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    # سجل الميتريكس باستخدام logger
    try:
        logger.error(f"Cache Metrics: {metrics}")
    except Exception as e:
        logger.error(f"Error logging cache metrics: {e}")

    return metrics
