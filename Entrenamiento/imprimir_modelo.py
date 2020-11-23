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
import sys
import os 


print("\nEl directorio de trabajo es: " + os.getcwd())


nombres = ['Modelo_gris_guardado', 'Modelo_azul_guardado', 'Modelo_verde_guardado', 'Modelo_rojo_guardado']


for i in range(len(nombres)):

    print("\nCargando el modelo entrenado: " + str(nombres[i]) + '...')
    new_model = tf.keras.models.load_model(('Modelos_guardados/'+ nombres[i]))
    print("Modelo cargado exitosamente...")

    dot_img_file = '/Modelos_guardados/arquitectura_modelo' + str(nombres[i]) + '.png'
    tf.keras.utils.plot_model(new_model, to_file="modelo.png",show_shapes=True)


