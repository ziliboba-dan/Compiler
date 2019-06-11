from scoped_symbol_table import ScopedSymbolTable
class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class VariableSymbol(Symbol):
    def __init__(self, name, type):
        super(VariableSymbol, self).__init__(name, type)

    def __str__(self):
        return "<{class_name}(name='{name}', type='{type}')".format(
            class_name=self.__class__.__name__,
            name=self.name,
            type=self.type
        )

    __repr__ = __str__

class FunctionSymbol(Symbol):
    def __init__(self, name, parameters=None):
        super(FunctionSymbol, self).__init__(name)
        self.parameters = parameters if parameters is not None else []

    def __str__(self):
        return '<{class_name}(name={name}, parameters={parameters})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            parameters=self.parameters,
        )

    __repr__ = __str__


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.current_scope = None

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compoundstatement)

    def visit_WHILE(self, node):
        self.visit(node.condition_node)
        self.visit(node.block_node)
    def visit_NoneType(self, node):
        pass

    def visit_IF(self, node):
        self.visit(node.condition_node)
        self.visit(node.block_node)

    def visit_Condition(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Program(self, node):
        # print 'Entering global scope...'
        global_scope = ScopedSymbolTable(
            scope_name='global',
            scope_level=0,
            enclosing_scope=self.current_scope
        )
        self.current_scope = global_scope
        self.visit(node.packageclause)
        self.visit(node.block)
        print(global_scope)
        self.current_scope = self.current_scope.enclosing_scope
        # print 'Leaving global scope...'

    def visit_Packageclause(self, node):
        pass

    def visit_FunctionDeclaration(self, node):
        function_name = node.name
        if self.current_scope.lookup(function_name, current_scope_only=True) is not None:
            raise Exception(
                'Duplicate declaration for variable %s found' % function_name
            )
        function_symbol = FunctionSymbol(function_name)
        self.current_scope.insert(function_symbol)
        # print 'Entering %s scope' % function_name
        function_scope = ScopedSymbolTable(
            scope_name=function_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = function_scope

        for parameter in node.parameters:
            self.visit(parameter)

        self.visit(node.block)
        print(function_scope)
        self.current_scope = self.current_scope.enclosing_scope
        # print 'Leaving %s scope' % function_name

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Number(self, node):
        pass

    def visit_LITTERAL(self, node):
        pass

    def visit_CallFunc(self, node):
        pass
        # # func_name = node.name.value
        # # func_symbol = self.current_scope.lookup(func_name, current_scope_only=False)
        # # if not func_symbol:
        # #     raise Exception(
        # #         "Error: variable %s is undeclared" % func_name
        # #     )
        # for parameter in node.parameters:
        #     self.visit(parameter)

    def visit_VariableDeclaration(self, node):
        type_name = node.type.value
        type_array = node.type.array
        count_array = node.type.count_array
        # print(type_array)   #down 3 rows add in scope;
        # print(count_array)
        # print(type_name)
        i = 0
        # print(node.variable.value)
        if type_array == True:
            while (i < int(count_array)):
                type_symbol = self.current_scope.lookup(type_name)
                variable_name = node.variable.value + str(i)
                # print(variable_name)
                variable_symbol = VariableSymbol(variable_name, type_symbol)
                if self.current_scope.lookup(variable_name, current_scope_only=True) is not None:
                    raise Exception(
                        'Duplicate declaration for variable %s found' % variable_name
                )
                self.current_scope.insert(variable_symbol)
                i = i + 1
            type_symbol = self.current_scope.lookup(type_name)
            variable_name = node.variable.value
            variable_symbol = VariableSymbol(variable_name, type_symbol)
            if self.current_scope.lookup(variable_name, current_scope_only=True) is not None:
                raise Exception(
                    'Duplicate declaration for variable %s found' % variable_name
                )
            self.current_scope.insert(variable_symbol)

        else:
            type_symbol = self.current_scope.lookup(type_name)
            variable_name = node.variable.value
            variable_symbol = VariableSymbol(variable_name, type_symbol)
            if self.current_scope.lookup(variable_name, current_scope_only=True) is not None:
                raise Exception(
                    'Duplicate declaration for variable %s found' % variable_name
                )
            self.current_scope.insert(variable_symbol)

    def visit_Variable(self, node):
        variable_name = node.value
        id_name = node.id
        id_symbol = self.current_scope.lookup(id_name)
        # print(variable_name[:-len(id_name)])
        if id_symbol is not None:
            if self.current_scope.lookup(variable_name[:-len(id_name)]) is not None:
                if (str(id_symbol.type) != 'int'):
                    word = '[' + id_name + ']'
                    raise Exception(
                        "Error: array id not int %s" % word
                    )
            else:
                raise Exception(
                    "Error: variable %s is undeclared" % variable_name[:-len(id_name)]
                )
            return id_symbol.type
        else:
            variable_symbol = self.current_scope.lookup(variable_name)
            if not variable_symbol:
                raise Exception(
                    "Error: variable %s is undeclared" % variable_name
                )
            return variable_symbol.type


    def visit_Assign(self, node):
        self.visit(node.left)
        self.visit(node.right)
        name_left = node.left.value
        type_left = self.visit(node.left)
        # print(str(name_left) + 'left =' + str(type_left.type))

        type_right = ''
        # print(type(node.right).__name__)
        if ((type(node.right).__name__) == 'LITTERAL'):
            type_right = 'string'
        if ((type(node.right).__name__) == 'Number'):
            type_right = 'int'
        if ((type(node.right).__name__) == 'BinaryOperator'):
            type_right = self.visit(node.right)
            # print('right =' + str(type_right))
        if ((type(node.right).__name__) == 'Variable'):

            type_right = self.visit(node.right)
            # print(str(name_right) + 'right =' + str(type_rights.type))

        if (str(type_left) == str(type_right)):
            self.visit(node.left)
            self.visit(node.right)
        else:
            raise Exception(
                'Type not equal, int = str, or str = int'
            )


    def visit_BinaryOperator(self, node):
        type_left = ''
        # print(type(node.right).__name__)
        if ((type(node.left).__name__) == 'LITTERAL'):
            type_left = 'string'
        if ((type(node.left).__name__) == 'Number'):
            type_left = 'int'
        if ((type(node.left).__name__) == 'BinaryOperator'):
            type_left = self.visit(node.left)
        if ((type(node.left).__name__) == 'Variable'):
            # name_left = node.left.value
            # type_lefts = self.current_scope.lookup(name_left)
            # type_left = type_lefts.type
            # print(str(name_right) + 'right =' + str(type_rights.type))
            type_left = self.visit(node.left)

        type_right = ''
        # print(type(node.right).__name__)
        if ((type(node.right).__name__) == 'LITTERAL'):
            type_right = 'str'
        if ((type(node.right).__name__) == 'Number'):
            type_right = 'int'
        if ((type(node.right).__name__) == 'BinaryOperator'):
            self.visit(node.right)
        if ((type(node.right).__name__) == 'Variable'):
            # name_right = node.right.value
            # type_rights = self.current_scope.lookup(name_right)
            # type_right = type_rights.type
            type_right = self.visit(node.right)
            # print(str(name_right) + 'right =' + str(type_rights.type))

        if (str(type_left) == str(type_right)):
            self.visit(node.left)
            self.visit(node.right)
            return type_right
        else:
            raise Exception(
                'Type not equal, int = str, or str = int'
            )

    # Not sure about this
    def visit_Print(self, node):
        self.visit(node.expr)
