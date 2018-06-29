# CROMOSSOMO É A SOLUÇÃO  E O INDIVIDUO POSSUI O CROMOSSOMO
# CROSSOVER (cruzamento) É FAZER A JUNÇÃO DE DOIS CROMOSSOMOS, OU SEJA, MISTURAR DUAS SOLUÇÕES
# CADA ELEMENTO DO CROMOSSOMO É CHAMADO DE GENES
# NA SELEÇÃO DOS INDIVIDUOS SERÁ UTILIZADO O MÉTODO DA ROLETA VICIADA (Porcentagem correspondente 
# com a nota de cada individuo, sendo assim, os individuos com maior nota terão uma maior prababilidade
# de serem selecionando do que os outros)

# Importe para sortear números alet
from random import random
# Importe para geração de gráficos no Python
import matplotlib.pyplot as plt
# Importe para fazer a conexão com o banco de dados MySql
import pymysql

class Produto():
    
    # Inializando a classe de produtos
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor
        
class Individuo():
    
    # Inializando a classe de individuos
    def __init__(self, espacos, valores, limite_espacos, geracao=0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos
        # Soma de todos os valores da carga
        self.nota_avaliacao = 0
        self.espaco_usado = 0
        self.geracao = geracao
        self.cromossomo = []
        
        # ************** REVISAR **************
        # Inicializando os cromossomos
        for i in range(len(espacos)):
            if random() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")
                
    # Avaliando o cromossomo (solução)
    def avaliacao(self):
        nota = 0
        soma_espacos = 0
        for i in range(len(self.cromossomo)):
           if self.cromossomo[i] == '1':
               nota += self.valores[i]
               soma_espacos += self.espacos[i]
        if soma_espacos > self.limite_espacos:
            nota = 1
        self.nota_avaliacao = nota
        self.espaco_usado = soma_espacos
        
    # Fazer o cruzamento de cromossomos
    def crossover(self, outro_individuo):
        corte = round(random() * len(self.cromossomo))
        
        # Criando um filho com a mistura de dois cromossomos
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        
        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
                  Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1)]
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos
    
    # Altera aletoriamente os genes de um cromossomo
    def mutacao(self, taxa_mutacao):
        #print("Antes %s " % self.cromossomo)
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                elif self.cromossomo[i] == '0':
                    self.cromossomo[i] = '1'
        #print("Depois", self.cromossomo)
        return self
        
class AlgoritmoGenetico():
    
    # Construtor dos algoritmos genéticos
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        # Armazenar o individuo com a maior nota
        self.melhor_solucao = 0
        # Lista dos melhores individuos
        self.lista_solucoes = []
        
    # Inicializar a populacao de individuos de acordo com o tamanho da população
    def inicializa_populacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(espacos, valores, limite_espacos))
        # Inicializar a melhor solução com o primeiro individuo da população
        self.melhor_solucao = self.populacao[0]
        
    # Ordena a população pela nota
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)
        
    # Método para comparar dois individuos e verificar qual possui a maior nota
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
            
    # Soma total de todas as notas dos individuos de uma população
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
           soma += individuo.nota_avaliacao
        return soma
    
    # Fazer a da roleta viciada e retornar um individuo
    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai
    
    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("G:%s -> Valor: %s Espaço: %s Cromossomo: %s" % (self.populacao[0].geracao,
                                                               melhor.nota_avaliacao,
                                                               melhor.espaco_usado,
                                                               melhor.cromossomo))
    
    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        self.inicializa_populacao(espacos, valores, limite_espacos)
        
        for individuo in self.populacao:
            individuo.avaliacao()
        
        self.ordena_populacao() 
        self.melhor_solucao = self.populacao[0]
        # Adicionar nas melhores soluções
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
        
        self.visualiza_geracao()
        
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            # Fazer uma nova geração e adicionar na população
            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                
                # Adicionar os novos filhos para a nova população
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
            
            self.populacao = list(nova_populacao)
            
            for individuo in self.populacao:
                individuo.avaliacao()
            
            self.ordena_populacao()
            
            self.visualiza_geracao()
            
            # Como os individuos foram ordenados, a posicao [0] tem a maior nota
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao)
            self.melhor_individuo(melhor)
        
        print("\nMelhor solução -> G: %s Valor: %s Espaço: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao,
               self.melhor_solucao.nota_avaliacao,
               self.melhor_solucao.espaco_usado,
               self.melhor_solucao.cromossomo))
        
        return self.melhor_solucao.cromossomo
        
        
# Inicializando a classe principal
if __name__ == '__main__':
    # Criando a lista de produtos
    lista_produtos = []
    # Fazendo a conexao com o banco de dados
    conexao = pymysql.connect(host='localhost', user='root', passwd='*compostosmoleculares*', db='produtos')
    query = conexao.cursor()
    
    # Executando uma query para o banco de dados
    query.execute('select nome, espaco, valor, quantidade from produtos')
    
    # Percorrendo todos os produtos do banco de dados
    for produto in query:
        # Adicionanando o mesmo produto de acordo com a quantidade
        for i in range(produto[3]):
            lista_produtos.append(Produto(produto[0], produto[1], produto[2]))
    # Fechando a query banco de dados
    query.close()
    # Fechando a conexao com o banco de dados
    conexao.close()
    
    # CRIAÇÃO DE PRODUTOS DIRETAMENTE NO CÓDIGO
    '''lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
    lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
    lista_produtos.append(Produto("TV 55' ", 0.400, 4346.99))
    lista_produtos.append(Produto("TV 50' ", 0.290, 3999.90))
    lista_produtos.append(Produto("TV 42' ", 0.200, 2999.00))
    lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
    lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
    lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
    lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
    lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
    lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
    lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
    lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
    lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))'''
    
    # Criando listas de espacos, valores e nomes dos produtos
    espacos = []
    valores = []
    nomes = []
    
    # Passando a lista de produtos para as listas separadas
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
    
    # Limite de metros cúbicos que posso levar
    limite = 10
    tamanho_populacao = 20
    # 1% de probabilidade de trocar algum gene
    taxa_mutacao = 0.01
    numero_geracoes = 1000
    ag = AlgoritmoGenetico(tamanho_populacao)
    
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)
    
    # Mostrando todos os produtos que serão levados
    for i in range(len(lista_produtos)):
        if resultado[i] == '1':
            print("Nome: %s R$ %s " % (lista_produtos[i].nome,
                                       lista_produtos[i].valor))
            
    #for valor in ag.lista_solucoes:
    #    print(valor)
    
    # Valores do gráfico
    plt.plot(ag.lista_solucoes)
    # Título do gráfico
    plt.title("Acompanhamento dos valores")
    # Mostrar o gráfico
    plt.show() 
    
    