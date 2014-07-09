from django.conf import settings


def noaanode_urls(request):
    """Global values to pass to templates"""
    defaults = dict(
        SITEURL=getattr(settings, "SITEURL", "http://localhost/"),
        )

    return defaults