from django.conf.urls.defaults import *
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                              {'document_root': media_root}),
    (r'^tags', 'flashcards.views.tags'),
#    (r'^words', 'flashcards.views.words'),
    (r'^deck', 'flashcards.views.deck'),
    (r'^play', 'flashcards.views.play'),
    (r'^load', 'flashcards.views.load'),
#    (r'^deck/(.*)$', 'flashcards.views.deck'),
    (r'^play/(.*)$', 'flashcards.views.play'),
    (r'^tag/(.*)$', 'flashcards.views.tag'),
    (r'^word/(.*)$', 'flashcards.views.word'),
    (r'^gdata', 'flashcards.views.import_from_google'),
    (r'^cleardb', 'flashcards.views.cleardb'),
    (r'', 'flashcards.views.words'),
)
