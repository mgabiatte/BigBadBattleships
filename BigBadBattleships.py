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
                print(
                    f"Coordenadas inválidas! Digite Linha (0 a {linhas - 1}) e Coluna (0 a {colunas - 1})."
                )
        except ValueError:
            print("Por favor, capitão, digite apenas números inteiros!")

def posicionarNaviosJogador(tabuleiro):
    navios = 0
    print("\n--- SEU MAPA ATUAL ---")
    mostrarTabuleiro(tabuleiro)
    
    while navios < quantidadeNavios:
        print(f"\nOnde devemos posicionar o navio {navios + 1} capitão?")
        linha, coluna = obterCoordenadaValida("Linha: ", "Coluna: ")
        
        if tabuleiro[linha][coluna] == "N":
            print("Já existe um navio nessa posição!")
        else:
            tabuleiro[linha][coluna] = "N"
            navios += 1
            # feedback de onde o navio foi posicionado
            print("\n--- SEU MAPA ATUAL ---")
            mostrarTabuleiro(tabuleiro)

def posicionarNaviosComputador(tabuleiro):
    navios = 0
    while navios < quantidadeNavios:
        linha = random.randint(0, linhas - 1)
        coluna = random.randint(0, colunas - 1)
        if tabuleiro[linha][coluna] != "N":
            tabuleiro[linha][coluna] = "N"
            navios += 1

def ataqueJogador(tabuleiroReal, tabuleiroVisivel):
    while True:
        print("\nSua vez de atacar, capitão!")
        linha, coluna = obterCoordenadaValida(
            "Linha do ataque: ", "Coluna do ataque: "
        )
        # agora bloqueia disparos no mesmo local
        if (
            tabuleiroVisivel[linha][coluna] == "X"
            or tabuleiroVisivel[linha][coluna] == "O"
        ):
            print("Você já atacou essa coordenada! Escolha outro alvo.")
            continue

        if tabuleiroReal[linha][coluna] == "N":
            print("BOA! ALVO ATINGIDO!!!!")
            tabuleiroVisivel[linha][coluna] = "X"
            tabuleiroReal[linha][coluna] = "X"
            return True
        else:
            print("ERRAMOS O DISPARO!")
            tabuleiroVisivel[linha][coluna] = "O"
            tabuleiroReal[linha][coluna] = "O"
            return False

def ataqueComputador(tabuleiroReal, tabuleiroVisivel):
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

    if tabuleiroReal[linha][coluna] == "N":
        print("Computador acertou!")
        tabuleiroVisivel[linha][coluna] = "X"
        tabuleiroReal[linha][coluna] = "X"
        return True
    else:
        print("Computador errou!")
        tabuleiroVisivel[linha][coluna] = "O"
        tabuleiroReal[linha][coluna] = "O"
        return False

def contarNavios(tabuleiro):
    quantidade = 0
    for linha in tabuleiro:
        for posicao in linha:
            if posicao == "N":
                quantidade += 1
    return quantidade
# ==============================================================================
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
        print("\nVENCEMOS CAPITÃO!")
        break

    ataqueComputador(tabuleiroJogador, feedbackComputador)

    if contarNavios(tabuleiroJogador) == 0:
        print("\nCOMPUTADOR VENCEU!")
        break

print(
    "\nCriado cabulosamente por: Matheus Gabiatti; Rafael Rautte e Matheus Mariani!"
)
print("Obrigado por jogar nosso game!")

