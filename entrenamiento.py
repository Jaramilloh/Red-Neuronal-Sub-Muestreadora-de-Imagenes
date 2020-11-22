#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 18:04:55 2020

@author: felipe
"""

#https://www.tensorflow.org/tutorials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf
import tensorflow_addons as tfa

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import kerastuner as kt

import time
import sys
import os 
import shutil
import IPython

def plot_loss(hist, name, color):
    '''
    Funcion para graficar la perdida de entrenamiento vs. el epoch durante
    el entrenamiento del modelo
    Inputs:
        history: historial de perdidas en el entrenamiento del modelo
        name: nombre del conjunto de datos
        color: color del canal del conjunto de datos    
    '''
    plt.plot(hist, label=('perdida en el conjunto de datos '+ name), color=color)
    plt.ylim([4, 7])
    plt.xlabel('Epoch')
    plt.ylabel('Error')
    plt.title('Entrenamiento para canales de color BGR ')
    plt.legend()
    plt.grid(True)

def min_max_norm(X):
    '''
    Funcion para normalizar los conjuntos de datos, como se trabaja con valores de 8-bits,
    se sabe que el maximo es 255 y el minimo es 0, se aplica una normalizacion min-max
    Input
        X: conjunto de datos
    Output
        conjunto de datos normalizado
    '''
    return X/255.0

def r2_coef(y_true, y_pred):
    #https://en.wikipedia.org/wiki/Coefficient_of_determination
    '''
    Calculo del coeficiente de determinacion R2 para una regresion
    Inputs:
        y_true: Valor de salida para cada muestra en el conjunto de datos
        de validacion
        y_pred: Valor de salida predicho por el modelo entrenado para cada
        muestra del conjunto de datos de validacion
    Output:
        R2: Coeficiente de determinacion
    '''
    # SS_res = sum(y_real[i] - y_pred[i])^2
    resta = []
    for i in range(len(y_pred)):
        resta.append(np.power(np.subtract(y_true[i],y_pred[i]),2))
    SS_res = np.sum(np.array(resta))     

    # SS_tot = sum(y_real[i] - y_real_mean)^2
    mean = np.mean(y_true)
    resta = []
    for i in range(len(y_pred)):
        resta.append(np.power(np.subtract(y_true[i],mean),2))
    SS_tot = np.sum(np.array(resta))  

    r2 = 1 - (SS_res/SS_tot)
    return r2


print("\nEl directorio de trabajo es: " + os.getcwd())

# Ingresar los hiper parametros para el entrenamiento de la red neuronal:
# Algunos hiper-parametros se afinaron de acuerdo a https://www.tensorflow.org/tutorials/keras/keras_tuner
alfa_train = float(input("\nPor favor, ingrese el valor inicial del factor de aprendizaje (0.01 es el valor optimo determinado por el afinador de hiper-parametros): "))
alfa_reg_l1 = float(input("\nPor favor, ingrese el valor el factor de regularizacion l1 (1e-7 es el valor optimo determinado por el afinador de hiper-parametros): "))
alfa_reg_l2 = float(input("\nPor favor, ingrese el valor el factor de regularizacion l2: (1e-5 es el valor optimo determinado por el afinador de hiper-parametros) "))
batch_sz = int(input("\nPor favor, ingrese el numero de datos por cada lote de entrenamiento: "))
epchs = int(input("\nPor favor, ingrese el numero epochs (repeticiones por cada muestra): "))

# Especificar si se quiere entrenar con el conjunto de datos en escala de grises o los conjuntos de datos para los tres canales de color
channel = input("\nPor favor, introduza los canales de color a ser utilizados como conjunto de datos; 'gray' para escala de grises, 'bgr' para canales de color: ")
# Si se ingreso un canal incorrecto:
while channel != 'bgr' and channel != 'gray':
    print("Error: canal no reconocido...")
    channel = input("\nPor favor, introduza el canal a sub-muestrear: 'gray' para escala de grises, 'bgr' para canales de color: ")
    #sys.exit()

# Se abre un registro para guardar cada print en un archivo llamada log_entrenamiento.log
old_stdout = sys.stdout
log_file = open((str(channel)+"_entrenamiento.log"),"w")
sys.stdout = log_file
print("\nLos hiper-parametros para entrenar los modelos son:")
print("Factor de aprendizaje: %f " % (alfa_train))
print("Factor de regularizacion L1: %f " % (alfa_reg_l1))
print("Factor de regularizacion L2: %f " % (alfa_reg_l2))
print("Tamaño del lote (batch): %d " % (batch_sz))
print("Numero de epocas (epoch): %d " % (epchs))

start_time = time.time()

# Si se desea entrenar tres modelos para cada canal de color:
if channel == 'bgr':
    # Se inicializan listas con los nombres de los conjuntos de datos y el color correspondiente a cada canal
    dataframes = ['blue_channel.csv', 'green_channel.csv', 'red_channel.csv']
    color = ['blue', 'green', 'red']
    nombres = ['Modelo_azul_guardado', 'Modelo_verde_guardado', 'Modelo_rojo_guardado']
    # Directorios especificos de cada modelo entrenado:
    # Se elimina los directorios que almacenaran los modelos entrenados si ya existen
    if os.path.isdir('Modelos_guardados/Modelo_azul_guardado'):
        rmdir = 'Modelos_guardados/Modelo_azul_guardado'
        shutil.rmtree(rmdir)
    if os.path.isdir('Modelos_guardados/Modelo_verde_guardado'):
        rmdir = 'Modelos_guardados/Modelo_verde_guardado'
        shutil.rmtree(rmdir)
    if os.path.isdir('Modelos_guardados/Modelo_rojo_guardado'):
        rmdir = 'Modelos_guardados/Modelo_rojo_guardado'
        shutil.rmtree(rmdir)    
    # Se crean los directorios que almacenaran los modelos entrenados
    os.makedirs((os.getcwd() + '/Modelos_guardados/Modelo_azul_guardado' ), mode=0o777, exist_ok=False) 
    os.makedirs((os.getcwd() + '/Modelos_guardados/Modelo_verde_guardado' ), mode=0o777, exist_ok=False) 
    os.makedirs((os.getcwd() + '/Modelos_guardados/Modelo_rojo_guardado' ), mode=0o777, exist_ok=False)
    print("Se crearon los directorios objetivos para almacenar los modelos entrenados.")

# Si se desea entrenar un solo modelo para un canal en escala de grises:
elif channel == 'gray':
    # Se inicializan listas con el nombre del conjunto de datos y el color correspondiente
    dataframes = ['gray_channel.csv']
    color = ['gray']
    nombres = ['Modelo_gris_guardado']
    # Directorios especificos de cada modelo entrenado:
    # Se elimina los directorios que almacenaran los modelos entrenados si ya existen
    if os.path.isdir('Modelos_guardados/Modelo_gris_guardado'):
        rmdir = 'Modelos_guardados/Modelo_gris_guardado'
        shutil.rmtree(rmdir)    
    # Se crean los directorios que almacenaran los modelos entrenados
    os.makedirs((os.getcwd() + '/Modelos_guardados/Modelo_gris_guardado' ), mode=0o777, exist_ok=False) 
    print("Se crearon los directorios objetivos para almacenar el modelo entrenado.")   

# Directorio para almacenar los modelos entrenados:
# Se elimina el directorio general que guarda los modelos entrenados si ya existe
if os.path.isdir('Modelos_guardados') == False:
    # Se crea el directorio general que guarda los modelos entrenados
    os.makedirs((os.getcwd() + '/Modelos_guardados' ), mode=0o777, exist_ok=False) 

# Lista para almacenar las metricas de los modelos entrenados
r2_metrics = []
# Se recorre cada conjunto de datos para entrenar un modelo especifico
for i in range(len(dataframes)):

    print("\nSe utilizara el conjunto de datos " + str(dataframes[i]) + "...")
    print("Cargando conjunto de datos de 16 caracteristicas...")
    # Se lee el conjunto de datos en el archivo .csv
    df = pd.read_csv(('Dataset/'+dataframes[i]),delimiter=",")
    dfX=df[['X1','X2','X3','X4','X5','X6','X7','X8','X9','X10','X11','X12','X13','X14','X15','X16']]
    dfY=df['Y']
    print("El conjunto de datos tiene %d muestras." % (len(df.index)))
    # Se extraen los valores del dataframe y se convierten a punto flotante de 32-bits
    x = dfX.values
    y = dfY.values
    x = x.astype(np.float32)
    y = y.astype(np.float32)
    print("Normalizando y no-linealizando el conjunto de datos para tener 48 caracteristicas...")
    # Normalizacion de las muestras del conjunto de datos     
    x = min_max_norm(x)
    # Revolver el conjunto de datos y dividir el conjunto de datos en entrenamiento (75%) y validacion (25%)
    x, y = shuffle(x, y)
    # No-linealizacion del conjunto de datos
    X = x.copy()
    X_aux = X.copy()
    for j in range(X_aux.shape[1]):
        X = np.column_stack((X, (X_aux[:,j]*X_aux[:,j])))
    for j in range(X_aux.shape[1]):
        X = np.column_stack((X, (X_aux[:,-j-1]*X_aux[:,-j+1]*X_aux[:,-j])))
    # Se separa el conjunto de datos en entrenamiento y validacion
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    print("Inicializando la arquitectura de la red neuronal y los hiperparametros para su entrenamiento...")
    # Crear una clase para normalizar los datos de entrada a partir de x_train:
    #https://www.tensorflow.org/api_docs/python/tf/keras/layers/experimental/preprocessing/Normalization
    normalize = tf.keras.layers.experimental.preprocessing.Normalization()
    normalize.adapt(X_train)

    # Se define una interrupcion si no se cumple un factor de tolerancia en 8 epochs consecutivos
    # Cuando esto suceda, se retornan los parámetros con menor perdida:
    #https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/EarlyStopping
    callback = tf.keras.callbacks.EarlyStopping(
        monitor='loss', min_delta=0.0001, patience=8, verbose=0, mode='min',
        baseline=None, restore_best_weights=True
    )

    # Se definen las capas de la red neuronal:
    #https://www.tensorflow.org/api_docs/python/tf/keras/Model    
    model = tf.keras.Sequential([
        # Se define el numero de caracteristicas de cada muestra:
        # https://www.tensorflow.org/api_docs/python/tf/keras/layers/InputLayer
        tf.keras.layers.InputLayer(
            input_shape=(X.shape[1],)),
        # Capa que normaliza cada muestra de entrada:
        normalize,
        # Primera capa oculta con 16 perceptrones activados a partir de una funcion 'relu', ademas,
        # la funcion de perdida de cada perceptron estara regularizada por una norma L2 y una norma L1 (ElasticNet) 
        # en un factor alfa l1 y l2 dado por el usuario, esto con el fin de actualizar los pesos en cantidades menores,
        # para hacer la red mas robusta al ruido local en el conjunto de datos no-linealizado:
        # https://www.tensorflow.org/api_docs/python/tf/keras/regularizers/L1L2
        tf.keras.layers.Dense(
            16, 
            activation='relu',
            use_bias=True,
            kernel_regularizer=tf.keras.regularizers.L1L2(l1=alfa_reg_l1, l2=alfa_reg_l2)),                                                                                    
        tf.keras.layers.Dense(
            1,
            use_bias=True,
            kernel_regularizer=tf.keras.regularizers.L1L2(l1=alfa_reg_l1, l2=alfa_reg_l2))
    ])

    # Se compila la red neuronal con un optimizador Adam, con perdida y metrica igual al error absoluto medio entre los 
    # datos predichos y los datos de entrenamiento:
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=alfa_train), #https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/SGD
                loss = tf.keras.losses.MeanAbsoluteError(), #https://www.tensorflow.org/api_docs/python/tf/keras/losses
                metrics=['mean_absolute_error']) #https://www.tensorflow.org/api_docs/python/tf/keras/metrics 
    
    # Se entrena el modelo y se guarda el registro del entrenamiento:
    print("\nEmpezando el entrenamiento de la red neuronal:")
    print("Se entrenaran con %d muestras." % (X_train.shape[0]))
    history = model.fit(X_train, y_train, batch_size=batch_sz, epochs=epchs)#, callbacks=[callback]) #https://www.tensorflow.org/guide/keras/customizing_what_happens_in_fit
    # Se grafica el registro de entrenamiento del modelo:
    print("El entrenamiento ha finalizado exitosamente...")
    print("Creando una grafica del entrenamiento con %s..." % (dataframes[i]))
    hist = history.history['loss']
    plot_loss(hist, dataframes[i], color[i]) # Funcion para graficar el desempeño de la red en el entrenamiento

    print("Imprimiendo un resumen de la arquitectura de la red neuronal entrenada.")
    print(model.summary())

    # Se evalua el modelo entrenado a partir del conjunto de datos de validacion:
    print("\nIniciando evaluacion del modelo con el conjunto de datos de validacion...")
    print("Se evaluara con %d muestras." % (X_test.shape[0]))
    loss_test, metric_test = model.evaluate(X_test, y_test, batch_size=batch_sz, verbose=False)
    print("Perdida en el conjunto de validacion: %f, Error absoluto medio en el conjunto de validacion: %f" % (loss_test, metric_test))

    # Se predicen las salidas para el conjunto de datos de validacion, 
    # con el fin de evaluar el coeficiente de determinacion:
    y_pred = model.predict(X_test, batch_size=batch_sz)
    r2 = r2_coef(y_test, y_pred)
    r2_metrics.append(r2)
    print("Coeficiente R2: ", r2)

    # Se almacena el modelo entrenado
    model.save(('Modelos_guardados/'+ nombres[i]))
    print("\nEl modelo entrenado se ha guardado correctamente en: Modelos_guardados/" + nombres[i])

# Se almacena la grafica con el rendimiento del entrenamiento del modelo
plt.savefig(('Modelos_guardados/entrenamiento_'+str(channel)+'.png'), bbox_inches='tight')

# Resumen de la evaluacion de los modelos entrenados
print("\nCoeficientes de determinacion en cada modelo entrenado:")
for i in range(len(dataframes)):
    print("Para %s, R2 = %f " % (dataframes[i], r2_metrics[i]))

print("---Tiempo total de ejecucion del algoritmo de entrenamiento: %s segundos ---" % (time.time() - start_time))
sys.stdout = old_stdout
log_file.close()