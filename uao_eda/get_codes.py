import pandas as pd
import os
import requests
from time import time, sleep
import threading
import logging
import traceback

code_route = r"C:\Users\ivanr\OneDrive\Desktop\ESTUDIO_TRABAJO\PROYECTOS PROGRAMING\POESISMO DATA\codigos_uao.txt"
data_route = r"C:\Users\ivanr\OneDrive\Desktop\ESTUDIO_TRABAJO\PROYECTOS PROGRAMING\POESISMO DATA\data\uao_ctas"
archivos = os.listdir(data_route)
with open(code_route, "r") as f:
    codigos = f.read().splitlines()

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

def get_estados_de_cuenta(codes: list):
    for idx, i in enumerate(codes):
        if f"{i}_ctadt.pdf" not in archivos:
            try:
                url = f"http://wlapp.uao.edu.co/reports/rwservlet?connrepuao_ice&jobtype=jt_uao_ice&report=Estado_Cta_Web_Uao10g.rdf&destype=cache&desformat=pdf&mi_cliente={i}"
                start = time()
                sleep(1)
                response = requests.get(url)
                if len(response.content) >= 11000:
                    with open(data_route + f"\{i}_ctadt.pdf", "wb") as f:
                        f.write(response.content)
                        logging.info(f"{idx}: Descargado {i}_ctadt.pdf exitosamente en {time() - start} segundos")
                        # print(f"{idx}:Se descargo el archivo {i}_ctadt.pdf exitosamente.\nDemoró: {time() - start} segundos")
                else:
                    logging.info(f"{idx}:El archivo {i}_ctadt.pdf no cumple con el tamaño mínimo de 11000 bytes, será elimando de la lista de codigos")
                    codigos.remove(i)
                    with open(code_route, "w") as b:
                        b.write("\n".join(codigos))
                    # print(f"{idx}:El archivo {i}_ctadt.pdf no cumple con el tamaño mínimo de 11000 bytes")
            except Exception as e:
                logging.error(traceback.format_exc())
        else:
            logging.info(f"{idx}:El archivo {i}_ctadt.pdf ya existe, sera eliminado de la lista de codigos")
            codigos.remove(i)
            # print(f"{idx}:El archivo {i}_ctadt.pdf ya existe.")
            with open(code_route, "w") as b:
                b.write("\n".join(codigos))

def list_splitter(lst: list,n: int) -> list:
    return [lst[i::n] for i in range(n)]

codes_splitted = list_splitter(codigos, 50)

threads = []

for idx, code_list in enumerate(codes_splitted):
    t = threading.Thread(target=get_estados_de_cuenta, args=(code_list,))
    print(f"Thread {idx} created")
    t.start()
    threads.append(t)

for idx, t in enumerate(threads):
    print(f"Thread {idx} joined")
    t.join()