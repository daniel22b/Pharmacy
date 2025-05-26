## Example 1 - modules in python
## See example in calculator folder
########################################
## Example 2 - datatime module
# from datetime import date
# print(date.today())
###########################################
## Zapis/odczyt danych typ słownik do pliku
## Example 3 - load .csv file as dictionary
# import csv
# with open('customer.csv', mode='r') as csv_file:
#     csv_reader = csv.DictReader(csv_file)     # each line as dict
#     for row in csv_reader:
#         print(row)

## more option, see info: https://docs.python.org/3/library/csv.html


################# Project 1
## Twoim zadaniem jest utworzenie pakietu obsługi
## nowych i aktualnych klientów nowo-utworzonej apteki
## oraz jej dostępnych zasobów tj. leków 
## Administratorem jest osoba, która świetnie zna pythona
## Klienci dostaja tzw. kartę stałego klienta (ID konta)
###############################################
############    Zasoby:
## Pakiet Pharmacy powinien zawierać 3 pliki zawierające następujące dane:
## drugs.xlsx - dane leków
## address.csv - baza adresów aktualnych uzytkowników
## customer.csv - dane osobowe aktualnych uzytkowników
## folder DATABASE
################################################
############  Specyfikacja oprogramowania:
## Utwórz następujące moduły:
## 1. Moduł main - główny moduł, który administruje zasobami apteki online
## musi zawierać:  def __main__() (uruchamia program)
## 2. Moduł obsługi dodawania/usuwania nowych obiektów do bazy zawierający 2 funkcje:
## funkcja 1: dodanie nowego leku do bazy (book.csv)
## funkcja 2: usuwanie leków z bazy opcje: wględem ID lub nazwy (drugs.xlsx)
##
## 3. Moduł obsługi klienta zawierający funkcje tj.:
## 1: rejestracja nowego klienta lub usuwanie danych klienta z bazy tj.
## dodawanie/usuwanie (przez administratora) danych
## nowego/bieżącego klienta do/z bazy tj. do/z pliku customer.csv i address.csv
## Nowy klient podaje swoje dane (imie, nazwisko), nadawany jest w/w klientowi losowy numer ID złożony z 4 cyfr
## ponadto po rejestracji w folderze DATABASE tworzony jest plik tekstowy (nazwa pliku to ID klienta)
## do którego będą zapisywane dane zakupionego przez klienta e-booka oraz
## data zakupu a potem wygaśnięcia dostepu do e-booka
## Usuwanie danych klienta opcje: względem ID lub NAME
## Zakup leków przez użytkownika zawiera funkcje: zakup leku przez klienta (z nr recepty lub bez numeru)
##
## Jeśli skończyłeś zadanie, przyjmij rolę programisty
## który dostał zadanie aktualizacji utworzonego pakietu
## Nie modyfikując i nie zmieniając nazw funkcji "udekoruj" funkcje
## dodając nowe funkcjonalnosci: 
# np. funkcja: "zakup leku przez klienta" i nadpisz jej zawartość
## tak aby klient miał możliwość zakupu dowolnej liczby leków równocześnie (bez recepty)

## WYMAGANIA:
## - +możesz programować wyłącznie w paradygmacie funkcyjnym
## - utwórz funkcję wyższego rzędu
## - utwórz funkcję wielu zmiennych wejściowych
## - +utwórz funkcję zagnieżdzoną
## - użyj dekoratora
## - wykonaj dokumentację dla conajmniej 3 funkcji i 2 modułów
## - conajmniej dla 3 funkcji wykonaj obsługę wyjątków
## - +wykonaj interfejs graficzny dla użytkownika  
## - +pakiet powinien być udostępniony w repozytorium github

## WSKAZANIA:
## - możesz zwiększyć liczbę modułów
## - dla zapisu/odczytu daty oraz danych do bazy wykorzystaj odpowiednie pakiety
## - dla lepszej kontroli zasobów ksiegarnii możesz dodadać moduł monitorowania liczby danych
## tj. liczba użytkowniów, średnia/max/min liczba kupionych leków, liczba dostępnych leków
## - możesz dodawać inne funkcjonalności do utworzonego pakietu tak aby twój pakiet był 
## konkurencyjnym produktem na rynku
## jest to sklep online logowanie uzytkownika mile widziane 
## możesz dodawać inne niezbędne kolumny do baz danych (plików csv, xlsx)


################# Project 2
## Twoim zadaniem jest utworzenie pakietu obsługi
## nowych i aktualnych klientów nowo-utworzonego sklepu online żabka
## oraz jej dostępnych zasobów tj. produktów spożywczych 
## Administratorem jest osoba, która świetnie zna pythona
## Klienci dostaja tzw. kartę stałego klienta (ID konta)
###############################################
############    Zasoby:
## Pakiet Frog powinien zawierać 3 pliki zawierające następujące dane:
## products.xlsx - dane produktów spożywczych
## customer.csv - dane osobowe aktualnych klientów sklepu posiadających jego kartę stałego klienta
## folder DATABASE
################################################
############  Specyfikacja oprogramowania:
## Utwórz następujące moduły:
## 1. Moduł main - główny moduł, który administruje zasobami sklepu online
## musi zawierać:  def __main__() (uruchamia program)
## 2. Moduł obsługi dodawania/usuwania nowych obiektów do bazy zawierający 2 funkcje:
## funkcja 1: dodanie nowego produktu do bazy (products.xlsx)
## funkcja 2: usuwanie produktów z bazy opcje: wględem ID lub nazwy (products.csv)
##
## 3. Moduł obsługi klienta zawierający funkcje tj.:
## 1: rejestracja nowego klienta lub usuwanie danych klienta z bazy tj.
## dodawanie/usuwanie (przez administratora) danych
## nowego/bieżącego klienta do/z bazy tj. do/z pliku customer.csv i address.csv
## Nowy klient podaje swoje dane (imie, nazwisko), nadawany jest w/w klientowi losowy numer ID złożony z 4 cyfr
## ponadto po rejestracji w folderze DATABASE tworzony jest plik tekstowy (nazwa pliku to ID klienta)
## do którego będą zapisywane dane zakupionych przez klienta produktu/ów (rodzaj i ilość)
## Usuwanie danych klienta opcje: względem ID lub NAME
## Zakup produktów przez użytkownika zawiera funkcje: zakup produktu przez klienta
##
## Jeśli skończyłeś zadanie, przyjmij rolę programisty
## który dostał zadanie aktualizacji utworzonego pakietu
## Nie modyfikując i nie zmieniając nazw funkcji "udekoruj" funkcje
## dodając nowe funkcjonalnosci: 
# np. funkcja: "zakup produktu przez klienta" i nadpisz jej zawartość
## tak aby klient miał możliwość zakupu dowolnej liczby produktów równocześnie

## WYMAGANIA:
## - możesz programować wyłącznie w paradygmacie funkcyjnym
## - utwórz funkcję wyższego rzędu
## - utwórz funkcję wielu zmiennych wejściowych
## - utwórz funkcję zagnieżdzoną
## - użyj dekoratora
## - wykonaj dokumentację dla conajmniej 3 funkcji i 2 modułów
## - conajmniej dla 3 funkcji wykonaj obsługę wyjątków
## - wykonaj interfejs graficzny dla użytkownika  
## - pakiet powinien być udostępniony w repozytorium github

## WSKAZANIA:
## - możesz zwiększyć liczbę modułów
## - dla zapisu/odczytu daty oraz danych do bazy wykorzystaj odpowiednie pakiety
## - dla lepszej kontroli zasobów ksiegarnii możesz dodadać moduł monitorowania liczby danych
## tj. liczba użytkowniów, średnia/max/min liczba kupionych leków, liczba dostępnych leków
## - możesz dodawać inne funkcjonalności do utworzonego pakietu tak aby twój pakiet był 
## konkurencyjnym produktem na rynku
## jest to sklep online logowanie uzytkownika mile widziane 
## możesz dodawać inne niezbędne kolumny do baz danych (plików csv, xlsx)


################# Project 3
## Twoim zadaniem jest utworzenie pakietu obsługi
## nowych i aktualnych klientów nowo-utworzonej księgarni internetowej
## oraz jej dostępnych zasobów tj. ebook-ow. 
## Administratorem jest osoba, która świetnie zna pythona
## Klienci dostaja tzw. kartę stałego klienta (ID konta)
###############################################
############    Zasoby:
## Pakiet Bookstore powinien zawierać 3 pliki zawierające następujące dane:
## book.csv - dane ebook-ow
## address.csv - baza adresów aktualnych uzytkowników
## customer.csv - dane osobowe aktualnych uzytkowników
## folder DATABASE
################################################
############  Specyfikacja oprogramowania:
## Utwórz następujące moduły:
## 1. Moduł main - główny moduł, który administruje zasobami księgarni online
## musi zawierać:  def __main__() (uruchamia program)
## 2. Moduł obsługi dodawania/usuwania nowych obiektów do bazy zawierający 2 funkcje:
## funkcja 1: dodanie nowej książki do bazy (book.csv)
## funkcja 2: usuwanie książki do bazy opcje: wględem ID lub tytułu (book.csv)
##
## 3. Moduł obsługi klienta zawierający funkcje tj.:
## 1: rejestracja nowego klienta lub usuwanie danych klienta z bazy tj.
## dodawanie/usuwanie (przez administratora) danych
## nowego/bieżącego klienta do/z bazy tj. do/z pliku customer.csv i address.csv
## Nowy klient podaje swoje dane (imie, nazwisko), nadawany jest w/w klientowi losowy numer ID złożony z 4 cyfr
## ponadto po rejestracji w folderze DATABASE tworzony jest plik tekstowy (nazwa pliku to ID klienta)
## do którego będą zapisywane dane zakupionego przez klienta e-booka oraz
## data zakupu a potem wygaśnięcia dostepu do e-booka
## Usuwanie danych klienta opcje: względem ID lub NAME
## Zakup książki przez użytkownika zawiera funkcje: zakup książki książek przez klienta
##
## Jeśli skończyłeś zadanie, przyjmij rolę programisty
## który dostał zadanie aktualizacji utworzonego pakietu
## Nie modyfikując i nie zmieniając nazw funkcji "udekoruj" funkcje
## dodając nowe funkcjonalnosci: 
# np. funkcja: "zakup książki przez klienta" i nadpisz jej zawartość
## tak aby klient miał możliwość zakupu dowolnej liczby książek

## WYMAGANIA:
## - możesz programować wyłącznie w paradygmacie funkcyjnym
## - utwórz funkcję wyższego rzędu
## - utwórz funkcję wielu zmiennych wejściowych
## - utwórz funkcję zagnieżdzoną
## - użyj dekoratora
## - wykonaj dokumentację dla conajmniej 3 funkcji i 2 modułów
## - conajmniej dla 3 funkcji wykonaj obsługę wyjątków
## - wykonaj interfejs graficzny dla użytkownika  
## - pakiet powinien być udostępniony w repozytorium github

## WSKAZANIA:
## - możesz zwiększyć liczbę modułów
## - dla zapisu/odczytu daty oraz danych do bazy wykorzystaj odpowiednie pakiety
## - dla lepszej kontroli zasobów ksiegarnii możesz dodadać moduł monitorowania liczby danych
## tj. liczba użytkowniów, średnia/max/min liczba kupionych ebooków, liczba dostępnych ebooków
## - możesz dodawać inne funkcjonalności do utworzonego pakietu tak aby twój pakiet był 
## konkurencyjnym produktem na rynku 
## jest to sklep online logowanie uzytkownika mile widziane 
## możesz dodawać inne niezbędne kolumny do baz danych (plików csv, xlsx)
