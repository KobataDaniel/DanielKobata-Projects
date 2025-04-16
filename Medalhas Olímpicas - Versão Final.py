from enum import Enum,auto
from dataclasses import dataclass
import sys
sys.setrecursionlimit(10**4) 

class Medalha(Enum):
    OURO = auto()
    PRATA = auto()
    BRONZE = auto()

class Genero(Enum):
    M = auto()
    W = auto()
    X = auto()
    O = auto()

@dataclass
class Quadro:
    MEDALHA:Medalha
    PAIS:str
    GENERO:Genero

@dataclass
class Info:
    COUNTRY:str
    GOLD:int
    SILVER:int
    BRONZE:int
    TOTAL:int

def main():
    if len(sys.argv) < 2:
        print('Nenhum nome de arquivo informado.')
        sys.exit(1)

    if len(sys.argv) > 2:
        print('Muitos parâmetro. Informe apenas um nome de arquivo.')
        sys.exit(1)
    tabela = le_arquivo(sys.argv[1])
    
    matriz_quadro:list[list[Quadro]] = []
    adiciona_quadro(tabela,matriz_quadro)
    resultado = calcula_medalhas(matriz_quadro)
    paises = lista_paises(matriz_quadro)

    print('Quadro de classificação:')
    print(quadro_classificacao(resultado))

    print('Países com medalhistas de um único gênero (M ou W):')
    print(genero_unico(paises,matriz_quadro))

def le_arquivo(nome:str) -> list[list[str]]:
    '''Lê o conteúdo do arquivo *nome* e devolve uma lista onde cada elemento é
    uma lista com os valores das colunas de uma linha (valores separados por
    vírgula). A primeira linha do arquivo, que deve conter o nome das
    colunas, é descartado.

    Por exemplo, se o conteúdo do arquivo for

    tipo,cor,ano
    carro,verde,2010
    moto,branca,1995

    a resposta produzida é
    [['carro', 'verde', '2010'], ['moto', 'branca', '1995']]
    '''
    try:
        with open(nome) as f:
            tabela = []
            linhas = f.readlines()
            for i in range(1, len(linhas)):
                tabela.append(linhas[i].split(','))
            return tabela
    except IOError as e:
        print(f'Erro na leitura do arquivo "{nome}": {e.errno} - {e.strerror}.');
        sys.exit(1)

def adiciona_quadro(tabela:list[list],matriz_quadro:list[list[Quadro]]) -> list:
    '''Localiza as informações de *medalha*, *país* e *gênero* na planilha medals.csv e as adiciona à uma matriz.'''
    for i in tabela:
        if i[0] == 'Gold Medal':
            medalha = Medalha.OURO
        elif i[0] == 'Silver Medal':
            medalha = Medalha.PRATA
        elif i[0] == 'Bronze Medal':
            medalha = Medalha.BRONZE
        
        pais = i[10]
        if len(pais) > 3:
            pais = i[11]
        
        if i[4] == 'M':
            genero = Genero.M
        elif i[4] == 'W':
            genero = Genero.W
        elif i[4] == 'X':
            genero = Genero.X
        elif i[4] == 'O':
            genero = Genero.O

        matriz_quadro.append([Quadro(medalha,pais,genero)])
    return matriz_quadro

def lista_paises(matriz_quadro:list[list[Quadro]]) -> list[str]:
    '''Retorna os nomes de todos os países de *matriz_quadro* sem os repetir.'''
    paises = []
    for i in matriz_quadro:
        for quadro in i:
            if quadro.PAIS not in paises:
                paises.append(quadro.PAIS)
    return paises

def calcula_medalhas(matriz_quadro:list[list[Quadro]]) -> list[Info]:
    '''Retorna cada país com suas respectivas quantidades de medalhas de *ouro*, *prata*, *bronze* e o *total*.'''
    resultado = []
    for pais in lista_paises(matriz_quadro):
        info = Info(pais,0,0,0,0)
        resultado.append(info)
    for linha in matriz_quadro:
        for elem in linha:
            for info in resultado:
                if elem.PAIS == info.COUNTRY:
                    if elem.MEDALHA == Medalha.OURO:
                        info.GOLD += 1
                    elif elem.MEDALHA == Medalha.PRATA:
                        info.SILVER += 1
                    elif elem.MEDALHA == Medalha.BRONZE:
                        info.BRONZE += 1
                    info.TOTAL = info.GOLD + info.SILVER + info.BRONZE
    return resultado

def quadro_classificacao(resultado:list[str]) -> str:
    '''Computa e exibe o quadro de classificação com o número de medalhas de ouro,
    prata, de bronze e o total de medalhas de cada país. A classificação é dada pelo
    maior número de medalhas no total, se houver empate, pelo maior número de medalhas
    de ouro, se houver empate, pelo maior número de medalhas de prata e se houver empate,
    pelo maior número de medalhas de bronze.
    Exemplo:
    >>> quadro_classificacao([Info(COUNTRY='BEL', GOLD=3, SILVER=1, BRONZE=6, TOTAL=10),
    Info(COUNTRY='ITA', GOLD=12, SILVER=13, BRONZE=15, TOTAL=40), Info(COUNTRY='AUS', GOLD=18, SILVER=19, BRONZE=16, TOTAL=53)])
    País Ouro Prata Bronze Total
    AUS    18    19     16    53
    ITA    12    13     15    40
    BEL     3     1      6    10
    '''
    n = len(resultado)
    for i in range(n):
        for j in range(0,n-i-1):
            if ((resultado[j].TOTAL < resultado[j+1].TOTAL) or
                (resultado[j].TOTAL == resultado[j+1].TOTAL and resultado[j].GOLD < resultado[j+1].GOLD) or
                (resultado[j].TOTAL == resultado[j+1].TOTAL and resultado[j].GOLD == resultado[j+1].GOLD and
                 resultado[j].SILVER < resultado[j+1].SILVER) or
                (resultado[j].TOTAL == resultado[j+1].TOTAL and resultado[j].GOLD == resultado[j+1].GOLD and
                 resultado[j].SILVER == resultado[j+1].SILVER and
                 resultado[j].BRONZE < resultado[j+1].BRONZE)):
                resultado[j], resultado[j+1] = resultado[j+1], resultado[j]
    quadro = "País Ouro Prata Bronze Total\n"
    for info in resultado:
        quadro += (f"{info.COUNTRY:4} {info.GOLD:4} {info.SILVER:5} {info.BRONZE:6} {info.TOTAL:5}\n")
    return quadro
    
def genero_unico(paises:list[str],matriz_quadro:list[list[Quadro]]) -> str:
    '''Identifica quais países tiveram atletas de um único gênero, ou seja, somente *M* ou somente *W*, com medalhas.
    Exemplo:
    >>> genero_unico(['GUA', 'QAT', 'CIV'],[[Quadro(MEDALHA=<Medalha.BRONZE: 3>, PAIS='GUA', GENERO=<Genero.M: 1>)],
    [Quadro(MEDALHA=<Medalha.OURO: 1>, PAIS='GUA', GENERO=<Genero.W: 2>)],
    [Quadro(MEDALHA=<Medalha.BRONZE: 3>, PAIS='QAT', GENERO=<Genero.M: 1>)],
    [Quadro(MEDALHA=<Medalha.BRONZE: 3>, PAIS='CIV', GENERO=<Genero.M: 1>)]])
    QAT, CIV
    '''
    def verificar_generos(pais:str,matriz_quadro:list[list[Quadro]],indice_linha:int,generos:list[Genero]):
        '''Confere se o gênero (M ou W) se repete ou não. Os gêneros X e O são ignorados.'''
        if indice_linha >= len(matriz_quadro):
            return generos
        linha = matriz_quadro[indice_linha]
        for quadro in linha:
            if quadro.PAIS == pais and quadro.GENERO in [Genero.M, Genero.W]:
                if quadro.GENERO not in generos:
                    generos.append(quadro.GENERO)
        return verificar_generos(pais,matriz_quadro,indice_linha+1,generos)
    
    def adiciona_pais(paises:list[str],indice:int):
        '''Adiciona o país à lista *resultado* caso tenha somente medalhistas de um gênero.'''
        if indice >= len(paises):
            return []
        pais_atual = paises[indice]
        generos = verificar_generos(pais_atual,matriz_quadro,0,[])
        resultado = []
        if len(generos) == 1:
            resultado = [pais_atual]
        proximo_resultado = adiciona_pais(paises,indice+1)
        return resultado + proximo_resultado

    def formatar_resultado(resultado:list[str],indice:int,formatado:str):
        '''Formata para retornar os resultados separados por vírgula.'''
        if indice >= len(resultado):
            return formatado
        pais = resultado[indice]
        if formatado:
            formatado += ', '
        formatado += pais
        return formatar_resultado(resultado,indice+1,formatado)
    resultado = adiciona_pais(paises,0)
    return formatar_resultado(resultado,0,'')

if __name__ == '__main__':
    main()