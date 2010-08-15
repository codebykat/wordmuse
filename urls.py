from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()
admin_pattern = (r'^admin/(.*)', admin.site.root)

from django.conf import settings

urlpatterns = patterns('',
    # Example:
    # (r'^wordmuse/', include('wordmuse.foo.urls')),

    admin_pattern,
    #(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^%s$' % settings.LOGIN_URL[1:], 'django.contrib.auth.views.login', {'template_name':'login.html'}),
    (r'^wordmuse/accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'', include('wordmuse.flashcards.urls')),
)
