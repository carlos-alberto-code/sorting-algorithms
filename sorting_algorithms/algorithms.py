from typing import List

def bubble_sort(numbers: List[int]):
    """ Algoritmo de oredenación burbuja:
    Recorre la lista de números y compara cada elemento con el siguiente.
    Si el elemento actual es mayor que el siguiente, los intercambia.
    Repite el proceso hasta que no se realice ningún intercambio.
    """
    n = len(numbers)
    for i in range(n):
        for j in range(0, n-i-1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers

def selection_sort(numbers: List[int]):
    """ Algoritmo de ordenación por selección:
    Recorre la lista de números y busca el menor elemento.
    Intercambia el menor elemento con el primer elemento de la lista.
    Repite el proceso con el resto de la lista.
    """
    n = len(numbers)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if numbers[j] < numbers[min_index]:
                min_index = j
        numbers[i], numbers[min_index] = numbers[min_index], numbers[i]
    return numbers

def insertion_sort(numbers: List[int]):
    """ Algoritmo de ordenación por inserción:
    Recorre la lista de números y compara cada elemento con los anteriores.
    Si el elemento actual es menor que el anterior, los intercambia.
    Repite el proceso hasta que el elemento actual sea mayor que el anterior.
    """
    n = len(numbers)
    for i in range(1, n):
        key = numbers[i]
        j = i - 1
        while j >= 0 and key < numbers[j]:
            numbers[j + 1] = numbers[j]
            j -= 1
        numbers[j + 1] = key
    return numbers

def merge_sort(numbers: List[int]):
    """ Algoritmo de ordenación por mezcla:
    Divide la lista en mitades hasta que cada sublista tenga un solo elemento.
    Luego combina las sublistas en orden ascendente.
    """
    def merge(left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    if len(numbers) <= 1:
        return numbers
    middle = len(numbers) // 2
    left = merge_sort(numbers[:middle])
    right = merge_sort(numbers[middle:])
    return merge(left, right)
