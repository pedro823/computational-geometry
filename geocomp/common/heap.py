identity = lambda x: x

class Heap:

    @classmethod
    def from_list(cls, element_list: list, is_max_heap: bool, key_function=identity):
        heap = cls(is_max_heap, key_function)
        for element in element_list:
            heap.insert(element)
        return heap


    def __init__(self, is_max_heap: bool, key_function=identity):
        ''' Initializes an empty heap.
            :param is_max_heap: True if heap should be a max-heap.
                                False otherwise.
            :param key_function: A function that extracts the key
            from the element. The heap will be indexed by the key.
        '''
        self.heap = []
        self.key_function = key_function
        self.length = 0
        self.is_max_heap = is_max_heap

    def insert(self, element):
        key = self.key_function(element)
        self.heap.append(element)
        self.__promote(len(self.heap) - 1)

    def peek_top(self):
        return self.heap[0]

    def pop_element(self):
        top_element = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.__sink(0)
        return top_element

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

            if self.__is_less_or_eq(child, self.heap[index]) ^ self.is_max_heap:
                break
            # swap
            temp = self.heap[index]
            self.heap[index] = child
            self.heap[child_idx] = temp
            index = child_idx

    def __is_less_or_eq(self, element1, element2):
        key_elem1 = self.key_function(element1)
        key_elem2 = self.key_function(element2)
        return key_elem1 < key_elem2

    def __is_root(self, index):
        return index == 0

    def __parent(self, index):
        return (index - 1) // 2

    def __left(self, index):
        return index * 2 + 1

    def __right(self, index):
        return index * 2 + 2

    def __sibling(self, index):
        return index + 1 if index & 1 else index - 1
