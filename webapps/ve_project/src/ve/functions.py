# -*- coding: utf-8 -*-

from __future__ import division
import random
import re
import Levenshtein as lev
import aspell
import string
import unicodedata
import distance


# Function help()
# ========================================================================================

def help_words(randomsent, randomsent_machinet):
	"""
	Takes as input translations as unicode strings and makes a list of  unique, 
	lowercased and tokenized words without punctuation marks.
	The order is randomized.
	"""
	
	global bothtranslations

	bothtranslations = []
	
	patter_punct = r'([^a-zA-Z0-9_ÀÁÈÉÍÓÚÜàáèéíñóúü]+)'
	pattern_no_punct = r'([a-zA-Z0-9_ÀÁÈÉÍÓÚÜàáèéíñóúü]+)'
	exclude = set(string.punctuation)
	# split where not ES alphanumeric
	
	randomchoice_translation = randomsent.encode('utf8').split()
	refsp_without_inverted_marks = []
	
	randomchoice_machinetranslation = randomsent_machinet.encode('utf8').split()
	
	for word in randomchoice_translation:
		for punc in exclude:

			if not word.startswith(punc) and not word.endswith(punc): ##favor...píntame
				word = word.lower().replace('¡','').replace('¿', '').replace(punc, ' ')
			
			else:
				word = word.lower().replace('¡','').replace('¿', '').replace(punc, '')          	
                refsp_without_inverted_marks.append(word)
                                                       
        for word in refsp_without_inverted_marks:
            m = re.match(pattern_no_punct, word)
            if word.isalnum() or m:
                bothtranslations.append(word)

	for word in randomchoice_machinetranslation:
#            # this is not necces. here, but we can use it if we want to be 100% 
           word = word.lower().replace('¡','').replace('¿', '')
           m = re.match(pattern_no_punct, word)
           if word.isalnum() or m:
                bothtranslations.append(word)
	
	
	#random.shuffle(bothtranslations)
	bothtranslations = list(sorted(set(bothtranslations)))
	bothtranslations = ' '.join(bothtranslations)

	return bothtranslations



def spelling_checker(inputsentence, reft, mtdetok, mttok):

	"""
	Function for checking the spelling of each word in users sentence and 
	underlining it if spelled wrongly, using Aspell
	"""
	 
	global saved_tr, highlight
	
	# works only local:
	#spelling = aspell.Speller('lang', 'es')
	spelling = aspell.Speller(('local-data-dir','/home/dobati/usr/lib64/aspell-0.60'),)
	saved_tr = inputsentence.encode('utf-8')
	
	patter_punct = r'([^a-zA-Z0-9_ÀÁÈÉÍÓÚÜàáèéíñóúü]+)'
	pattern_no_punct = r'([a-zA-Z0-9_ÀÁÈÉÍÓÚÜàáèéíñóúü]+)'
	
	trans_no_punct = re.split(patter_punct, saved_tr)	# get a list of token including whitespace and punct as token
	
	#################################################################################
	# words in translations should be marked as spelled correctly
	words_in_translations = []
	reft = reft.encode('utf8').split()
	mtdetok = mtdetok.encode('utf8').split()
	mttok = mttok.encode('utf8').split()
	words_in_translations = list(set(reft + mtdetok + mttok))
	#################################################################################

	spelled_list = []

	for word in trans_no_punct:
		
		m = re.match(pattern_no_punct, word)	# match all words with no punct
		
		
		word1 = word.decode('utf8')
		word1 = unicodedata.normalize('NFKD', word1).encode('ASCII', 'ignore')	# replace diacritics to nearest ascii letter
			
			# if word has no diacritics
		if word == word1:
			if m:
				checked_spelling = spelling.check(word)
					#########################################
					### added and word not in words_in_translations:
				if checked_spelling != 1 and word not in words_in_translations:				
					word = '<highlight>'+word+'</highlight>'	#'underline the false pronounced word (save_it) in the translation'
					spelled_list.append(word)
				else:
					spelled_list.append(word)
				# include whitespace and punct
			else:
				spelled_list.append(word)
			
			# if word has diacritics, check the word with no diacritics as diacritics not recognise in aspell
		else:
			if m:
				checked_spelling = spelling.check(word1)
				#########################################
				### added "and word not in words_in_translations"
				if checked_spelling != 1 and word not in words_in_translations:
					word = '<highlight>'+word+'</highlight>' 	#'underline the false pronounced word (save_it) in the translation'
					spelled_list.append(word)
				else:
					spelled_list.append(word)
			# include whitespace and punct
			else:
				spelled_list.append(word)

	saved_tr = ''.join(spelled_list)

	return saved_tr


# Function compare_ref()
# ========================================================================================

def compare_ref(usertrans, targettrans):
	"""
	Takes the target translation and the user translation as inputs.
	Based on their edit distance returns an evaluation.
	@ targettrans: target translation (ideal translation of a text)
	@ usertrans: translation provided by the user
	"""
	
	evaluation = {'very good': ['Superb translation!', 'Great work!', 'Perfect score!', 'High five!'], \
			'good': ['Good translation!', 'Nice work!', 'Almost perfect!'], \
			'fair': ['Not bad!', 'Almost there!'], \
			'average': ['You can do better!', 'Shall we practice a little more?']
			}
	
	# encode sentences to UTF-8
	ut = usertrans.encode('utf-8')
	tt = targettrans.encode('utf-8')
	
	# works only local:
	#spelling = aspell.Speller('lang', 'es')#
	spelling = aspell.Speller(('local-data-dir','/home/dobati/usr/lib64/aspell-0.60'),)
	# remove punctuation
	replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
	
	# added  .replace('¿','').replace('¡','') because the string method does not recognize ¿¡
	tt = tt.translate(replace_punctuation).lower().replace('¿','').replace('¡','').split()	
	ut = ut.translate(replace_punctuation).lower().replace('¿','').replace('¡','').split()
	
	# if less than 5 words in both sentences
	if len(tt) < 5 and len(ut) < 5:
		word_is_es = 0
		word_in_ref = 0
		length_tt = len(tt)
		length_ut = len(ut)
		
		# check if w in user also in ref
		for w in ut:
			if w in tt:
				word_in_ref += 1
		
		# check if w in user is spanish
		for w in ut:
			w = w.decode('utf8')
			w = unicodedata.normalize('NFKD', w).encode('ASCII', 'ignore')
			
			if spelling.check(w) == 1:
				word_is_es += 1
			else:
				continue
		
		# get ratio spanish word and word in ref
		ratio_is_es = word_is_es/length_ut
		ratio_in_ref = word_in_ref/length_tt
		
		# get levensthein ratio token and characters
		lensum = len(tt)+len(ut)
		ratio_lev_tok = (lensum - distance.levenshtein(tt, ut)) / lensum
		
		tt = ' '.join(tt)
		ut = ' '.join(ut)
		ratio_lev_let = lev.ratio(tt,ut)
		
		# get best ratio	
		best_lev_ratio = max(ratio_lev_tok, ratio_lev_let)
		
		# if user sent less than 3 words, check if at least half words in ref and all words spanish
		if length_ut < 3:
			if ratio_in_ref >= 0.5:
				if ratio_is_es == 1:
					if best_lev_ratio >= 0.6:
						return random.choice(evaluation['very good'])
					else:
						return random.choice(evaluation['fair'])
				else:
					return random.choice(evaluation['average'])
			else:
				return random.choice(evaluation['average'])
		
		# if user sent between 3 and 4 words, check at least 60% words in ref and 90% words spanish
		else:
			if ratio_in_ref >= 0.6:
				if ratio_is_es >= 0.9:
					if best_lev_ratio >= 0.7:
						return random.choice(evaluation['very good'])
					elif best_lev_ratio >= 0.6:
						return random.choice(evaluation['good'])
					else:
						return random.choice(evaluation['average'])
				
				elif ratio_is_es >= 0.5:
					if best_lev_ratio >= 0.9:
						return random.choice(evaluation['good'])
					elif best_lev_ratio >= 0.7:
						return random.choice(evaluation['fair'])
					else:
						return random.choice(evaluation['average'])
				else:
					return random.choice(evaluation['average'])
			else:
				return random.choice(evaluation['average'])
	
	# if either sentence have more than 5 words, get best levensthein ratio (token VS. characters) 	
	else:
		lensum = len(tt)+len(ut)

		ratio_lev_tok = (lensum - distance.levenshtein(tt, ut)) / lensum
		tt = ' '.join(tt)
		ut = ' '.join(ut)
		ratio_lev_let = lev.ratio(tt,ut)
		
		ratio = max(ratio_lev_let, ratio_lev_tok)

		if ratio >= 0.9:
			return random.choice(evaluation['very good'])
		elif ratio >= 0.75:
			return random.choice(evaluation['good'])
		elif ratio >= 0.6:
			return random.choice(evaluation['fair'])
		else:
			return random.choice(evaluation['average'])


# Function compare_mt()
# ========================================================================================

def compare_mt(usertrans, referencetrans, machinetrans):
	"""
	Compare if user translation better or worst
	than machine translation
	"""
	
	# deleted: 'You did as good as the machine translation!'
	evaluation = {'better': ['Congratulations, you did better than the machine translation!', \
							 'Be proud, you were better than the machine translation!', \
							 'You are the best, even better than the machine translation!'], \
					'same': [
							 'This is a tie between you and the machine translation!', \
							 'The machine translation was about as good as you!'], \
					'worst': ["The machine translation beat you, let's try to do better!", \
							  "What a shame, you were defeated by the machine translation.", \
							  "Next time, you will beat the machine translation, but not this time!"]}
	
	# encode sentences to UTF-8
	ut = usertrans.encode('utf8')
	tt = referencetrans.encode('utf8')
	mt = machinetrans.encode('utf8')
	
			
	# remove punctuation
	replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
	
	#added  .replace('¿','').replace('¡','') because the string method does not recognize ¿¡
	ut = ut.translate(replace_punctuation).lower().replace('¿','').replace('¡','')
	tt = tt.translate(replace_punctuation).lower().replace('¿','').replace('¡','')
	mt = mt.translate(replace_punctuation).lower().replace('¿','').replace('¡','')
	
	# levensthein characters ratio
	lev_let_ut = lev.ratio(tt, ut)
	lev_let_mt = lev.ratio(tt, mt)
	
	# levensthein tokens ratio
	ut = ut.split()
	tt = tt.split()
	mt = mt.split()
	
	lensum_user = len(ut)+len(tt)
	lensum_machine = len(mt)+len(tt)
	
	lev_tok_ut = (lensum_user - distance.levenshtein(tt, ut)) / lensum_user
	lev_tok_mt = (lensum_machine - distance.levenshtein(tt, mt)) / lensum_machine
	
	# get best levensthien ratio
	ratio_ut = max(lev_let_ut, lev_tok_ut)
	ratio_mt = max(lev_let_mt, lev_tok_mt)

	########################################################
	# added:
	#
	# evaluate if user better, worst or similar than machine
	if abs(ratio_ut - ratio_mt) < 0.07:
		return random.choice(evaluation['same'])
	else:
		if ratio_ut > ratio_mt:
			return random.choice(evaluation['better'])
		else:
			return random.choice(evaluation['worst'])
	
	# TO DO: add some more specific evaluations and tie the two Feedbacks together



