import re

def open_txt(filename: str):
    lines = []
    with open(filename, "r") as f:
        for line in f:
            lines.append(line.rstrip())
    return lines

def tokenize(line: str) -> list:
    tokens = []
    for i, char in enumerate(line):
        if char.isnumeric():
            tokens.append(int(char))
        elif char != " ":
            tokens.append(char)
    return tokens

def _parentheses(tokens: list):
    # tokens = ["(" ... ")" ...]
    stack_count = 0
    for i, token in enumerate(tokens):
        if token == "(":
            stack_count += 1
        elif token == ")":
            stack_count -= 1
            if stack_count == 0:
                # return the index of corresponding ")"
                return i

class Node:
    def __init__(self, value: int | str | None) -> None:
        self.value = value
        self.left = None
        self.right = None

def _values_by_layer(root: Node) -> list[list[int | str]]:
    layers = []
    layer = [root]
    while layer:
        layers.append([])
        new_layer = []
        for node in layer:
            layers[-1].append(node.value)
            if node.left:
                new_layer.append(node.left)
            if node.right:
                new_layer.append(node.right)
        layer = new_layer
    return layers

class Tree_Expr:
    def add_nodes(self, tokens: list, current: Node="root", parent: Node=None) -> None:
        if current == "root":
            current = self.root

        if current.value is None:
            if isinstance(tokens[0], int):
                if tokens[1:]:
                    current.left = Node(tokens[0])
                    current.value = tokens[1]
                    current.right = Node(None)
                    self.add_nodes(tokens[2:], current, parent)
                else: # trivial case, the expr is an int
                    current.value = tokens[0]
            else: # tokens[0] == "(", simply ignore the the leading parentheses
                end_idx = _parentheses(tokens)
                if end_idx == len(tokens) - 1:
                    self.add_nodes(tokens[1:-1], current, parent)
                else:
                    self.add_nodes(tokens[1:end_idx], current, parent)
            return

        if isinstance(tokens[0], int):
            current.right.value = tokens[0]
            if tokens[1:]:
                self.add_nodes(tokens[1:], current)
        elif tokens[0] == "+" or tokens[0] == "*":
            next = Node(tokens[0])
            next.left = current
            next.right = Node(None)
            if parent == None:
                self.root = next
            else:
                parent.right = next
            self.add_nodes(tokens[1:], next, parent)
        elif tokens[0] == "(":
            end_idx = _parentheses(tokens)
            self.add_nodes(tokens[1:end_idx], current.right, current)
            if tokens[end_idx+1:]:
                next = Node(tokens[end_idx+1])
                next.left = current
                next.right = Node(None)
                if parent == None:
                    self.root = next
                self.add_nodes(tokens[end_idx+2:], next, parent)

    def __init__(self, tokens: list[int | str]) -> None:
        self.root = Node(None)
        self.add_nodes(tokens)

    def print(self) -> None:
        layers = _values_by_layer(self.root)
        for layer in layers:
            print(layer)

if __name__ == "__main__":
    lines = open_txt("test.txt")
    # lines = open_txt("aoc18.txt")
    print(*lines, sep="\n")
    lines_tokens = []
    for line in lines:
        lines_tokens.append(tokenize(line))
    # print(*lines_tokens, sep="\n")
    tree = Tree_Expr(lines_tokens[1])
    tree.print()
