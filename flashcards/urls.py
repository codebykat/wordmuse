from django.conf.urls.defaults import *
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")
prefix = "wordmuse/"

urlpatterns = patterns('flashcards.views',
#    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
#                              {'document_root': media_root}),
    (r'^%stags' % prefix, 'tags'),
#    (r'^words', 'words'),
    (r'^%sdeck' % prefix, 'deck'),
    (r'^%splay' % prefix, 'play'),
    (r'^%sload' % prefix, 'load'),
#    (r'^deck/(.*)$', 'deck'),
    (r'^%splay/(.*)$' % prefix, 'play'),
    (r'^%stag/(.*)$' % prefix, 'tag'),
    (r'^%sword/(.*)$' % prefix, 'word'),
    (r'^%sgdata' % prefix, 'import_from_google'),
    (r'^%scleardb' % prefix, 'cleardb'),
    (r'%s' % prefix, 'words'),
)
