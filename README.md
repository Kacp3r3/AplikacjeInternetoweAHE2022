# Aplikacje internetowe AHE 2022
## Spis treści
1. Opis programu
2. Struktura
3. Instrukcja uruchomienia
4. Żródła i przydatne linki
   
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

6. Uruchamianie  
   Otwarcie pliku app.py a następnie kliknięcie przycisku "play" w prawym górnym rogu.  
   lub poleceniem
   > `python app.py`

## 4. Przydatne linki i źródła
[Strona flaska](https://flask.palletsprojects.com/en/2.0.x/)  
[Przykładowe mini projekty we flasku](https://python101.readthedocs.io/pl/latest/webflask/)  
[Strona bootstrapa](https://getbootstrap.com/)  
[Przykłady w Bootstrapie](https://www.w3schools.com/bootstrap/bootstrap_examples.asp)  
[Kurs flaska (6h youtube)](https://www.youtube.com/watch?v=Qr4QMBUPxWo&t=1793s)  
[Kurs bootstrap (3h youtube)](https://www.youtube.com/watch?v=-qfEOE4vtxE)