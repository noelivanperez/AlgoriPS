# Ejemplo de aplicación de parche semántico

1. Crea un archivo con la regla deseada en la carpeta `plugins`.
2. Ejecuta `python -m algorips apply parche.yml`.
3. El sistema revisa tu código y hace cambios automáticamente.
4. Verás un diff parecido a este:
```
- print("hola")
+ print("hola mundo")
```
Es como pedirle a un ayudante que cambie todas las frases por ti.
