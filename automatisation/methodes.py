from playwright.sync_api import sync_playwright
import re
from .constantes import *
import os
import json
import getpass


class Methodes :
    def __init__(self) :
         self.dictionnaire_first = not os.path.isfile("data.json")
         self.page = None
         self.cours_consultés = {}
         self.user_name = None
         self.password = None
         self.telecharger = "y"




    def est_premiere_fois(self):
        """ cette fonction permet de vérifier si le programme se lance pour la première fois
        si c'est le cas elle crée un fichier qui contient le mot de passe 
        et le nom de l'utilisateur et les cours qu'il a vus sur moodle"""
        if  not os.path.isfile(login_path):
            self.user_name = input("user_name : ")
            self.password = getpass.getpass("mot de passe : ")
            with open(login_path,"w") as f :
                f.write(self.user_name+"\n")
                f.write(self.password)
                f.close()
            os.system(f"attrib +h {login_path}")
            self.telecharger = input("vous voulez télécharger les anciens cours ? [y/n] : ").lower()
            while(self.telecharger not in {"y" , "n"}):
                self.telecharger = input("veuillez répondre par 'y' ou 'n' s'il vous plaît : ").lower()
        else : 
            with open(login_path,"r") as f :
                self.user_name = f.readline()
                self.password = f.readline()
                f.close()
            if self.dictionnaire_first :
                print("il semble que vous avez supprimé le fichier data.json \n")
                self.telecharger = input("vous voulez télécharger les anciens cours ? [y/n] : ").lower()
                while(self.telecharger not in {"y" , "n"}):
                    self.telecharger = input("veuillez répondre par 'y' ou 'n' s'il vous plaît : ").lower()
            else :
                    json_file = open("data.json","r")
                    self.cours_consultés = json.load(json_file)
                    json_file.close()


    def load_and_login(self , browser):
        self.page = browser.new_page()
        self.page.goto(moodle , timeout=None)
        self.page.locator("#username").fill(self.user_name)   
        self.page.locator("#password").fill(self.password) 
        self.page.locator("#loginbtn").click()



    def type_file(self , file , name):             # savoir si le document pdf s'agit d'un cours, TD ou bien TP
        if td.search(name):
            return "td"
        elif tp.search(name) :
            return "tp"
        return "cours"


    def lien_valide(self , lien):
        to_replace = {"user":"course","1860&course=":"" , "&showallcourses=1":""}
        for clé,valeur in to_replace.items() : 
            lien = re.sub(clé , valeur , lien)
        return lien


    def modules_liens_liste(self):  
        #cette fonction retourne la liste de liens des modules
        self.page.goto(profile)
        modules = self.page.locator('.contentnode li a')
        nombre_modules = modules.count()
        liens_incomplets = [modules.nth(i).get_attribute("href") for i in range(nombre_modules) ]
        return [*map(self.lien_valide, liens_incomplets )]

    def deja_consulté(self , cours, module_name):
        # pour vérifier si un cours est déjâ consulté
        return cours in self.cours_consultés[module_name] 



    def Telecharger_fichier(self,element, name , module_name , link) :          # element désigne un fichier 
        ftype = self.type_file(element , name)
        nom_sb = re.sub(r"\n[a-zA-Z]+|\\*\"*\/*\:*\**\?*\<*\>*\|*","",name)                   # pour supprimer "\nFichier" qui existe à la fin du nom
        # parfois le fichier n'est pas un pdf il peut être une image par exemple
        with self.page.expect_download() as download_info:
            # initialiser le téléchargement
                element.locator("css=.instancename").click()
                # attendre que le téléchargement commence
                download = download_info.value
                # attendre la fin du processus du téléchargement
                path = download.path()
                # sauvegarder le fichier installer
                download.save_as(f"{module_name}/{ftype}/{nom_sb}.pdf")


    def Telecharger_dossier(self , element , name , module_name , link) :
        element.locator("css=.instancename").click()
        nom_sb = nom_sb = re.sub(r"\n[a-zA-Z]+|\\*\"*\/*\:*\**\?*\<*\>*\|*","",name)   # pour supprimer "\nDossier" qui existe à la fin du nom
        download_button = self.page.locator('#region-main input').nth(0)

        if download_button.get_attribute("type") == "hidden" :            # tester si le dossier est vide (y a pas de download button)
                self.page.goto(link)
                return 0
        with self.page.expect_download() as download_info:
        # initialiser le téléchargement
            download_button.click()
            # attendre que le téléchargement commence
            download = download_info.value
            # attendre la fin du processus du téléchargement
            path = download.path()
            # sauvegarder le fichier installer
            download.save_as(f"{module_name}/{nom_sb}.zip")
            self.page.goto(link)




    def elements_liste(self , link):
        self.page.goto(link)
        module_name = self.page.locator("css=h1").inner_text()
        # chercher les fichier
        elements = self.page.locator("css=.modtype_resource , .modtype_folder ")
        n = elements.count()
        if self.dictionnaire_first :
            self.cours_consultés[module_name] = []
        for i in range (n):
            cours_id = elements.nth(i).get_attribute("id")
            est_pdf = elements.nth(i).locator(".activityicon").get_attribute("src")
            if not self.deja_consulté(cours_id , module_name) :
                if self.telecharger=="y" :
                    name = (elements.nth(i)).locator("css=.instancename").inner_text()
                    class_ = elements.nth(i).get_attribute("class")
                    if class_.__contains__("modtype_resource") and est_pdf == pdf :
                        self.Telecharger_fichier(elements.nth(i), name , module_name , link)
                    elif  class_.__contains__("modtype_folder") :                                                      
                        self.Telecharger_dossier(elements.nth(i), name , module_name , link)
                self.cours_consultés[module_name].append(cours_id)
    
    def finir_leprogramme(self):
        json_file = open("data.json","w")
        json.dump(self.cours_consultés , json_file)
        json_file.close()


