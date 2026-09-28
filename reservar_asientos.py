import threading
import random
from time import time
from time import sleep

#Función para que un hilo intente reservar un asiento
def intentarReservar(index_asiento, index_hilo, tries):

    while tries < 3:
        #Si el asiento ya está ocupado, vuelve a intentar con otro asiento aleatorio
        if(asientos[index_asiento].acquire(blocking=False) == False):
            tries += 1
            index_asiento = random.randint(0, CANTIDAD_ASIENTOS-1)
        else:

            #Si no está ocupado, lo bloquea y duerme entre 0 y 4 segundos
            time1 = time()
            sleep(random.randint(0, 4))
            time2 = time()

            sleeping_time = time2 - time1

            #Si 2 o más segundos, la transacción se cancela. Se libera el asiento e intenta reservar otro asiento aleatorio
            if(sleeping_time >= 2):
                print(f"Persona No. {index_hilo+1} no pudo completar la transacción, sigue buscando asientos.\n")
                tries += 1
                asientos[index_asiento].release()
                index_asiento = random.randint(0, CANTIDAD_ASIENTOS-1)
                
            else:
                #La transacción se completó
                print(f"Compra confirmada para persona {index_hilo+1}, No. Asiento: {index_asiento+1}\n")
                return 0

    #Si es su tercer intento reservando, se rinde
    print(f"Persona No. {index_hilo+1} no pudo encontrar asientos. Compra cancelada\n")
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