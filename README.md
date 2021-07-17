## Raspberry Pi 3B+ Lectura de Wiegand
Lectura de WIEGAND mediante rasperry

### Descripción
Codigo para la lectura de tags/tarjetas RFID mediante una lectora de RFID conectada a una Raspberry Pi con Pigpio.

### Requisitos 
* Python 2.7
* [Pigpio](http://abyz.me.uk/rpi/pigpio/download.html)
* Tener en cuenta que la raspberry pi (cualquier versión) trabaja con entradas en GPIO de 3.3 volts, es recomendable realizar un divisor de voltaje de al menos esta cantidad y hasta un pico de 3.5 volts, en cuestión de lo que se ha trabajado, este divisor no trabaja como uno "normal", ya que los valores adecuados en teoría serian con R1 = 100R y R2 = 220R dando un voltaje aproximado de 3.43 volts, esto en práctica no es así (al menos para el modelo de la lectora testeada la cual es una ROSSLARE AY-Z12A), en las pruebas la R1 = 100R y R2 = 2.2k, esto arroja en práctica un voltaje de 3.32 volts.
### Instalación de Pigpio
    $ sudo apt-get update
    $ sudo apt-get install pigpio python-pigpio python3-pigpio


### Instrucciones de uso 

    $ sudo pigpiod
    $ git clone https://github.com/chosen99/wiegand_py.git
    $ cd wiegand_py
    $ python wiegand.py


### Metodo de conexión 
* GPIO (BCM)
* Se necesita conectar el cable verde (D0) en el GPIO 14 y el cable blanco (D1) en el GPIO 15.
* Tambien es requerido conectar la tierra (GND) de la lectora a la Raspberry en un pin GND, de lo contrario esto genera que haya ruido durante la lectura y los datos no puedan ser interpretados correcatmente.
