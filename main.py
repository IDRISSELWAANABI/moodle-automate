
from playwright.sync_api import sync_playwright
from automatisation.methodes import Methodes

m = Methodes()
m.est_premiere_fois()
with sync_playwright() as playwright:
    browser = playwright.firefox.launch(headless=False)
    # initialiser la page et se connecte au profile sur moodle 
    m.load_and_login(browser)
    # obtenir le lien de chaque module
    liens = m.modules_liens_liste() 
    for lien in liens :
        # obtenir la liste des éléments du module correspondant au lien choisi
        # et télécharger ceux qui viennent d'être ajoutés
        m.elements_liste(lien)
    browser.close()
m.finir_leprogramme()
