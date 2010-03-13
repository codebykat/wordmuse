from django.db import models
from django import VERSION

class Tag(models.Model):
  if VERSION[0] >= 1:
    name = models.CharField(max_length=50)
  else:
    name = models.CharField(maxlength=50)

  def __unicode__(self):
    return self.name

  def __str__(self):
    return self.name

  class Admin:
    pass

class Word(models.Model):
  if VERSION[0] >= 1:
    name = models.CharField(max_length=50, unique=True)
  else:
    name = models.CharField(maxlength=50, unique=True)

  siblings = models.ManyToManyField('self', blank=True, null=True)
  tags = models.ManyToManyField(Tag, blank=True, null=True)

  def __unicode__(self):
    return self.name

  def __str__(self):
    return self.name

  class Admin:
    pass


class Card(models.Model):
  front = models.ForeignKey(Word, related_name="front_set")
  back = models.ForeignKey(Word, related_name="back_set")

class Deck(models.Model):
  if VERSION[0] >= 1:
    name = models.CharField(max_length=50, unique=True)
  else:
    name = models.CharField(maxlength=50, unique=True)

  left = models.ManyToManyField(Tag, related_name='left_set')
  right = models.ManyToManyField(Tag, related_name='right_set', blank=True, null=True)
  cards = models.ManyToManyField(Card, blank=True, null=True)

  def __unicode__(self):
    return self.name

  def __str__(self):
    return self.name

  class Admin:
    pass


if VERSION[0] >= 1:
  from django.contrib import admin

  admin.site.register(Tag)
  admin.site.register(Word)
