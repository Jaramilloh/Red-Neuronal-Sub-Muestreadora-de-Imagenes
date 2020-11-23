#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 18:04:55 2020

@author: felipe
"""

import cv2
import numpy as np
import os
import sys

import shutil
import time
import csv

'''
Pseudo-algoritmo:
1. Identificar como entrada del usuario cual canal
se extraera como conjunto de datos: si los tres canales
de color, o solo el canal en escala de grises.
2. Identificar los directorios con las muestras, siendo
las imagenes en alta resolucion y las salidas, siendo 
las imagenes en baja resolucion. Directorios 'X' y 'Y'
respectivamente.
3. Obtener dos listas con los nombres de los archivos HR
y LR. Se organizan ambas listas en orden alfanumerico
4. Empezar a recorrer cada imagen HR con su homologa LR:
    
    1. Por cada pixel en la imagen LR, extraer una ventana
    de 4 x 4 pixeles en la imagen HR respectivamente.

    NOTA: la decimacion espacial introduce efectos de espejo
    en la primera fila de pixeles en algunas imagenes, esto
    se debe a que el proceso se realiza en el dominio de
    la frecuencia y al ser un paso de ida y de vuelta, alguna
    informacion se pierde.

    Por lo tanto, se filtran las muestras ruidosas, i.e. 
    aquellas muestras cuyas salidas no se encuentren dentro
    del rango de sus caracteristicas.

    2. Guardar las 16 caracteristicas de cada muestra con
    su salida en una fila nueva en un documento .csv 
    nombrado con el canal de color correspondiente.
'''

print("\nEl directorio de trabajo es: " + os.getcwd())

channel = input("\nPor favor, introduza el canal a extraer: 'gray' para escala de grises, 'bgr' para canales de color: ")
# Si se ingreso un canal incorrecto:
while channel != 'bgr' and channel != 'gray':
    print("Error: canal no reconocido...")
    channel = input("\nPor favor, introduza el canal a sub-muestrear: 'gray' para escala de grises, 'bgr' para canales de color: ")
    #sys.exit()

start_time = time.time()


#  Se obtienen los nombres de los archivos de las imagenes HR
filelistHR = os.listdir('X')
for fichier in filelistHR[:]:
    if not(fichier.endswith(".png")): # Remueve nombres de archivos que no sean .png
        filelistHR.remove(fichier)
filelistHR.sort()

#  Se obtienen los nombres de los archivos de las imagenes LR
filelistLR = os.listdir('Y')

if len(filelistHR) == len(filelistLR):

    for fichier in filelistLR[:]:
        if not(fichier.endswith(".png")): # Remueve nombres de archivos que no sean .png
            filelistLR.remove(fichier)
    filelistLR.sort()
    
    if channel == 'gray':
        
        if os.path.isfile('gray_channel.csv'):
            os.remove((os.getcwd() + '/gray_channel.csv'))
            
        with open('gray_channel.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "X10", "X11", "X12", "X13", "X14", "X15", "X16", "Y"])

            for i in range(len(filelistHR)):

                if filelistHR[i] == filelistLR[i][3:]:

                    start_time_aux = time.time()        
            
                    # Imagenes a extraer datos
                    print("\nProcesando imagenes: " + str(filelistHR[i]) + ', ' + str(filelistLR[i]))
                    
                    imgHR = cv2.imread((os.getcwd() + '/X/' + filelistHR[i]), 0)
                    imgLR = cv2.imread((os.getcwd() + '/Y/' + filelistLR[i]), 0)
            
                    for row in range(imgLR.shape[0]):
                        for col in range(imgLR.shape[1]):
                            Y = np.float32(imgLR[row,col])
                            X = np.float32(imgHR[row*4:row*4+4, col*4:col*4+4].flatten())

                            # Se filtran las muestras ruidosas
                            if np.max(X) >= Y and np.min(X) <= Y:
                                writer.writerow([X[0], X[1], X[2], X[3], X[4], X[5], X[6], X[7], X[8], X[9], X[10], X[11], X[12], X[13], X[14], X[15], Y])          
                    
                    print("Se han almacenado correctamente los resultados de la imagen %d..." % (i))
                    print("---Tiempo de ejecucion: %s segundos ---" % (time.time() - start_time_aux))
    
    if channel == 'bgr':
        
        if os.path.isfile('red_channel.csv') and os.path.isfile('blue_channel.csv') and os.path.isfile('green_channel.csv'):
            os.remove((os.getcwd() + '/red_channel.csv'))
            os.remove((os.getcwd() + '/blue_channel.csv'))
            os.remove((os.getcwd() + '/green_channel.csv'))
            
        
        chn = ['blue_channel.csv', 'green_channel.csv', 'red_channel.csv']
        
        for k in range(len(chn)):
            
            with open(chn[k], 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "X10", "X11", "X12", "X13", "X14", "X15", "X16", "Y"])
    
        
                for i in range(len(filelistHR)):
        
                    if len(filelistHR[i]) == len(filelistLR[i][3:]):
                        start_time_aux = time.time()        
                
                        # Imagenes a extraer datos
                        print("\nProcesando imagenes: " + str(filelistHR[i]) + ', ' + str(filelistLR[i]))
                        
                        imgHR = cv2.imread((os.getcwd() + '/X/' + filelistHR[i]), cv2.IMREAD_COLOR)
                        imgLR = cv2.imread((os.getcwd() + '/Y/' + filelistLR[i]), cv2.IMREAD_COLOR)
        
                        chHR = imgHR[:,:,k]
                        chLR = imgLR[:,:,k]      
                        
                        for row in range(imgLR.shape[0]):
                            for col in range(imgLR.shape[1]):
                                
                                Y = np.float32(chLR[row,col])
                                X = np.float32(chHR[row*4:row*4+4, col*4:col*4+4].flatten())
                                
                                if np.max(X) >= Y and np.min(X) <= Y:
                                    writer.writerow([X[0], X[1], X[2], X[3], X[4], X[5], X[6], X[7], X[8], X[9], X[10], X[11], X[12], X[13], X[14], X[15], Y])
                        
                        print("Se han almacenado correctamente los resultados de la imagen %d..." % (i))
                        print("---Tiempo de ejecucion: %s segundos ---" % (time.time() - start_time_aux))
                        
                          
print("---\nTiempo total de ejecucion: %s segundos ---" % (time.time() - start_time_aux))
            
            

