# ============================================================
# Programa Principal - Sistema de Persistencia Jerárquica
# Materia: Programación 1
# Parcial 2 - Gestión de Libros con Recursividad y Persistencia
# ============================================================

# Importamos el módulo que contiene todas las funciones CRUD y utilitarias.
# Este módulo (funciones_jerarquia.py) implementa la lógica de persistencia,
# validaciones, recursividad y manejo de archivos CSV.
import funciones_jerarquia as fcs

# ------------------------------------------------------------
#  CONFIGURACIÓN INICIAL
# ------------------------------------------------------------

# ROOT indica la carpeta raíz donde se guardará la jerarquía de datos.
# Ejemplo de estructura que se crea automáticamente:
# ./biblioteca/
# ├── Ficción/
# │   ├── Tolkien/
# │   │   └── El Hobbit/libros.csv
# │   └── García Márquez/
# │       └── Cien años de soledad/libros.csv
# └── Historia/
#     └── Yuval Harari/
#         └── Sapiens/libros.csv
ROOT = "./biblioteca"

# Creamos la carpeta raíz si no existe (persistencia avanzada)
fcs.inicializar_root(ROOT)

# ------------------------------------------------------------
#  MENÚ PRINCIPAL
# ------------------------------------------------------------

# Bucle infinito que muestra el menú principal hasta que el usuario elija salir.
while True:
    print("\n===== GESTIÓN DE LIBROS =====")
    print("1. Alta de libro")
    print("2. Mostrar todos los libros")
    print("3. Modificar libro (por título)")
    print("4. Eliminar libro (por título)")
    print("5. Ordenar libros por precio")
    print("6. Mostrar estadísticas")
    print("7. Filtrar libros por atributo")
    print("8. Salir")

    # El usuario elige una opción.
    opcion = input("Seleccione una opción: ").strip()

    # --------------------------------------------------------
    #  ESTRUCTURA MATCH-CASE (similar a switch)
    # --------------------------------------------------------
    # Evalúa el valor ingresado y ejecuta el bloque correspondiente.
    match opcion:

        # ------------------- OPCIÓN 1 ------------------------
        # ALTA DE LIBRO
        case "1":
            try:
                # Solicitamos los datos del nuevo libro.
                genero = fcs.validar_cadena(input("Género: "))
                autor = fcs.validar_cadena(input("Autor: "))
                titulo = fcs.validar_cadena(input("Título: "))
                precio = fcs.validar_numero(input("Precio: "))
                anio = fcs.validar_anio(input("Año de publicación: "))

                # Llamamos a la función que crea la jerarquía y guarda el libro.
                fcs.alta_libro(ROOT, genero, autor, titulo, precio, anio)
            except Exception as e:
                print(f"Error: {e}")

        # ------------------- OPCIÓN 2 ------------------------
        # MOSTRAR TODOS LOS LIBROS (LECTURA RECURSIVA)
        case "2":
            # Se lee toda la jerarquía de carpetas recursivamente.
            libros = fcs.leer_toda_jerarquia(ROOT)

            # Si no hay datos, se informa.
            if not libros:
                print("No hay libros registrados.")
            else:
                # Si hay libros, se muestran en formato tabular simple.
                for l in libros:
                    print(f"{l['codigo_libro']} | {l['titulo']} | {l['autor']} | {l['genero']} | ${l['precio']} | {l['anio']}")

        # ------------------- OPCIÓN 3 ------------------------
        # MODIFICAR LIBRO (POR TÍTULO)
        case "3":
            titulo = input("Ingrese el título del libro a modificar: ").strip()
            nuevo_precio = input("Nuevo precio (vacío para no cambiar): ").strip()
            nuevo_anio = input("Nuevo año (vacío para no cambiar): ").strip()

            # Validamos nuevos valores (solo si el usuario ingresó algo)
            if nuevo_precio:
                try:
                    nuevo_precio = fcs.validar_numero(nuevo_precio)
                except Exception as e:
                    print(e)
                    continue
            if nuevo_anio:
                try:
                    nuevo_anio = fcs.validar_anio(nuevo_anio)
                except Exception as e:
                    print(e)
                    continue

            # Llamamos a la función que actualiza los datos.
            fcs.actualizar_libro(ROOT, titulo, nuevo_precio or None, nuevo_anio or None)

        # ------------------- OPCIÓN 4 ------------------------
        # ELIMINAR LIBRO (POR TÍTULO)
        case "4":
            titulo = input("Ingrese el título del libro a eliminar: ").strip()
            # Llama a la función que permite seleccionar y eliminar el libro.
            fcs.eliminar_libro(ROOT, titulo)

        # ------------------- OPCIÓN 5 ------------------------
        # ORDENAR LIBROS POR PRECIO
        case "5":
            libros = fcs.leer_toda_jerarquia(ROOT)
            ordenados = fcs.ordenar_libros(libros, "precio")
            print("\n--- Libros ordenados por precio ---")
            for l in ordenados:
                print(f"{l['titulo']} - ${l['precio']}")

        # ------------------- OPCIÓN 6 ------------------------
        # ESTADÍSTICAS
        case "6":
            libros = fcs.leer_toda_jerarquia(ROOT)
            fcs.estadisticas(libros)

        # ------------------- OPCIÓN 7 ------------------------
        # FILTRO (por género, autor, año, etc.)
        case "7":
            libros = fcs.leer_toda_jerarquia(ROOT)
            if not libros:
                print("No hay libros para filtrar.")
                continue

            # Se permite al usuario escribir el atributo y el valor deseado.
            atributo = input("Atributo (ej. genero, autor, anio): ").strip()
            valor = input(f"Valor de {atributo}: ").strip()

            # Filtramos y mostramos los resultados.
            resultado = fcs.filtrar_libros(libros, atributo, valor)
            if resultado:
                print("\n--- Libros encontrados ---")
                for l in resultado:
                    print(f"{l['titulo']} | {l['autor']} | {l['genero']} | ${l['precio']} | {l['anio']}")

        # ------------------- OPCIÓN 8 ------------------------
        # SALIR DEL PROGRAMA
        case "8":
            print("Saliendo del sistema de biblioteca... ")
            break

        # ------------------- CASO INVÁLIDO -------------------
        case _:
            print("Opción inválida. Intente nuevamente.")
