#-*-coding:utf-8 -*-
from math import exp

class Degrau:
	def avaliar(self, x):
		if x >= 0: 
			return 1
		else: 
			return 0
	
	def derivada(self, x):
		pass
		
class Sinal:
	def avaliar(self, x):
		if x > 0:
			return 1
		elif x == 0:
			return 0
		else:
			return -1
	
	def derivada(self, x):
		pass
	

class Sinal2:
	def avaliar(self, x):
		if x >= 0: 
			return 1
		else: 
			return -1
	
	def derivada(self, x):
		return None	
		
class Sinal3:
	pass

#rampa simétrica	
class Simetrica:
	def __init__(self, faixa = 1):
		self.faixa = faixa
	
	def avaliar(self, x):
		if x > self.faixa:
			return self.faixa
		elif x <  -self.faixa:
			return -self.faixa
		else:
			return x
	
	def derivada(self, x):
		pass

#sigmóide
class Logistica:
	def __init__(self, beta=1):
		self.beta = beta
		
	def avaliar(self, x):
		return 1./(1+exp(-self.beta * x))

	def derivada(self, x):
		return exp(-self.beta * x) / (1+exp(-self.beta * x))**2


class Logistica2:
	def avaliar(self, x):	
		return 1./(1+exp(-x))	

	def derivada(self, x):
		x = self.avaliar(x)
		return x*(1-x)		
		
#tangente hiperbólica
class Hiperbolica:
	def __init__(self, beta=1):
		self.beta = beta
		
	def avaliar(self, x):
		return (1-exp(-self.beta * x))/(1+exp(-self.beta * x))

	def derivada(self, x):
		pass

class Gaussiana:
	def __init__(self, media=0, desvio = 0.5):
		self.media = media
		self.desvio = desvio
		
	def avaliar(self, x):
		return exp(-((x-self.media)**2/(2 * self.desvio**2)))

	def derivada(self, x):
		pass

class GaussianaNdimensional:
	def __init__(self, media=[0.0], desvio = 0.5):
		self.media = media
		self.desvio = desvio
		
	def avaliar(self, x):
		return exp(-sum(map(lambda xi,mi: (xi-mi)**2, x, self.media)) / (2 * self.desvio**2))


	def derivada(self, x):
		avaliar = self.avaliar(x)
		return avaliar * (1 - avaliar)


class Linear:
	def avaliar(self, x):
		return x

	def derivada(self, x):
		return 1
