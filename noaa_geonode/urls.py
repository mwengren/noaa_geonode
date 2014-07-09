from django.conf.urls import include, patterns, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from geonode.sitemap import LayerSitemap, MapSitemap
from django.views.generic import TemplateView

import geonode.proxy.urls

from geonode.api.urls import api

import autocomplete_light

# Setup Django Admin
autocomplete_light.autodiscover()
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('geonode',)
}

sitemaps = {
    "layer": LayerSitemap,
    "map": MapSitemap
}

urlpatterns = patterns('',

    # Static pages
    url(r'^/?$', TemplateView.as_view(template_name='site_index.html'), name='home'),
    url(r'^help/$', TemplateView.as_view(template_name='help.html'), name='help'),
    url(r'^developer/$', TemplateView.as_view(template_name='developer.html'), name='developer'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),

    # Layer views
    (r'^layers/', include('geonode.layers.urls')),

    # Map views
    (r'^maps/', include('geonode.maps.urls')),

    # Catalogue views
    (r'^catalogue/', include('geonode.catalogue.urls')),

    # Search views
    url(r'^search/$', TemplateView.as_view(template_name='search/search.html'), name='search'),

    # Social views
    (r"^account/", include("account.urls")),
    (r'^people/', include('geonode.people.urls')),
    (r'^avatar/', include('avatar.urls')),
    (r'^comments/', include('dialogos.urls')),
    (r'^ratings/', include('agon_ratings.urls')),
    (r'^activity/', include('actstream.urls')),
    (r'^announcements/', include('announcements.urls')),
    #(r'^notifications/', include('notification.urls')),
    (r'^messages/', include('user_messages.urls')),
    (r'^social/', include('geonode.social.urls')),
    # Accounts
    url(r'^account/ajax_login$', 'geonode.views.ajax_login',
                                       name='account_ajax_login'),
    url(r'^account/ajax_lookup$', 'geonode.views.ajax_lookup',
                                       name='account_ajax_lookup'),
    url(r'^security/permissions/(?P<resource_id>\d+)$', 'geonode.security.views.resource_permissions',
                                       name='resource_permissions'),

    # Meta
    url(r'^lang\.js$', TemplateView.as_view(template_name='lang.js', content_type='text/javascript'), name='lang'),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog',
                                  js_info_dict, name='jscat'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
                                  {'sitemaps': sitemaps}, name='sitemap'),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^autocomplete/', include('autocomplete_light.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^groups/', include('geonode.groups.urls')),
    (r'^documents/', include('geonode.documents.urls')),
    (r'^services/', include('geonode.services.urls')),
    url(r'', include(api.urls)),
    )

if "geonode.contrib.dynamic" in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^dynamic/', include('geonode.contrib.dynamic.urls')),
    )

if 'geonode.geoserver' in settings.INSTALLED_APPS:
    # GeoServer Helper Views
    urlpatterns += patterns('', 
        # Upload views
        (r'^upload/', include('geonode.upload.urls')),
        (r'^gs/', include('geonode.geoserver.urls')),
    )

# Set up proxy
urlpatterns += geonode.proxy.urls.urlpatterns

# Serve static files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler403 = 'geonode.views.err403'

#Featured Maps Pattens
#urlpatterns += patterns('',
#    (r'^(?P<site>[A-Za-z0-9_\-]+)/$', 'geonode.maps.views.featured_map'),
#    (r'^(?P<site>[A-Za-z0-9_\-]+)/info$', 'geonode.maps.views.featured_map_info'),
#)
