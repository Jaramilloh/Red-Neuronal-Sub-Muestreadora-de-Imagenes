# Red Neuronal Sub-Muestreadora de Imágenes
Este repositorio contiene el código fuente y los materiales para el proyecto de la Red Neuronal Sub-Muestreadora de Imágenes, desarrollado en la asignatura de enfásis "Inteligencia Artificial" en el programa de Ingeniería Electrónica de la Pontificia Universidad Javeriana. ***Autores: Juan Felipe Jaramillo Hernández, María Fernanda Hernández Baena, Jose David Cifuentes Semanate.***

Este repositorio contiene los códigos para [entrenar](entrenamiento.py) y [validar](validacion_sub-muestreo_imagenes.py) la red neuronal, además de los códigos para la [generación](Dataset/) del [conjunto de datos](Dataset/crear_dataframe.py) a partir de los recursos disponibles en [Common Objects in Context](https://cocodataset.org/#termsofuse) [1] (*Imágenes pertenecientes a [Flickr](https://www.flickr.com/creativecommons/) con licencia [Creative Commons](https://creativecommons.org/licenses/by/4.0/legalcode)*). También se encuentra un modelo pre-entrenado para cada canal de color o para escala de grises. El video y el artículo se pueden encontrar acá:

Video: <>
Artículo: <>

Tabla de Contenidos
=================

<!--ts-->
   * [Red Neuronal Sub-Muestreadora de Imágenes](#Red-Neuronal-Sub-Muestreadora-de-Imágenes)
   * [Tabla de Contenidos](#tabla-de-contenidos)
   * [Resultados Obtenidos](#Resultados-Obtenidos)
   * [Resultados Obtenidos](#Resultados-Obtenidos)
   * [Ejecutar el modelo pre-entrenado](#Ejecutar-el-modelo-pre-entrenado)
   * [Generación del conjunto de datos](#Generación-del-conjunto-de-datos)
   * [Entrenar el modelo](#Entrenar-el-modelo)
   * [Referencias](#Referencias)
<!--te-->

### Resultados Obtenidos
Nuestra red neuronal es capaz de sub-muestrear una imagen de entrada en un factor K = 4, penalizando las frecuencias altas con el fin de evitar efectos de aliasing en la imagen re-muestreada. 

La arquitectura de alto nivel del sistema se representa a continuación; el usuario debe elegir si la imagen se sub-muestreara en los tres canales de color o en un solo canal representado como escala de grises.

![arquitectura alto nivel](Modelos_guardados/arquitectura_alto_nivel_sistema.png)

**Imagen de entrada HR**

![Lenna - Imagen de entrada HR](Imagenes_HR/lenna.png)

**Imagen de salida LR en RGB o escala de grises**

![Lenna - Imagen de salida LR rgb](Imagenes_LR/lenna_bgr_sub-muestreada.png)
![Lenna - Imagen de salida LR gris](Imagenes_LR/lenna_gray_sub-muestreada.png)

**Imagen de entrada HR**

![Planta - Imagen de entrada HR](Imagenes_HR/planta.png)

**Imagen de salida LR en RGB o escala de grises**

![Planta - Imagen de salida LR](Imagenes_LR/planta_bgr_sub-muestreada.png)
![Planta - Imagen de salida LR](Imagenes_LR/planta_gray_sub-muestreada.png)


## Ejecutar el modelo pre-entrenado

Antes de ejecutar el sistema, por favor introduzca las imágenes en alta resolución dentro
del directorio [Imagenes_HR](Imagenes_HR). El sistema podrá ser ejecutado para sub-muestrear todas las imágenes contenidas en el directorio HR, o, sub-muestrear una sola imagen
especificada por el usuario a través del nombre del archivo.

Para ejecutar el modelo pre-entrenado, corra el código [validacion_sub-muestreo_imagenes.py](validacion_sub-muestreo_imagenes.py), ubicado de forma absoluta en la raíz del repositorio. Se le solicitará al usuario introducir el color del canal o canales a extraer.

```python
channel = input("\nPor favor, introduza el canal a sub-muestrear: 'gray' para escala de grises, 'bgr' para canales de color: ")
```

También se le solicitará introducir el caso especifico de sub-muesteo.

```python
print("\nPor favor, seleccione el caso adecuado:")
print("1. Se sub-muestrearan todas las imagenes dentro del directorio Imagenes_HR")
print("2. Se sub-muestreara una imagen especifica en el directorio Imagenes_HR")
caso = int(input("Caso: "))
```

Los resultados serán almacenados en el directorio [Imagenes_LR](Imagenes_LR). Este repositorio cuenta con dos imágenes de prueba (enseñadas anteriormente) dentro del directorio de imágenes de alta resolución.

## Generación del conjunto de datos

La generación del conjunto de datos consiste en dos pasos: sub-muestrear espacialmente las imágenes del conjunto de datos de [Common Objects in Context](https://cocodataset.org/#termsofuse) (*Imágenes pertenecientes a [Flickr](https://www.flickr.com/creativecommons/) con licencia [Creative Commons](https://creativecommons.org/licenses/by/4.0/legalcode)*) y la creación de los conjuntos de datos de entrenamiento y validación en formato .csv.

Las imágenes a sub-muestrear se encuentran en el directorio [Dataset/X](Dataset/X) y estas deben estar en formato .png. 

Ejecute el código [decimacion_espacial_linux.py](Dataset/decimacion_espacial_linux.py) o [decimacion_espacial_windows.py](Dataset/decimacion_espacial_windows.py) (de acuerdo a su sistema operativo) en la ubicación absoluta [/Dataset/](Dataset). Los códigos se diferencian en que, en Linux, se aplica multiproceso en 4 núcleos de la CPU para optimizar el proceso de sub-muestreo. 

Se le solicitará al usuario introducir el factor K de sub-muestreo.
También se le solicitará introducir el caso especifico de sub-muesteo.

```ruby
K = int(input("\nPor favor, introduzca el factor de sub-muestreo, debe ser divisible entre 2 en la medida de lo posible (se tomara el numero entero del valor introducido): "))
```

Además, se solicitará introducir el número de iteraciones o filtros para probar con cada imagen.

```ruby
itr = int(input("Por favor, introduzca el numero de iteraciones para optimizar la sub-muestreo de cada imagen (se tomara el numero entero del valor introducido): "))
```

Lo anterior con el fin de identificar el filtro con el mínimo error absoluto medio local en el número de iteraciones. El error absoluto medio se calcula a partir de la imagen filtrada y sub-muestreada, que es sobre-muestreada (escalada) por el mismo factor K y es comparada con la imagen original en alta resolución. Se evalúan los 'itr' filtros especificados por el usuario y se elige el mejor almacenando sus resultados.

El código anterior generará los siguientes directorios respectivamente: [Y](Dataset/Y), [Filtros_Gaussianos](Dataset/Filtros_Gaussianos), [Interpolacion_bicubica](Dataset/Interpolacion_bicubica), los cuales almacenarán las imágenes originales sub-muestreadas en los tres canales de color, La función de transferencia, en frecuencia, del filtro implementado en cada imagen, y por último, la escalización a partir de una interpolación bicúbica de las imágenes resultantes en [Y](Dataset/Y), esto último para motivos prácticos de evaluación a desarrollar más adelante en el protocolo de pruebas del sistema.


**Imagen contenida dentro [X](Dataset/X)**

![Imagen HR](Dataset/X/000000000009.png)

**Filtro Gaussiano almacenado en [Filtros_Gaussianos](Dataset/Filtros_Gaussianos) aplicado sobre la imagen anterior**

![Filtro Gaussiano](Dataset/Filtros_Gaussianos/flt_gaussian_000000000009.png)

**Imagen sub-muestreada almacenada en [Y](Dataset/Y)**

![Imagen LR](Dataset/Y/LR_000000000009.png)

**Imagen sub-muestreada pero sobre-muestreada en el mismo factor, almacenada en [Interpolacion_bicubica](Dataset/Dataset/Interpolacion_bicubica)**

![Imagen LR](Dataset/Interpolacion_bicubica/bicHR_000000000009.png)

Una vez el primer paso es ejecutado, se debe realizar el segundo paso: la creación de los conjuntos de datos en formato .csv. Para esto, ejecute el código [crear_dataframe.py](Dataset/crear_dataframe.py) ubicado de forma absoluta en el directorio [/Dataset/](Dataset). Se solicitará al usuario introducir cuál canal de color desea extraer en formato .csv.

```python
channel = input("\nPor favor, introduza el canal a extraer: 'gray' para escala de grises, 'bgr' para canales de color: ")
```

De seleccionar el canal 'gray', se creará y escribirá un archivo .csv llamado [gray_channel.csv](Dataset/gray_channel.csv). Si se seleccionan los tres canales de color RGB, se crearán y escribirán los siguientes archivos: [blue_channel.csv](Dataset/blue_channel.csv), [green_channel.csv](Dataset/green_channel.csv), [red_channel.csv](Dataset/red_channel.csv). Los archivos anteriores son los contenedores del conjunto de datos para entrenar y evaluar a la red neuronal sub-muestreadora de imágenes.

NOTA: la decimacion espacial introduce efectos de espejo en la primera fila de pixeles en algunas imagenes, esto se debe a que el proceso se realiza en el dominio de la frecuencia y es necesario centralizar las frecuencias bajas aplicando una dft shift para poder operar la imagen con el filtro en frecuencia, y realizar el proceso inverso. Por dimensiones pares de las imágenes, se presentan estos efectos en los bordes. Por lo tanto, se filtran las muestras ruidosas, i.e. aquellas muestras cuyas salidas no se encuentren dentro del rango de sus caracteristicas.

```python
# Se filtran las muestras ruidosas
if np.max(X) >= Y and np.min(X) <= Y:
    writer.writerow([X[0], X[1], X[2], X[3], X[4], X[5], X[6], X[7], X[8], X[9], X[10], X[11], X[12], X[13], X[14], X[15], Y]) 
```

**5 primeras muestras en el conjunto de datos [blue_channel.csv](Dataset/blue_channel.csv)**

```
X1,X2,X3,X4,X5,X6,X7,X8,X9,X10,X11,X12,X13,X14,X15,X16,Y
153.0,153.0,150.0,149.0,151.0,151.0,152.0,153.0,155.0,153.0,155.0,157.0,154.0,154.0,158.0,162.0,149.0
155.0,152.0,149.0,142.0,150.0,146.0,141.0,136.0,149.0,142.0,134.0,126.0,146.0,137.0,128.0,116.0,116.0
131.0,117.0,108.0,90.0,123.0,109.0,99.0,81.0,112.0,98.0,86.0,75.0,99.0,90.0,76.0,67.0,82.0
70.0,65.0,49.0,36.0,63.0,54.0,41.0,31.0,54.0,46.0,34.0,25.0,50.0,43.0,31.0,16.0,47.0
15.0,11.0,5.0,0.0,19.0,13.0,5.0,1.0,22.0,15.0,6.0,2.0,22.0,12.0,4.0,1.0,12.0
```

## Entrenar el modelo

**Arquitectura de la red neuronal para regresión:**

![arquitectura red neuronal](Modelos_guardados/modelo.png)

Cada muestra tiene 16 caracteríticas, las cuales se no-linealizan con el cuadrado de estas mismas y la multiplicación entre estas, obteniendo un total de 48 características de entrada en la red. 
Después de la capa de entrada, tiene una capa para normalizar las muestras de entrada a partir de una normalización con media y desviación estándar del conjunto de datos de entrenamiento.

La red neuronal tiene una sola capa interna de 16 neuronas activados a partir de una funcion 'relu' y una sola neurona en la capa de salida, ademas, la funcion de perdida de cada perceptron estará regularizada por una norma L2 y una norma L1 (ElasticNet) en un factor alfa l1 y l2 dado por el usuario, esto con el fin de actualizar los pesos en cantidades menores para hacer la red mas robusta al ruido local en el conjunto de datos no-linealizado.

Antes de entrenar el modelo, asegúrese de haber ejecutado los códigos anteriores para la generación del conjunto de datos y la obtención de los archivos  [gray_channel.csv](Dataset/gray_channel.csv), [blue_channel.csv](Dataset/blue_channel.csv), [green_channel.csv](Dataset/green_channel.csv), [red_channel.csv](Dataset/red_channel.csv).

Para entrenar al modelo, ejecute el código [entrenamiento.py](entrenamiento.py) ubicado de forma absoluta en la raíz del repositorio. Se solicitará al usuario ingresar los hiper parámetros para compilar y entrenar la red neuronal.

```python
# Ingresar los hiper parametros para el entrenamiento de la red neuronal:
# Algunos hiper-parametros sugeridos se afinaron de acuerdo a https://www.tensorflow.org/tutorials/keras/keras_tuner
alfa_train = float(input("\nPor favor, ingrese el valor inicial del factor de aprendizaje (0.01 es el valor optimo determinado por el afinador de hiper-parametros): "))
alfa_reg_l1 = float(input("\nPor favor, ingrese el valor el factor de regularizacion l1 (1e-7 es el valor optimo determinado por el afinador de hiper-parametros): "))
alfa_reg_l2 = float(input("\nPor favor, ingrese el valor el factor de regularizacion l2: (1e-5 es el valor optimo determinado por el afinador de hiper-parametros) "))
batch_sz = int(input("\nPor favor, ingrese el numero de datos por cada lote de entrenamiento: "))
epchs = int(input("\nPor favor, ingrese el numero epochs (repeticiones por cada muestra): "))
```

También se solicitará introducir el conjunto de datos a utilizar para cada canal de color respectivamente. Para cada canal de color, se almacenará el modelo entrenado en [Modelos_guardados](Modelos_guardados)

```python
# Especificar si se quiere entrenar con el conjunto de datos en escala de grises o los conjuntos de datos para los tres canales de color
channel = input("\nPor favor, introduza los canales de color a ser utilizados como conjunto de datos; 'gray' para escala de grises, 'bgr' para canales de color: ")
```

Si se elige el canal de color en escala de grises, se almacenará el modelo entrenado en [Modelos_guardados/Modelo_gris_guardado](Modelos_guardados/Modelo_gris_guardado). Si se elige los tres canales de color, se guardarán tres modelos entrenados respectivamente en [Modelos_guardados/Modelo_azul_guardado](Modelos_guardados/Modelo_azul_guardado), [Modelos_guardados/Modelo_verde_guardado](Modelos_guardados/Modelo_verde_guardado), [Modelos_guardados/Modelo_rojo_guardado](Modelos_guardados/Modelo_rojo_guardado).

Todo el registro del entrenamiento es guardado en un archivo de texto [bgr_entrenamiento.log](bgr_entrenamiento.log), o [gray_entrenamiento.log](gray_entrenamiento.log), para destacar, acá se encuentra el desempeño de cada modelo entrenado versus épocas y las métricas evaluadas sobre el modelo entrenado. 

Se utilizó la métrica R2 o coeficiente de determinación para evaluar el modelo de regresión entrenado. La ecuación implementada se obtuvó de [Coeficiente de Determinación.](https://en.wikipedia.org/wiki/Coefficient_of_determination)

```
Coeficientes de determinacion en cada modelo entrenado:
Para blue_channel.csv, R2 = 0.986496 
Para green_channel.csv, R2 = 0.983607 
Para red_channel.csv, R2 = 0.984299 
Para gray_channel.csv, R2 = 0.983838 
```

También se genera y almacena una gráfica en [Modelos_guardados/entrenamiento_gray.png](Modelos_guardados/entrenamiento_gray.png), [Modelos_guardados/entrenamiento_bgr.png](Modelos_guardados/entrenamiento_bgr.png), que muestran el desempeño de cada modelo versus las épocas en las que se entrenó. El error es el [error absoluto medio](https://en.wikipedia.org/wiki/Mean_absolute_error). 

![rendimiento entrenamiento canal gray](Modelos_guardados/entrenamiento_gray.png)

![rendimiento entrenamiento canal bgr](Modelos_guardados/entrenamiento_bgr.png)

### Referencias
