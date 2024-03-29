import os
import shutil


def copiar_archivos(origen, destino):
    # Verificar si la carpeta de destino existe, si no, crearla
    if not os.path.exists(destino):
        os.makedirs(destino)

    # Obtener la lista de archivos en la carpeta de origen
    archivos = os.listdir(origen)

    # Recorrer cada archivo en la carpeta de origen
    for archivo in archivos:
        # Eliminar caracteres inválidos del nombre del archivo
        nombre_valido = ''.join(c for c in archivo if c.isalnum() or c in ['.', '_', '-'])

        # Si el nombre del archivo no es igual al original, imprimir un mensaje
        if nombre_valido != archivo:
            print(f"Renombrando '{archivo}' a '{nombre_valido}'")

        # Copiar el archivo al destino con el nombre válido
        shutil.copy(os.path.join(origen, archivo), os.path.join(destino, nombre_valido))


# Rutas de la carpeta de origen y la carpeta de destino
carpeta_origen = 'carpeta_destino/Gloria Trevi (Todas las canciones)'
carpeta_destino = 'gloria'

# Llamar a la función para copiar los archivos
copiar_archivos(carpeta_origen, carpeta_destino)
