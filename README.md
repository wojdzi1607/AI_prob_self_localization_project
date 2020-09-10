# Działanie sensora
Prawdopodobieństwo lokalizacji jest obliczane dla 4 kierunków orientacji niezależnie.

Macierz T zbudowana jest z 4 podmacierzy, dla których obliczana jest wartość czynnika przejść.
Odpowiednia dla kierunków [N, E, S, W]. Po wykonaniu akcji forward istnieje 0.95 szansy, że robot
się przesunie i 0.05, że zostanie w miejscu. Dla akcji obrotu istnieje 1 szansy, że zostanie w miejscu.

Macierz O zbudowana jest z 4 podmacierzy, dla których obliczana jest wartość czynnika sensora.
Odpowiednia dla kierunków [N, E, S, W]. Dla każdej lokacji porównuje odczyt z sensora z sąsiadującymi
komórkami i oblicza wartość prob. Wszystko wykonywane jest 4 razy dla 4 kierunków odpowiednio "tłumacząc"
odczyt sensora percept ['fwd', 'bckwd', 'left', 'right'] na percept_tmp [N, E, S, W].

Na końcu 4 podmacierze T i 4 podmacierze O są ze sobą odpowiednio mnożone. Wynik wpisywany jest
do łącznego rozkładu prawdopodobieństwa self.P

Przy rozpocząciu nowego kroku, jeżeli poprzednią akcją był obrót, odpowiednio zamienia
podmacierze self.P między sobą, uwzględniając eps.move (np. po turnleft P[0] będzie na 5% P[0],
a na 95% P[1])

Sensor "nie rozjeżdża" się w czasie. Poniżej zdjęcie działania dla n=500
![alt text](https://github.com/wojdzi1607/Projekt_SI/blob/master/500n.png?raw=true)

# Uwzględnienie bump
Jeżeli wystąpiło bump, tj. robot uderzył w ścianę naprzeciwko to:

W obliczaniu macierzy T wartość czynnika przejść w aktualnej lokacji = 1. (tak samo jak przy obrocie).

W obliczaniu macierzy O:
- prawdopodobieństwo, że naprzeciwko robota jest ściana, jest równa 1 ('fwd' w sensorze jest poprawny
na 1, a nie 0.95 szansy)
- prawdopodobieństwo, że robot jest w lokacji, w której skierowany jest tak, że naprzeciwko nie
ma ściany wynosi 0

PS. na początku wywołania funkcji ustawiana jest flaga 'bump', a w sensorze [bump] zmieniane jest
na [fwd], lub [fwd] jest dopisywane, jeżeli sensor błędnie nie wykrył [fwd].
 
# Heurestyka

- kiedy sensor wykryje ścianę naprzeciwko, skręci w lewo lub prawo (70%:30%)
- kiedy sensor nie wykryje ściany naprzeciwko i z lewej (wybór pomiędzy fwd a lewo),
poruszy się fwd lub skręci w lewo (20%:80%)
- kiedy sensor nie wykryje ściany naprzeciwko i z prawej (wybór pomiędzy fwd a prawo),
poruszy się fwd lub skręci w prawo (20%:80%)
- w przeciwnym wypadku preferuje poruszanie się naprzód (80%)