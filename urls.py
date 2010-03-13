from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()
admin_pattern = (r'^admin/(.*)', admin.site.root)

urlpatterns = patterns('',
    # Example:
    # (r'^wordmuse/', include('wordmuse.foo.urls')),

    admin_pattern,
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'', include('wordmuse.flashcards.urls')),
)
