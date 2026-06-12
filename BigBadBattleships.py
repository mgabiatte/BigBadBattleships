import random

linhas = 10
colunas = 10

NAVIOS = [
    ("Porta-aviões", 5),
    ("Navio-tanque", 4),
    ("Contratorpedeiro", 3),
    ("Submarino", 2),
    ("Destroier", 1),
]

cidades = ["Curitiba", "Pindamonhangaba", "Xique-Xique", "Londrina", "Maringá", "Ponta Grossa", "Cascavel", "São José dos Pinhais", "Foz do Iguaçu", "Colombo", "Guarapuava", "Paranaguá", "Araucária", "Toledo", "Apucarana", "Pinhais", "Campo Largo", "Almirante Tamandaré", "Umuarama", "Piraquara", "Francisco Beltrão", "Cambé", "Sarandi", "Fazenda Rio Grande", "Castro", "Paranavaí", "Telêmaco Borba", "Rolândia", "Irati", "Lapa", "Morretes", "Antonina",]

def criarTabuleiro():
    tabuleiro = []
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            linha.append("~")
        tabuleiro.append(linha)
    return tabuleiro

# para nova exibição do mapa, nao estamos mais às cegas =)
def mostrarTabuleiro(tabuleiro):
    print("   " + " ".join(str(c) for c in range(colunas)))
    for idx, linha in enumerate(tabuleiro):
        print(f"{idx} | " + " ".join(linha))

def obterCoordenadaValida(mensagemLinha, mensagemColuna):
    while True:
        try:
            linha = int(input(mensagemLinha))
            coluna = int(input(mensagemColuna))

            if 0 <= linha < linhas and 0 <= coluna < colunas:
                return linha, coluna
            else:
                cidade = random.choice(cidades)
                print(
                    f"⚠️  Coordenadas inválidas, assim vamos atingir {cidade} Senhor! \n-> Digite Linha (0 a {linhas - 1}) e Coluna (0 a {colunas - 1})."
                )
        except ValueError:
            print("⚠️  Por favor, capitão, digite apenas números inteiros!")

def obterDirecaoValida():
    while True:
        direcao = input("Direção (H para horizontal, V para vertical): ").strip().upper()
        if direcao in ("H", "V"):
            return direcao
        print("⚠️  Digite apenas H ou V, Senhor!")

def posicionarNavioJogador(tabuleiro, navioNome, navioTamanho, indice):
    print(f"\n-> Posicione o {navioNome} (tamanho {navioTamanho})")
    while True:
        linha, coluna = obterCoordenadaValida("Linha da proa: ", "Coluna da proa: ")
        direcao = obterDirecaoValida()

        posicoes = []
        valido = True

        for k in range(navioTamanho):
            if direcao == "H":
                l, c = linha, coluna + k
            else:
                l, c = linha + k, coluna

            if not (0 <= l < linhas and 0 <= c < colunas):
                print("⚠️  O navio ultrapassa os limites do mapa, Senhor!")
                valido = False
                break

            if tabuleiro[l][c] != "~":
                print("⚠️  Já existe um navio nessa região, Senhor!")
                valido = False
                break

            posicoes.append((l, c))

        if valido:
            for l, c in posicoes:
                tabuleiro[l][c] = str(indice)
            return posicoes

def posicionarNaviosJogador(tabuleiro):
    print("\n--- SEU MAPA ATUAL ---")
    mostrarTabuleiro(tabuleiro)
    registroNavios = []

    for i, (nome, tamanho) in enumerate(NAVIOS):
        posicoes = posicionarNavioJogador(tabuleiro, nome, tamanho, i)
        registroNavios.append({"nome": nome, "tamanho": tamanho, "posicoes": set(posicoes), "afundado": False})
        # feedback de onde o navio foi posicionado
        print("\n--- SEU MAPA ATUAL ---")
        mostrarTabuleiro(tabuleiro)

    return registroNavios

def posicionarNaviosComputador(tabuleiro):
    registroNavios = []

    for i, (nome, tamanho) in enumerate(NAVIOS):
        while True:
            direcao = random.choice(["H", "V"])
            if direcao == "H":
                linha = random.randint(0, linhas - 1)
                coluna = random.randint(0, colunas - tamanho)
            else:
                linha = random.randint(0, linhas - tamanho)
                coluna = random.randint(0, colunas - 1)

            posicoes = []
            valido = True

            for k in range(tamanho):
                if direcao == "H":
                    l, c = linha, coluna + k
                else:
                    l, c = linha + k, coluna

                if tabuleiro[l][c] != "~":
                    valido = False
                    break

                posicoes.append((l, c))

            if valido:
                for l, c in posicoes:
                    tabuleiro[l][c] = str(i)
                registroNavios.append({"nome": nome, "tamanho": tamanho, "posicoes": set(posicoes), "afundado": False})
                break

    return registroNavios

def verificarAfundamento(linha, coluna, tabuleiroReal, registroNavios, tabuleiroVisivel):
    for navio in registroNavios:
        if (linha, coluna) in navio["posicoes"] and not navio["afundado"]:
            navio["posicoes"].discard((linha, coluna))
            if len(navio["posicoes"]) == 0:
                navio["afundado"] = True
                return navio["nome"]
            return None
    return None

def contarNaviosVivos(registroNavios):
    return sum(1 for n in registroNavios if not n["afundado"])

def ataqueJogador(tabuleiroReal, tabuleiroVisivel, registroNaviosComputador):
    while True:
        print("\n-> Nossa vez de atacar, capitão!")
        linha, coluna = obterCoordenadaValida("Linha do ataque: ", "Coluna do ataque: ")

        # agora bloqueia disparos no mesmo local
        if (
            tabuleiroVisivel[linha][coluna] == "X"
            or tabuleiroVisivel[linha][coluna] == "O"
        ):
            print("⚠️  Já atacamos essa, Senhor! Escolha outra.")
            continue

        if tabuleiroReal[linha][coluna] != "~" and tabuleiroReal[linha][coluna] != "O" and tabuleiroReal[linha][coluna] != "X":
            print("-> ISSO! ALVO ATINGIDO, SENHOR!!!!")
            tabuleiroVisivel[linha][coluna] = "X"
            tabuleiroReal[linha][coluna] = "X"

            afundado = verificarAfundamento(linha, coluna, tabuleiroReal, registroNaviosComputador, tabuleiroVisivel)
            if afundado:
                print(f"⚓ AFUNDAMOS O {afundado.upper()} INIMIGO, CAPITÃO!! ATAQUE NOVAMENTE!")
                return True, True
            return True, False
        else:
            print("MALDIÇÃO!! ERRAMOS O DISPARO!")
            tabuleiroVisivel[linha][coluna] = "O"
            tabuleiroReal[linha][coluna] = "O"
            return False, False

def ataqueComputador(tabuleiroReal, tabuleiroVisivel, registroNaviosJogador):
    while True:
        linha = random.randint(0, linhas - 1)
        coluna = random.randint(0, colunas - 1)
        # computador agora tbm não repete tiros no mesmo lugar, oq tava acontecendo bastante
        if (
            tabuleiroVisivel[linha][coluna] != "X"
            and tabuleiroVisivel[linha][coluna] != "O"
        ):
            break

    print(f"\nComputador atacou ({linha},{coluna})")

    if tabuleiroReal[linha][coluna] != "~" and tabuleiroReal[linha][coluna] != "O" and tabuleiroReal[linha][coluna] != "X":
        print("Droga!!! o Computador nos acertou, senhor!")
        tabuleiroVisivel[linha][coluna] = "X"
        tabuleiroReal[linha][coluna] = "X"

        afundado = verificarAfundamento(linha, coluna, tabuleiroReal, registroNaviosJogador, tabuleiroVisivel)
        if afundado:
            print(f"⚓ O Computador afundou nosso {afundado}!! Resistam!")
        return True
    else:
        print("UFA! o Computador errou!")
        tabuleiroVisivel[linha][coluna] = "O"
        tabuleiroReal[linha][coluna] = "O"
        return False

# ==============================================================================
print("\n" + "#" * 45)
print("           ⚓ BigBadBattleships ⚓          ")
print("     Primeiro jogo AAAA de Batalha Naval      ")
print("#" * 45)

tabuleiroJogador = criarTabuleiro()
tabuleiroComputador = criarTabuleiro()

feedbackJogador = criarTabuleiro()
feedbackComputador = criarTabuleiro()

print("\nPOSICIONE SEUS NAVIOS")
registroNaviosJogador = posicionarNaviosJogador(tabuleiroJogador)
registroNaviosComputador = posicionarNaviosComputador(tabuleiroComputador)

while True:
    print("\n========================")
    print("SEU TABULEIRO")
    mostrarTabuleiro(tabuleiroJogador)

    print("\nATAQUES NO COMPUTADOR")
    mostrarTabuleiro(feedbackJogador)

    print("\nNavios do jogador:", contarNaviosVivos(registroNaviosJogador))
    print("Navios do computador:", contarNaviosVivos(registroNaviosComputador))

    acertou, afundou = ataqueJogador(tabuleiroComputador, feedbackJogador, registroNaviosComputador)
    while afundou:
        if contarNaviosVivos(registroNaviosComputador) == 0:
            break
        acertou, afundou = ataqueJogador(tabuleiroComputador, feedbackJogador, registroNaviosComputador)

    if contarNaviosVivos(registroNaviosComputador) == 0:
        print("\nYES!!! VENCEMOS CAPITÃO!!!")
        break

    ataqueComputador(tabuleiroJogador, feedbackComputador, registroNaviosJogador)

    if contarNaviosVivos(registroNaviosJogador) == 0:
        print("\nNÃO! COMPUTADOR VENCEU E A HUMANIDADE SUCUMBIU!")
        break

print(
    "\nCriado cabulosamente por: Matheus Gabiatti; Rafael Rautte e Matheus Mariani!"
)
print("Obrigado por jogar nosso game!")
