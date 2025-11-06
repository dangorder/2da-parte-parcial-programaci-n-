EJERCICIO FINAL INTEGRADOR: 

GESTION GERARQUICA DE DATOS

# 📚 Sistema de Persistencia Jerárquica de Libros  
### Parcial 2 – Programación 1  
Integrantes: Ignacio Sanchez, Fernando Torrez, Nicolas Valdez   
**Lenguaje:** Python 3.x  
**Tema:** Persistencia avanzada, recursividad y estructura jerárquica de datos  

---

## 🧩 Descripción general

Este proyecto implementa un **sistema de gestión de libros** con **persistencia avanzada** en Python.  
Los datos se almacenan en una **estructura jerárquica de carpetas**, reflejando las relaciones lógicas entre los libros:

"biblioteca/
├── Ficción/
│   └── Tolkien/
│       └── El Hobbit/libros.csv
└── Historia/
    └── Yuval Harari/
        └── Sapiens/libros.csv "


        
Cada archivo `libros.csv` almacena la información de los libros pertenecientes a ese autor y título, garantizando **persistencia física** en el sistema de archivos.

---

## ⚙️ Funcionalidades implementadas (CRUD completo)

| Funcionalidad | Descripción | Requisito |
|----------------|-------------|-----------|
| **Alta (Create)** | Crea carpetas dinámicamente según el género, autor y título. Guarda los datos del libro en un CSV. | ✅ |
| **Lectura global (Read)** | Lee recursivamente todos los archivos `libros.csv` dentro de la jerarquía y consolida los datos. | ✅ |
| **Modificación (Update)** | Permite modificar precio y/o año de un libro según su título. | ✅ |
| **Eliminación (Delete)** | Busca un libro por título y lo elimina del CSV correspondiente. | ✅ |
| **Ordenamiento** | Ordena los libros por atributo (por ejemplo, precio). | ✅ |
| **Estadísticas** | Calcula total, precio mínimo, máximo y promedio. | ✅ |
| **Filtrado** | Permite buscar libros por género, autor o año. | ✅ |

---

## 🧠 Conceptos aplicados

| Concepto | Descripción |
|-----------|-------------|
| **Persistencia avanzada** | Los datos se guardan en archivos CSV organizados en carpetas jerárquicas. |
| **Estructura jerárquica de 3 niveles** | Género → Autor → Título. |
| **Recursividad** | La función `leer_toda_jerarquia()` recorre de manera recursiva todas las carpetas para leer los libros. |
| **Librería `os`** | Usada para crear directorios, listar carpetas y manejar rutas dinámicamente. |
| **Seguridad y calidad del código** | Uso de `with open()`, manejo de excepciones, validaciones, indentación PEP 8 y modularización. |
| **Modularización** | El código se divide en dos archivos: `main.py` (programa principal) y `funciones_jerarquia.py` (lógica y utilidades). |

---

## 🧾 Estructura del proyecto

📁 proyecto_biblioteca/
│

├── 📄 main.py

│ → Menú principal (interfaz de usuario)

│

├── 📄 funciones_jerarquia.py

│ → Módulo con todas las funciones CRUD, recursividad y validaciones

│

├── 📄 README.md

│ → Documento explicativo del proyecto

│

└── 📁 biblioteca/

→ Carpeta raíz donde se guarda toda la jerarquía de datos (se crea automáticamente)


---

## 🚀 Instrucciones de ejecución

1. **Descargar o clonar el proyecto.**  
   Asegurarse de tener Python 3.10 o superior (por el uso de `match-case`).

2. **Ejecutar el programa principal:**
   ```bash
   python main.py

Seguir las opciones del menú:

1. Alta de libro
2. Mostrar todos los libros
3. Modificar libro (por título)
4. Eliminar libro (por título)
5. Ordenar libros por precio
6. Mostrar estadísticas
7. Filtrar libros por atributo
8. Salir

Los datos se guardarán automáticamente en la carpeta biblioteca/, incluso si se cierra el programa.

🖥️ Ejemplo de ejecución

===== GESTIÓN DE LIBROS =====
1. Alta de libro
2. Mostrar todos los libros
3. Modificar libro (por título)
4. Eliminar libro (por título)
5. Ordenar libros por precio
6. Mostrar estadísticas
7. Filtrar libros por atributo
8. Salir
Seleccione una opción: 1
Género: Ficción
Autor: Tolkien
Título: El Hobbit
Precio: 3500
Año de publicación: 1937
✅ Libro agregado correctamente.

Seleccione una opción: 2
21bfa93c-320a-4a1f-b13e-27a9ad17c623 | El Hobbit | Tolkien | Ficción | $3500.0 | 1937

Seleccione una opción: 6
Total de libros: 1
Precio mínimo: $3500.00
Precio máximo: $3500.00
Promedio de precios: $3500.00

Seleccione una opción: 8
Saliendo del sistema de biblioteca... 📚

🔍 Detalles técnicos adicionales

Recursividad:
La función leer_toda_jerarquia() llama a sí misma para recorrer subcarpetas.
Esto permite consolidar toda la información de manera automática sin importar cuántos niveles existan.

Manejo seguro de archivos:
Se usan archivos temporales .tmp al modificar o eliminar registros, garantizando que no se corrompan los datos si ocurre un error.

UUID:
Cada libro tiene un identificador único (codigo_libro) generado con uuid.uuid4() para evitar duplicados.

Validaciones:

validar_cadena() → evita campos vacíos.

validar_numero() → controla que el precio sea positivo.

validar_anio() → asegura que el año esté dentro del rango 1500–2025.

🧾 Conclusión

El sistema de gestión de libros desarrollado demuestra la aplicación práctica de los conceptos de persistencia avanzada, recursividad y modularización en Python.
A través de una estructura jerárquica de tres niveles (Género → Autor → Título), el programa permite almacenar y gestionar información de forma ordenada y permanente mediante archivos CSV.
El uso de la librería os, junto con funciones validadas y manejo seguro de archivos, garantiza la integridad de los datos y la automatización del sistema.
En conjunto, el proyecto cumple los objetivos del parcial, integrando un CRUD completo, estadísticas, filtrado y recorrido recursivo de carpetas, reflejando un desarrollo robusto, claro y funcional.
