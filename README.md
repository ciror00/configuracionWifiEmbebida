# Configuracion Wifi Embebida

Código en Micropython para configurar una red wifi desde un servidor montado en la misma placa. Se conmuta la modalidad AP y STA.

## Modo de funcionamiento

Se inicia la placa en modo *acces point* y se prende un servidor web, accesible desde la IP 192.168.4.1. Al conectarse en el servidor se muestra el formulario para cargar ***Red y Contraseña*** de la red wifi donde se desea conectar. Al seleccion la opcion *gurdar* la placa guarda los datos y cambios a modo *station* e intenta conectarse a la red que se configuró anteriormente.
