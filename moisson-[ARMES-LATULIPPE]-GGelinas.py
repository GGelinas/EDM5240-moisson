'''
Script Python pour le travail de mi-session
Titre: moisson-[ARMES-LATULIPPE]-GGelinas.py
Réalisé par Geneviève Gélinas / GELG19608607 dans le cadre du cours EDM5240 - Technologie de l'information appliquée au journalisme
Date de réalisation: Samedi 3 mars 2017

Description général du script: 
Créer un fichier .csv avec des données moissonnées
'''


# coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup

#Création d'une variable avec le nom de notre futur fichier csv dans lequel on va mettre le résultat de notre moisson.
fichier = "latulippearmes.csv" 

#Soyons polis!
entetes = {
	"User-Agent":"Genevieve Gelinas - Requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM (EDM5240)",
	"From":"gelinas.genevieve@gmail.com"
}

#Création de variables qui serviront à des compteurs.
n=1
c=0
j=0

#Création d'une boucle à l'infini pour que le script moissonne toutes les pages du catalogue 'armes', car nous ne savons pas combien il y a de pages en tout.
while 1:
	try:
    		#Création d'une variable avec notre url de départ
		url = "https://www.latulippe.com/fr/catalogue/armes/?page={}".format(n)
		#print(url)
  
   		#Une demande est envoyée à requests pour établir une connexion avec cet url, ensuite il placera le contenu dans une variable appelée 'contenu'.
		contenu = requests.get(url, headers=entetes)
    
   		#Une demande est envoyée à BeautifulSoup pour qu'il prenne le texte de ce contenu, du texte html, et de l'analyser. Ensuite il le mettera le résultat dans une variable appelée 'page'.
		page = BeautifulSoup(contenu.text,"html.parser")
		#print(page)
   
   		#L'info qu'on cherche est dans une page avec plusieurs items. Chaque item est dans un élément html <div>, donc on utilise le .find_all pour les réunir tous dans une liste
		urlDesArmes = page.find_all("div", class_="titre")
		#print(urlDesArmes)
		
	    	#On utilise un autre .find_all pour repérer la dernière page contenant des produits étant donné que nous ne savons pas combien il y a de pages en tout dans le catalogue.
	   	#Cette dernière page est caractérisée par l'absence de la balise ul.
    		ul = page.find_all("ul", class_="produits")
		#print(ul)
		
    		print ("page", n) #Permet de savoir à quelle page nous sommes rendus dans le moissonnage.
		
		c+=1 #Compteur pour le numéro de la page
		n+=1 #Compteur du numéro de page de l'url
		
    		#Création d'une boucle qui consultera chacun des produits affichés dans le catalogue et en extraiera tous les produits qui auront la mention de 'semi-automatique'. 
		for urlArme in urlDesArmes:
			try:
       				#Création d'une liste qui contiendra les urls de chacun des produits.
				Arme = [] 
        			url2 = urlArme.a["href"] #On va chercher l'hyperlien vers la sous-page qui contient plus d'infos sur les produits.
				#print (url2)
				url2 = "https://www.latulippe.com" + url2
				#print (url2)
				Arme.append(url2)
				#print(Arme)

        			#Une demande est envoyée à requests pour établir une connexion avec l'url2, ensuite il placera le contenu dans une variable appelée 'contenu2'.
				contenu2 = requests.get(url2)
        			#Une demande est envoyée à BeautifulSoup pour qu'il prenne le texte de ce contenu, du texte html, et de l'analyser. Ensuite il le mettera le résultat dans une variable appelée 'page2'.
				page2 = BeautifulSoup(contenu2.text, "html.parser")
				#print (page2)
			
        			#Création d'une liste qui contiendra le nom des items(produits), qui auront dans leur titre les mots 'semi-automatique', et leur prix.
				semiautomatique = []
				titre = page2.title.text.split("|")[0].strip() #On va chercher le titre de l'onglet pour qu'il soit plus lisible. 
				#print(titre)
				semiautomatique.append(titre)
				#print(semiautomatique)
				
        			#On utilise un .find pour trouver le prix des produits recensés et on le rattache à la liste semiautomatique.
				prix = page2.find("b", itemprop="price").text
				#print(prix)
				prix = prix.replace(u'\xa0', u' ') #Permet d'enlever les caractères '\xa0' pour un meilleur affichage dans la liste.
				semiautomatique.append(prix)
				#print(semiautomatique)
				
				#On demande au script de chercher parmi tous les items ceux qui ont la mention des mots 'semi-automatique'.
				findSA = semiautomatique[0].find("semi-automatique")
        
        			#Création d'une condition pour déterminer les items qui contiennent les mots 'semi-automatique'.
				if findSA != -1:
					j+=1 #Compteur pour le nombre d'items recensés
					print(j," ","page",c," ",semiautomatique)
					
          				#Inscription de la liste semiautomatique dans une nouvelle ligne d'un fichier csv.
					armesmoisson = open(fichier,"a")
					coucou = csv.writer(armesmoisson)
					coucou.writerow(semiautomatique)

			except:
				print("Erreur programme")
		
		#Transformation de la variable 'ul' en variable bool. Permet au script de déterminer la dernière page html qui contient des produits dessus et arrête le programme.
		flag = bool(ul)	
		if flag == False:
			print("Fin du programme")
			break


	except:
		print ("Erreur programme")
		break

'''
*******MON SCRIPT SANS LES COMMENTAIRES*******

# coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup

fichier = "latulippearmes.csv"

entetes = {
	"User-Agent":"Genevieve Gelinas - Requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM (EDM5240)",
	"From":"gelinas.genevieve@gmail.com"
}

n=1
c=0
j=0

while 1:
	try:
		url = "https://www.latulippe.com/fr/catalogue/armes/?page={}".format(n)
		#print(url)

		contenu = requests.get(url, headers=entetes)
		page = BeautifulSoup(contenu.text,"html.parser")
		#print(page)

		urlDesArmes = page.find_all("div", class_="titre")
		#print(urlDesArmes)
		#print(len(urlDesArmes))
		
		ul = page.find_all("ul", class_="produits")
		#print(ul)
		
		print ("page", n)
		
		c+=1 #Compteur pour le numéro de la page
		n+=1 #Compteur du numéro de page de l'url
		

		for urlArme in urlDesArmes:
			try:
				Arme = []
				url2 = urlArme.a["href"]
				#print (url2)
				url2 = "https://www.latulippe.com" + url2
				#print (url2)
				Arme.append(url2)
				#print(Arme)

				contenu2 = requests.get(url2)
				page2 = BeautifulSoup(contenu2.text, "html.parser")
				#print (page2)
			
				semiautomatique = []
				titre = page2.title.text.split("|")[0].strip()
				#print(titre)
				semiautomatique.append(titre)
				#print(semiautomatique)
				
				prix = page2.find("b", itemprop="price").text
				#print(prix)
				prix = prix.replace(u'\xa0', u' ')
				semiautomatique.append(prix)
				#print(semiautomatique)
				
				findSA = semiautomatique[0].find("semi-automatique")

				if findSA != -1:
					j+=1 #Compteur pour le nombre d'items recensés
					print(j," ","page",c," ",semiautomatique)
													
					armesmoisson = open(fichier,"a")
					coucou = csv.writer(armesmoisson)
					coucou.writerow(semiautomatique)

			except:
				print("Erreur programme")
		
		
		flag = bool(ul)	
		if flag == False:
			print("Fin du programme")
			break


	except:
		print ("Erreur programme")
		break
'''
