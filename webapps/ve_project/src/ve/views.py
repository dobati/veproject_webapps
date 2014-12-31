# -*- coding: utf-8 -*-
# views.py

# Imports
# ========================================================================================

# To be able to render a page when you click on it
from django.shortcuts import render

# import Tables Models for all domain
from .models import GeneralEnEs
from .models import SubsEnEs
from .models import EuconstEnEs
from .models import ThelittleprinceEnEs

# import model for the user input - translation
from .models import UserInput

# ===== FOR user IP ===== #
from .models import ip
import datetime

# import form for the user input - translation
from .forms import UserInputForm

# for choosing random input from the database
import random

# ===== FOR LATER with own random function ===== #
# if we want to make the random faster, we should define our own random function
#from .models import Random
# ============================================== #

# import the functions
import functions
from .functions import help_words
from .functions import spelling_checker
from .functions import compare_ref
from .functions import compare_mt

# ===================== END Imports ===================== #

# Views for the index and about pages
# ========================================================================================

# View for the main page:
def index(request):
	return render(request, "index.html")

# View for the page about us                           
def about_us(request):
	return render(request, "about_us.html")

# View for the page about Vé                      
def about_ve(request):
	return render(request, "about_ve.html")

# Views for the pages where the user is asked to translate
# ========================================================================================

def general1(request):
	return trans(request, "Your choice: General domain, level 1", GeneralEnEs, 1)
	
def general2(request):
	return trans(request, "Your choice: General domain, level 2", GeneralEnEs, 2)
	
def general3(request):
	return trans(request, "Your choice: General domain, level 3", GeneralEnEs, 3)


def books1(request):
	return trans(request, "Your choice: Books, level 1", ThelittleprinceEnEs, 1)
	
def books2(request):
	return trans(request, "Your choice: Books, level 2", ThelittleprinceEnEs, 2)
	
def books3(request):
	return trans(request, "Your choice: Books, level 3", ThelittleprinceEnEs, 3)
	
	
def movies1(request):
	return trans(request, "Your choice: Movies, level 1", SubsEnEs, 1)

def movies2(request):
	return trans(request, "Your choice: Movies, level 2", SubsEnEs, 2)

def movies3(request):
	return trans(request, "Your choice: Movies, level 3", SubsEnEs, 3)
	
	
def legaltexts1(request):
	return trans(request,  "Your choice: Legal Texts, level 1", EuconstEnEs, 1)

def legaltexts2(request):
	return trans(request,  "Your choice: Legal Texts, level 2", EuconstEnEs, 2)
	
def legaltexts3(request):
	return trans(request,  "Your choice: Legal Texts, level 3", EuconstEnEs, 3)


# Function trans()
# ========================================================================================

def trans(request, message, dbtable, levelchoice):
    
	"""
	User gets a random sentence according to domain and level
	and can submit her translation.
	It makes use of translate.html
	"""

	# ===== FOR LATER with user IP ===== #		--> currently in feedback()
	#x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	#
	#if x_forwarded_for:
	#    ipaddress = x_forwarded_for.split(',')[-1].strip()
	#else:
	#    ipaddress = request.META.get('REMOTE_ADDR')
	#get_ip= ip() #imported class from model
	#get_ip.ip_address= ipaddress
	#get_ip.pub_date = datetime.date.today() #import datetime
	#get_ip.save()
	# ================================== #
	
	# get random row from database
	randomchoice = random.choice(dbtable.objects.filter(level=levelchoice))
	# get source from row (smart_unicode)
	r = randomchoice.original()
	# get target from row (smart_unicode)
	t = randomchoice.translation()
	# get tokenised MT translation from row (smart_unicode)
	mt_tok = randomchoice.machine_translation_tok()
	
	# call the help function to make suggestions to the user
	#js_data = help_words(randomchoice,machine_trans_of_randomchoice_tok)
	
	# save infos in session hash
	##	USING "if not" to assure feedback analyse same sentence as the one the user got
	##	ELSE: the views directly take the next sentence
	##### TO DO:	ameliorate this as changing level in-between translating
	#####			or coming back without clearing history make first sentence
	#####			translation and feedback not match!!
	if not 'message' in request.session:				# info about domain and level as message
		request.session['message'] = message			
	if not 'levelchoice' in request.session:			# info about level
		request.session['levelchoice'] = levelchoice	
	if not 'random_sent' in request.session:			# source sentence
		request.session['random_sent'] = r	
	if not 'random_target' in request.session:			# target sentence
		request.session['random_target'] = t	
	if not 'random_machine_detok' in request.session:	# machine sentence not tokenised
		request.session['random_machine_detok'] = randomchoice.machine_translation_detok()
	if not 'random_machine_tok' in request.session:		# machine sentence tokenised
		request.session['random_machine_tok'] = mt_tok
	
	
	if request.method == 'POST':
		form = UserInputForm(request.POST)

		if form.is_valid():
			# save user translation in session hash
			request.session['user_translation'] = form.cleaned_data.get('form_translation')
			
			# get previous info from session hash
			message = request.session['message']
			user_translation = request.session['user_translation']
			#dbtable = ThelittleprinceEnEs
			levelchoice = request.session['levelchoice']
			random_sent = request.session['random_sent']
			random_target = request.session['random_target']
			random_machine_detok = request.session['random_machine_detok']
			random_machine_tok = request.session['random_machine_tok']
			
			# return feedback
			return feedback(
				request,
				message,
				user_translation,
				dbtable,
				levelchoice,
				random_sent,
				random_target,
				random_machine_detok,
				random_machine_tok)
		
		# if form is not valid (enter "Send" with empty form or "See solution")	
		else:
			# get previous info from session hash
			message = request.session['message']
			levelchoice = request.session['levelchoice']
			random_sent = request.session['random_sent']
			random_target = request.session['random_target']
			random_machine_detok = request.session['random_machine_detok']
			
			return solution(request, message, dbtable, levelchoice, random_sent, random_target, random_machine_detok)
		
	else:
		form = UserInputForm()

	return render(request, "translate.html", {
		'chosen_topic': message,
		'r': r,
		'form': form,
		'js_data': help_words(t,mt_tok),		# help words for user
		})



def feedback(request, message, user_translation, dbtable, levelchoice, random_sent, random_target, random_machine_detok, random_machine_tok):
	"""
	Feedback for user.
	It uses feedback.html
	TO DO: add get_ip when we have implemented it.
	"""
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	
	if x_forwarded_for:
	    ipaddress = x_forwarded_for.split(',')[-1].strip()
	else:
	    ipaddress = request.META.get('REMOTE_ADDR')
	get_ip= ip() #imported class from model
	get_ip.ip_address= ipaddress
	get_ip.pub_date = datetime.date.today() #import datetime
	get_ip.save()
	
	your_translation = 'Your translation:'
	reference_translation = 'Reference translation:'
	machine_translation = 'Machine translation:'
	
	# save user input in table 'userinput'
	trans = UserInput(translation=user_translation, source=random_sent, target=random_target, machine=random_machine_detok, user_ip=get_ip)
	trans.save(force_insert=True)
	
	form = UserInputForm()

	# feedbacks
	feedback_user = compare_ref(user_translation, random_target)
	compare_to_mt = compare_mt(user_translation, random_target, random_machine_detok)
	
	# check spelling
	user_translation = spelling_checker(user_translation, random_target, random_machine_detok, random_machine_tok)
	
	# delete infos in session hash
	del request.session['message']
	del request.session['user_translation']
	del request.session['levelchoice']
	del request.session['random_sent']
	del request.session['random_target']
	del request.session['random_machine_detok']
	del request.session['random_machine_tok']
	
	return render(request, "feedback.html",
				  {
					'chosen_topic': message,
					'random_sent': random_sent,
					'form': form,
					'your_translation': your_translation,
					'user_translation': user_translation,	# highlight wrongly spelled words
					'reference_translation': reference_translation,
				    'machine_translation': machine_translation,
				    't' :random_target,
				    'machine_t' : random_machine_detok, 
				    'feedback_user': feedback_user,
				    'compare_to_mt': compare_to_mt,
				  })
	
def solution(request, message, dbtable, levelchoice, random_sent, random_target, random_machine_detok):
	"""
	Show solution to user without feedback.
	Either due to "Send" with empty text box
	or "See solution" with empty text box.
	It uses feedback.html
	"""
	
	form = UserInputForm()
	
	your_translation = 'Your translation:'
	reference_translation = 'Reference translation:'
	machine_translation = 'Machine translation:'
	
	# delete infos in session hash
	del request.session['message']
	if 'user_translation' in request.session:
		del request.session['user_translation']
	del request.session['levelchoice']
	del request.session['random_sent']
	del request.session['random_target']
	del request.session['random_machine_detok']
	if 'random_machine_tok' in request.session:
		del request.session['random_machine_tok']
	
	return render(request, "feedback.html",
				  {
					'chosen_topic': message,
					'random_sent': random_sent,
					'form': form,
					'your_translation': your_translation,
					'user_translation': 'Nada :-(',
					'reference_translation': reference_translation,
				    'machine_translation': machine_translation,
				    't' :random_target,
				    'machine_t' : random_machine_detok, 
				  })