# Fase 2 – Uso y Pruebas de la GUI

## Objetivo de la fase
Proveer una interfaz gráfica mediante Electron y React para facilitar la interacción con el asistente.

## Requisitos Previos
- Node.js 18+
- Dependencias instaladas mediante `npm install` dentro de `gui/`.

## Instalación y Configuración
1. Ir a la carpeta `gui` y descargar dependencias:
   ```bash
   cd gui
   npm install
   ```
2. Iniciar la aplicación en modo desarrollo:
   ```bash
   npm run start
   ```

## Guía de Uso
- **Home**: seleccionar la carpeta de proyecto para analizar.
- **Analyze**: visualizar métricas y gráfica generada.
- **Diffs**: revisar archivos modificados y aplicar parches.
- **Tests**: ejecutar suites y examinar resultados.
- **Settings**: modificar opciones y guardarlas en `algorips.yaml`.

## Ejecución de Pruebas
Desde `gui/` ejecutar:
```bash
npm run test
```
Esto dispara Jest + React Testing Library y muestra la cobertura de componentes.

## Resultados Esperados
- La GUI se inicia mostrando la pantalla Home.
- Cada vista responde con transiciones suaves y diseño adaptativo.
- Todas las pruebas de interfaz deben pasar sin errores.


