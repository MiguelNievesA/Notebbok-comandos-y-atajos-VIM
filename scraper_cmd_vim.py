###################
#     MODULES     #
###################
from lxml import html
import requests as rq
from random_user_agent.user_agent import UserAgent
import nbformat as nbf
import json

#####################
#   MAIN PROGRAM    #
#####################

#Variables necesarias
result = [] #Lista que contendra todos los diccionaros de la informacion

nb = nbf.v4.new_notebook() #Notebook jupyter donde agregaremos los datos

#CONFIG
agent = UserAgent()
head = {"user-agent": agent.get_random_user_agent()}

#Obtenemos el contenido html del sitio web
url = "https://geekland.eu/atajos-de-teclado-y-comandos-para-usar-vim-eficientemente/"
response = rq.get(url, headers=head).content

#Parseamos el arbol y usamos xpath para obtener los elementos
parse = html.fromstring(response)

#ELEMENTOS
titles = parse.xpath("//article[@id='post-13175']//h2/text()")
tables = parse.xpath("//article[@id='post-13175']//figure/table")

print("Procesando comandos y atajos Vim...")
for t in tables:

	#Obtenemos los columnas de la tabla
	content = t.xpath("./tbody//tr")

	#Obtenemos rows de la tabla de la pagina
	rows = t.xpath("./thead//th/text()")
	
	#Creamos el diccionario donde guardaremos la informacion
	dict_table = {rows[0]:[], rows[1]:[]}

	#Recorremos las columnas
	for t in content:

		#Añadimos elementos al diccionario
		cmd = t.xpath(".//span/text()")[0]
		func = t.xpath(".//td/text()")[0]
		dict_table[rows[0]].append(cmd)
		dict_table[rows[1]].append(func)

	#Agregamos a la lista 
	result.append(dict_table)

#############################
#   Creamos archivos json   #
#############################

for i in range(1, len(titles)):

	t_json = result[i-1]
	ti_json = titles[i-1]

	#Abrimos y escrimos en el archivo
	with open(f'tables json/{ti_json}.json', 'a') as f:
		json_content = json.dumps(t_json)

		f.write(json_content)
	

#############################
#     Creamos Notebook      #
#############################

print("Creando notebook...")
count = -1

for m in titles:
	mark = nbf.v4.new_markdown_cell(f"# {m}")
	count+=1

	r = result[count]

	text_code = f"import pandas as pd \ntable_{count} = {json.dumps(r)} \ndf = pd.DataFrame(table_{count}) \ndf"
	code = nbf.v4.new_code_cell(text_code)

	nb["cells"].append(mark)
	nb["cells"].append(code)

with open("cmd_vim.ipynb", "w", encoding="utf-8") as f:
	nbf.write(nb, f)

print("Notebook creado!")