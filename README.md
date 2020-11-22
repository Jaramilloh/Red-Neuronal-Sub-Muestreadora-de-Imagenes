# Red-Neuronal-Sub-Muestreadora-de-Imagenes
Este repositorio contiene el código fuente y los materiales para el proyecto de la Red Neuronal Sub-Muestreadora de Imágenes, desarrollado en la asignatura de enfásis "Inteligencia Artificial" en el programa de Ingeniería Electrónica de la Pontificia Universidad Javeriana. ***Autores: Juan Felipe Jaramillo Hernández, María Fernanda Hernández Baena, Jose David Cifuentes Semanate.***

Este repositorio contiene los códigos para entrenar y validar la red neuronal, además de los códigos para la generación del conjunto de datos a partir de los recursos disponibles en [Common Objects in Context](https://cocodataset.org/#termsofuse) (*Imágenes pertenecientes a [Flickr](https://www.flickr.com/creativecommons/) con licencia [Creative Commons](https://creativecommons.org/licenses/by/4.0/legalcode)*). También se encuentra un modelo pre-entrenado para cada canal de color o para escala de grises. El video y el artículo se pueden encontrar acá:

Video: <>
Preprint: <>

### Resultados Obtenidos
Nuestra red neuronal es capaz de sub-muestrear una imagen en un factor K = 4, penalizando las frecuencias altas con el fin de evitar efectos de aliasing en la imagen re-muestreada, más adelante se explicará en más detalle el proceso de aprendizaje de la red neuronal. La arquitectura de alto nivel del sistema se representa a continuación:


![arquitectura alto nivel](Modelos_guardados/arquitectura_alto_nivel_sistema.png)



[Lenna - Imagen de entrada HR](Imagenes_HR/lenna.png)
![Lenna - Imagen de salida LR rgb](Imagenes_LR/lenna_bgr_sub-muestreada.png)
![Lenna - Imagen de salida LR gris](Imagenes_LR/lenna_gray_sub-muestreada.png)

![Planta - Imagen de entrada HR](Imagenes_HR/planta.png)
![Planta - Imagen de salida LR](Imagenes_LR/planta_bgr_sub-muestreada.png)
![Planta - Imagen de salida LR](Imagenes_LR/planta_gray_sub-muestreada.png)
