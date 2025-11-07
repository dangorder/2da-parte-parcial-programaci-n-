import os
import csv
import uuid

# Nombre del archivo CSV que se guarda en cada carpeta de tercer nivel (Título)
CSV_FILE = "libros.csv"

# Orden/columnas obligatorias del CSV — mantener consistencia al escribir/leer
REQUIRED_FIELDS = ["codigo_libro", "titulo", "autor", "genero", "precio", "anio"]


# --------------------------- VALIDACIONES ---------------------------
def validar_cadena(texto):
    """
    Valida que `texto` sea una cadena no vacía.
    - Entrada: texto (cualquier tipo convertible a str).
    - Salida: devuelve texto.strip() si es válido.
    - Lanza: ValueError si la cadena está vacía después de strip().
    Razón: evita campos vacíos en el CSV (nombre, autor, género, etc.).
    """
    if not texto.strip():
        raise ValueError("El campo no puede estar vacío.")
    return texto.strip()


def validar_numero(valor):
    """
    Valida que `valor` represente un número positivo (float).
    - Entrada: valor (cadena o número).
    - Salida: float(valor) si es > 0.
    - Lanza: ValueError en caso contrario.
    Uso: validar precio del libro.
    """
    try:
        num = float(valor)
        if num <= 0:
            raise ValueError
        return num
    except ValueError:
        raise ValueError("Debe ingresar un número positivo.")


def validar_anio(valor): 
    """
    Valida que `valor` sea un año razonable entre 1500 y 2025 (int).
    - Entrada: valor (cadena o número).
    - Salida: int(valor) si está en rango.
    - Lanza: ValueError si no es entero o está fuera de rango.
    Nota: ajustar el rango si es necesario (por ejemplo, 2026+).
    """
    try:
        anio = int(valor)
        if anio < 1500 or anio > 2025:
            raise ValueError
        return anio
    except ValueError:
        raise ValueError("Debe ingresar un año válido entre 1500 y 2025.")


# --------------------------- INICIALIZACIÓN --------------------------
def inicializar_root(root):
    """
    Crea la carpeta raíz `root` si no existe.
    - Entrada: root (ruta relativa o absoluta).
    - Efecto: crea el directorio con os.makedirs(..., exist_ok=True).
    - No devuelve nada.
    Importante: no borra nada si ya existe.
    """
    os.makedirs(root, exist_ok=True)


# --------------------------- CRUD: ALTA ------------------------------
def alta_libro(root, genero, autor, titulo, precio, anio):
    """
    Alta (Create): agrega un libro en la jerarquía Género/Autor/Título.
    - Construye la ruta: root/genero/autor/titulo
    - Crea carpetas si hace falta con os.makedirs(..., exist_ok=True)
    - Genera un codigo_libro único con uuid.uuid4() -> string
    - Abre (append) CSV_FILE en esa carpeta y escribe una fila con los campos REQUIRED_FIELDS.
    - Usa `with open(...)` para manejo seguro de archivos.
    - Parámetros:
        root: carpeta raíz donde se guardan datos
        genero, autor, titulo: strings (deben validarse antes)
        precio: número (float) validado por validar_numero
        anio: entero validado por validar_anio
    - Manejo de errores: captura Exception general y muestra mensaje; no propaga.
    """
    # Construcción de la ruta jerárquica
    path = os.path.join(root, genero, autor, titulo)
    os.makedirs(path, exist_ok=True)  # crea carpetas si no existen

    codigo_libro = str(uuid.uuid4())  # identificador único (UUID)
    csv_path = os.path.join(path, CSV_FILE)

    # Diccionario con la información a escribir en el CSV
    nuevo = {
        "codigo_libro": codigo_libro,
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "precio": precio,
        "anio": anio,
    }

    try:
        file_exists = os.path.exists(csv_path)
        # Abrimos en modo 'a' (append). Si no existe, escribimos la cabecera primero.
        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=REQUIRED_FIELDS)
            if not file_exists or os.path.getsize(csv_path) == 0:
                writer.writeheader()
            writer.writerow(nuevo)
        print(" Libro agregado correctamente.")
    except Exception as e:
        # Aquí podríamos diferenciar tipos de excepción (IOError, OSError), pero
        # un mensaje general es suficiente para un proyecto académico.
        print(f"Error al guardar el libro: {e}")


# --------------------------- LECTURA RECURSIVA -----------------------
def leer_toda_jerarquia(root):
    """
    Read All (obligatoriamente recursivo).
    - Recorre de forma recursiva todos los subdirectorios dentro de `root`.
    - Cada vez que encuentra un archivo llamado CSV_FILE lo abre y lee sus filas.
    - Consolida todas las filas en una lista `libros` de diccionarios.
    - Añade la clave "_origen" a cada registro con la ruta absoluta/parcial del CSV,
    para saber en qué archivo reside cada ítem (útil para actualizar/eliminar).
    - Retorna la lista completa de libros (puede estar vacía).
    - Mecanismo recursivo: la función interna `recorrer(ruta)` se llama a sí misma
    cuando encuentra un subdirectorio: `recorrer(subruta)` -> caso recursivo.
    Caso base: cuando no hay subdirectorios o cuando se encuentra un CSV (lo lee).
    - Manejo de errores: captura excepciones de filesystem dentro del bloque try,
    y continúa (no interrumpe toda la lectura por un error parcial).
    """
    libros = []

    def recorrer(ruta):
        try:
            # Lista los nombres dentro de `ruta` (archivos y carpetas)
            for elemento in os.listdir(ruta):
                subruta = os.path.join(ruta, elemento)
                # Si es un directorio, llamo recursivamente
                if os.path.isdir(subruta):
                    recorrer(subruta)  #  llamada recursiva
                # Si el nombre coincide con CSV_FILE, lo abro y leo sus filas
                elif elemento == CSV_FILE:
                    with open(subruta, "r", newline="", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            # Añadimos trazabilidad: desde qué archivo proviene este registro
                            row["_origen"] = subruta
                            libros.append(row)
        except Exception:
            # Ignoramos carpetas inaccesibles o errores puntuales de lectura
            # Podríamos loguear el error en una solución más robusta.
            pass

    recorrer(root)  # inicio de la recursión desde la raíz
    return libros


# --------------------------- MODIFICACIÓN ----------------------------
def actualizar_libro(root, titulo, nuevo_precio=None, nuevo_anio=None):
    """
    Update: Actualiza precio y/o año de un libro identificado por su título.
    - Estrategia:
        1. Recolectar todos los libros con leer_toda_jerarquia(root).
        2. Buscar el primer libro cuya 'titulo' coincida (case-insensitive).
        3. Abrir el CSV de origen y reescribirlo en un archivo temporal:
            - al encontrar la fila correcta (comparando codigo_libro), modificar campos
            - escribir todas las otras filas tal cual
        4. Reemplazar el archivo original por el temporal con os.replace (más seguro)
    - Parámetros:
        root: ruta raíz
        titulo: título a buscar (string)
        nuevo_precio: float o None
        nuevo_anio: int o None
    - Observación: si existen múltiples libros con el mismo título, se actualiza
      el **primer** que se encuentre (la versión principal usa búsqueda por titulo
    en main.py para seleccionar cuál modificar; aquí se usa la coincidencia directa).
    """
    libros = leer_toda_jerarquia(root)

    # Buscamos una coincidencia por título (case-insensitive)
    encontrado = None
    for l in libros:
        if l["titulo"].lower() == titulo.lower():
            encontrado = l
            break

    if not encontrado:
        print(" Libro no encontrado.")
        return

    origen = encontrado["_origen"]  # path del CSV donde está la fila a modificar

    try:
        temp = origen + ".tmp"
        # Abrimos archivo original para leer y temp para escribir
        with open(origen, "r", newline="", encoding="utf-8") as infile, \
            open(temp, "w", newline="", encoding="utf-8") as outfile:
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                # Identificamos la fila mediante codigo_libro (único)
                if row["codigo_libro"] == encontrado["codigo_libro"]:
                    # Aplicamos cambios solo a las columnas permitidas
                    if nuevo_precio:
                        row["precio"] = nuevo_precio
                    if nuevo_anio:
                        row["anio"] = nuevo_anio
                # Escribimos la fila (modificada o no)
                writer.writerow(row)
        # Reemplazo atómico del CSV original por el temp (reduce ventana de corrupción)
        os.replace(temp, origen)
        print(" Libro actualizado correctamente.")
    except Exception as e:
        # Si ocurre un error, intentamos no dejar temp suelto (podríamos eliminarlo)
        print(f"Error al actualizar el libro: {e}")


# --------------------------- ELIMINACIÓN ------------------------------
def eliminar_libro(root, titulo):
    """
    Delete: Elimina un libro buscándolo por título (coincidencia parcial).
    - Paso 1: obtener todos los libros.
    - Paso 2: filtrar aquellos cuyo título contiene la cadena `titulo` (case-insensitive).
    - Si hay múltiples coincidencias, pide al usuario seleccionar cuál eliminar.
    - Antes de borrar pregunta confirmación 's'/'n'.
    - Reescribe el CSV de origen sin la fila eliminada (mismo patrón que en actualizar).
    - Parámetros:
        root: ruta raíz
        titulo: cadena para buscar en 'titulo' de cada registro
    """
    libros = leer_toda_jerarquia(root)
    encontrados = [l for l in libros if titulo.lower() in l["titulo"].lower()]

    if not encontrados:
        print(" No se encontraron libros con ese título.")
        return

    # Si hay varias coincidencias, mostramos opciones para seleccionar
    if len(encontrados) > 1:
        print("\nSe encontraron varios libros con ese título:")
        for i, l in enumerate(encontrados, start=1):
            print(f"{i}. {l['titulo']} - {l['autor']} ({l['genero']}) - {l['anio']}")
        indice = input("Seleccione el número del libro a eliminar: ").strip()
        if not indice.isdigit() or not (1 <= int(indice) <= len(encontrados)):
            print("Selección inválida.")
            return
        encontrado = encontrados[int(indice) - 1]
    else:
        encontrado = encontrados[0]

    origen = encontrado["_origen"]

    # Confirmación del usuario antes de eliminar
    confirm = input(f"¿Seguro que desea eliminar '{encontrado['titulo']}'? (s/n): ").lower()
    if confirm != "s":
        print("Operación cancelada.")
        return

    try:
        temp = origen + ".tmp"
        with open(origen, "r", newline="", encoding="utf-8") as infile, \
            open(temp, "w", newline="", encoding="utf-8") as outfile:
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                # Escribimos todas las filas excepto la que queremos eliminar
                if row["codigo_libro"] != encontrado["codigo_libro"]:
                    writer.writerow(row)
        os.replace(temp, origen)
        print(" Libro eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar el libro: {e}")


# --------------------------- ORDENAMIENTO Y ESTADÍSTICAS -------------
def ordenar_libros(libros, clave):
    """
    Ordena una lista de libros por `clave`.
    - Intenta convertir la clave a float para orden numérico (ej. 'precio', 'anio').
    - Si falla (campo no numérico), ordena lexicográficamente (case-insensitive).
    - Retorna una lista nueva ordenada; no modifica la original.
    """
    try:
        return sorted(libros, key=lambda x: float(x.get(clave, 0)))
    except Exception:
        return sorted(libros, key=lambda x: x.get(clave, "").lower())


def estadisticas(libros):
    """
    Calcula y muestra estadísticas básicas sobre la lista `libros`.
    - Calcula: total, mínimo, máximo y promedio de 'precio'.
    - Si no hay precios validables, muestra un mensaje y retorna.
    - No devuelve estructura; imprime en consola (fácil de adaptar si se necesita retorno).
    """
    precios = [float(l["precio"]) for l in libros if l.get("precio")]
    if not precios:
        print("No hay precios cargados para calcular estadísticas.")
        return
    print(f"Total de libros: {len(libros)}")
    print(f"Precio mínimo: ${min(precios):.2f}")
    print(f"Precio máximo: ${max(precios):.2f}")
    print(f"Promedio de precios: ${sum(precios)/len(precios):.2f}")


# --------------------------- FILTRO ----------------------------------
def filtrar_libros(libros, atributo, valor):
    """
    Filtra la lista `libros` por `atributo == valor` (comparación case-insensitive).
    - Parámetros:
        libros: lista de diccionarios (resultado de leer_toda_jerarquia)
        atributo: nombre de la columna (ej. 'genero', 'autor', 'anio')
        valor: valor buscado (string)
    - Retorna: lista con coincidencias (puede estar vacía).
    - Imprime mensaje si no encuentra coincidencias.
    """
    resultado = []
    for l in libros:
        if str(l.get(atributo, "")).lower() == str(valor).lower():
            resultado.append(l)
    if not resultado:
        print(f"No se encontraron libros con {atributo} = {valor}.")
    return resultado
