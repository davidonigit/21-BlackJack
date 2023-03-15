import random

class Carta:
    def __init__(self, naipe, figura):
        self.naipe = naipe
        self.figura = figura
        
    def __str__(self):
        return f"{self.figura['figura']} de {self.naipe}"

class Deck:
    def __init__(self):
        self.cartas = []
        naipes = ["Paus", "Ouros", "Copas", "Espadas"]
        figuras = [ 
            {"figura": "A", "valor": 11},
            {"figura": "2", "valor": 2},
            {"figura": "3", "valor": 3},
            {"figura": "4", "valor": 4},
            {"figura": "5", "valor": 5},
            {"figura": "6", "valor": 6},
            {"figura": "7", "valor": 7},
            {"figura": "8", "valor": 8},
            {"figura": "9", "valor": 9},
            {"figura": "10", "valor": 10},
            {"figura": "J", "valor": 10},
            {"figura": "Q", "valor": 10},
            {"figura": "K", "valor": 10},
            ]
        
        for naipe in naipes:
            for figura in figuras:
                self.cartas.append(Carta(naipe, figura))
    
    def embaralhar(self):
        if len(self.cartas) > 1:
            random.shuffle(self.cartas)
    
    def puxar_cartas(self, numero):
        cartas_puxadas = []
        for n in range(numero):
            if len(self.cartas) > 0:
                carta = self.cartas.pop()
                cartas_puxadas.append(carta)
        return cartas_puxadas

class Mao:
    def __init__(self, dealer=False):
        self.cartas = []
        self.valor = 0
        self.dealer = dealer

    def add_carta(self, lista_cartas):
        self.cartas.extend(lista_cartas)

    def calcular_mao(self):
        self.valor = 0
        possui_as = False
        
        for carta in self.cartas:
            valor_carta = int(carta.figura["valor"])
            self.valor += valor_carta
            if carta.figura["figura"] == "A":
                possui_as = True

        if possui_as and self.valor > 21:
            self.valor -= 10

    def get_valor(self):
        self.calcular_mao()
        return self.valor

    def is_blackjack(self):
        return self.get_valor == 21

    def display(self, mostrar_cartas_dealer=False):
        if self.dealer:
            print("Mão do Dealer: ")
        else:
            print("Sua mão: ")

        for index, carta in enumerate(self.cartas):
            if index == 0 and self.dealer \
            and not mostrar_cartas_dealer and not self.is_blackjack():
                print("escondido")
            else:
                print(carta)

        if not self.dealer:
            print("Valor:", self.get_valor())
        print()

class Jogo:
    def play(self):
        numero_jogo = 0
        jogos_restantes = 0

        while jogos_restantes <= 0:
            try:
                jogos_restantes = int(input("Quantos jogos voce quer jogar? "))
            except:
                print("É preciso digitar um numero")

        while numero_jogo < jogos_restantes:
            numero_jogo += 1

            deck = Deck()
            deck.embaralhar()

            mao_jogador = Mao()
            mao_dealer = Mao(dealer=True)

            for i in range(2):
                mao_jogador.add_carta(deck.puxar_cartas(1))
                mao_dealer.add_carta(deck.puxar_cartas(1))

            print()
            print("*"*30)
            print(f"Jogo numero {numero_jogo} de {jogos_restantes}")
            print("*"*30)
            mao_jogador.display()
            mao_dealer.display()

            if self.testa_vencedor(mao_jogador, mao_dealer):
                continue

            escolha = ""
            while mao_jogador.get_valor() < 21 and escolha not in ["m", "manter"]:
                escolha = input("Escolha entre 'Puxar' ou 'Manter': ").lower()
                print()
                while escolha not in ["p", "m", "puxar", "manter"]:
                    escolha = input("Escolha 'Puxar' ou 'Manter' (ou P/M): ").lower()
                    print()
                if escolha in ["p", "puxar"]:
                    mao_jogador.add_carta(deck.puxar_cartas(1))
                    mao_jogador.display()
                    
            if self.testa_vencedor(mao_jogador, mao_dealer):
                continue

            mao_jogador_valor = mao_jogador.get_valor()
            mao_dealer_valor = mao_dealer.get_valor()

            while mao_dealer_valor < 17:
                mao_dealer.add_carta(deck.puxar_cartas(1))
                mao_dealer_valor = mao_dealer.get_valor()

            mao_dealer.display(mostrar_cartas_dealer=True)

            if self.testa_vencedor(mao_jogador, mao_dealer):
                continue

            print("Resultados Finais: ")
            print("Sua mão:", mao_jogador_valor)
            print("Mão Dealer:", mao_dealer_valor)
            print()
            
            self.testa_vencedor(mao_jogador, mao_dealer, True)

        print("\nObrigado por jogar!")
        
    def testa_vencedor(self, mao_jogador, mao_dealer, game_over=False):
        if not game_over:
            if mao_jogador.get_valor() > 21:
                print("Você estourou. Vitória do Dealer!")
                return True
            elif mao_dealer.get_valor() > 21:
                print("Dealer estourou. Você venceu!")
                return True
            elif mao_jogador.get_valor() == mao_dealer.get_valor() == 21:
                print("BlackJack duplo. Empate!")
                return True
            elif mao_jogador.is_blackjack():
                print("BlackJack! Você venceu!")
                return True
            elif mao_dealer.is_blackjack():
                print("BlackJack! Vitória do Dealer!")
                return True
        else:
            if mao_jogador.get_valor() > mao_dealer.get_valor():
                print("Você venceu!")
            elif mao_jogador.get_valor() == mao_dealer.get_valor():
                print("Empate!")
            else:
                print("Dealer venceu!")
            return True
        return False
jogo = Jogo()
jogo.play()
