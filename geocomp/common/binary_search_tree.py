class Node:
    RED = True
    BLACK = False

    def __init__(self, id: int, key, color: bool = RED):
        self.color = color
        self.key = key
        self.left = self.right = self.parent = NilNode.instance()
        self.id = id

    def __str__(self, level: int = 0, indent: str = "   ") -> str:
        left_id = "Nil" if not self.left else self.left.id
        right_id = "Nil" if not self.right else self.right.id
        parent_id = "Nil" if not self.parent else self.parent.id
        return f"Node(id={self.id}, parent={parent_id}, left={left_id}, right={right_id}, red={self.color})"

    def __nonzero__(self):
        return True

    def __bool__(self):
        return True

    def is_red(self) -> bool:
        return self.color == Node.RED


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

    def is_red(self) -> bool:
        return False

class BinarySearchTree:
    def __init__(self):
        self.root = NilNode.instance()
        self.size = 0
        self.control = {}

    def __str__helper(self, node: Node, level: int = 0, indent: str = "   "):
        s = level * indent + str(node)
        if node.left:
            s += "\n" + self.__str__helper(node.left, level + 1, indent)
        if node.right:
            s += "\n" + self.__str__helper(node.right, level + 1, indent)
        return s

    def __str__(self, indent: str = "  "):
        if not self.root:
            return "(root.size = 0, balanced = True)\n(Empty tree)"
        res, _ = self.is_rbt()
        return f"(root.size = {self.size}, RBT = {res})\n" + \
               self.__str__helper(self.root, indent=indent)

    def is_empty(self) -> bool:
        return bool(self.root)

    def insert(self, id: int, key):
        new_node = Node(id, key)
        self.control[new_node.id] = new_node
        self.root = self.__insert(self.root, new_node)
        self.root.parent = NilNode.instance()
        self.__insert_balance(new_node)
        self.size += 1

        res, err = self.is_rbt()
        if not res:
            print(str(self))
            raise Exception(err)

    def __insert(self, act_node, new_node: Node) -> Node:
        if not act_node:
            return new_node

        if new_node.key < act_node.key:
            act_node.left = self.__insert(act_node.left, new_node)
            act_node.left.parent = act_node
        else:
            act_node.right = self.__insert(act_node.right, new_node)
            act_node.right.parent = act_node

        return act_node

    def __insert_balance(self, node: Node):
        while node != self.root and node.parent.is_red():
            parent = node.parent
            if parent == parent.parent.left:
                uncle = parent.parent.right
                if uncle and uncle.is_red():
                    node = parent.parent
                    self.__flip_colors(node)
                else:
                    if node == parent.right:
                        node = parent
                        self.__rotate_left(node)
                    self.__rotate_right(node.parent.parent)
            else:
                uncle = parent.parent.left
                if uncle and uncle.is_red():
                    node = parent.parent
                    self.__flip_colors(node)
                else:
                    if node == parent.left:
                        node = parent
                        self.__rotate_right(node)
                    self.__rotate_left(node.parent.parent)
        self.root.color = Node.BLACK

    def delete(self, id: int) -> Node:
        if not (id in self.control):
            return

        old = self.control[id]
        del self.control[id]

        if old.left and old.right:
            new_old = self.__successor(old)
            old.key = new_old.key
            old.id = new_old.id
            self.control[old.id] = old
            old = new_old

        child = old.right if not old.left else old.left
        child.parent = old.parent
        if old == old.parent.left:
            old.parent.left = child
        elif old == old.parent.right:
            old.parent.right = child
        else:
            self.root = child

        if not old.is_red():
            if child.is_red():
                child.color = Node.BLACK
            else:
                self.__delete_balance(child)

        self.size -= 1

        res, err = self.is_rbt()
        if not res:
            print(str(self))
            raise Exception(err)
        return old

    def __delete_balance(self, node):
        if self.root == node or node.is_red():
            node.color = Node.BLACK
            return
        left = (node == node.parent.left)
        parent = node.parent
        sibling = node.parent.right if left else node.parent.left
        if sibling.is_red():
            if left:
                self.__rotate_left(parent)
                sibling = parent.right
            else:
                self.__rotate_right(parent)
                sibling = parent.left
        if not sibling.right.is_red() and not sibling.left.is_red():
            sibling.color = Node.RED
            self.__delete_balance(parent)
        else:
            if left:
                if not sibling.right.is_red():
                    self.__rotate_right(sibling)
                    sibling = parent.right
                self.__rotate_left(parent)
            else:
                if not sibling.left.is_red():
                    self.__rotate_left(sibling)
                    sibling = parent.left
                self.__rotate_right(parent)
            sibling.left.color = Node.BLACK
            sibling.right.color = Node.BLACK

    def minimum(self, node = None):
        if node is None: node = self.root
        while node.left:
            node = node.left
        return node

    def maximum(self, node = None):
        if node is None: node = self.root
        while node.right:
            node = node.right
        return node

    def __successor(self, node: Node):
        if node.right:
            return self.minimum(node.right)
        parent = node.parent
        while parent and node == parent.right:
            node, parent = parent, parent.parent
        return parent

    def __rotate_right(self, node: Node):
        child = node.left
        node.left = child.right
        child.right = node
        child.color = child.right.color
        child.right.color = Node.RED
        child.parent = node.parent
        node.parent = child
        if node.left: node.left.parent = node
        if child.parent.left == node:
            child.parent.left = child
        elif child.parent.right == node:
            child.parent.right = child
        else:
            self.root = child

    def __rotate_left(self, node: Node):
        child = node.right
        node.right = child.left
        child.left = node
        child.color = child.left.color
        child.left.color = Node.RED
        child.parent = node.parent
        node.parent = child
        if node.right: node.right.parent = node
        if child.parent.left == node:
            child.parent.left = child
        elif child.parent.right == node:
            child.parent.right = child
        else:
            self.root = child

    def __flip_colors(self, node: Node):
        node.color = not node.color
        node.left.color =  not node.left.color
        node.right.color =  not node.right.color

    def is_rbt(self) -> tuple:
        if not self.root:
            return (True, "")
        node = self.root
        final_blacks = 1
        while node:
            node = node.right
            if not node.is_red():
                final_blacks += 1
        errors, ids = self.__is_rbt(self.root, 0, final_blacks)
        if errors == 0:
            return (True, "")
        elif errors == 1:
            return (False, f"Tree is not balanced on ids {ids}")
        elif errors == 2:
            return (False, f"Tree has double red nodes on ids {ids}")
        return (False, f"Tree is not balanced and has double red nodes on ids {ids}")

    def __is_rbt(self, node, blacks: int, final_blacks: int):
        if not node.is_red():
            blacks += 1
        elif node.left.is_red() or node.right.is_red():
            return (2, [node.id])
        if not node:
            return (0, []) if blacks == final_blacks else (1, [-1])
        lerr, lids = self.__is_rbt(node.left, blacks, final_blacks)
        rerr, rids = self.__is_rbt(node.right, blacks, final_blacks)
        if lerr != 0 and rerr != 0:
            return (lerr ^ rerr, lids + rids)
        if lerr != 0:
            return (lerr, lids)
        if rerr != 0:
            return (rerr, rids)
        return (0, [])
