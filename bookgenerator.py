import numpy as np

livre = open('livre_final.txt', 'w+')

list_excepted = [".", ",", ";", "?", "!", "*", ":", "/", "-", "_", "’", "‘", "'", "(", ")", "[", "]", "{", "}", "\""]
after_point = [".", "?", "!"]
params_dico = {}

with open('stuff/parameters.txt', 'r') as f:
	for line in f:
		params_dico[line.split("=")[0]] = line.split("=")[1].replace("\n", "")


def getRand(values, first_value):
	#values is a dict {} of probabilities in percent %
	rand_numb = np.random.uniform(0.0, 100.0)
	ep = {}
	sp = {}
	current_point = 0
	index_of_value = ""
	proba_point = 0

	for i in values:
		sp[i] = current_point
		ep[i] = current_point + values[i]
		current_point = ep[i]

	for i in values:
		if ep[i] > rand_numb and sp[i] < rand_numb:
			index_of_value = i
			proba_point = ep[i]-sp[i]
			if proba_point < float(params_dico["proba_tab"]) and first_value in after_point:
				return {"0" : index_of_value, "1": "true"}
			else:
				return {"0" : index_of_value, "1": "false"}



def getAllWords(word):
	dico_final = {}
	with open('stuff/dataset_final.txt', 'r') as f:
		for line in f:
			if (" " + word + "++") in line:
				part1 = line.split('==')[0]
				dico_final[part1.split('++')[1]] = float(line.split('==')[1].replace("%", "").replace("\n", "").replace("+", "").replace("=", ""))


	return dico_final

current_word = params_dico["start_word"]
livre.write(current_word.title())
next_maj = False

print(params_dico)


for i in range(int(params_dico["nb_word"])):
	
	dico_return = getRand(getAllWords(current_word), current_word)
	cache = dico_return["0"]
	put_tab = dico_return["1"]
	if cache in list_excepted and current_word in list_excepted:
		dico_return = getRand(getAllWords(cache), cache)
		cache = dico_return["0"]
		put_tab = dico_return["1"]
	if cache in list_excepted:
		if cache in after_point:
			next_maj = True
		livre.write(cache)
	else:
		if next_maj:

			if put_tab == "true":
				livre.write("\n\t" + cache.title())
			else:
				livre.write(" " + cache.title())
			
			next_maj = False
		else:
			livre.write(" " + cache)
		

	current_word = cache
	print("mot", i)
