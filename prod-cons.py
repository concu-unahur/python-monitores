import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


def productor(monitor):
    print("Voy a producir")
    for i in range(30):
        with monitor:          # hace el acquire y al final un release
            items.append(i)    # agrega un ítem
            monitor.notify()   # Notifica que ya se puede hacer acquire
        time.sleep(2)


class consumer(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor

    def run(self):
        while (True):
            with self.monitor:          # Hace el acquire y al final un release
                while len(items)<1:     # si no hay ítems para consumir
                    self.monitor.wait()  # espera la señal, es decir el notify
            x = items.pop(0)     # saca (consume) el primer ítem
            logging.info(f'Consumí {x}')
            time.sleep(1)


# la lista de ítems a consumir
items = []

# El monitor
items_monit = threading.Condition()

# un thread que consume
cons1 = consumer(items_monit)
cons1.start()

# El productor
productor(items_monit)



        
