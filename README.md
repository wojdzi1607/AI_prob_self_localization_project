# lokalizacja

Uznałem, że robot będzie zachowywał się jak osoba z mapą wrzucona do labiryntu.
Czyli będzie analizował otaczające go ściany i zakładał czy był na początku skierowany
na N, E, S czy W.

Agent ma vector kierunków który na początku wynosi [N, E, S, W], agent sam oblicza w którą stronę
się obraca, w zależności od wykonywanych akcji.

Dla każdej "zakładanej" orientacji początkowej obliczane jest prawdopodobieństwo lokalizacji.

To pradwopodobieństwo sumuje się co krok wyłaniając po paru iteracjach prawidłową lokację.

Teraz najważniejsze:
Założyłem że agent naprawdę jest tylko w jednej możliwej konfiguracji orientacji. Czyli na początku
był skierowany tylko w jedną stronę, dlatego najwyższe prawdopodobieństwo jest przypisywane do
odpowiedniej orientacji zależnie od obliczonej orientacji.

CZYLI np: po 5 krokach agent uznał że na początku był skierowany na [S] i prawdopodobieństwo
lokalizacji robota wpisuje w np. lewą kropkę bo obliczył że po 5 krokach będzie skierowany na [W].

Przyznaję że na eps_move = 0 działa idealnie, ale jak jest >0 to przy errorze potrzeba mu pare
iteracji żeby z powtorem ogarnął gdzie jest.

# heurestyka

Agent tworzy mapę odwiedzonych miejsc korzystając z obliczanej orientacji zawsze zakładając
że jest skierowany na [N]. Mapa jest 31x31, zaczyna od punktu (15, 15), używa oczywiście percept.
Kiedy ma tylko jedną możliwość ruchu to ją wybiera. Kiedy więcej to wybiera to miejsce gdzie jeszcze
nie był. Kiedy cofa się i ma do wyboru dwa miejsca w których już był to wybiera losowo.