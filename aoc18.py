def open_txt(filename: str):
    lines = []
    with open(filename, "r") as f:
        for line in f:
            lines.append(line.rstrip())
    return lines

def tokenize(line: str) -> list:
    tokens = []
    for char in line:
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

def _arithmetic(a: int, b: int, op: str) -> int:
    if op == "+":
        return a + b
    elif op == "*":
        return a * b

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
                #  parentheses precedence already taken care when adding the edges
                end_idx = _parentheses(tokens)
                if end_idx == len(tokens) - 1:
                    self.add_nodes(tokens[1:-1], current, parent)
                else:
                    current.value = tokens[end_idx+1]
                    current.left = Node(None)
                    self.add_nodes(tokens[1:end_idx], current.left, current)
                    current.right = Node(None)
                    self.add_nodes(tokens[end_idx+2:], current, parent)
            return

        if isinstance(tokens[0], int):
            current.right.value = tokens[0]
            if tokens[1:]:
                self.add_nodes(tokens[1:], current, parent)
        elif tokens[0] == "+" or tokens[0] == "*":
            next = Node(tokens[0])
            next.left = current
            next.right = Node(None)
            if current == self.root:
                self.root = next
            elif parent.left == current:
                parent.left = next
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
                if current == self.root:
                    self.root = next
                elif parent.left == current:
                    parent.left = next
                else:
                    parent.right = next
                self.add_nodes(tokens[end_idx+2:], next, parent)

    def __init__(self, tokens: list[int | str]) -> None:
        self.root = Node(None)
        self.add_nodes(tokens)

    def print(self) -> None:
        layers = _values_by_layer(self.root)
        for layer in layers:
            print(layer)

    def _recur(self, current: Node):
        if isinstance(current.value, int):
            return current.value
        elif isinstance(current.left.value, int):
            if isinstance(current.right.value, int):
                return _arithmetic(current.left.value, current.right.value, current.value)
            else:
                return _arithmetic(current.left.value, self._recur(current.right), current.value)
        else:
            if isinstance(current.right.value, int):
                return _arithmetic(self._recur(current.left), current.right.value, current.value)
            else:
                return _arithmetic(self._recur(current.left), self._recur(current.right), current.value)

    def evaluate(self) -> int:
        return self._recur(self.root)

def part1(lines: list[str]) -> int:
    result = 0
    for line in lines:
        tokens = tokenize(line)
        tree = Tree_Expr(tokens)
        result += tree.evaluate()
    return result

def part2(lines: list[str]) -> int:
    result = 0
    for line in lines:
        tokens = tokenize(line)
        modified = []
        while tokens:
            token = tokens.pop(0)
            if token == "+":
                if modified[-1] == ")":
                    start_idx = _parentheses(modified[::-1])
                    modified.insert(-1 - start_idx, "(")
                else:
                    modified.insert(-1, "(")
                if tokens[0] == "(":
                    end_idx = _parentheses(tokens)
                    tokens.insert(end_idx+1, ")")
                else:
                    tokens.insert(1, ")")
            modified.append(token)
        # print(modified)
        tree = Tree_Expr(modified)
        result += tree.evaluate()
    return result

if __name__ == "__main__":
    # lines = open_txt("test.txt")
    lines = open_txt("aoc18.txt")
    # print(*lines, sep="\n")
    print("part 1: ", part1(lines))
    print("part 2: ", part2(lines))
