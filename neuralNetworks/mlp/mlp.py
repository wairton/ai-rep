#-*-coding:utf-8 -*-

from funcoes import *
from random import random, shuffle

class Neuronio:
	def __init__(self, nentries, weights, limiar, factivation):
		if weights  is None:
			self.weights = [random() for x in range(nentries)]
		else:
			self.weights = weights
		self.limiar = limiar
		self.activation = factivation()
		self.soma = 0
		self.output = 0.0
		self.derivada = 0.0
		
	def evaluate(self, entrada):
		self.soma = sum(map(lambda p, e: p*e, self.weights, entrada))
		self.output = self.activation.evaluate(self.soma - self.limiar)
		self.derivada = self.activation.derivada(self.soma - self.limiar)
		return self.output

	def updateWeights(self, delta):
		self.weights = map(lambda p,d: p+d, self.weights, delta)

	def desenha(self):
		print len(self.weights)
		print self.weights
		print

class Camada:
	def __init__(self, nNeuronios, nentries, funcao, entrada=False):
		self.neuronios = []
		self.thetas = None
		weights = None
		self.output = None
		self.entrada = entrada
		if entrada== True:
			weights = [1.0]

		for n in range(nNeuronios):
			self.neuronios.append(Neuronio(nentries, weights, 0, funcao))

	def evaluate(self, amostra):
		if self.entrada == False: 
			self.output = [neuronio.evaluate(amostra) for neuronio in self.neuronios]
		else:
			self.output = amostra
		return self.output

	def desenha(self):
		for neuronio in self.neuronios:
			neuronio.desenha()
			print

	def atualizarErro(self, desejado):
		self.erro = map(lambda s,d: s-d, self.output, desejado)	#o erro não deveria ficar dentro do neurônio?
		self.funcaoErro = sum(map(lambda e: e**2, self.erro))/2.0
		return self.funcaoErro

	def obterweights(self, indice):
		return [neuronio.weights[indice] for neuronio in self.neuronios]

	def updateWeights(self, outputAnterior, aprendizagem):
		for indice in range(len(self.neuronios)):
			delta = map(lambda s: - aprendizagem * s * self.thetas[indice], outputAnterior)
			self.neuronios[indice].updateWeights(delta)
		
	def getSoma(self):
		return [n.soma for n in self.neuronios]

	#self.output
	def getCalculado(self):
		return [n.calculado for n in self.neuronios]
		

class Mlp:
	def __init__(self, arquitetura, funcao, aprendizagem):
		self.aprendizagem = aprendizagem
		self.arquitetura = arquitetura
		self.camadas = []
		self.camadas.append(Camada(arquitetura[0], 1, Linear,True))

		for n, camada in enumerate( arquitetura[1:-1]):
			self.camadas.append(Camada(camada, arquitetura[n], funcao))

		self.camadas.append(Camada(arquitetura[-1], arquitetura[-2], funcao))

	def desenha(self):
		for camada in self.camadas:
			camada.desenha()
			print

	def evaluate(self, amostra):
		output = self.camadas[0].evaluate(amostra)
		for camada in self.camadas[1:]:
			output = camada.evaluate(output)
		return output		

	def treinar(self, amostras, desejados, epocas):	
		for epoca in range(epocas):
			print 'época:', epoca + 1
			erro = 0.0
			for i in range(len(amostras)):
				erro += self.feedForward(amostras[i], desejados[i])
				self.backPropagate()
			print 'erro atual:', erro
				

	def backPropagate(self):
		camadaAtual = len(self.camadas) - 1
		#backpropagando na última camada
		aux = []		
		for i, neuronio in enumerate(self.camadas[camadaAtual].neuronios):
			aux.append(neuronio.derivada * self.camadas[camadaAtual].erro[i])
		self.camadas[camadaAtual].thetas = aux
		
		camadaAtual -= 1
		#backpropagando camadas intermediárias
		while (camadaAtual > 0):
			aux = []
			thetas = self.camadas[camadaAtual+1].thetas#thetas da camada a frente
			for i, neuronio in enumerate(self.camadas[camadaAtual].neuronios):
				weights = self.camadas[camadaAtual+1].obterweights(i)
				aux.append(neuronio.derivada * sum(map(lambda p, t: p*t, weights, thetas)))						
			self.camadas[camadaAtual].thetas =  aux
			camadaAtual -= 1

		#atualizando weights
		camadaAtual  = len(self.camadas) - 1
		while (camadaAtual > 0):
			self.camadas[camadaAtual].updateWeights(self.camadas[camadaAtual-1].output, self.aprendizagem)
			camadaAtual -= 1
				
	def feedForward(self, amostra, desejado):
		output = self.camadas[0].evaluate(amostra)
		for camada in self.camadas[1:]:
			output = camada.evaluate(output)
		erro = self.camadas[-1].atualizarErro(desejado)
		return erro

	def teste(self, amostras, desejados, epocas):
		print 'inicio do teste'
		self.treinar(amostras, desejados, epocas)
		for amostra in amostras:
			print self.evaluate(amostra)

	def teste2(self, amostrasTreino, desejadosTreino, amostrasTeste, desejadosTeste, epocas):
		print 'inicio do teste'
		retornoTreino = []
		retornoTeste = []
		for epoca in range(epocas):
			erroTreino = 0.0
			erroTeste = 0.0
			for i in range(len(amostrasTreino)):
				erroTreino += self.feedForward(amostrasTreino[i], desejadosTreino[i])
				self.backPropagate()
			for i in range(len(amostrasTeste)):
				erroTeste += self.feedForward(amostrasTeste[i], desejadosTeste[i])
			retornoTreino.append(erroTreino)
			retornoTeste.append(erroTeste)
			print epoca+1,':',erroTreino, erroTeste
		for amostra in amostrasTreino:
			print self.evaluate(amostra)
		print '-' * 80
		for amostra in amostrasTeste:
			print self.evaluate(amostra)

		self.grafico(epocas, retornoTreino, retornoTeste)

	def grafico (self, epocas, retornoTreino, retornoTeste):
		try: 
			import matplotlib.pyplot as plotter
			plotter.plot(range(epocas), retornoTreino, range(epocas), retornoTeste)
			aux1, aux2 = max(retornoTreino), max(retornoTeste)
			print aux1, aux2
			maximo = 0
			if aux1>aux2:
				maximo = aux1
			else:
				maximo = aux2

			aux1, aux2 = min(retornoTreino), min(retornoTeste)
			minimo = 0
			print minimo, maximo
			if aux1<aux2:
				minimo = aux1
			else:
				minimo = aux2
			#plotter.axis = ([0, epocas, minimo-1.0, 50])
			plotter.grid(True)
			plotter.ylabel('erro')
			plotter.xlabel('epocas')
			plotter.show()
		except ImportError:
			print 'matplotlib não instalado!'

if __name__ == '__main__':
	arquivo = open('wine.txt', 'r')
	linhas = arquivo.readlines()
	arquivo.close()
	amostras = []
	desejados = []
	shuffle(linhas)
	for linha in linhas:
		aux = [float(i) for i in linha.split()]
		amostras.append(aux[:-3])
		desejados.append(aux[-3:])
	
	rede = Mlp((13,8,4,3), Logistica2, 0.2)
	rede.desenha()
#	rede.teste(amostras, desejados, 1000)
	rede.teste2(amostras[:50], desejados[:50], amostras[50:], desejados[50:], 2000)

