# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.

# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.

#from __future__ import unicode_literals
from django.utils.encoding import smart_unicode
from django.db import models

#import random		# eventually later if random function model manager


class GeneralEnEs(models.Model):
	 id = models.IntegerField(primary_key=True)  # AutoField?
	 source = models.TextField()
	 target = models.TextField()
	 level = models.IntegerField()
	 detok = models.TextField()
	 tok = models.TextField()
	 entrydate = models.DateTimeField(db_column='entryDate')  # Field name made lowercase.
	 
	 def __unicode__(self):
		  return smart_unicode(self.source)
	 
	 def sent_id(self):
		  return self.id
	 
	 def original(self):
		  return smart_unicode(self.source)
	  
	 def translation(self):
		  return smart_unicode(self.target)
	 
	 def niveau(self):
		  return self.level
	 
	 def machine_translation_detok(self):
		  return smart_unicode(self.detok)
	 
	 def machine_translation_tok(self):
		  return smart_unicode(self.tok)
	 
	 class Meta:
		  db_table = 'general_en_es'

class SubsEnEs(models.Model):
	 id = models.IntegerField(primary_key=True)  # AutoField?
	 source = models.TextField()
	 target = models.TextField()
	 level = models.IntegerField()
	 detok = models.TextField()
	 tok = models.TextField()
	 entrydate = models.DateTimeField(db_column='entryDate')  # Field name made lowercase.
	 
	 def __unicode__(self):
		  return smart_unicode(self.source)
	 
	 def sent_id(self):
		  return self.id
	 
	 def original(self):
		  return smart_unicode(self.source)
	  
	 def translation(self):
		  return smart_unicode(self.target)
	 
	 def niveau(self):
		  return self.level
	 
	 def machine_translation_detok(self):
		  return smart_unicode(self.detok)
	 
	 def machine_translation_tok(self):
		  return smart_unicode(self.tok)
	 
	 class Meta:
		  db_table = 'subs_en_es'      

class EuconstEnEs(models.Model):
	 id = models.IntegerField(primary_key=True)  # AutoField?
	 source = models.TextField()
	 target = models.TextField()
	 level = models.IntegerField()
	 tok = models.TextField()
	 detok = models.TextField()
	 entrydate = models.DateTimeField(db_column='entryDate')  # Field name made lowercase.
	 
	 def __unicode__(self):
		  return smart_unicode(self.source)
	 
	 def sent_id(self):
		  return self.id
	 
	 def original(self):
		  return smart_unicode(self.source)
	  
	 def translation(self):
		  return smart_unicode(self.target)
	 
	 def niveau(self):
		  return self.level
	 
	 def machine_translation_detok(self):
		  return smart_unicode(self.detok)
	 
	 def machine_translation_tok(self):
		  return smart_unicode(self.tok)
	 
	 class Meta:
		  db_table = 'euconst_en_es'

class ThelittleprinceEnEs(models.Model):
	 id = models.IntegerField(primary_key=True)  
	 source = models.TextField()
	 target = models.TextField()
	 level = models.IntegerField()
	 detok = models.TextField()
	 tok = models.TextField()
	 entrydate = models.DateTimeField(db_column='entryDate')  # Field name made lowercase.   
	 
	 def __unicode__(self):
		  return smart_unicode(self.source)
	 
	 def sent_id(self):
		  return self.id
	 
	 def original(self):
		  return smart_unicode(self.source)
	  
	 def translation(self):
		  return smart_unicode(self.target)
	 
	 def niveau(self):
		  return self.level
	 
	 def machine_translation_detok(self):
		  return smart_unicode(self.detok)
	 
	 def machine_translation_tok(self):
		  return smart_unicode(self.tok)
	 
	 class Meta:
		  db_table = 'thelittleprince_en_es'
         
# ======= FOR LATER WITH USER IP ADDRESS ======= #

class ip(models.Model):
#	 #id = models.AutoField(primary_key=True)
#	 #pub_date = models.DateTimeField('date published')
	 pub_date = models.DateTimeField(auto_now_add=True,auto_now=True)
	 ip_address = models.IPAddressField()
	 timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	 updated = models.DateTimeField(auto_now_add=False, auto_now=True)
#	 
#	# pass
#	# class Meta:
#	#	  db_table = 'ip'
#
	 def __unicode__(self):
		  return self.ip_address

# ============================================= #

class UserInput(models.Model):
	 #id = models.AutoField(primary_key=True)
	 translation = models.TextField()
	 source = models.TextField()
	 target = models.TextField()
	 machine = models.TextField()
	 user_ip = models.ForeignKey(ip)		# for later with user IP
	 timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	 updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	 
	 class Meta:
		  db_table = 'userinput'

	 def __unicode__(self):
		  return smart_unicode(self.translation)
	 
	# def sent_id(self):
	#	  return self.id


#bis hier
##########################################################################################

# if you have time to implement other random function

# class Random(models.Manager):
#     def random(db):
#         count = db.aggregate(count=Count('id'))['count']
#         random_index = randint(0, count - 1)
#         return db.all()[random_index]

