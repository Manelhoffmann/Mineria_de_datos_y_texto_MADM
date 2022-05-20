import Cython as Cython
from owlready2 import *

# Creamos una ontología:
onto = get_ontology("http://dbpedia.org/resource/")  # Indicamos el link

# Si al crear la ontología se le indica una barra al final de la url permite la construcción de dicha url tal y como se necesita.


# Definimos las clases y propiedades de la ontología:
with onto:
    class Bird(Thing):
        namespace = onto


    class Post(Thing):
        pass

    class URL(Thing):
        pass

    class from_post(ObjectProperty):
        domain = [Bird]
        range = [Post]

    class from_link_bird_obj(ObjectProperty):
        domain = [Bird]
        range = [URL]

# Con anterioridad se ha extraído de la documentación owlready2 la forma de crear una nueva clase de propiedad
# Es decir, se ha creado una nueva propiedad subclasificando la clase ObjectProperty
# A través de "domain" y "range" se ha especificado el dominio y el rando de la propiedad.

# Salvamos la ontología:
def save_onto():
    onto.save("C:/Users/34658/OneDrive/Documentos/MYOntology.xml", format="rdfxml")


# Apertura con protege
# !cat C:/Users/34658/OneDrive/Documentos/post_birds/MYOntology.xml
