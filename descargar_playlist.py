import os
import sys
import threading
from pytube import Playlist


def corregir_nombre_archivo(nombre):
    # Lista de caracteres válidos en un nombre de archivo
    caracteres_validos = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")

    # Eliminar caracteres inválidos del nombre del archivo
    nombre_valido = ''.join(c for c in nombre if c in caracteres_validos)

    return nombre_valido

# Definir semáforo como variable global
semaforo = threading.Semaphore(4)

def descargar_video(video, carpeta_destino, mp3=False):
    try:
        print(f'Descargando video: {video.title}')
        if mp3:
            audio_stream = video.streams.filter(only_audio=True).first()
            audio_stream.download(output_path=carpeta_destino)
            os.rename(os.path.join(carpeta_destino, audio_stream.default_filename), os.path.join(carpeta_destino, f"{corregir_nombre_archivo(video.title)}.mp3"))
        else:
            first = video.streams.filter(progressive=True, file_extension='mp4').first()
            first.download(output_path=carpeta_destino)
            os.rename(os.path.join(carpeta_destino, first.default_filename), os.path.join(carpeta_destino, f"{corregir_nombre_archivo(video.title)}.mp4"))
        print(f'{video.title} descargado correctamente.')
    except Exception as e:
        print(f'Error al descargar video: {e}')
    finally:
        semaforo.release()  # Liberar el semáforo después de terminar

def descargar_lista_reproduccion(url_lista, carpeta_destino, mp3=False):
    try:
        playlist = Playlist(url_lista)
        playlist._video_regex = None  # Evitar la verificación de la URL
        nombre_carpeta = playlist.title  # Obtener el nombre de la lista de reproducción
        carpeta_destino_lista = os.path.join(carpeta_destino, nombre_carpeta)
        os.makedirs(carpeta_destino_lista, exist_ok=True)  # Crear la carpeta de destino

        # Crear un hilo para descargar cada video de la lista de reproducción
        hilos = []
        for video in playlist.videos:
            semaforo.acquire()  # Adquirir el semáforo antes de crear un nuevo hilo
            hilo = threading.Thread(target=descargar_video, args=(video, carpeta_destino_lista, mp3))
            hilos.append(hilo)
            hilo.start()

        # Esperar a que todos los hilos terminen
        for hilo in hilos:
            hilo.join()

        print("Descarga de la lista de reproducción completada.")
    except Exception as e:
        print(f'Error al descargar lista de reproducción: {e}')

if __name__ == "__main__":
    # Verificar si se proporcionó la URL de la lista de reproducción como argumento
    if len(sys.argv) < 2:
        print("Uso: python descargar_playlist.py <URL_de_la_lista_de_reproducción> [-mp3]")
        sys.exit(1)

    # Obtener la URL de la lista de reproducción desde los argumentos de la línea de comandos
    url_lista_reproduccion = sys.argv[1]

    # Verificar si se proporcionó el argumento opcional -mp3
    mp3 = False
    if len(sys.argv) == 3 and sys.argv[2] == "-mp3":
        mp3 = True

    # Carpeta de destino para guardar los videos
    carpeta_destino = 'carpeta_destino'

    # Descargar la lista de reproducción en múltiples hilos
    descargar_lista_reproduccion(url_lista_reproduccion, carpeta_destino, mp3)
# Output:


