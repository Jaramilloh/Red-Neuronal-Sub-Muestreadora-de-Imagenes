#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 18:04:55 2020

@author: felipe
"""


import sys
import cv2
import numpy as np
import os
import shutil
import time

start_time = time.time()

def filtro_gaussian(img, sigmax, sigmay):
    '''
    Esta funcion genera el filtro Gaussiano en las dimensiones de la
    imagen a filtrar, con la frecuencia de corte especifica.

    Entradas:
        img: imagen a filtrar
        K: factor de decimacion
        sigmax: desviacion estandar (frecuencia de corte) en la dimension 'x'
        sigmay: desviacion estandar (frecuencia de corte) en la dimension 'y'
    Salidas:
        gaussian_norm: filtro Gaussiano en frecuencia
    '''
    kx=img.shape[0] # Tamaño de la ventana en x
    ky=img.shape[1] # Tamaño de la ventana en y

    # Generación de la ventana del filtro Gaussiano en espacio de 'kx'x'ky'
    # con la frecuencia de corte espacial dada por 'sigmax' y 'sigmay'
    x=np.float32(cv2.getGaussianKernel(kx,sigmax))
    y=np.float32(cv2.getGaussianKernel(ky,sigmay))
    gaussian=x*y.T

    # Normalizar min-max el filtro en espacio para pasarlo a frecuencia
    gauss_min = np.min(gaussian)
    gauss_max = np.max(gaussian)
    gaussian_norm = (gaussian - gauss_min)/(gauss_max - gauss_min)

    # Se crean dos matrices con el mismo filtro, uno para multiplicar la parte real, y otro para multiplicar la parte imaginaria
    gausss = np.zeros((gaussian_norm.shape[0], gaussian_norm.shape[1], 2), dtype=np.float32)
    gausss[:,:,0] = gaussian_norm
    gausss[:,:,1] = gaussian_norm
    
    return gausss

def iteraciones_opt(img, gaussian, sfft_img_c1, sfft_img_c2, sfft_img_c3, K):
    '''
    Esta funcion evalua los 'n' filtros Gaussianos generados (especificados en el
    numero de iteraciones), al filtrar la imagen especifica, decimarla y escalarla
    de nuevo a partir de una interpolacion bicubica para calcular un error entre
    esta y la imagen original sin filtrar y sin decimar.

    Entradas:
        img: imagen a filtrar
        gaussian: filtro Gaussiano en frecuencia a probar
        sfft_img_c1: canal B  en frecuencia de la imagen a filtrar
        sfft_img_c2: canal G  en frecuencia de la imagen a filtrar
        sfft_img_c3: canal R  en frecuencia de la imagen a filtrar
        K: factor de decimacion
    Salidas:
        J: costo entre la imagen filtrada decimada y escalada y 
        la imagen orginal
        img_dwn: imagen filtrada decimada
    '''
    # Multiplicación del filtro y cada canal de color en frecuencia
    img_filteredc1 = sfft_img_c1*gaussian
    img_filteredc2 = sfft_img_c2*gaussian
    img_filteredc3 = sfft_img_c3*gaussian

    # Inverse DFT shift
    img_fltc1_aux = np.fft.ifftshift(img_filteredc1)
    img_fltc2_aux = np.fft.ifftshift(img_filteredc2)
    img_fltc3_aux = np.fft.ifftshift(img_filteredc3)

    # Inverse DFT
    img_fltc1 = cv2.idft(img_fltc1_aux)
    img_fltc2 = cv2.idft(img_fltc2_aux)
    img_fltc3 = cv2.idft(img_fltc3_aux)

    # Se obtiene la magnitud de la parte real e imaginaria de cada canal en frecuencia
    img_fltc1 = cv2.magnitude(img_fltc1[:,:,0],img_fltc1[:,:,1])
    img_fltc2 = cv2.magnitude(img_fltc2[:,:,0],img_fltc2[:,:,1])
    img_fltc3 = cv2.magnitude(img_fltc3[:,:,0],img_fltc3[:,:,1])

    # Se normalizan los valores de cada canal en 0 y 255
    img_fltc1 = cv2.normalize(img_fltc1, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)
    img_fltc2 = cv2.normalize(img_fltc2, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)
    img_fltc3 = cv2.normalize(img_fltc3, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)

    # Se juntan los canales en una sola imagen
    img_flt = cv2.merge((img_fltc1, img_fltc2, img_fltc3))
    img_dwn = img_flt[0::K,0::K] 

    # Se interpola la imagen decimada
    img_resize = cv2.resize(img_dwn, None, fx=K, fy=K, interpolation = cv2.INTER_CUBIC)
    # Se calcula el error entre la imagen interpolada y la imagen original
    if img.shape == img_resize.shape:
        J = 1/(2*len(img.flat))*(np.sum(np.power(np.subtract(img_resize,img),2)))
    else:
        img_auxx = img_resize.flatten()
        img_auxx = img_auxx[:len(img.flatten())]
 
        J = 1/(2*len(img.flat))*(np.sum(np.power(np.subtract(img_auxx,img.flatten()),2)))

    return J, img_dwn

'''
PSEUDO-ALGORITMO - MAIN:
1. Ubicarse de forma absoluta en el directorio global contenedor de los
directorios de cada campo de luz
2. Obtener una lista con los nombres de los directorios de los campos de luz
3. Recorrer cada directorio del campo de luz:
    1. Crear los directorios internos donde se almacenaran los resultados: 
    imagenes decimadas e imagenes decimadas interpoladas bicubicamente.
4. Obtener una lista con el nombre de los archivos de las imagenes de sub-apertura
del campo de luz decimado angularmente, estos archivos se encuentran en el directorio
"Decimado_angular" dentro del directorio de cada campo de luz.
4. Recorrer la lista de archivos.
    1. Sub-muestrear espacialmente la imagen y almacenar los resultados 
    en su directorio correspondiente.
    
PSEUDO-ALGORITMO - DECIMACION ESPACIAL:
Con el fin de evitar aliasing en la imagen decimada.
1. Para cada imagen en la lista de archivos de las imagenes de sub apertura del
campo de luz decimado angularmente:
    2. Generar los 'itr' filtros Gaussianos a probar, el primer filtro
    Gaussiano tendra una frecuencia de corte igual a la desviacion estandar: fcx = fsx/(2*K),
    fcy = fsy/(2*K), siendo 'K' el factor de decimacion. La frecuencia de corte en 'x' y en 'y'
    de los siguientes filtros ira aumentando en 1 hasta generar los 'itr' filtros.
    3. Para cada filtro:
        1. Se filtrara la imagen con el filtro y se decimara una vez filtrada
        2. La imagen filtrada se interpolara (escalara) bicubicamente en el mismo factor 
        'K' de decimacion.
        3. Se calcular el error entre la imagen original y la imagen filtrada-decimada-interpolada
    4. El filtro con menor error sera elegido y su resultado sera almacenado
'''


if sys.platform == "linux" or sys.platform == "linux2":
    pth = input("\nPor favor, introduzca la ruta de trabajo absoluta: ")
    os.chdir(pth)
else:
    pth = input("\nPor favor, introduzca la ruta de trabajo absoluta, recuerde cambiar '\\' por '/': ")
    os.chdir(pth)

HR_dirs = ['X']
print ("\nLos directorios que contienen las imagenes HR son : " + str(HR_dirs)) 

# Especificar el factor de decimacion y el numero de iteraciones
Ki = input("\nPor favor, introduzca el factor de sub-muestreo, debe ser divisible entre 2 en la medida de lo posible (se tomara el numero entero del valor introducido): ")
K = int(Ki)
if (K <= 0) and (K > 10) and (K%2 != 0):
    print("Numero invalido, se elegirá el valor por defecto K = 4")
    K = 4

itri = input("Por favor, introduzca el numero de iteraciones para optimizar la decimacion de cada imagen (se tomara el numero entero del valor introducido): ")
itr = int(itri)
if (itr <= 0) and (itr > 300):
    print("Numero invalido, se elegirá el valor por defecto itr = 100")
    itr = 100
 
print("\nSe decimaran todas las imagenes en un factor %d, con %d iteraciones en cada una para optimizar la frecuencia de corte del filtro pasabajos..." % (K, itr)) 

# Se elimina los directorios si ya existen
if os.path.isdir('Y'):
    rmdir = 'Y'
    shutil.rmtree(rmdir)
if os.path.isdir('Filtros_Gaussianos'):
    rmdir = 'Filtros_Gaussianos'
    shutil.rmtree(rmdir)
if os.path.isdir('Interpolacion_bicubica'):
    rmdir = 'Interpolacion_bicubica'
    shutil.rmtree(rmdir)        

# Se crean los directorios "Decimado_espacial_angular", "Filtros_Gaussianos" y "Interpolacion_bicubica"
os.makedirs((os.getcwd() + '/Y' ), mode=0o777, exist_ok=False) # Se crea el directorio para almacenar las imagenes sub-muestreadas espacialmente
os.makedirs((os.getcwd() + '/Filtros_Gaussianos' ), mode=0o777, exist_ok=False) # Se crea el directorio para almacenar los filtros Gaussianos implementados a cada imagen
os.makedirs((os.getcwd() + '/Interpolacion_bicubica' ), mode=0o777, exist_ok=False) # Se crea el directorio para almacenar las imagenes sub-muestreadas espacialmente pero escaladas bicubicamente
print("Se crearon los directorios objetivos para almacenar los resultados.")

i = 0
print("\nRecorriendo el directorio : " + str(HR_dirs[i]))
# Se crean los directorios objetivos dentro del directorio del campo de luz para almacenar las imagenes sub-muestreadas espacialmente,
# los filtro Gaussianos, y las imagenes sub-muestreadas pero interpoladas en el mismo factor por una funcion bicubica.

#  Se obtienen los nombres de los archivos de las imagenes de sub-apertura
filelist=os.listdir(HR_dirs[i])
for fichier in filelist[:]:
    if not(fichier.endswith(".png")): # Remueve nombres de archivos que no sean .png
        filelist.remove(fichier)
filelist.sort()

# Se recorren las imagenes de sub-apertura encontradas
j = 0
for files in filelist:

    start_time_aux = time.time()
    
    # Imagen a decimar
    print("\nProcesando imagen: " + str(HR_dirs[i] + '/X/' + files))
    img = cv2.imread((HR_dirs[i] + '/' + files), cv2.IMREAD_COLOR)
    
    # Frecuencia de corte inicial, teoricamente dada por el Teorema de Muestro de Nyquist
    # fcx = fsx/(2*K)
    # fcy = fsy(2*K)
    # Ambos valores teoricos se disminuyen 10 pixeles, por consideraciones de implementacion
    sigmax = int((1/(2*K))*(img.shape[0]))
    sigmay = int((1/(2*K))*(img.shape[1]))

    sigmasx = np.arange(sigmax, sigmax+itr, 1)
    sigmasy = np.arange(sigmay, sigmay+itr, 1)
    
    # Generacion de los filtros Gaussianos a evaluar
    gaussian = []
    gaussian = [filtro_gaussian(img, sigmasx[i], sigmasy[i]) for i in range(len(sigmasx))]

    # Extraccion de los canales de color de la imagen a decimar
    b,g,r = cv2.split(img)

    # FFT para cada canal de color
    img_fft_img_c1 = cv2.dft(np.float32(b),flags = cv2.DFT_COMPLEX_OUTPUT)
    sfft_img_c1 = np.fft.fftshift(img_fft_img_c1)

    img_fft_img_c2 = cv2.dft(np.float32(g),flags = cv2.DFT_COMPLEX_OUTPUT)
    sfft_img_c2 = np.fft.fftshift(img_fft_img_c2)

    img_fft_img_c3 = cv2.dft(np.float32(r),flags = cv2.DFT_COMPLEX_OUTPUT)
    sfft_img_c3 = np.fft.fftshift(img_fft_img_c3)

    # Listas donde se almacenaran los resultados
    Js = []
    img_dwn = []

    # Se empiezan a evaluar los filtros 
    for gauss in gaussian:
        j_aux, img_aux = iteraciones_opt(img, gauss, sfft_img_c1, sfft_img_c2, sfft_img_c3, K)
        Js.append(j_aux)
        img_dwn.append(img_aux)

    # Se obtiene el indice del filtro Gaussiano con menor error
    ind_min = np.argmin(Js)
    print("Con Sigmax=%d, Sigmay=%d, el costo entre la imagen original y la imagen escalada es J=%f" % (sigmasx[ind_min], sigmasy[ind_min], np.min(Js)))  
    
    # Se guarda la imagen decimada por el filtro Gaussiano con menor error
    name = os.getcwd() + '/Y/LR_' + files
    cv2.imwrite(name, img_dwn[ind_min])
    
    # Se guarda el filtro Gaussiano
    norm_gaussian = cv2.normalize(gaussian[ind_min], None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)
    norm_gaussian.astype(np.uint8)
    name = os.getcwd() + '/Filtros_Gaussianos/flt_gaussian_' + files
    cv2.imwrite(name, norm_gaussian[:,:,0])
    
    # Se guarda la imagen decimada interpolada bicubicamente
    img_resize = cv2.resize(img_dwn[ind_min], None, fx=K, fy=K, interpolation = cv2.INTER_CUBIC)
    name = os.getcwd() + '/Interpolacion_bicubica/bicHR_' + files
    cv2.imwrite(name, img_resize)
    j += 1
    
    print("Se han almacenado correctamente los resultados de la imagen %d..." % (j))
    print("---Tiempo de ejecucion: %s segundos ---" % (time.time() - start_time_aux))
            
print("Las %d imagenes se han sido decimadas espacialmente correctamente..." % (j))

print("--- Execution time: %s seconds ---" % (time.time() - start_time))








