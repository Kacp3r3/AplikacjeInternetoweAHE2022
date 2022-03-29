# Aplikacje internetowe AHE 2022
## Spis treści
1. Opis programu
2. Struktura
3. Instrukcja uruchomienia
4. "Notatki"
5. Wymagania na zaliczenie
6. Żródła i przydatne linki
   
## 1. Program
Aplikacja internetowa napisana we flasku(backend) oraz Bootstrapie(frontend)
, rozwijana wraz z upływem semestru.  
Pomysłem na aplikacje jest wyświetlanie temperatury i wilgotności w poszczególnych salach budynku.   
W zależności od uprawnień każdy użytkownik ma możliwość podglądu warunków w pomieszczeniach.  
Dostępy przyznaje administrator aplikacji za pomocą odpowiedniego panelu.

## 2. Struktura projektu
* app.py - Głowny skrypt do uruchamiania serwisu
* make_db.py - Generator bazy danych
* requirements.txt - Zależności pythona wymagane do uruchomienia
* [ ] env - Folder z wirtualnym środowiskiem pythona do utworzenia samemu
* [ ] condition_monitor - Folder ze skryptami projektu
  * forms.py - Definicje formularzy (np. logowania)
  * models.py - Definicje tabel w bazie danych
  * routes.py - Definicje podstron serwisu
  * \_\_init\_\_.py - Definicja paczki pythonowej
  * [ ] templates - Folder z Szablonami html podstron
    * base.html
    * home.html
    * ...

## 3. Instrukcja
### Wymagane oprogramowanie
1. Python
2. Visual Studio Code
3. Wtyczki pythonowe do VSC (Python i Pylance)
   
### Windows
1. Otwarcie projektu w VSC

2. Otwarcie terminala  
   Z paska w górnym lewym rogu: `Terminal -> New terminal`

3. Utworzenie wirtualnego środowiska python o nazwie env:
   > `python -m venv env`
4. Aktywacja środowiska w PowerShellu *
   > `. ./env/Scripts/activate.ps1`  

    \* Jeżeli się nie uda, należy zmienić `execution-policy` w PS komendą: 
    > `set-executionpolicy RemoteSigned`
5. Instalacja zależności
   > `pip install -r requirements.txt`

6. Wybranie env jako domyślnego środowiska uruchomieniowego  
   Ctrl+Shift+P, następnie wpisać lub wyszukać opcję "Select interpreter" i wskazać ścieżkę do python'a - /env/Scripts/python.exe

7. Uruchamianie  
   Otwarcie pliku app.py a następnie kliknięcie przycisku "play" w prawym górnym rogu.  
   lub poleceniem
   > `python app.py`

## 4. "Notatki"
### Podstawowe zagadnienia  
`app = Flask(\_\_name\_\_)` - Utworzenie instancji aplikacji flask'owej o nazwie jak skrypt startowy.  
`app.config["SQLALCHEMY_DATABASE_URI"] = "link"` - Konfiguracja linku do bazy danych  
`app.config["SECRET_KEY"] = "losowy ciąg znaków"` - Klucz uzywany do szyfrowania bez niego nie zadziała m.in. logowanie   
`db = SQLAlchemy(app)` - Instancja bazy danych  
`bcypt = Bcrypt(app)` - Narzędzie do szyfrowania np. haseł  

### Tworzenie formularzy we Flasku
```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

#Dziedziczymy z FlaskForm
class NazwaFormularza(FlaskForm):
   #nazwa pola = typPola(etykieta, validatory=[])
   pole = StringField(label="Tekst nad Polem", validators=[Length(min=2, max = 15)]) 
   pole2 = PasswordField(label = "Password", validators=[Length(min=8),DataRequired()])
   #Przycisk do zatwierdzenia formularza
   submit = SubmitField(label = "Create Account")
```

### Modele w bazie danych
```python
from flask_sqlalchemy import SQLAlchemy
#Dziedziczymy z db.Model ( db = SQLAlchemy(app) )
class NazwaTabeliWBazie(db.Model):
    #Nazwe mozna jeszcze zmienić
    __tablename__ = "Nadpisana_nazwa"
    #Klucz podstawowy 
    id = db.Column(db.Integer, primary_key = True)
    #pole = db.Column(typ_pola (Float, Boolean, Datetime... ), opcje(unique, nullable, ondelete, default...))
    pole1 = db.Column(db.String(10), unique=True, nullable=False)
    pole2 = db.Column(db.Integer())
```
### Definicja podstron
```python
flask import redirect, render_template, url_for, flash
app = Flask(__name__)

#Strona domowa
@app.route("/")
@app.route("/home")
def home_page():
   info = { "example" : "dictonary" }
   return render_template("home.html", doPrzekazania = info)

#Podstrona z parametrem jako częśc linku
@app.route("/item/<id>")
def items_page(id):
   info = { "Parametr" : id }
   return render_template(url_for("items_page")), doPrzekazania = info)

#Przykładowa strona logowania
@app.route("/login")
def login_page():
   if current_user.authenticated:
      flash("Jestes juz zalogowany jako { current_user.username }", category="info")
      return render_template(url_for("home_page"))
   
   #Utworzenie formularza
   form = LoginForm()
   if form.validate_on_submit():
         #Dodanei uzytkownika do bazy
         return render_template(url_for("main_page"))
   
   #Jezeli sa jakies błedy, wyświetl je
   if form.errors != {}:
        for error in form.errors.values():
            flash(f'There was an error with creating a user: {error}', category='danger')

   return render_template("home.html", form = form)

@app.route("/logout")
@login_required() #Tylko zalogowany uzytkownik moze wejsc na te podstrone
def items_page(id):
   return render_template("home.html")
```
### Szablony z podstronami
W folderze `templates` umieszczamy pliki html z kodami podstron

Składnia `Jinja` do wstrzykiwania kodu w `HTML`
```Jinja
!! Spacje pomiędzy %} a poleceniami są istotne !!
{% for i in range(10) %} - Blok instrukcji (for/while/if/with/block)
{% endfor %} - Zakończenie bloku instrukcji (endfor/endwhile/endif/endwith/endblock)
{{ nazwa_zmiennej }} - pobranie zawartości zmiennej
{% extens nazwa.html %} - Deklaracja rozszerzenia jakiegoś szablonu (patrz home.html -> base.html)
{% block nazwa_bloku %} - Zaznaczenie, że w tym miejscu szablon rozszerzający może umieścić własny kod
{% endblock %} - zakończenie block
```

## 5. Wymagania na zaliczenie
Projekt aplikacji posiadającej:
- Rejestracje/Logowanie/Wylogowywanie
- Konta użytkowników z różnymi prawami (np. Admin/Moderator/User/Guest)
- Zarządzanie przez Admina pozostałymi użytkownikami/zasobami
  (np. Admin przyznajde dostęp innym użytkownikom dostęp do podglądania wyników pomiarów temperatury z danej sali)
- Responsywny interfejs napisany w Bootstrap'ie
- ... TBA

Ilość osób w grupie: 2-3  
Sposób przedstawiania: Krótka prezentacja  
Termin: 14 Czerwca 2022 stacjonarnie  


## 6. Przydatne linki i źródła
[Strona flaska](https://flask.palletsprojects.com/en/2.0.x/)  
[Przykładowe mini projekty we flasku](https://python101.readthedocs.io/pl/latest/webflask/)  
[Strona bootstrapa](https://getbootstrap.com/)  
[Przykłady w Bootstrapie](https://www.w3schools.com/bootstrap/bootstrap_examples.asp)  
[Kurs flaska (6h youtube)](https://www.youtube.com/watch?v=Qr4QMBUPxWo&t=1793s)  
[Kurs bootstrap (3h youtube)](https://www.youtube.com/watch?v=-qfEOE4vtxE)