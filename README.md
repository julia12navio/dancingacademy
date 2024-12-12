Instrucciones para descargar el proyecto
A este proyecto se podrá acceder siempre que el servidor alojado en AWS esté activado. Pero si
queremos instalar el repositorio de dancingacademy deberemos seguir diferentes pasos.
Repositorio en GitHub: https://github.com/julia12navio/dancingacademy
1. Se deberá tener instalado odoo.
2. Descargar módulos.
Este paso se puede hacer de dos formas. O bien descargando las módulos del
repositorio en el directorio de addons o bien descargando el repositorio y añadiendo la
ruta a addons_path en odoo.conf.
  a) Descargar módulos en addons.
      1. Acceder al directorio addons con ruta /opt/odoo/odoo/addons
      2. Descargar todas las carpetas del repositorio en addons. Estos son las
      carpetas que se deben añadir:
      - dancingacademy_attendance
      - dancingacademy_base
      - dancingacademy_classes
      - dancingacademy_members
      - dancingacademy_monthly
      - dancingacademy_website
      3. Reiniciar servidor
      4. Acceder a Odoo.
      5. Ir a aplicaciones y actualizar la lista de aplicaciones.
      6. Buscar los módulos que se han descargado e instalarlos.
  b) Descargar repositorio.
      1. Decidir en qué carpeta queremos nuestro repositorio. Lo
      recomendable es tenerla en la ruta /opt/odoo/odoo
      2. Descargar el repositorio.
      git clone https://github.com/julia12navio/dancingacademy.git
      Ahora tendremos la ruta de carpetas
      /opt/odoo/odoo/dancingacademy
      3. Ir a odoo.conf
      En el caso de mi máquina esta en esta ruta de carpetas
      /etc/odoo/odoo.conf
      4. Editar odoo.conf
      Tiene que tener una estructura parecida a la del cuadro de texto de
      debajo de las instrucciones. En addons_path añadimos la ruta donde
      hemos descargado el repositorio.
      5. Reiniciar Servidor
      6. Acceder a Odoo
      7. Ir a aplicaciones y actualizar la lista de aplicaciones.
      8. Buscar los módulos de dancingacademy e instalarlos.
