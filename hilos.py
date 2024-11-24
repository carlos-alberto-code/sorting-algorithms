from threading import Thread
from sorting_algorithms.algorithms import bubble_sort, selection_sort

t1 = Thread(target=bubble_sort, args=([5, 4, 3, 2, 1],))
t1.start()
print(t1)
t2 = Thread(target=selection_sort, args=([5, 4, 3, 2, 1],))
t2.start()
print(t2)

t1.join()
t2.join()
# ¿Cuál es la salida de este código?
#
# A) El código generará una excepción porque las funciones bubble_sort y selection_sort no son seguras para hilos.
# B) El código generará una excepción porque las funciones bubble_sort y selection_sort no están definidas.
# C) El código se ejecutará sin errores e imprimirá las listas ordenadas.
# D) El código se ejecutará sin errores pero no imprimirá las listas ordenadas.
#
# Respuesta: C) El código se ejecutará sin errores e imprimirá las listas ordenadas.
