import random

linhas = 5
colunas = 10
quantidadeNavios = 5

def criarTabuleiro():
    tabuleiro = []
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            linha.append("~")
        tabuleiro.append(linha)
    return tabuleiro

def mostrarTabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(" ".join(linha))

def posicionarNaviosJogador(tabuleiro):
    navios = 0
    while navios < quantidadeNavios:
        print(f"\nnOnde devemos posicionar o navio {navios + 1} capitão?")
        linha = int(input("Linha: "))
        coluna = int(input("Coluna: "))
        if tabuleiro[linha][coluna] == "N":
            print("Já existe um navio nessa posição!")
        else:
            tabuleiro[linha][coluna] = "N"
            navios += 1

def posicionarNaviosComputador(tabuleiro):
    navios = 0
    while navios < quantidadeNavios:
        linha = random.randint(0, linhas - 1)
        coluna = random.randint(0, colunas - 1)
        if tabuleiro[linha][coluna] != "N":
            tabuleiro[linha][coluna] = "N"
            navios += 1

def ataqueJogador(tabuleiroReal, tabuleiroVisivel):
    linha = int(input("\nLinha do ataque: "))
    coluna = int(input("Coluna do ataque: "))

    if tabuleiroReal[linha][coluna] == "N":
        print("ISSO! ALVO ATINGIDO!!!!")
        tabuleiroVisivel[linha][coluna] = "X"
        tabuleiroReal[linha][coluna] = "X"
        return True
    else:
        print("ERRAMOS O DISPARO!")
        tabuleiroVisivel[linha][coluna] = "O"
        return False

def ataqueComputador(tabuleiroReal, tabuleiroVisivel):
    while True:
        linha = random.randint(0, linhas - 1)
        coluna = random.randint(0, colunas - 1)
        if tabuleiroVisivel[linha][coluna] == "~":
            break
    print(f"\nComputador atacou ({linha},{coluna})")

    if tabuleiroReal[linha][coluna] == "N":
        print("Computador acertou!")
        tabuleiroVisivel[linha][coluna] = "X"
        tabuleiroReal[linha][coluna] = "X"
        return True
    else:
        print("Computador errou!")
        tabuleiroVisivel[linha][coluna] = "O"
        return False

def contarNavios(tabuleiro):
    quantidade = 0
    for linha in tabuleiro:
        for posicao in linha:
            if posicao == "N":
                quantidade += 1
    return quantidade

# PRINCIPAL!!
tabuleiroJogador = criarTabuleiro()
tabuleiroComputador = criarTabuleiro()

feedbackJogador = criarTabuleiro()
feedbackComputador = criarTabuleiro()

print("POSICIONE SEUS NAVIOS")
posicionarNaviosJogador(tabuleiroJogador)
posicionarNaviosComputador(tabuleiroComputador)

while True:
    print("\n========================")
    print("SEU TABULEIRO")
    mostrarTabuleiro(tabuleiroJogador)
    
    print("\nATAQUES NO COMPUTADOR")
    mostrarTabuleiro(feedbackJogador)
    
    print("\nNavios do jogador:", contarNavios(tabuleiroJogador))
    print("Navios do computador:", contarNavios(tabuleiroComputador))

    ataqueJogador(tabuleiroComputador, feedbackJogador)

    if contarNavios(tabuleiroComputador) == 0:
        print("\nTODOS OS INIMIGOS ELIMINADOS. VENCEMOS CAPITÃO!")
        break

    ataqueComputador(tabuleiroJogador, feedbackComputador)

    if contarNavios(tabuleiroJogador) == 0:
        print("\nFOMOS ABATIDOS, O COMPUTADOR VENCEU!")
        break

print("\nCriado cabulosamente por: Matheus Gabiatti; Rafael Rautte e Matheus Mariani!")
