'''
RODRIGO ROSA

Raspagem de dados em uma pagina que tem elementos(BOTÕES) de java script com os modulos:
Selenium
request
beatifulsoap
pandas DATAFRAME

OBJETIVO: COMPARAR O ANO DE 2018 COM O DE 2017 E VER QUAL O ANO QUE AS LICITAÇÕES FICARAM
MAIS CARAS, OU SEJA, O ANO QUE A PREFEITURA DE SJC GASTOU MAIS COM LICITAÇÕES

'''

#Importa pandas para converter lista em dataframe
import pandas as pd
pd.set_option('display.max_rows', 1500)
pd.set_option('display.max_columns', 1500)
pd.set_option('display.width', 1500)

# modulo time foi utilizado para esperar o carregamento das paginas atraves do firefox
import time
 
# o modulo webdriver e necessario para definir qual navegador sera utilizado para fazer a automacao
from selenium import webdriver
 
# o modulo select sera utilizado para interagir com selecionar o botão "consultar"
from selenium.webdriver.support.ui import Select
 
# esse modulo sera utilizado para trabalhar os dados que pegarmos
from bs4 import BeautifulSoup
 
# a linha abaixo define qual e o navegador que queremos utilizar
driver = webdriver.Firefox()
 
# abaixo foi definido o site que vai ser feita a raspagem
driver.get("http://servicos2.sjc.sp.gov.br/servicos/portal_da_transparencia/contratos.aspx")
 
# o Sleep abaixo e para aguardar o carregamento da pagina
time.sleep(5)
 
# Aqui estou buscando o elemento que possui na classe o valor botao
consultar_btn = driver.find_element_by_class_name("botao")
 
# aqui e feito um clique no elemento que foi encontrado acima
consultar_btn.click()
 
# aguardando o carregamento da pagina
time.sleep(5)

#armazena um codigo em HTML que da acesso a tabela de dados
dados = driver.find_element_by_class_name("fonte_grid_transparencia")

#aqui e pegado o codigo HTML que esta dentro da classe "fonte_grid_transparencia"
#que é a tabela onde temos os contratos das LICITAÇÕES
html = dados.get_attribute("innerHTML")

# usando o beautifulsoap para fazer a analise desse codigo html
# dentro da variavel soup temos o tabela das licitações retornado pelo selenium ja analisado pelo beatifulsoap
soup = BeautifulSoup(html, "html.parser")

#----------------------------------------Processamento dos dados recolhidos 2018

contratos = soup.find_all("tr")#pegando todas as colunas e criando uma lista de colunas

itens_limpos = []#lista de itens limpos vazia

lista_contratos = []#lista que contera cada contrato (lista de itens limpos (contrato,numero_ano,fornecedor,CPF/CNPJ,valor e licitação))

for i in range(1,len(contratos)-1,1): #começo,fim,passo
    '''print(contratos[i])
    print("\n")'''

    linha=(contratos[i].find_all("td"))#pegando todas as linhas e criando uma lista de linhas

    for item_sujo in linha:#limpando os dados brutos
        item_sujo = (item_sujo.next_element).get_text()#remove aquelas tags feias
        #item_sujo = item_sujo.get_text()#remove aquelas tags feias
        itens_limpos.append(item_sujo)#criando uma lista de itens limpos

    for i in range(0,len(itens_limpos)-1): #Adicionando Numero/Ano dos contratos a lista de itens limpos
        if(itens_limpos[i]=='' and itens_limpos[i-1]=='CONTRATO'):
            itens_limpos[i]=(str(307-len(itens_limpos)))+'/2018'
        if (itens_limpos[i]==''):#limpando espaços q o slstrip n limpou
            del itens_limpos[i]

#print(itens_limpos)

#----------------------------Separando cada contrato((contrato,numero_ano,fornecedor,CPF/CNPJ,valor e licitação)) em uma lista
while(itens_limpos):
    lista_contratos.append(itens_limpos[0:6])
    del itens_limpos[0:6] 
#print(lista_contratos)

'''for cont in lista_contratos:#exibindo cada contrato dentro de lista de contratos
    for linha in cont:
        print(linha)
    print('\n')'''


print('------------------------------------ 2018 ------------------------------------')

df = pd.DataFrame(lista_contratos, columns=['Tipo','TíNúmero/Ano','Fornecedor','CPF/CNPJ','Valor (R$)','Licitação'])
print(df)

#Fechar navegador
driver.quit()

#-------------calculando o total de licitações de 2018
Total_2018=0
for linha in df['Valor (R$)']:
    linha = linha.replace(',','')
    linha = linha.replace('.','')
    Total_2018 = Total_2018 + int(linha)
    
print('Custo Total com licitações em 2018 R$:',Total_2018)

print('\n')
print('------------------------------------ 2017 ------------------------------------')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  2017  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#Importa pandas para converter lista em dataframe
import pandas as pd_2017
pd_2017.set_option('display.max_rows', 1500)
pd_2017.set_option('display.max_columns', 1500)
pd_2017.set_option('display.width', 1500)

# modulo time foi utilizado para esperar o carregamento das paginas atraves do firefox
import time
 
# o modulo webdriver e necessario para definir qual navegador sera utilizado para fazer a automacao
from selenium import webdriver
 
# o modulo select sera utilizado para interagir com selecionar o botão "consultar"
from selenium.webdriver.support.ui import Select
 
# esse modulo sera utilizado para trabalhar os dados que pegarmos
from bs4 import BeautifulSoup
 
# a linha abaixo define qual e o navegador que queremos utilizar
driver = webdriver.Firefox()
 
# abaixo foi definido o site que vai ser feita a raspagem
driver.get("http://servicos2.sjc.sp.gov.br/servicos/portal_da_transparencia/contratos.aspx")
 
# o Sleep abaixo e para aguardar o carregamento da pagina
time.sleep(5)
 
# Interagindo com o combo box (procurando o elemento '2017')
select = Select(driver.find_element_by_name("ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$modelo_master_meio$modelo_uma_coluna_meio$ctl02$Transp_Contratos_v2_6$cmbAno"))

# Alterando o valor do ComboBox
select.select_by_value("2017")

# Buscando o elemento que possui na classe o valor botao
consultar_btn = driver.find_element_by_class_name("botao")
 
# É feito um clique no elemento que foi encontrado acima
consultar_btn.click()
 
# aguardando o carregamento da pagina
time.sleep(5)

#armazena um codigo em HTML que da acesso a tabela de dados
dados = driver.find_element_by_class_name("fonte_grid_transparencia")

#aqui e pegado o codigo HTML que esta dentro da classe "fonte_grid_transparencia"
#que é a tabela onde temos os contratos das LICITAÇÕES
html = dados.get_attribute("innerHTML")

# usando o beautifulsoap para fazer a analise desse codigo html
# dentro da variavel soup temos o tabela das licitações retornado pelo selenium ja analisado pelo beatifulsoap
soup = BeautifulSoup(html, "html.parser")

#----------------------------------------Processamento dos dados recolhidos 2017

contratos_2017 = soup.find_all("tr")#pegando todas as colunas e criando uma lista de colunas

itens_limpos = []#lista de itens limpos vazia

lista_contratos = []#lista que contera cada contrato (lista de itens limpos (contrato,numero_ano,fornecedor,CPF/CNPJ,valor e licitação))

for i in range(1,len(contratos_2017)-1,1): #começo,fim,passo
    '''print(contratos[i])
    print("\n")'''

    linha=(contratos_2017[i].find_all("td"))#pegando todas as linhas e criando uma lista de linhas

    for item_sujo in linha:#limpando os dados brutos
        item_sujo = item_sujo.next_element#remove aquelas tags feias
        item_sujo = item_sujo.lstrip()#remove aquelas tags feias
        itens_limpos .append(item_sujo)#criando uma lista de itens limpos

    for i in range(0,len(itens_limpos)-1): #Adicionando Numero/Ano dos contratos a lista de itens limpos
        if(itens_limpos[i]=='' and itens_limpos[i-1]=='CONTRATO'):
            itens_limpos[i]=(str(307-len(itens_limpos)))+'/2017'
        if (itens_limpos[i]==''):#limpando espaços q o slstrip n limpou
            del itens_limpos[i]

#----------------------------Separando cada contrato((contrato,numero_ano,fornecedor,CPF/CNPJ,valor e licitação)) em uma lista
while(itens_limpos):
    lista_contratos.append(itens_limpos[0:6])
    del itens_limpos[0:6] 

df_2017 = pd_2017.DataFrame(lista_contratos, columns=['Tipo','TíNúmero/Ano','Fornecedor','CPF/CNPJ','Valor (R$)','Licitação'])
print(df_2017)

#Fechar navegador
driver.quit()

Total_2017=0
for linha in df_2017['Valor (R$)']:
    linha = linha.replace(',','')
    linha = linha.replace('.','')
    Total_2017 = Total_2017 + int(linha)
    
print('Custo Total com licitações em 2017 R$:',Total_2017)
print('\n')

if Total_2017 > Total_2018:
    print('A PMSJC gastou mais no ano de 2017 com licitações que no ano de 2018...\nAté o presente momento...')
else:
    print('A PMSJC gastou mais no ano de 2018 com licitações que no ano de 2017...\nAté o presente momento...')
    



















