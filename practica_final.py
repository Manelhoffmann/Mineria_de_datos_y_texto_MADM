from SPARQLWrapper import SPARQLWrapper, JSON
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
from Ontology import *

# Utilizando SPARQLWrapper se crea un conector para ejecutar consultas de forma remota

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)  # Formato

# Por tanto, a través de una query, se obtienen todos los nombres de los pájaros de la dbpedia.
sparql.setQuery(""" 
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT * WHERE {
    ?x rdf:type <http://dbpedia.org/ontology/Bird> . }
 """)

# Se procede a extraer la información necesaria. También se eliminan mayúsculas, barras bajas y paréntesis.
# El objetivo de este proceso es el de poder buscar los nombres tal y como se encuentran en los posts.
try:
    ret = sparql.queryAndConvert()

    birds = {}  # Construcción de un diccionario de pájaros.
    for r in ret["results"]["bindings"]:
        link = r['x']['value']
        link_name = link.split("/")[-1]
        name = link_name.replace("_", " ")
        name = name.replace("(", "")
        name = name.replace(")", "")
        name = name.lower()
        birds[name] = (link_name, link)

except Exception as e:
    print(e)

# Apertura de entradas:
root_post = "C:/Users/34658/OneDrive/Documentos/post_birds/"
posts = os.listdir(root_post)

names_birds_text = []
objects_list = []
for post in posts:  # Iteración de entradas
    file = open(root_post + post, 'r')
    try:
        post_text = file.read()  # Lectura de cada post
        post_text = post_text.lower()  # Conversión de mayúsculas a minúsculas
        for b in birds:
            if b in post_text:  # Cada "b" es una key del diccionario
                names_birds_text.append(b)
                bird_link_name = birds[b][0]
                link = birds[b][1]
                bird_obj = Bird(bird_link_name)
                # Instancia en la ontología
                post_obj = Post(post)
                link_obj = URL(link)

                bird_obj.from_post = [post_obj]
                bird_obj.from_link_bird_obj = [link_obj]

                objects_list.append(bird_obj)

    except Exception as e:
        print(e)
    file.close()

url_dbpedia = []  # Lista de url's
for i in Bird.instances(): url_dbpedia.append(i.iri)
# Con la función iri se obtienen los en la dbpedia de las aves


save_onto()  # Se salva la ontología

# Aquellas palabras que guardan similitud entre las palabras de la dbpedia y las del texto se guardan incluyendo su correspondiente link.

# Lista de nombres de pájaros que aparecen en el texto
print(names_birds_text)
# len(names_birds_text)
# En las entradas se han localizado 119 nombres de pájaros. Destacar que hay nombres que pueden estar repetidos y aparecer en diferentes entradas.
# Se han detectado 91 nombres de pájaros diferentes.
# -------------------------------------------------------------------------------

# Apéndice:

# Hay que destacar como se han realizado diferentes pruebas para intentar optimizar la búsqueda de las palabras en el texto.
# El código se encuentra comentado pues no se ha obtenido mejora en los resultados finales.
# Algunas de las pruebas han sido:
# - Eliminar signos de puntuación innecesarios
# - Tokenizar
# - Eliminar las StopWords
# - Eliminan los afijos morfológicos de las palabras, dejando solo la raíz de la palabra
# - A través del reconocimiento de entidades nombradas eliminar un conjunto de palabras en las que podemos afirmar
# con seguridad que no son nombres de pájaros
# - Eliminar duplicados


# A continuación la demostración:

# # Eliminación de la puntuación.
# punto = string.punctuation
# punto = punto.replace("-", "")
# for p in punto:
#     words = words.replace(p, " ")


# Eliminar stopwords, tokenización:
# example_sent = words
# stop_words = set(stopwords.words('english'))
# word_tokens = word_tokenize(example_sent)
# filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
# filtered_sentence = []

# for w in word_tokens:
#     if w not in stop_words:
#         filtered_sentence.append(w)


# # Pasar las palabras al infinitivo:
# stemmer = PorterStemmer()
# words_in_text = []
# for w in filtered_sentence:
#     if w[-1] == "s": #Para evitar manipular palabras correctas se han seleccionado solo las que terminen en s
#         words_in_text.append(stemmer.stem(w))
#     else:
#         words_in_text.append(w)

# str_review_nouns = " ".join(words_in_text)  # transformar de una lista a un str para adaptar el código para spacy


# #Reconocimiento de entidades nombradas:
# Selección de palabras que no son nombres de pájaros:
# NER = spacy.load("en_core_web_sm")
# text1 = NER(str_review_nouns)

# list_not_bird = []
# for word in text1.ents:
#     if (
#          word.label_ == "DATE" or
#          word.label_ == "TIME" or
#          word.label_ == "CARDINAL" or
#          word.label_ == "QUANTITY" or
#          word.label_ == "FAC"):
#         list_not_bird.append(word)


# # Eliminamos duplicados. Convertimos a set y luego a lista
# unic_list_not_bird = list(set(list_not_bird))

# Eliminar las palabras que estamos seguros de que no son pájaros para facilitar el match entre las palabras de la dbpedia y las del texto
# for w in unic_list_not_bird:
#     str_review_nouns = str_review_nouns.replace(w.text, "")
