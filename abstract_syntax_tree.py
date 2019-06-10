import json

class AbstractSyntaxTree(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


class Program(AbstractSyntaxTree):
    def __init__(self, packageclause, block):
        self.block = block
        self.packageclause = packageclause

class Block(AbstractSyntaxTree):
    def __init__(self, declarations, compoundstatement):
        self.declarations = declarations
        self.compoundstatement = compoundstatement

class Packageclause(AbstractSyntaxTree):
    def __init__(self, name):
        self.name = name

class Type(AbstractSyntaxTree):
    def __init__(self, token, array, count_array):
        # self.token = token
        self.value = token.type
        self.array = array
        self.count_array = count_array


class VariableDeclaration(AbstractSyntaxTree):
    def __init__(self, variable, type):
        self.variable = variable
        self.type = type
# Add MASSIV THAT CHECK IN SEMANTIC

class FunctionDeclaration(AbstractSyntaxTree):
    def __init__(self, token, token_name, parameters, block):
        self.type = token.type
        self.name = token_name
        self.parameters = parameters
        self.block = block


class Variable(AbstractSyntaxTree):
    def __init__(self, token, id):
        # self.token = token
        self.value = str(token.value) + str(id)


class UnaryOperator(AbstractSyntaxTree):
    def __init__(self, op, expr):
        # self.token = op
        self.op = op.type
        self.expr = expr


class BinaryOperator(AbstractSyntaxTree):
    def __init__(self, left, op, right):
        self.left = left
        # self.token = op
        self.op = op.type
        self.right = right


class Number(AbstractSyntaxTree):
    def __init__(self, token):
        # self.token = token
        self.value = token.value


class Compound(AbstractSyntaxTree):
    """Represents a '{ }' block"""
    def __init__(self):
        self.children = []


class Assign(AbstractSyntaxTree):
    def __init__(self, left, op, right):
        self.left = left
        # self.token = op
        self.op = op.type
        self.right = right

class Print(AbstractSyntaxTree):
    def __init__(self, token, expr):
        self.type = token.type
        self.expr = expr

class NoOp(AbstractSyntaxTree):
    pass

class Parameter(AbstractSyntaxTree):
    def __init__(self, variable_node, type_node):
        self.variable_node = variable_node
        self.type_node = type_node

class IF(AbstractSyntaxTree):
    def __init__(self, condition_node, block_node):
        self.type = 'IF'
        self.condition_node = condition_node
        self.block_node = block_node

class WHILE(AbstractSyntaxTree):
    def __init__(self, condition_node, block_node):
        self.type = 'WHILE'
        self.condition_node = condition_node
        self.block_node = block_node

class CallFunc(AbstractSyntaxTree):
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

class Condition(AbstractSyntaxTree):
    def __init__(self, left, op, right):
        self.left = left
        # self.token = op
        self.op = op.type
        self.right = right
