from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
import gdata
import gdata.spreadsheet
import gdata.spreadsheet.service
from wordmuse.flashcards.models import Word, Tag, Deck
import csv

def words(request):
  words = Word.objects.order_by('name')
  return render_to_response('words.html', {'words':words},
                            context_instance=RequestContext(request))

def word(request, word):
  try:
    dbword = Word.objects.get(name=word)
    tags = dbword.tags.order_by('name')
    sibs = dbword.siblings.order_by('name')
  except:
    return HttpResponseRedirect('/words')
  return render_to_response('word.html',
                            {'word':dbword, 'tags':tags, 'siblings':sibs},
                            context_instance=RequestContext(request)  
                           )
def tags(request):
  tags = Tag.objects.order_by('name')
  return render_to_response('tags.html', {'tags':tags},  
                            context_instance=RequestContext(request))  

def tag(request, tag):
  try:
    dbtag = Tag.objects.get(name=tag)
    words = dbtag.word_set.order_by('name')
  except:
    return HttpResponseRedirect('/tags')
  #for word in words:
  #  print "checking word %s " % word
  #  valid_sibs = words & word.siblings.all()
  #  for sib in valid_sibs:
    #  print sib
  return render_to_response('tag.html',
                            {'tag':dbtag, 'words':words},
                            context_instance=RequestContext(request))  

def deck(request, name=""):
  #try:
  #  deck = Deck.objects.get(name=name)
  #  left = deck.left.all()
  #  right = deck.right.all()
  #except:
  #  return HttpResponseRedirect('/words')
  tags = Tag.objects.all()
  return render_to_response('deck.html', {'tags':tags}, context_instance=RequestContext(request))
  #                          {'deck':deck, 'left':left, 'right':right})

def play(request):
  #try:
  #deck = Deck.objects.get(name=name)
  #left = deck.left.all()
  #right = deck.right.all()
  left = request.POST.getlist('left')
  right = request.POST.getlist('right')

  leftwords = Word.objects.filter(tags__name=left[0])
  for ltag in left:
    # todo: currently this does left[0] twice, which doesn't matter but is inefficient
    leftwords = leftwords.filter(tags__name=ltag)
  #print leftwords

  cards = []
  for word in leftwords:
    #print "processing word %s.  siblings:" % word
    #print word.siblings.all()
    #rightword = getsiblingwithtag(word.siblings.all(), right)
    rightwords = word.siblings.filter(tags__name=right[0])
    #print "looking for sibling with tag %s" % right[0]
    for rtag in right:
      # todo: doing right[0] twice here
      rightwords = word.siblings.filter(tags__name=rtag)
    if len(rightwords) > 0:
      rightword = rightwords[0]
      #print "got sibling %s " % rightword
      cards.append({'front':word, 'back':rightword})

  #for l in left:
  #  leftwords = l.word_set.order_by('name')
  #  print leftwords

    #for word in leftwords:
    #  rightword = word.siblings.get(tag=l)

  #except:
  #  return HttpResponseRedirect('/words')
  #return render_to_response('play.html',
  #                          {'deck':deck, 'left':leftwords, 'right':right})
  return render_to_response('play.html', {'cards':cards},
                            context_instance=RequestContext(request))  


@user_passes_test(lambda u: u.is_superuser)
def load(request):
  # if csv file provided, loadcsv
  if request.method == 'POST':
    
    try:
      fh = request.FILES['csvfile']
    except:
      return HttpResponseRedirect("/")

    if file == '':
      # TODO: error checking (correct file type, etc.)
      return HttpResponseRedirect("/")

    try:
      fh = fh['content'].split('\n')
    except: pass

    table = csv.reader(fh)
    headers = table.next()
    #print "headers: %s" % headers
    
    for row in table:
       sibs = []
       #print "processing %s" % row
       for i in range(len(row)):
         if row[i] == "":
           continue
         headertags = headers[i]
         if headertags == "TAGS":
           tags = row[i].split("|")
           for tagname in tags:
             t, created = Tag.objects.get_or_create(name=tagname)
             for sib in sibs:
               sib.tags.add(t)
         else:
           #print "creating %s" % row[i]
           w, created = Word.objects.get_or_create(name=row[i])
           tags = headertags.split('|')
           for tagname in tags:
             #print "adding tag %s " % tagname
             t, created = Tag.objects.get_or_create(name=tagname)
             w.tags.add(t)
           
           # make sibling of all other words in row
           for sib in sibs:
             #print "adding siblings %s " % sib
             w.siblings.add(sib)

           sibs.append(w)

  return HttpResponseRedirect("/")


@user_passes_test(lambda u: u.is_superuser)
def import_from_google(request):
  gd_client = gdata.spreadsheet.service.SpreadsheetsService()
  gd = gdata.service.GDataService()
  key = 'pbK5P3b_eaymr4SovVi1mWA'
  worksheets_feed = gd_client.GetWorksheetsFeed(key, visibility='public', projection='values')

  for entry in worksheets_feed.entry:
    wksht_id = entry.id.text.rsplit('/', 1)[1]

    list_url = "http://spreadsheets.google.com/feeds/list/%s/%s/public/values" % (key, wksht_id)
    feed = gd.GetFeed(list_url)

    # get headers from cell feed (because list feed removes special characters)
    cell_url = "http://spreadsheets.google.com/feeds/cells/%s/%s/public/values" % (key, wksht_id)
    cell_feed = gd.GetFeed(cell_url + "?max-row=1")

    headers = []
    for cell in cell_feed.entry:
      headers.append(cell.content.text)
    #print "got headers %s" % headers

    for row in feed.entry:
       sibs = []
       cells = row.FindExtensions()

       #print "processing %s" % row

       for i,cell in enumerate(cells):
         if cell.text is None:
           continue

         #print "processing %s" % cell.text

         #headertags = cell.tag
         headertags = headers[i]
         #print "got header %s" % headertags
         if headertags.lower() == "tags":
           tags = cell.text.split("|")
           for tagname in tags:
             t, created = Tag.objects.get_or_create(name=tagname)
             for sib in sibs:
               sib.tags.add(t)
         else:
           #print "creating %s" % cell.text
           w, created = Word.objects.get_or_create(name=cell.text)
           tags = headertags.split('|')
           for tagname in tags:
             #print "adding tag %s " % tagname
             t, created = Tag.objects.get_or_create(name=tagname)
             w.tags.add(t)
           
           # make sibling of all other words in row
           for sib in sibs:
             #print "adding siblings %s " % sib
             w.siblings.add(sib)

           sibs.append(w)

  return HttpResponseRedirect("/")

@user_passes_test(lambda u: u.is_superuser)
def cleardb(request):
  if request.method == 'POST':
    Word.objects.all().delete()
    Tag.objects.all().delete()
  return HttpResponseRedirect("/")
