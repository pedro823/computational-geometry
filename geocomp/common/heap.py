identity = lambda x: x

class Heap:

    @classmethod
    def from_list(cls, element_list: list, is_max_heap: bool = False, key_function=identity):
        heap = cls(is_max_heap, key_function)
        for element in element_list:
            heap.insert(element)
        return heap


    def __init__(self, is_max_heap: bool = False, key_function=identity):
        ''' Initializes an empty heap.
            :param is_max_heap: True if heap should be a max-heap.
                                False otherwise.
            :param key_function: A function that extracts the key
            from the element. The heap will be indexed by the key.
        '''
        self.heap = []
        self.key_function = key_function
        self.is_max_heap = is_max_heap

    def insert(self, element):
        key = self.key_function(element)
        self.heap.append(element)
        self.__promote(len(self.heap) - 1)

    def peek_top(self):
        return self.heap[0]

    def pop_element(self):
        top_element = self.heap[0]
        if len(self.heap) > 1:
            self.heap[0] = self.heap.pop()
            self.__sink(0)
        else:
            self.heap.pop()
        return top_element
    
    __len__ = lambda self: len(self.heap)

    __str__ = lambda self: 'Heap: ' + str(self.heap)
    
    __bool__ = __nonzero__ = lambda self: len(self) > 0
    
    def __promote(self, index):
        element = self.heap[index]
        while not self.__is_root(index):
            parent_index = self.__parent(index)
            parent = self.heap[parent_index]
            if self.__is_less_or_eq(parent, element) ^ self.is_max_heap:
                break
            # swap
            self.heap[parent_index] = element
            self.heap[index] = parent
            index = parent_index

    def __sink(self, index):
        while self.__left(index) < len(self.heap):
            child_idx = self.__left(index)
            child = self.heap[child_idx]
            if self.__right(index) < len(self.heap):
                right_child = self.heap[self.__right(index)]
                if self.__is_less_or_eq(right_child, child) ^ self.is_max_heap:
                    child_idx = self.__right(index)
                    child = right_child

            if self.__is_less_or_eq(self.heap[index], child) ^ self.is_max_heap:
                break
            # swap
            temp = self.heap[index]
            self.heap[index] = child
            self.heap[child_idx] = temp
            index = child_idx

    def __is_less_or_eq(self, element1, element2):
        key_elem1 = self.key_function(element1)
        key_elem2 = self.key_function(element2)
        return key_elem1 <= key_elem2

    @staticmethod
    def __is_root(index):
        return index == 0

    @staticmethod
    def __parent(index):
        return (index - 1) // 2

    @staticmethod
    def __left(index):
        return index * 2 + 1

    @staticmethod
    def __right(index):
        return index * 2 + 2

    @staticmethod
    def __sibling(index):
        return index + 1 if index & 1 else index - 1

# Unit testing
if __name__ == '__main__':
    heap = Heap.from_list([5, 9, 10, 2, 4, 12, 1, 3, 0, -1, 56])
    for i in range(10):
        heap.insert(10 + i)
    while heap:
        print(heap.pop_element())