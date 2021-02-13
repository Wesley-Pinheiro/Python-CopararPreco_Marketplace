#13.02.2021
#Guia em: https://youtu.be/-iH32asPT84

#BIBLIOTECAS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv 

iLISTADEPTO = ['carnes-aves-e-peixes','hortifruti']
iREDESUPER = ['big-washington-luis','carrefour-brooklin']
iLISTACATEGORIA = []
iITENSREDE= []

class NowPrecoBot:
	def __init__(self):
		self.bot = webdriver.Firefox(executable_path = 'C:/Program Files (x86)/Mozilla Maintenance Service/geckodriver.exe')

	def CapturaNow(self,iNOMEREDE):
		iCONTAITENS = 0

		#Navega até a pagina da rede
		bot = self.bot
		bot.get('https://supermercadonow.com/produtos/' + str(iNOMEREDE) + '/setores/')	
		time.sleep(2)
		iREDE = str(bot.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[1]/div[4]/div/div[1]/div/span").text)
		print("Iniciando rede: " + iREDE)

		# Acessar os departamentos da lista iLISTADEPTO
		for iNOMEDEPTO in iLISTADEPTO:
			iLISTACATEGORIA.clear()
			print("Iniciando departamento: " + iNOMEDEPTO)
			try:
				bot.get('https://supermercadonow.com/produtos/' + str(iNOMEREDE) + '/setores/' + str(iNOMEDEPTO) + '/')	

				#Percorer as categorias - guardar as urls das categorias (variaveis)
				iCONTCATEGORIA = 1
				while True:
					try:
						iURL_CATEGORIA = str(bot.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/ul/li[" + str(iCONTCATEGORIA) + "]/a").get_attribute('href'))
						iNOME_CATEGORIA = str(bot.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/ul/li[" + str(iCONTCATEGORIA) + "]/a/span").text)
						iLISTACATEGORIA.append((iURL_CATEGORIA,iNOME_CATEGORIA))
						iCONTCATEGORIA += 1
					except:
						break

				for iURL_COMPLETA_CATEGORIA in iLISTACATEGORIA:
					iSEQUENCIA_ITM = 1
					try:
						print("Iniciando categoria: " + str(iURL_COMPLETA_CATEGORIA[1]))
						bot.get(iURL_COMPLETA_CATEGORIA[0])
						time.sleep(2)

						while True:
							try:
								iDESCRICAO_PROD = str(bot.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div/div[" + str(iSEQUENCIA_ITM) + "]/div[6]/div/div/span").text)
								iPRECO1_PROD = str(bot.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div/div[" + str(iSEQUENCIA_ITM) + "]/div[2]/div/div[1]/span").text)
								iPRECO2_PROD = "0"
								iPRECO2_PROD =  str(bot.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div/div[" + str(iSEQUENCIA_ITM) + "]/div[2]/div/div[2]/span").text)
								if str(iPRECO2_PROD[0:2] != "R$"):
									iPRECO2_PROD = "0"
								iPRECO1_PROD = iPRECO1_PROD.replace("R$","").replace(" ","")
								iPRECO2_PROD = iPRECO2_PROD.replace("R$","").replace(" ","")

								iITENSREDE.append((iREDE,iNOMEDEPTO,iURL_COMPLETA_CATEGORIA[1],iDESCRICAO_PROD,iPRECO1_PROD,iPRECO2_PROD))

								iSEQUENCIA_ITM += 1
								
							except:
								break


					except:
						pass

			except:
				pass

			



Now = NowPrecoBot()
time.sleep(1)

for rede in iREDESUPER:
	print("iniciando lista de redes : " + str(rede))
	Now.CapturaNow(rede)

print("Finalizou lista de redes")

#criar o arquivo CSV com os resultados
with open('C:/Users/pinheiro/Google Drive/Projetos Python/Modelos/Temporarios/out.csv', "w", newline="") as f:
	writer = csv.writer(f)
	writer.writerows(iITENSREDE)

