# coding: utf-8
from __future__ import division
import re
from collections import OrderedDict
import numpy as np
import time

import os





class sentistrength:
	def __init__(self, config=dict()):
		file_path = os.path.dirname(os.path.abspath(__file__))
		os.chdir(file_path)
		self.negasi = [line.replace('\n','') for line in open("negatingword.txt").read().splitlines()]
		self.tanya = [line.replace('\n','') for line in open("questionword.txt").read().splitlines()]
		#create sentiment words dictionary
		self.sentiwords_txt = [line.replace('\n','').split(":") for line in open("sentiwords_id.txt").read().splitlines()]
		self.sentiwords_dict = OrderedDict()
		for term in self.sentiwords_txt:
			self.sentiwords_dict[term[0]] = int(term[1])
		#create emoticon dictionary
		self.emoticon_txt = [line.replace('\n','').split(" | ") for line in open("emoticon_id.txt").read().splitlines()]
		self.emoticon_dict = OrderedDict()
		for term in self.emoticon_txt:
			self.emoticon_dict[term[0]] = int(term[1])
		#create idioms dictionary
		self.idioms_txt = [line.replace('\n','').split(":") for line in open("idioms_id.txt").read().splitlines()]
		self.idioms_dict = OrderedDict()
		for term in self.idioms_txt:
			self.idioms_dict[term[0]] = int(term[1])
		#create boosterwords dictionary
		self.boosterwords_txt = [line.replace('\n','').split(":") for line in open("boosterwords_id.txt").read().splitlines()]
		self.boosterwords_dict = OrderedDict()
		for term in self.boosterwords_txt:
			self.boosterwords_dict[term[0]] = int(term[1])
		self.negation_conf = config["negation"]
		self.booster_conf = config["booster"]
		self.ungkapan_conf = config["ungkapan"]
		self.consecutive_conf = config["consecutive"]
		self.repeated_conf = config["repeated"]
		self.emoticon_conf = config["emoticon"]
		self.question_conf = config["question"]
		self.exclamation_conf = config["exclamation"]
		self.punctuation_conf = config["punctuation"]
		self.mean_conf = False

	def senti(self,term):
		try:
			return self.sentiwords_dict[term]
		except:
			return 0

	def emosikon(self,term):
		try:
			return self.emoticon_dict[term]
		except:
			return 0

	def ungkapan(self,term):
		try:
			return self.idioms_dict[term]
		except:
			return 0

	def booster(self, term):
		try:
			return self.boosterwords_dict[term]
		except:
			return 0

	def cek_negationword(self, prev_term, prev_term2):
		if prev_term in self.negasi or prev_term2+" "+prev_term in self.negasi:
			self.score = -abs(self.score) if self.score>0 else abs(self.score)

	def cek_boosterword(self,term):
		booster_score = self.booster(term)
		if booster_score !=0 and self.score>0: self.score += booster_score
		if booster_score !=0 and self.score<0: self.score -= booster_score

	def cek_consecutive_term(self, prev_term):
		if self.prev_score>0 and self.score >=3: self.score+=1 
		if self.prev_score<0 and self.score <=-3: self.score-=1 

	def cek_ungkapan(self, bigram,trigram, i):
		bigram = ' '.join(bigram)
		trigram = ' '.join(trigram)
		ungkapan_score = self.ungkapan(bigram)
		if ungkapan_score==0:
			ungkapan_score = self.ungkapan(trigram)
		if ungkapan_score!=0:
			self.score = ungkapan_score
			self.prev_score = 0
			self.pre_max_pos[i-1] = 1
			self.pre_max_neg[i-1] = -1
			self.max_pos = self.pre_max_pos[i-2] #if len(self.pre_max_pos)>1 else 1
			self.max_neg = self.pre_max_neg[i-2] #if len(self.pre_max_neg)>1 else -1
			self.sentence_score[i-1] = re.sub(r'\[\d\]','',self.sentence_score[i-1])

	def cek_repeated_punctuation(self, next_term):
		if re.search(r'!{2,}',next_term) and self.score >=3: self.score+=1
		if re.search(r'!{2,}',next_term) and self.score <=-3: self.score-=1

	def remove_extra_repeated_char(self, term):
		return re.sub(r'([A-Za-z])\1{2,}',r'\1',term)
	def plural_to_singular(self, term):
		return re.sub(r'([A-Za-z]+)\-\1', r'\1',term)
	def classify(self):
		result = "neutral"
		try:
			if self.mean_conf:
				mean_p = np.mean(self.mean_pos)
				mean_n = np.mean(self.mean_neg)
				print (mean_p, mean_n)
				if mean_p > mean_n:
					result = "Positif"
				elif mean_p < mean_n and not self.is_tanya:
					result = "Negatif"
				elif mean_p < mean_n and self.is_tanya:
					result = "Netral"
			else:
				if abs(self.sentences_max_pos) > abs(self.sentences_max_neg):
					result = "Positif"
				elif abs(self.sentences_max_pos) < abs(self.sentences_max_neg):
					result = "Negatif"
				elif abs(self.sentences_max_pos) == abs(self.sentences_max_neg):
					result = "Netral"
		except:
			print("error ",self.sentences_max_pos, self.sentences_max_neg)
		return result
	def cek_neutral_term(self,terms,i):
		if terms[i-1] in self.neutral_term or terms[i+1] in self.neutral_term: self.score=1 

	def main(self,sentence):
		self.neutral_term = ['jika','kalau']
		sentences = sentence.split('.')
		self.sentences_max_neg = -1
		self.sentences_max_pos = 1
		self.sentences_score = []
		self.sentences_text = []
		
		for sentence in sentences:
			self.max_neg = -1
			self.max_pos = 1
			self.mean_neg = [1]
			self.mean_pos = [1]
			self.sentence_score=[]

			terms = re.split(r'[\s,.]',sentence.lower())
			terms_length = len(terms)
			self.is_tanya = False
			self.sentence_text = ''

			if self.exclamation_conf and re.search('!',sentence): self.max_pos = 2
			self.prev_score = 0
			self.pre_max_pos = []
			self.pre_max_neg = []
			fix_score = 0
			for i,term in enumerate(terms):
				is_extra_char = False
				plural = ''
				self.score = 0
				if re.search(r'([A-Za-z])\1{3,}',term):
					is_extra_char = True
				term = self.remove_extra_repeated_char(term)
				if re.search(r'([A-Za-z]+)\-\1',term):
					plural = term
					term = self.plural_to_singular(term)

				#GET SENTI SCORE#
				self.score = self.senti(term)
				fix_score = fix_score +self.score

				#NEGATION HANDLER#
				if self.negation_conf and self.score !=0 and i>0:
					self.cek_negationword(terms[i-1],terms[i-2])

				#BOOSTERWORD HANDLER#
				if self.booster_conf and self.score !=0 and i>0 and i<=(terms_length-1):self.cek_boosterword(terms[i-1])
				if self.booster_conf and self.score !=0 and i>=0 and i<(terms_length-1):self.cek_boosterword(terms[i+1])

				#IDIOM/UNGKAPAN HANDLER#
				if self.ungkapan_conf and i>0 and i<=(terms_length-1):self.cek_ungkapan([terms[i-1],term],[terms[i-2],terms[i-1],term],i)

				#CONSECUTIVE SENTIMENT WORD#
				if self.consecutive_conf and i>0 and i<=(terms_length-1) and self.score !=0:self.cek_consecutive_term(terms[i-1])

				#+1 SENTI SCORE IF REPEATED CHAR ON POSITIVE/NEGATIVE +2 IF NEUTRAL TERM
				if self.repeated_conf and is_extra_char==True and self.score>0: self.score+=1
				if self.repeated_conf and is_extra_char==True and self.score<0: self.score-=1
				if self.repeated_conf and is_extra_char==True and self.score==0: self.score=2
				# print  "repeat char score", term, self.score
				if self.punctuation_conf and i>=0 and i<(terms_length-1): self.cek_repeated_punctuation(terms[i+1])
				# CEK APAKAH TERDAPAT KATA TANYA
				if self.question_conf and (term in self.tanya or re.search(r'\?',term)):self.is_tanya = True
				# CEK neutral term 
				if self.score!=0 and i>1 and i<(terms_length-2): self.cek_neutral_term(terms,i)
				# if self.score!=0 and i>0 and i<(terms_length-4): self.cek_neutral_term(terms,i)
				if self.emoticon_conf and self.score==0: self.score = self.emosikon(term)

				self.prev_score = self.score
				if self.mean_conf and self.score>0: self.mean_pos.append(self.score)	
				if self.mean_conf and self.score<0: self.mean_neg.append(abs(self.score))
				#GET MAX SCORE +ve/-ve	
				self.max_pos= self.score if self.score > self.max_pos else self.max_pos
				self.max_neg= self.score if self.score < self.max_neg else self.max_neg
				#insert score info current term
				self.pre_max_pos.append(self.max_pos)
				self.pre_max_neg.append(self.max_neg)
				# print self.pre_max_pos, self.pre_max_neg
				if plural !='': term = plural
				self.sentence_text += ' {}'.format(term)
				if self.score != 0:term = "{} [{}]".format(term, self.score)
				self.sentence_score.append(term)

			self.sentences_text.append(self.sentence_text)
			self.sentences_score.append(" ".join(self.sentence_score))
			if self.is_tanya: 
				self.max_neg = -1
			self.sentences_max_pos = self.max_pos if self.max_pos > self.sentences_max_pos else self.sentences_max_pos
			self.sentences_max_neg = self.max_neg if self.max_neg < self.sentences_max_neg else self.sentences_max_neg
			# print self.sentences_max_pos, self.sentences_max_neg
		sentence_result = self.classify()
		# print self.sentences_text
		return {"fix_score":fix_score, "classified_text":". ".join(self.sentences_score),"text":". ".join(self.sentences_text),"sentence_score":self.sentences_score,"max_positive":self.sentences_max_pos,"max_negative":self.sentences_max_neg,"kelas":sentence_result}

