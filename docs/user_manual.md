# Manual de Usuario de AlgoriPS

## 1. Introducción a AlgoriPS
AlgoriPS es una plataforma que ayuda a gestionar y aplicar parches semánticos en proyectos de software. Sirve para automatizar tareas de análisis, pruebas y despliegues de forma sencilla.

## 2. Instalación paso a paso
### 2.1 CLI
1. Clona el repositorio.
2. Ejecuta `pip install -r requirements.txt` para instalar dependencias.
3. Ejecuta `python -m algorips` para iniciar la interfaz de línea de comandos.

### 2.2 GUI
1. Ve a la carpeta `gui` y ejecuta `npm install`.
2. Usa `npm start` para abrir la interfaz gráfica en tu navegador.

### 2.3 Plugins
1. Los plugins viven en la carpeta `plugins`.
2. Copia o crea nuevos plugins aquí y reinicia la aplicación para que se carguen.

## 3. Tutorial básico de Docker
Docker te permite poner tu aplicación en una “cajita” llamada contenedor. Esta cajita incluye todo lo necesario para que funcione. Para usar Docker:
1. Instala Docker desde su sitio oficial.
2. Corre `docker build -t miimagen .` para crear la imagen.
3. Ejecuta `docker run miimagen` y listo. Piensa en esto como armar un juguete siguiendo un instructivo muy claro.

## 4. Tutorial básico de GitHub Actions
GitHub Actions es como una cadena de robots que hacen tareas cuando subes código. Cada robot es un paso del pipeline. Un ejemplo simple:
1. Cuando haces push, un robot instala las dependencias.
2. Otro robot corre las pruebas.
3. Si todo pasa, otro robot despliega tu app. ¡Y tú no tienes que hacerlo manualmente!

## 5. Tutorial básico de Python, Node.js y React
- **Python**: lenguaje sencillo para crear scripts. Usa `python archivo.py` para ejecutarlos.
- **Node.js**: entorno para correr JavaScript en servidor. Instala paquetes con `npm install paquete`.
- **React**: biblioteca para crear interfaces web. Inicia un proyecto con `npx create-react-app miapp`.

## 6. FAQs y troubleshooting
**¿No se instala algo?** Revisa que tengas internet y los permisos correctos.
**¿Fallan las pruebas?** Ejecuta `pytest -vv` para ver detalles.
**¿La GUI no carga?** Asegúrate de haber ejecutado `npm install` y luego `npm start` en la carpeta `gui`.
