"""
drive.py

Starts a driving loop

Usage:
    drive.py [--record]

Options:
  --record     record images to disk [default: False]
"""

import logging # libreria para administrar los log generados por nuestro programa.
import sys # libreria que permite utilizar herramientas del sistema, como impresion por consola.

from docopt import docopt # libreria para crear lineas de comando personalizadas para un programa.
from rover import Rover
from composers import Composer


def setup_logging(): # Configura los logs.
    '''
    Setup logging to output info to stdout
    '''
    root = logging.getLogger() # crea objeto Logger personalizado.
    root.setLevel(logging.INFO) # establece nivel de escritura de los log desde los INFO para ese Logger.

    ch = logging.StreamHandler(sys.stdout) # crea un manejador para enviar los logs por consola.
    ch.setLevel(logging.INFO) # mostrara por consola solo los de nivel de importancia info o mayor.
    formatter = logging.Formatter('%(asctime)s - %(message)s') # crea un formato para los logs. (asctime) -> tiempo de creacion del log. (message) -> mensaje del log.
    ch.setFormatter(formatter) # asigna el formato anterior a los log que se mostraran por consola.
    root.addHandler(ch) # y toda esta configuracion se asigna al Objeto Logger anterior.


if __name__ == "__main__": # si es el documento principal de ejecucion...
    arguments = docopt(__doc__) # analiza los argunmentos introducidos por consola siguiendo Usage y options de arriba. 
    setup_logging() # ejecuta la funcion anterior para los logs.
    composer = Composer() # Crea un Objeto de la Clase composer definida en ese mismo archivo.
    rover = composer.new_vehicle() # Define la variable rober como un Objeto de la clase Rover con los atributos definidos por el metodo new_vehicle de la clase composer.
    rover.record = arguments["--record"] # guarda en este atributo un booleano que comprueba si se añadio esta opcion al ejecutar.
    rover.run() # ejecuta el metodo run() de la clase rover.
