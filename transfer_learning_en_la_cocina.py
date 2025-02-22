# -*- coding: utf-8 -*-
"""Transfer Learning en la cocina

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kijMzfl1Mk3WytCWt7Yc4DGOAvWirwF9
"""

#Mostrar algunas imagenes con pyplot
#Categorizar una imagen de internet
from PIL import Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from io import BytesIO
import requests
import cv2
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import shutil

plt.figure(figsize=(15,15))

# data:
# ['T-shirt/top',
#'Trouser',
#'Pullover',
#'Dress',
#'Coat',
#'Sandal',
#'Shirt',
#'Sneaker',
#'Bag',
# 'Ankle boot']

carpeta = './content/ankle_boot'
imagenes = os.listdir(carpeta)

for i, nombreimg in enumerate(imagenes[:25]):
  plt.subplot(5,5,i+1)
  imagen = mpimg.imread(carpeta + '/' + nombreimg)
  plt.imshow(imagen)

#Crear carpetas para hacer el set de datos

#mkdir dataset
#mkdir dataset/cuchillo
#mkdir dataset/tenedor
#mkdir dataset/cuchara
#Copiar imagenes que subimos a carpetas del dataset

#Limitar para que todos tengan la misma cantidad de imagenes
#maximo 419 (el num. menor de imagenes que subi)

carpeta_fuente = './content/ankle_boot'
carpeta_destino = './content/ankle_boot/dataset/'

imagenes = os.listdir(carpeta_fuente)
count_images = 210 

for i, nombreimg in enumerate(imagenes):
    if i < count_images:
    #Copia de la carpeta fuente a la destino
     shutil.copy(carpeta_fuente + '/' + nombreimg, carpeta_destino + '/' + nombreimg)

carpeta_fuente = './content/bag'
carpeta_destino = './content/bag/dataset'

imagenes = os.listdir(carpeta_fuente)

for i, nombreimg in enumerate(imagenes):
  if i < count_images:
    #Copia de la carpeta fuente a la destino
    shutil.copy(carpeta_fuente + '/' + nombreimg, carpeta_destino + '/' + nombreimg)

carpeta_fuente = './content/coat'
carpeta_destino = './content/coat/dataset/'

imagenes = os.listdir(carpeta_fuente)

for i, nombreimg in enumerate(imagenes):
  if i < count_images:
    #Copia de la carpeta fuente a la destino
    shutil.copy(carpeta_fuente + '/' + nombreimg, carpeta_destino + '/' + nombreimg)

carpeta_fuente = './content/dress'
carpeta_destino = './content/dress/dataset/'

imagenes = os.listdir(carpeta_fuente)

for i, nombreimg in enumerate(imagenes):
  if i < count_images:
    #Copia de la carpeta fuente a la destino
    shutil.copy(carpeta_fuente + '/' + nombreimg, carpeta_destino + '/' + nombreimg)

carpeta_fuente = './content/pullover'
carpeta_destino = './content/pullover/dataset/'

imagenes = os.listdir(carpeta_fuente)

for i, nombreimg in enumerate(imagenes):
  if i < count_images:
    #Copia de la carpeta fuente a la destino
    shutil.copy(carpeta_fuente + '/' + nombreimg, carpeta_destino + '/' + nombreimg)

carpeta_fuente = './content/sandal'
carpeta_destino = './content/sandal/dataset/'

imagenes = os.listdir(carpeta_fuente)

for i, nombreimg in enumerate(imagenes):
  if i < count_images:
    #Copia de la carpeta fuente a la destino
    shutil.copy(carpeta_fuente + '/' + nombreimg, carpeta_destino + '/' + nombreimg)

carpeta_fuente = './content/sneaker'
carpeta_destino = './content/sneaker/dataset/'

imagenes = os.listdir(carpeta_fuente)

for i, nombreimg in enumerate(imagenes):
  if i < count_images:
    #Copia de la carpeta fuente a la destino
    shutil.copy(carpeta_fuente + '/' + nombreimg, carpeta_destino + '/' + nombreimg)

carpeta_fuente = './content/trouser'
carpeta_destino = './content/trouser/dataset/'

imagenes = os.listdir(carpeta_fuente)

for i, nombreimg in enumerate(imagenes):
  if i < count_images:
    #Copia de la carpeta fuente a la destino
    shutil.copy(carpeta_fuente + '/' + nombreimg, carpeta_destino + '/' + nombreimg)

carpeta_fuente = './content/tshirt'
carpeta_destino = './content/tshirt/dataset/'

imagenes = os.listdir(carpeta_fuente)

for i, nombreimg in enumerate(imagenes):
  if i < count_images:
    #Copia de la carpeta fuente a la destino
    shutil.copy(carpeta_fuente + '/' + nombreimg, carpeta_destino + '/' + nombreimg)


#Mostrar cuantas imagenes tengo de cada categoria en el dataset
#ls /content/dataset/cuchara | wc -l
#ls /content/dataset/cuchillo | wc -l
#ls /content/dataset/tenedor | wc -l

#Aumento de datos con ImageDataGenerator
#Crear el dataset generador
datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range = 30,
    width_shift_range = 0.25,
    height_shift_range = 0.25,
    shear_range = 15,
    zoom_range = [0.5, 1.5],
    validation_split=0.2 #20% para pruebas
)

#Generadores para sets de entrenamiento y pruebas
data_gen_entrenamiento = datagen.flow_from_directory('/content/dataset', target_size=(224,224),
                                                     batch_size=32, shuffle=True, subset='training')
data_gen_pruebas = datagen.flow_from_directory('/content/dataset', target_size=(224,224),
                                                     batch_size=32, shuffle=True, subset='validation')

#Imprimir 10 imagenes del generador de entrenamiento
for imagen, etiqueta in data_gen_entrenamiento:
  for i in range(10):
    plt.subplot(2,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(imagen[i])
  break
plt.show()

url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4"
mobilenetv2 = hub.KerasLayer(url, input_shape=(224,224,3))

#Congelar el modelo descargado
mobilenetv2.trainable = False

modelo = tf.keras.Sequential([
    mobilenetv2,
    tf.keras.layers.Dense(3, activation='softmax')
])

modelo.summary()

#Compilar como siempre
modelo.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

#Entrenar el modelo
EPOCAS = 50

historial = modelo.fit(
    data_gen_entrenamiento, epochs=EPOCAS, batch_size=32,
    validation_data=data_gen_pruebas
)

#Graficas de precisión
acc = historial.history['accuracy']
val_acc = historial.history['val_accuracy']

loss = historial.history['loss']
val_loss = historial.history['val_loss']

rango_epocas = range(50)

plt.figure(figsize=(8,8))
plt.subplot(1,2,1)
plt.plot(rango_epocas, acc, label='Precisión Entrenamiento')
plt.plot(rango_epocas, val_acc, label='Precisión Pruebas')
plt.legend(loc='lower right')
plt.title('Precisión de entrenamiento y pruebas')

plt.subplot(1,2,2)
plt.plot(rango_epocas, loss, label='Pérdida de entrenamiento')
plt.plot(rango_epocas, val_loss, label='Pérdida de pruebas')
plt.legend(loc='upper right')
plt.title('Pérdida de entrenamiento y pruebas')
plt.show()

def categorizar(url):
  respuesta = requests.get(url)
  img = Image.open(BytesIO(respuesta.content))
  img = np.array(img).astype(float)/255

  img = cv2.resize(img, (224,224))
  prediccion = modelo.predict(img.reshape(-1, 224, 224, 3))
  return np.argmax(prediccion[0], axis=-1)

#0 = cuchara, 1 = cuchillo, 2 = tenedor
url = 'https://th.bing.com/th/id/R.e44940120b7b67680af246c3b3e936f2?rik=XZPLfxf4nHlzyw&pid=ImgRaw&r=0' #debe ser 2
prediccion = categorizar (url)
print(prediccion)

#Crear la carpeta para exportarla a TF Serving
#mkdir -p carpeta_salida/modelo_cocina/1

#Guardar el modelo en formato SavedModel
#modelo.save('carpeta_salida/modelo_cocina/1')

#Hacerlo un zip para bajarlo y usarlo en otro lado
#zip -r modelo_cocina.zip /content/carpeta_salida/modelo_cocina/
