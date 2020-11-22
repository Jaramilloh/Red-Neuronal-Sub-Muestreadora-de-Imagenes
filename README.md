# Red Neuronal Sub-Muestreadora de Imágenes
Este repositorio contiene el código fuente y los materiales para el proyecto de la Red Neuronal Sub-Muestreadora de Imágenes, desarrollado en la asignatura de enfásis "Inteligencia Artificial" en el programa de Ingeniería Electrónica de la Pontificia Universidad Javeriana. ***Autores: Juan Felipe Jaramillo Hernández, María Fernanda Hernández Baena, Jose David Cifuentes Semanate.***

Este repositorio contiene los códigos para [entrenar](entrenamiento.py) y [validar](validacion_sub-muestreo_imagenes.py) la red neuronal, además de los códigos para la [generación](Dataset/) del [conjunto de datos](Dataset/crear_dataframe.py) a partir de los recursos disponibles en [Common Objects in Context](https://cocodataset.org/#termsofuse) (*Imágenes pertenecientes a [Flickr](https://www.flickr.com/creativecommons/) con licencia [Creative Commons](https://creativecommons.org/licenses/by/4.0/legalcode)*). También se encuentra un modelo pre-entrenado para cada canal de color o para escala de grises. El video y el artículo se pueden encontrar acá:

Video: <>
Artículo: <>

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
Asegúrese de clonar el repositorio y ejecutar los scripts de forma relativa en el directorio raíz
del repositorio.

Antes de ejecutar el sistema, por favor introduzca las imágenes en alta resolución dentro
del directorio [Imagenes_HR](Imagenes_HR). El sistema podrá ser ejecutado para sub-muestrear todas las imágenes contenidas en el directorio HR, o, sub-muestrear una sola imagen
especificada por el usuario a través del nombre del archivo.

Para ejecutar el modelo pre-entrenado, corra el código [validacion_sub-muestreo_imagenes.py](validacion_sub-muestreo_imagenes.py). Se le solicitará al usuario introducir el color del canal o canales a extraer.

```ruby
channel = input("\nPor favor, introduza el canal a sub-muestrear: 'gray' para escala de grises, 'bgr' para canales de color: ")
```

También se le solicitará introducir el caso especifico de sub-muesteo.
```ruby
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

Una vez el primer paso es ejecutado, se debe realizar el segundo paso: la creación de los conjuntos de datos en formato .csv. Para esto, ejecute el código [crear_dataframe.py](Dataset/crear_dataframe.py) ubicado de forma absoluta en el directorio [/Dataset/](Dataset). Se solicitará al usuario introducir cuál canal de color desea extraer en formato .csv.
```ruby
channel = input("\nPor favor, introduza el canal a extraer: 'gray' para escala de grises, 'bgr' para canales de color: ")
```
De seleccionar el canal 'gray', se creará y escribirá un archivo .csv llamado [gray_channel.csv](Dataset/gray_channel.csv). Si se seleccionan los tres canales de color RGB, se crearán y escribirán los siguientes archivos: [blue_channel.csv](Dataset/blue_channel.csv), [green_channel.csv](Dataset/green_channel.csv), [red_channel.csv](Dataset/red_channel.csv). Los archivos anteriores son los contenedores del conjunto de datos para entrenar y evaluar a la red neuronal sub-muestreadora de imágenes.


## Entrenar el modelo
La arquitectura de la red neuronal se compone de la siguiente manera:
