import multiprocessing
import time
import random
import os

NUM_WORKERS = 3
MAX_RETRIES = 2

def worker(worker_id):
    pid = os.getpid()
    print(f"[Worker {worker_id}] Iniciado con PID {pid}")
    
    # Simula trabajo y posible fallo
    work_time = random.randint(2, 5)
    time.sleep(work_time)

    # Simular fallo aleatorio
    if random.random() < 0.5:
        print(f"[Worker {worker_id}] ERROR CRITICO en PID {pid}")
        exit(1)

    print(f"[Worker {worker_id}] Finalizo correctamente")


def monitor():
    print("[Monitor] Sistema de supervision activo\n")

    processes = {}
    retries = {}

    # Crear trabajadores iniciales
    for i in range(NUM_WORKERS):
        p = multiprocessing.Process(target=worker, args=(i,))
        p.start()
        processes[i] = p
        retries[i] = 0

    # Supervisión continua
    while processes:
        for i, p in list(processes.items()):
            if not p.is_alive():
                p.join()

                if p.exitcode != 0:
                    if retries[i] < MAX_RETRIES:
                        retries[i] += 1
                        print(f"[Monitor] Reiniciando Worker {i} (Intento {retries[i]})\n")
                        new_p = multiprocessing.Process(target=worker, args=(i,))
                        new_p.start()
                        processes[i] = new_p
                    else:
                        print(f"[Monitor] Worker {i} alcanzo maximo de reintentos. Eliminado.\n")
                        del processes[i]
                else:
                    print(f"[Monitor] Worker {i} termino correctamente.\n")
                    del processes[i]

        time.sleep(1)

    print("[Monitor] Todos los procesos finalizaron.")


if __name__ == "__main__":
    monitor()
