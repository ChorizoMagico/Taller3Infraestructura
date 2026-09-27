import threading
import random
from time import time
from time import sleep

def intentarReservar(index_asiento, index_hilo, tries):
    if(tries == 3):
        print(f"Persona No. {index_hilo+1} no pudo encontrar asientos. Compra cancelada\n")
        return 0
    
    if(asientos[index_asiento].acquire(blocking=False) == False):
        tries += 1
        intentarReservar(random.randint(0, CANTIDAD_ASIENTOS-1),index_hilo, tries)
    else:

        time1 = time()
        sleep(random.randint(0, 4))
        time2 = time()

        sleeping_time = time2 - time1

        if(sleeping_time >= 2.5):
            print(f"Persona No. {index_hilo+1} no pudo completar la transacción, sigue buscando asientos.\n")
            tries += 1
            intentarReservar(random.randint(0, CANTIDAD_ASIENTOS-1),index_hilo, tries)
            asientos[index_asiento].release()
        else:
            print(f"Compra confirmada para persona {index_hilo+1}, No. Asiento: {index_asiento+1}\n")

        return 0



if __name__ == "__main__":

    CANTIDAD_HILOS = 20
    CANTIDAD_ASIENTOS = 5
    
    hilos = [None] * CANTIDAD_HILOS

    asientos = [None] * CANTIDAD_ASIENTOS

    for index in range(CANTIDAD_ASIENTOS):
        asientos[index] = threading.Lock()

    for index in range(CANTIDAD_HILOS):
        hilos[index] = threading.Thread(target=intentarReservar, args=(random.randint(0, CANTIDAD_ASIENTOS-1), index, 0))

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()
