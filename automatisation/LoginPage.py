from tkinter import *
from PIL import ImageTk, Image
#from .constantes import *
import requests
from bs4 import BeautifulSoup
import time

class LoginPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1166x718')
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.title('Login Page')

        # ========================================================================
        # ============================background image============================
        # ========================================================================
        self.bg_frame = Image.open('images\\background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        # ====== Login Frame =========================
        self.lgn_frame = Frame(self.window, bg='#040405', width=950, height=600)
        self.lgn_frame.place(x=200, y=70)

        # ========================================================================
        # ========================================================
        # ========================================================================
        self.txt = "Ne consultez pas moodle"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#040405",
                            fg='white',
                            bd=5,
                            relief=FLAT)
        self.heading.place(x=80, y=30, width=500, height=60)

        # ========================================================================
        # ============ Left Side Image ================================================
        # ========================================================================
        self.side_image = Image.open('images\\moodle.png')
        self.side_image = self.side_image.resize((300,300), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=70, y=200)

        # ========================================================================
        # ============ Sign In Image =============================================
        # ========================================================================

        self.sign_in_image = Image.open('images\\hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=130)

        # ========================================================================
        # ============ Sign In label =============================================
        # ========================================================================
        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white",
                                    font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)

        # ========================================================================
        # ============================username====================================
        # ========================================================================
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        # ===== Username icon =========
        self.username_icon = Image.open('images\\username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        # ========================================================================
        # ============================login button================================
        # ========================================================================
        self.lgn_button = Image.open('images\\btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=500)
        self.login = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#f98012', cursor='hand2', activebackground='#f98012', fg='white',command=self.get)
        self.login.place(x=20, y=10)


        # ========================================================================
        # ============================password====================================
        # ========================================================================

        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)

        # ======== Password icon ================
        self.password_icon = Image.open('images\\password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)
        # ========= show/hide password ==================================================================
        self.show_image = ImageTk.PhotoImage \
            (file='images\\show.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='images\\hide.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                activebackground="white"
                                , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

        #======================== drop down Menu =============================
        self.dp_label = Label(self.lgn_frame, text="Télécharger les anciens cours", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.dp_label.place(x=550, y=450)

        OPTIONS = ["y" , "n" ] 
        self.variable = StringVar(self.lgn_frame)
        self.variable.set(OPTIONS[0]) # default value
        self.option_menu = OptionMenu(self.lgn_frame, self.variable, *OPTIONS , )
        self.option_menu.configure(highlightbackground="#040405")
        self.option_menu.place(x=800 , y=455)

        #===================================================================================================
        #============================== la deuxième page ==================================================
        #======================================================================================================

        self.frame2 = Frame(self.window, bg='#040405', width=950, height=600)
        self.label = self.text("Vous vous êtes connecté à Moodle avec succès " , 100 , 100 , "#f98012" , 26 , self.frame2)
        self.label = self.text("laissez le reste à nous  :)" , 300 , 160 , "white" , 25 , self.frame2)
        self.label = self.text("dorénavant tous vos cours seront téléchargés sur votre Desktop \nfermez cette fenêtre, s'il vous plaît" 
                                , 200 , 480 , "white" , 14 , self.frame2)

        
        # l'image du robot
        self.image = Image.open('images\\moobo.png')
        self.image = self.image.resize((250,250), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(self.image)
        self.side_image_label = Label(self.frame2, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=330, y=220)






    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')

    def text(self , text , x , y , couleur , font_size , frame ):
            self.label = Label(frame, text=text,bg='#040405' , fg=couleur,
                                font=("yu gothic ui", font_size, "bold"))
            self.label.place(x=x, y=y)
        #========================== get password and username value=======================================================
    def get(self):
        self.password = self.password_entry.get()
        self.user_name = self.username_entry.get()
        self.telecharger = self.variable.get()
        if self.password=="" or self.user_name=="":
            self.text("donner un nom et un mot de passe correctes" , 550 , 560, "#FF4500" , 12 , self.lgn_frame)
        else : 
            test = self.test_input()
            if test==True :
                self.lgn_frame.place_forget()
                self.frame2.place(x=200, y=70)
            else :
                self.text("donner un nom et un mot de passe correctes" , 550 , 560, "#FF4500" , 12 ,self.lgn_frame )


    # pour tester si le mot de passe et le nom d'utilisateur sont correctes
    def test_input(self):
        with requests.Session() as s :
            response = s.get("http://m.inpt.ac.ma/login/index.php")
            soup0 = BeautifulSoup(response.text , "html.parser")
            logintoken = soup0.find("input", {"name":"logintoken"})["value"]
            ldata = {'username': self.user_name , 'password': self.password , "logintoken" : logintoken}
            r= s.post("http://m.inpt.ac.ma/login/index.php", data=ldata)
            soup1 = BeautifulSoup(r.text , "html.parser")
            erreur = soup1.select("#loginerrormessage")
            return True if erreur==[] else False
    

 
 
            


def tkinter_page():
    window = Tk()
    m = LoginPage(window)
    window.mainloop()
    return m



