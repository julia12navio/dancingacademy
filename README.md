# DancingAcademy

**Proyecto final de ciclo del Grado Superior de Desarrollo de Aplicaciones Multiplataforma (DAM).**

---

# Instrucciones para Descargar el Proyecto

Este proyecto estará disponible siempre que el servidor alojado en AWS esté activado. Sin embargo, si se desea instalar el repositorio de **DancingAcademy**, deberán seguirse los siguientes pasos.

Repositorio en GitHub: [https://github.com/julia12navio/dancingacademy](https://github.com/julia12navio/dancingacademy)

## Requisitos Previos
1. Tener **Odoo** instalado.

## Pasos para Descargar e Instalar los Módulos

Los módulos pueden descargarse de dos maneras:  
- Descargando directamente los módulos en el directorio `addons`.  
- Clonando el repositorio y añadiendo la ruta a `addons_path` en `odoo.conf`.

### Método 1: Descargar Módulos en `addons`
1. Acceder al directorio `addons` con la ruta `/opt/odoo/odoo/addons`.
2. Descargar las carpetas de módulos desde el repositorio en el directorio `addons`. Estas son las carpetas que se deben añadir:
   - `dancingacademy_attendance`
   - `dancingacademy_base`
   - `dancingacademy_classes`
   - `dancingacademy_members`
   - `dancingacademy_monthly`
   - `dancingacademy_website`
3. Reiniciar el servidor.
4. Acceder a Odoo.
5. Ir a **Aplicaciones** y actualizar la lista de aplicaciones.
6. Buscar los módulos descargados e instalarlos.

### Método 2: Descargar el Repositorio Completo
1. Seleccionar la carpeta donde se desea clonar el repositorio. Se recomienda usar la ruta `/opt/odoo/odoo`.
2. Clonar el repositorio ejecutando el siguiente comando:
   ```bash
   git clone https://github.com/julia12navio/dancingacademy.git
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
