class Node:
    RED = True
    BLACK = False

    def __init__(self, id, key, color = RED):
        if not type(color) == bool:
            raise TypeError("Bad value for color parameter, expected True/False but given %s" % color)
        self.color = color
        self.key = key
        self.left = self.right = self.parent = NilNode.instance()
        self.id = id

    def __str__(self, level = 0, indent = "   "):
        s = level * indent + str(self.key)
        if self.left:
            s = s + "\n" + self.left.__str__(level + 1, indent)
        if self.right:
            s = s + "\n" + self.right.__str__(level + 1, indent)
        return s

    def __nonzero__(self):
        return True

    def __bool__(self):
        return True


class NilNode(Node):
    __instance__ = None

    @classmethod
    def instance(self):
        if self.__instance__ is None:
            self.__instance__ = NilNode()
        return self.__instance__

    def __init__(self):
        self.color = Node.BLACK
        self.key = None
        self.left = self.right = self.parent = None

    def __nonzero__(self):
        return False

    def __bool__(self):
        return False

class BinarySearchTree:
    def __init__(self):
        self.root = NilNode.instance()
        self.size = 0
        self.control = {}

    def __str__helper(self, node, level = 0, indent = "   "):
        s = level * indent + str(node.id)
        if node.left:
            s += "\n" + self.__str__helper(node.left, level + 1, indent)
        if node.right:
            s += "\n" + self.__str__helper(node.right, level + 1, indent)
        return s

    def __str__(self, indent="  "):
        return ("(root.size = %d)\n" % self.size) + \
                self.__str__helper(self.root, indent=indent)

    def _get_seq(self):
        mn = self.minimum()
        s = str(mn.id)
        next = self.successor(mn)
        while next:
            s += " " + str(next.id)
            next = self.successor(next)
        return s

    def insert(self, id, key):
        x = Node(id, key)
        self.control[x.id] = x
        self.__insert_helper(x)

        x.color = Node.RED
        while x != self.root and x.parent.color == Node.RED:
            if x.parent == x.parent.parent.left:
                y = x.parent.parent.right
                if y and y.color == Node.RED:
                    x.parent.color = Node.BLACK
                    y.color = Node.BLACK
                    x.parent.parent.color = Node.RED
                    x = x.parent.parent
                else:
                    if x == x.parent.right:
                        x = x.parent
                        self.__left_rotate(x)
                    x.parent.color = Node.BLACK
                    x.parent.parent.color = Node.RED
                    self.__right_rotate(x.parent.parent)
            else:
                y = x.parent.parent.left
                if y and y.color == Node.RED:
                    x.parent.color = Node.BLACK
                    y.color = Node.BLACK
                    x.parent.parent.color = Node.RED
                    x = x.parent.parent
                else:
                    if x == x.parent.left:
                        x = x.parent
                        self.__right_rotate(x)
                    x.parent.color = Node.BLACK
                    x.parent.parent.color = Node.RED
                    self.__left_rotate(x.parent.parent)
        self.root.color = Node.BLACK

    def delete(self, id):
        z = self.control[id]
        if not z.left or not z.right:
            y = z
        else:
            y = self.successor(z)
        if not y.left:
            x = y.right
        else:
            x = y.left
        x.parent = y.parent

        if not y.parent:
            self.root = x
        else:
            if y == y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x

        if y != z:
            z.key = y.key
            z.id = y.id
            self.control[z.id] = z

        if y.color == Node.BLACK:
            self.__delete_fixup(x)

        self.size -= 1
        return y

    def minimum(self, x = None):
        if x is None: x = self.root
        while x.left:
            x = x.left
        return x

    def maximum(self, x = None):
        if x is None: x = self.root
        while x.right:
            x = x.right
        return x

    def successor(self, x):
        if x.right:
            return self.minimum(x.right)
        y = x.parent
        while y and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self, x):
        if x.left:
            return self.maximum(x.left)
        y = x.parent
        while y and x == y.left:
            x = y
            y = y.parent
        return y

    def search(self, id):
        # if x is None: x = self.root
        # while x and x.key != key:
        #     if key < x.key:
        #         x = x.left
        #     else:
        #         x = x.right
        # print(x, "<<<<")
        return self.control[id]

    def is_empty(self):
        return bool(self.root)

    def __left_rotate(self, x):
        if not x.right:
            raise "x.right is nil!"
        y = x.right
        x.right = y.left
        if y.left: y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y

    def __right_rotate(self, x):
        if not x.left:
            raise "x.left is nil!"
        y = x.left
        x.left = y.right
        if y.right: y.right.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.right = x
        x.parent = y

    def __insert_helper(self, z):
        y = NilNode.instance()
        x = self.root
        while x:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if not y:
            self.root = z
        else:
            if z.key < y.key:
                y.left = z
            else:
                y.right = z

        self.size += 1

    def __delete_fixup(self, x):
        while x != self.root and x.color == Node.BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == Node.RED:
                    w.color = Node.BLACK
                    x.parent.color = Node.RED
                    self.__left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == Node.BLACK and w.right.color == Node.BLACK:
                    w.color = Node.RED
                    x = x.parent
                else:
                    if w.right.color == Node.BLACK:
                        w.left.color = Node.BLACK
                        w.color = Node.RED
                        self.__right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = Node.BLACK
                    w.right.color = Node.BLACK
                    self.__left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == Node.RED:
                    w.color = Node.BLACK
                    x.parent.color = Node.RED
                    self.__right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == Node.BLACK and w.left.color == Node.BLACK:
                    w.color = Node.RED
                    x = x.parent
                else:
                    if w.left.color == Node.BLACK:
                        w.right.color = Node.BLACK
                        w.color = Node.RED
                        self.__left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = Node.BLACK
                    w.left.color = Node.BLACK
                    self.__right_rotate(x.parent)
                    x = self.root
        x.color = Node.BLACK
