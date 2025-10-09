# <center> Taller volumenes y redes en Docker </center>
<center>
Centro de Investigación y de Estudios Avanzados del Instituto Politécnico Nacional

<!-- ![Cinvestav logo](/imgs/logo2.jpg) -->
<img src="./imgs/logo2.jpg" alt="Cinvestav logo" width="200">

Este repositorio reune algunos ejemplos practicos que muestran de manera practica y teorica el funcionamiento de los volumnes, las monturas y las redes utilizando docker de forma inicial.
</center>

## Volumenes
<center>
Docker utiliza **mecanismos de montaje (mounts)** para compartir o persistir datos entre contenedores y el host.  
Estos montajes permiten que los datos sobrevivan a la eliminación de un contenedor o que se compartan entre varios.

![mounts ](/imgs/types-of-mounts-volume.png)

</center>

### Comandos basicos

|Comando|Descripcion|
|---|---|
|docker volume create NOMBRE|Crea un nuevo volumen de Docker con el nombre especificado.|
|---|---|
|docker volume ls|Lista todos los volúmenes de Docker en el sistema.|
|---|---|
|docker volume inspect NOMBRE|Muestra información detallada sobre un volumen específico (ruta, driver, etiquetas, etc.).|
|docker volume rm NOMBRE|Elimina un volumen específico.|


### 1. Volume (Volumen)

Los volúmenes son el mecanismo preferido para conservar los datos generados y utilizados por contenedores Docker. Si bien los montajes de enlace dependen de Estructura de directorios de la máquina host, los volúmenes son completamente administrados por Docker. Los volúmenes tienen varias ventajas sobre los montajes de enlace:

   * Es más fácil realizar copias de seguridad o migrar volúmenes que montajes enlazados.
   * Los volúmenes se pueden compartir de forma más segura entre varios contenedores.
   * Los controladores de volumen le permiten almacenar volúmenes en hosts remotos o proveedores de nube, para cifrar el contenido de los volúmenes o agregar otra funcionalidad.
   * Los nuevos volúmenes pueden tener su contenido rellenado previamente por un contenedor.

Además, los volúmenes suelen ser una mejor opción que conservar los datos en un la capa escribible del contenedor, porque un volumen no aumenta el tamaño del contenedores que lo utilizan y el contenido del volumen existe fuera del ciclo de vida de un contenedor dado. 

### 2. Bind Mounts (Montajes de enlace)

Los bind mounts en Docker son una forma de compartir un archivo o directorio del sistema de archivos del host (la máquina donde se ejecuta Docker) directamente con un contenedor.

Son esenciales para el desarrollo y para persistir datos, ya que el contenedor puede leer y escribir en esa ubicación del host, y los cambios son visibles inmediatamente en ambos lados.
* Permiten que los datos generados por el contenedor persistan incluso después de que este se detenga o se elimine, ya que están almacenados en el sistema de archivos del host. 
* El origen del mount es una ruta absoluta específica en el sistema de archivos del host.
* Los montajes de enlace no se administrados por Docker.

### 3. Tmpfs mounts
El tmpfs mount en Docker es una forma de montar un sistema de archivos temporal en un contenedor. A diferencia de los bind mounts o los volumes, los datos almacenados en un tmpfs mount nunca se escriben en el disco del host ni en el sistema de archivos de almacenamiento de Docker.

Todos los datos se almacenan exclusivamente en la memoria del host (RAM). Esto lo hace extremadamente rápido, pero no persistente.
* Los datos se guardan en la memoria del host (RAM). Esto ofrece un rendimiento de lectura y escritura muy alto.
* Tan pronto como el contenedor se detiene o se elimina, todos los datos almacenados en el tmpfs mount se pierden definitivamente.

## Redes 
</center>
La creación de redes Docker es crucial porque define cómo los contenedores se comunican entre sí, el sistema host y las redes externas. En aplicaciones en contenedores, diferentes servicios (como bases de datos, API y componentes front-end) a menudo se ejecutan en contenedores separados. Estos contenedores necesitan una red eficiente para la comunicación, la transferencia de datos y el escalado. El modelo de red de Docker simplifica la gestión y configuración de estas conexiones, garantizando aislamiento, seguridad y flexibilidad.

![networks ](/imgs/Redes.webp)
</center>

### Comandos basicos

|Comando|Descripcion|
|---|---|
|docker network create -d bridge NOMBRE|Crea una nueva red definida por el usuario.|
|docker network ls|Lista todas las redes de Docker en el sistema.|
|docker network inspect NOMBRE|Muestra información detallada sobre una red, incluyendo qué contenedores están conectados y sus IPs.|
|docker network rm NOMBRE|Elimina una red de Docker.|

### Bridge
El driver **bridge (puente)** es el driver de red predeterminado y más común que usa Docker. Esencialmente, crea una red virtual privada dentro del host (la máquina donde se ejecuta Docker) a la que se conectan todos los contenedores que no especifican otra red. Cuando Docker se instala, crea una interfaz de red virtual en el host, generalmente llamada docker0 (de ahí el nombre "puente"). Esta actúa como un conmutador (switch).
* Los contenedores conectados a la misma red bridge pueden comunicarse entre sí usando sus direcciones IP privadas.
* Docker configura reglas de NAT (Network Address Translation). El tráfico que sale del contenedor hacia internet (o la red externa) es enmascarado con la dirección IP pública del host.
* Por defecto, los contenedores son inaccesibles desde el exterior. Para exponer un servicio, debes usar la opción -p (publicar puertos) al ejecutar el contenedor. Docker usa iptables para mapear un puerto del host al puerto del contenedor.

### Host
El driver de red host en Docker es un modo de red que elimina el aislamiento de red entre el contenedor y el host (la máquina donde se ejecuta Docker). Cuando un contenedor se ejecuta con el driver host, comparte directamente la pila de red del host.
* El contenedor utiliza la dirección IP del host.
* El contenedor comparte los mismos puertos que el host. Si un servicio dentro del contenedor escucha en el puerto 80, ese servicio es accesible directamente en el puerto 80 del host, sin necesidad de mapeo de puertos (-p).
* Al eliminar el bridge de red y las capas de NAT (traducción de direcciones de red) que Docker normalmente configura, se logra la mejor latencia y rendimiento de red posible.
* Solo un servicio puede escuchar en un puerto específico a la vez. Si el host ya tiene un servidor web ejecutándose en el puerto 80, no puedes ejecutar un contenedor con network host que también intente usar el puerto 80.
* La configuración de red de tu contenedor pasa a depender del sistema operativo del host, lo que reduce la portabilidad.


### None
El driver de red **none** en Docker es el controlador de red más simple y estricto. Su propósito es deshabilitar completamente la interfaz de red de un contenedor.
* El contenedor está completamente aislado de la red del host, de internet y de cualquier otro contenedor. Es como si estuviera encerrado sin ningún cable de red conectado.
* Al no tener interfaz de red, no se le asigna una dirección IP.
* Solo puede comunicarse consigo mismo a través de la interfaz de loopback 








