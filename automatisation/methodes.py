import re
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from winotify import Notification, audio
from .LoginPage import tkinter_page
from .constantes import *

class Methodes:
    def __init__(self):
        self.First = False
        self.page = None
        self.user_name = None
        self.password = None
        self.telecharger = "y"
        self.cours_consultes = {}
        self.toast = Notification(
            app_id="Moodle",
            title="Attention",
            msg="Un cours a été ajouté sur Moodle",
            duration="long",
            icon=r"C:\Users\ayoub\Desktop\moodle-automate\automatisation\Mobile-M-Icon-1-corners.png"
        )
        self.toast.set_audio(audio.Mail, loop=False)

    def est_premiere_fois(self):
        if not os.path.isfile(login_path):
            tkinter_page0 = tkinter_page()
            self.user_name, self.password = tkinter_page0.user_name, tkinter_page0.password
            self.telecharger = tkinter_page0.telecharger
            with open(login_path, "w") as f:
                f.write(f"{self.user_name}\n{self.password}")
                os.system(f"attrib +h {login_path}")
                self.First = True
        else:
            with open(login_path, "r") as f:
                self.user_name, self.password = f.readline().strip(), f.readline().strip()
                if self.dictionnaire_first:
                    print("Il semble que vous ayez supprimé le fichier data.json.\n")
                    self.telecharger = input("Voulez-vous télécharger les anciens cours ? [y/n] : ").lower()
                    while self.telecharger not in {"y", "n"}:
                        self.telecharger = input("Veuillez répondre par 'y' ou 'n' s'il vous plaît : ").lower()
                else:
                    with open("data.json", "r") as json_file:
                        self.cours_consultes = json.load(json_file)

    def load_and_login(self, browser):
        self.page = browser.new_page()
        self.page.goto(moodle, timeout=None)
        self.page.locator("#username").fill(self.user_name)
        self.page.locator("#password").fill(self.password)
        self.page.locator("#loginbtn").click()

    def type_file(self, name):
        if td.search(name):
            return "td"
        elif tp.search(name):
            return "tp"
        return "cours"

    def lien_valide(self, lien):
        to_replace = {"user": "course", "1860&course=": "", "&showallcourses=1": ""}
        for cle, valeur in to_replace.items():
            lien = re.sub(cle, valeur, lien)
        return lien

    def modules_liens_liste(self):
        self.page.goto(profile)
        modules = self.page.locator('.contentnode li a')
        return [self.lien_valide(module.get_attribute("href")) for module in modules]

    def deja_consulte(self, cours, module_name):
        return cours in self.cours_consultes.get(module_name, [])

    def telecharger_fichier(self, element, name, module_name):
        ftype = self.type_file(name)
        nom_sb = re.sub(r"\n[a-zA-Z]+|\\*\"*\/*\:*\**\?*\<*\>*\|*", "", name)  # Remove unnecessary characters
        element.locator("css=.instancename").click()
        download_button = self.page.wait_for_selector('#region-main input[type="hidden"]', timeout=5)
        if not download_button:
            self.page.goto(self.page.url)
            return
        download_button.click()
        with self.page.expect_download() as download_info:
            download = download_info.value
            path = download.path()
            download.save_as(f"{homedir}\\Desktop\\Moodle\\{module_name}\\{ftype}\\{nom_sb}.pdf")
            if not self.First:
                self.toast.add_actions(label="Appuyez ici", launch=f"{homedir}\\Desktop\\Moodle\\{module_name}\\{ftype}\\{nom_sb}.pdf")
                self.toast.show()

    def telecharger_dossier(self, element, name, module_name):
        element.locator("css=.instancename").click()
        download_button = self.page.wait_for_selector('#region-main input[type="hidden"]', timeout=5)
        if not download_button:
            self.page.goto(self.page.url)
            return
        download_button.click()
        nom_sb = re.sub(r"\n[a-zA-Z]+|\\*\"*\/*\:*\**\?*\<*\>*\|*", "", name)  # Remove unnecessary characters
        with self.page.expect_download() as download_info:
            download = download_info.value
            path = download.path()
            download.save_as(f"{homedir}\\Desktop\\Moodle\\{module_name}\\{nom_sb}.zip")
            if not self.First:
                self.toast.add_actions(label="Appuyez ici", launch=f"{homedir}\\Desktop\\Moodle\\{module_name}\\{nom_sb}.zip")
                self.toast.show()

    def elements_liste(self, link):
        self.page.goto(link)
        module_name = self.page.locator("css=h1").inner_text()
        elements = self.page.locator("css=.modtype_resource , .modtype_folder ")
        for element in elements:
            cours_id = element.get_attribute("id")
            est_pdf = element.locator(".activityicon").get_attribute("src")
            if not self.deja_consulte(cours_id, module_name):
                if self.telecharger == "y":
                    name = element.locator("css=.instancename").inner_text()
                    if "modtype_resource" in element.get_attribute("class") and est_pdf == pdf:
                        self.telecharger_fichier(element, name, module_name)
                    elif "modtype_folder" in element.get_attribute("class"):
                        self.telecharger_dossier(element, name, module_name)
                self.cours_consultes.setdefault(module_name, []).append(cours_id)

    def finir_leprogramme(self):
        with open("data.json", "w") as json_file:
            json.dump(self.cours_consultes, json_file)
