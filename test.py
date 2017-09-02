from collections import defaultdict
import os
import operator

list_pdf = os.listdir("training pdf")
number_pdf = len(list_pdf)

cache_before = ""
x = 0
d = open('stuff/data.txt', 'w+')
file = open('stuff/partial.txt', 'w+')
file2 = open('stuff/partial_2.txt', 'w+')
file3 = open('stuff/dataset_final.txt', 'w+')
dico_en = open('stuff/english_dico.txt', 'w+')
file4 = open('stuff/Results.txt', 'w+')
list_excepted = [".", ",", "?", "!", ":", "’", "‘", "'", ]
unallow_carac = ["(", ")", "[", "]", "{", "}", "\"", "*", ";", "/", "-", "_", "¥"]
word_assoc = defaultdict(dict)
word_tot = dict()
total_words = 0

#remplir le fichier txt
for i in range(number_pdf):

	pdfFileObj = open('training pdf/' + list_pdf[i], 'r')
	print("processing book", i)

	for line in pdfFileObj:
		for word in line.split():
			if not word.isupper():
				d.write(word + " ")
	print("processing finished")

d.close()

with open('stuff/data.txt', 'r') as f:
    for line in f:
        for word in line.split():
        	for s in list_excepted:
        		if s in word:
        			#mo contient
        			word = word.replace(s, "")
        			

        			word = word + "\n" + s
        	file.write(word + "\n")	

file.close()
with open('stuff/partial.txt', 'r') as f1:
    for line in f1:
        for word in line.split():
        	if x == 0:
        		cache_before = word
        	else:
        		if not any(ext in cache_before for ext in unallow_carac) and not any(ext in word for ext in unallow_carac):
        			#check if word is in dictionary
	        		if not cache_before[:1].isupper() and not word[:1].isupper():
	        			#This is not a proper noun
	        			if cache_before in dico_en and word[:1] in dico_en:
	        				file2.write(" " + cache_before + "++" + word + "\n")
	        		elif not word[:1].isupper() and cache_before[:1].isupper():
	        			#This is not a proper noun
	        			if word in dico_en:
	        				file2.write(" " + cache_before.title() + "++" + word + "\n")
	        		elif word[:1].isupper() and not cache_before[:1].isupper():
	        			#This is not a proper noun
	        			if cache_before in dico_en:
	        				file2.write(" " + cache_before + "++" + word.title() + "\n")
	        		elif word[:1].isupper() and cache_before[:1].isupper():
	        			file2.write(" " + cache_before.title() + "++" + word.title() + "\n")

	        		if word_assoc.get(cache_before,{}).get(word):
	        			word_assoc[cache_before][word] += 1
	        		else:
	        			word_assoc[cache_before][word] = 1
	        			

	        		if word_tot.get(cache_before):
	        			
	        			word_tot[cache_before] += 1
	        		else:
	        			word_tot[cache_before] = 1

	        		cache_before = word
        		
        	x+=1

for x in word_assoc:
    for y in word_assoc[x]:
        
        percentage = word_assoc[x][y]/word_tot[x] * 100
        file3.write(" " + str(x) + '++' + str(y) + '==' + str(percentage) + '%\n')
        total_words += word_assoc[x][y]

file3.close()

probas_dic = dict()

with open('stuff/dataset_final.txt', 'r') as f:
    for line in f:
    	proba = line.split("==")[1].replace("%", "").replace("\n", "").replace("=", "")
    	other_side = line.split("==")[0]
    	probas_dic[other_side] = proba

    	
#probas_dic = sorted(probas_dic, key=probas_dic.get)	
for i in probas_dic:
	file4.write(str(probas_dic[i]))

file4.close()

print('done with', total_words, 'words')

