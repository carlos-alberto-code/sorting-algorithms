from typing import List
from abc import ABC, abstractmethod

class SortingAlgorithm(ABC):
    # Esta es una clase abstracta que define un método abstracto llamado sort
    @abstractmethod
    def sort(self, numbers: List[int]) -> List[int]:
        # Este método debe ser implementado por las clases que hereden de SortingAlgorithm
        # Con este método se busca mejorar la evolución del código
        # Así se puede depender de la clase abstracta SortingAlgorithm en lugar de depender de las clases concretas o de funciones como en el caso de la versión 1.
        pass

class BubbleSort(SortingAlgorithm):
    def sort(self, numbers: List[int]) -> List[int]:
        n = len(numbers)
        for i in range(n):
            for j in range(0, n-i-1):
                if numbers[j] > numbers[j+1]:
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
        return numbers

class SelectionSort(SortingAlgorithm):
    def sort(self, numbers: List[int]) -> List[int]:
        n = len(numbers)
        for i in range(n):
            min_index = i
            for j in range(i+1, n):
                if numbers[j] < numbers[min_index]:
                    min_index = j
            numbers[i], numbers[min_index] = numbers[min_index], numbers[i]
        return numbers

class InsertionSort(SortingAlgorithm):
    def sort(self, numbers: List[int]) -> List[int]:
        n = len(numbers)
        for i in range(1, n):
            key = numbers[i]
            j = i - 1
            while j >= 0 and key < numbers[j]:
                numbers[j + 1] = numbers[j]
                j -= 1
            numbers[j + 1] = key
        return numbers

class MergeSort(SortingAlgorithm):
    def sort(self, numbers: List[int]) -> List[int]:
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
        left = self.sort(numbers[:middle])
        right = self.sort(numbers[middle:])
        return merge(left, right)
