
from selenium import webdriver
from automatisation.methodes import Methodes

m = Methodes()
m.est_premiere_fois()
options = webdriver.FirefoxOptions()
options.headless = True
browser = webdriver.Firefox(options=options)
m.load_and_login(browser)
liens = m.modules_liens_liste()
for lien in liens:
    m.elements_liste(lien)
browser.quit()
m.finir_leprogramme()

