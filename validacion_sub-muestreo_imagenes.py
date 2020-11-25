#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 18:04:55 2020

@author: felipe
"""

#https://www.tensorflow.org/tutorials
import numpy as np
import cv2
import tensorflow as tf

import time
import sys
import os 
import shutil

def min_max_norm(X):
    '''
    Funcion para normalizar los conjuntos de datos, como se trabaja con valores de 8-bits,
    se sabe que el maximo es 255 y el minimo es 0, se aplica una normalizacion min-max
    Input
        X: conjunto de datos
    Output
        conjunto de datos normalizado
    '''
    return X/(255)

print("\nEl directorio de trabajo es: " + os.getcwd())

# Especificar si se quiere entrenar con el conjunto de datos en escala de grises o los conjuntos de datos para los tres canales de color
channel = input("\nPor favor, introduza el canal a sub-muestrear: 'gray' para escala de grises, 'bgr' para canales de color: ")
# Si se ingreso un canal incorrecto:
while channel != 'bgr' and channel != 'gray':
    print("Error: canal no reconocido...")
    channel = input("\nPor favor, introduza el canal a sub-muestrear: 'gray' para escala de grises, 'bgr' para canales de color: ")
    #sys.exit()


print("\nPor favor, seleccione el caso adecuado:")
print("1. Se sub-muestrearan todas las imagenes dentro del directorio Validacion/Imagenes_HR")
print("2. Se sub-muestreara una imagen especifica en el directorio Validacion/Imagenes_HR")
caso = int(input("Caso: "))
while caso != 1 and caso !=2:
    print("Error: caso no reconocido...")
    caso = int(input("Caso: "))

start_time = time.time()

if caso == 1:
    print("Se sub-muestrearan todas las imagenes .png contenidas en el directorio Validacion/Imagenes_HR, los resultados se almacenaran en el directorio Imagenes_LR...")
    #  Se obtiene una lista con los nombres de los archivos de las imagenes a sub-muestrear
    filelist=os.listdir('Validacion/Imagenes_HR')
    for fichier in filelist[:]:
        if (fichier.endswith(".png") == True) or (fichier.endswith(".jpg") == True): # Remueve nombres de archivos que no sean .png
            None
        else:       
            filelist.remove(fichier)
    filelist.sort()
    
    print("\nArchivos a sub-muestrear:")
    print(filelist)

elif caso == 2:
    file_name = input("\nPor favor, ingrese el nombre de la imagen a sub-muestrear junto a su formato (png, jpg): ")
    filelist = [file_name]
    while os.path.isfile('Validacion/Imagenes_HR/'+file_name) == False:
        print("El archivo no existe dentro del directorio Validacion/Imagenes_HR, por favor, ingrese un archivo valido:")
        file_name = input("\nPor favor, ingrese el nombre de la imagen a sub-muestrear junto a su formato (png, jpg): ")

for fl in filelist:
    
    start_time_aux = time.time()
    print("\nSub-muestreando la imagen %s" % (fl))

    # Si se desea sub-muestrear la imagen en los tres canales de color
    if channel == 'bgr':
        img = cv2.imread(('Validacion/Imagenes_HR/'+fl), cv2.IMREAD_COLOR)
        h, w = img.shape[0:2]
        # Se verifican las dimensiones de la imagen, que sean divisibles entre 4
        if h%4 == 0 and w%4 == 0:
            print("Las dimensiones de la imagen son correctamente divisibles entre 4")
        else:
            print("Las dimensiones de la imagen no son incorrectamente divisibles entre 4, eliminando bordes extra...")
            while h%4 != 0:
                img_aux = img.copy()
                img = img_aux[0:-1,:,:]
                h, w = img.shape[0:2]
            while w%4 != 0:
                img_aux = img.copy()
                img = img_aux[:,0:-1,:]
                h, w = img.shape[0:2]    
        # Se crean  listas con nombres auxiliares
        nombres = ['Modelo_azul_guardado', 'Modelo_verde_guardado', 'Modelo_rojo_guardado']
        color = ['blue', 'green', 'red']
        # Se crea la matriz de imagen de la imagen sub-muestreada
        imgLR = np.zeros((int(h/4), int(w/4), 3), dtype=np.uint8)

    # Si se desea sub-muestrear la imagen en escala de grises
    elif channel == 'gray':
        img = cv2.imread(('Validacion/Imagenes_HR/'+fl), 0)
        h, w = img.shape[0:2]
        # Se verifican las dimensiones de la imagen, que sean divisibles entre 4
        if h%4 == 0 and w%4 == 0:
            print("Las dimensiones de la imagen son correctamente divisibles entre 4")
        else:
            print("Las dimensiones de la imagen no son incorrectamente divisibles entre 4, eliminando bordes extra...")
            while h%4 != 0:
                img = img[0:-1,:,:]
                h, w = img.shape[0:2].copy()
            while w%4 != 0:
                img = img[:,0:-1,:]
                h, w = img.shape[0:2].copy()
        # Se crean listas con nombres auxiliares
        nombres = ['Modelo_gris_guardado']
        color = ['gray']
        # Se crea la matriz de imagen de la imagen sub-muestreada
        imgLR = np.zeros((int(h/4), int(w/4), 1), dtype=np.uint8)

    # Se recorre cada modelo especifico para procesar el canal especifico
    for i in range(len(nombres)):

        print("Procesando el canal " + str(color[i]))

        # Se extrae la matriz de imagen del canal de color actual
        if channel == 'gray':
            canal = img[:,:]
        else:
            canal = img[:,:,i]
        # Se extraen ventanas de 4x4 pixeles y se almacenan como vectores de 16 caracteristicas
        x = []
        for row in range(int(h/4)):
            for col in range(int(w/4)):
                x.append(np.float32(canal[row*4:row*4+4, col*4:col*4+4].flatten()))
        # Se crea un np.array a partir de la informacion extraida anteriormente
        X = np.array(x)
        # Normalizacion de las muestras del conjunto de datos de la imagen a sub-muestrear     
        X = min_max_norm(X)
        # No-linealizacion del conjunto de datos
        X_aux = X.copy()
        for j in range(X_aux.shape[1]):
            X = np.column_stack((X, (X_aux[:,j]*X_aux[:,j])))
        for j in range(X_aux.shape[1]):
            X = np.column_stack((X, (X_aux[:,-j-1]*X_aux[:,-j+1]*X_aux[:,-j])))

        #print(X.shape)
        # Se carga el modelo entrenado para el canal de color especifico
        print("Cargando el modelo entrenado: " + str(nombres[i]) + '...')
        new_model = tf.keras.models.load_model(('Entrenamiento/'+ nombres[i]))
        # Se chequea la arquitectura de la red neuronal
        #print(new_model.summary())

        # Se realizan las predicciones a partir de los datos de entrada
        predictions = new_model.predict(X)
        imgLR[:,:,i] = np.uint8(predictions.reshape(int(h/4), int(w/4)))

    cv2.imwrite(('Validacion/Imagenes_LR/'+fl[:-4] + '_' + str(channel) + '_sub-muestreada.png') ,imgLR)
    print("La imagen %s ha sido sub-muestreada exitosamente..." % (fl))
    print("---Tiempo de ejecucion: %s segundos ---" % (time.time() - start_time_aux))

print("---Tiempo de ejecucion: %s segundos ---" % (time.time() - start_time))
