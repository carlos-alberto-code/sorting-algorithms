from typing import List
from abc    import ABC, abstractmethod


class SortingAlgorithm(ABC):
    def __init__(self, numbers: List[int]):
        self.numbers = numbers

    @abstractmethod
    def sort(self) -> List[int]:
        pass


class BubbleSort(SortingAlgorithm):
    def __init__(self, numbers: List[int]):
        super().__init__(numbers)

    def sort(self) -> List[int]:
        n = len(self.numbers)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.numbers[j] > self.numbers[j+1]:
                    self.numbers[j], self.numbers[j+1] = self.numbers[j+1], self.numbers[j]
        return self.numbers


class SelectionSort(SortingAlgorithm):
    def __init__(self, numbers: List[int]):
        super().__init__(numbers)

    def sort(self) -> List[int]:
        n = len(self.numbers)
        for i in range(n):
            min_index = i
            for j in range(i+1, n):
                if self.numbers[j] < self.numbers[min_index]:
                    min_index = j
            self.numbers[i], self.numbers[min_index] = self.numbers[min_index], self.numbers[i]
        return self.numbers


class InsertionSort(SortingAlgorithm):
    def __init__(self, numbers: List[int]):
        super().__init__(numbers)

    def sort(self) -> List[int]:
        n = len(self.numbers)
        for i in range(1, n):
            key = self.numbers[i]
            j = i - 1
            while j >= 0 and key < self.numbers[j]:
                self.numbers[j + 1] = self.numbers[j]
                j -= 1
            self.numbers[j + 1] = key
        return self.numbers


class MergeSort(SortingAlgorithm):
    def __init__(self, numbers: List[int]):
        super().__init__(numbers)

    def sort(self) -> List[int]:
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

        if len(self.numbers) <= 1:
            return self.numbers
        middle = len(self.numbers) // 2
        left = MergeSort(self.numbers[:middle]).sort()
        right = MergeSort(self.numbers[middle:]).sort()
        return merge(left, right)


def crear_algoritmos(nums: List[int]) -> List[SortingAlgorithm]:
    return [
        # BubbleSort(nums.copy()),
        # SelectionSort(nums.copy()),
        InsertionSort(nums.copy()),
        MergeSort(nums.copy())
    ]
