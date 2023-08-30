# WavTrigger Project Manual
## Indice
- [Introduction](#introduction)
- [Informacion General](#informacion-general)
- [Hardware](#hardware)
- [Software](#software)
- [WavTrigger](#wavtrigger)
- [Renamer.py](#renamerpy)
    - [Atajos de teclado](#atajos-de-teclado)

## Introduction
Este proyecto consiste en la creación de un sistema de reproducción de audio mediante un microcontrolador Arduino y un módulo de reproducción de audio WavTrigger. El sistema se controla desde una matriz de 9 botones, donde 8 equivalen a un numero asignado y el último a un botón para detener todos los audios. Además, se implementó un sistema de bancos de audios, donde se pueden almacenar hasta 8 audios por cada botón, y se puede cambiar de banco mediante los botones de subir o bajar en el shield del LCD.


## Informacion General

Los archivos deben renombrarse antes de ser cargados en la MicroSD. Para esto se creó un script en Python que permite renombrar los archivos de forma automática, según el número de botón y el banco en el que se encuentre. 

Para renombrarse de forma manual se debe seguir el siguiente formato: 
```
001_pista1-banco1.wav
002_pista2-banco1.wav
...
009_pista9-banco2.wav
``` 
Cada 8 pistas se cambia de banco.

Los botones del shield tienen su función asignada de la siguiente forma:
```
UP: Subir banco
DOWN: Bajar banco
LEFT: Pausa el audio actual
RIGHT: Continua la reproducción del audio actual
SELECT: Detener todos los audios
```

## Hardware
- Arduino UNO
- WavTrigger
- LCD Keypad Shield
- Matriz de 9 botones (ya creada)

La conexion serial al WavTrigger se conecta de la sigueinte forma:
realiza conectando el pin 9 del Arduino al pin RX del WavTrigger y el pin 8 del Arduino al pin TX del WavTrigger
```
Arduino          WavTrigger
Pin8      <--->  TX
Pin9      <--->  RX
GND       <--->  GND
```

La matriz de botones, se conecta de la siguiente forma:
```
P <---> VCC 5V
N <---> GND
s <---> Pin A0
```

Importante: Tanto el WavTrigger como el arduino deben tener alimentacion externa por separado, aunque se le puede conectar el pin VCC del WavTrigger al pin 5V del Arduino, pero no es recomendable. **El WavTrigger debe tener una alimentacion de 5V**.

## Software
- Arduino IDE
- Python 3.7

  
**Se requieren las librerias WavTrigger, LiquidCrystal, AltSoftSerial, Metro para el funcionamiento del sistema. Las carpetas estan incluidas en este repositorio, deben ser movidas a la carpeta de libraries de ArduinoIDE** 

Dentro del codigo se pueden modificar ciertos valores para adaptarlos a las necesidades del usuario. Estos son:

```cpp
// En la linea 150 a la 158. Activa los sonidos en modo LOOP
    if (sonido == 1) {
      wav.trackLoop(1, 1);
    }
    if (sonido == 15) {
      wav.trackLoop(15, 1);
    }
    if (sonido == 16) {
      wav.trackLoop(16, 1);
    }
    if (sonido == #) {
      wav.trackLoop(#, 1);
    }
```
    
```cpp
// En la linea 160 a la 164. Activa los sonidos en modo SOLO o POLY (dependiendo del sonido)
    if (sonido == 17) {
      wav.trackPlayPoly(17);
    } else {
      wav.trackPlaySolo(sonido);
    }
```

## WavTrigger
En cualquier cambio en el codigo del arduino el WavTrigger debe ser reiniciado para que los cambios se apliquen, si no, los cambios en el codigo anterior seguirán funcionando.

Los triggers en el WaveTrigger se asignan de la siguiente forma: se asignan a las pistas en ese orden, y el boton reproduce la pista 1, se usa para debug. El switch debe estar en modo RUN para que funcione el sistema, si no, no se reproducirá nada y posiblemente el WavTrigger se apague.

## Renamer.py
Este script permite renombrar los archivos de forma automática, según el orden en que se añada la pista. 

Al abrir la ventana, se debe seleccionar los archivos que se desean renombrar en orden, es decir si ingreso la pista `perro.wav` y luego `gato.wav`, despues de renombrar, el archivo `perro.wav` se llamará `001_perro.wav` y el archivo `gato.wav` se llamará `002_gato.wav`.

Los archivos deben ser wav, y se debe seleccionar una carpeta de destino. Los archivos renombrados se guardarán en la carpeta seleccionada.

Doble click derecho o BackSpace en un archivo en la lista para eliminarlo.

Espacio en un archivo en la lista para reproducirlo.

`BaseName`: Al agregar un baseName, se le agregará al final del nombre de cada archivo, por ejemplo si el baseName es `pista`, el archivo `001_perro.wav` se llamará `001_perro_pista.wav`.

### Atajos de teclado
- `Ctrl + O:` Abrir archivos
- `Ctrl + S:` Seleccionar carpeta de destino
- `Ctrl + E:` Seleccionar carpeta de destino
- `Ctrl + R:` Renombrar archivos
- `Ctrl + Q:` Salir del programa
- `Ctrl + Enter:` Renombrar archivos
- `Insert:` Agregar archivos
- `A:` Agregar archivos
- `Delete:` Eliminar archivos seleccionados
- `Escape 2 veces:` Salir del programa
- `Enter:` Renombrar archivos

