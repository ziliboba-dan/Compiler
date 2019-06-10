import token_names as tokens
import abstract_syntax_tree as AST

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        raise Exception(message)

    def accept(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            error_message = """
                Trying to accept token type \'{}\' but current token type is \'{}\'
            """.format(token_type, self.current_token.type)
            self.error(error_message)

    def Program(self):
        """
        SourceFile -> Packageclause Block
        """
        packageclause_nodes = self.packageclause()
        block_node = self.block()
        program_node = AST.Program(packageclause_nodes, block_node)
        return program_node

    def block(self):
        """
        Block -> Decl CompStatement
        """
        # packageclause_nodes = self.packageclause()
        declaration_nodes = self.decl()
        compound_statement_node = self.compstatement()
        block_node = AST.Block(declaration_nodes, compound_statement_node)
        return block_node

    def packageclause(self):
        """
        packageclause : "package" identifier .
        """
        if self.current_token.type == tokens.PACKAGE:
            self.accept(tokens.PACKAGE)
            if self.current_token.type == tokens.ID:
                id_node = self.variable()
                packageclause_node = AST.Packageclause(id_node)
                self.accept(tokens.SEMI)
                return packageclause_node
        else:
            self.error("Add package main")

    def decl(self):
        """
        Decl -> ("var" (VarDeclaration)+)*
               | ("func" ID "(" ParametrList ")" "{" Block "}")*
               | Empty
        """
        declarations = []
        parameters = []

        while True:
            while self.current_token.type == tokens.VAR:
                self.accept(tokens.VAR)
                while self.current_token.type == tokens.ID:
                    declarations.extend(self.vardeclaration())
                self.accept(tokens.SEMI)
            while self.current_token.type == tokens.FUNCTION:
                token = self.current_token
                self.accept(tokens.FUNCTION)
                token_name = self.current_token.value
                self.accept(tokens.ID)
                if self.current_token.type == tokens.LPAREN:
                    self.accept(tokens.LPAREN)
                    # print(self.current_token)
                    parameters = self.parametrlist()
                    self.accept(tokens.RPAREN)
                else:
                    self.error("PARAMETRS GIVEEEEEEE, nu lan prost skobochki")
                self.accept(tokens.LBRACE)
                block_node = self.block()
                self.accept(tokens.RBRACE)
                self.accept(tokens.SEMI)
                function_declaration = AST.FunctionDeclaration(token, token_name, parameters, block_node)
                declarations.append(function_declaration)
            else:
                break
        return declarations

    def parametrlist(self):
        """
        ParametrList -> Parametrs
                | Parametrs "," ParametrList
        """
        if self.current_token.type == tokens.ID:
            parameter_nodes = self.vardeclaration()
            return parameter_nodes
        else:
            return []


    def vardeclaration(self):
        """
        VarDeclaration -> ID ("[" Number"]")? ("," ID ("[" Number"]")?)*  TypeSpec #ID~Variable~identifier
        """
        id = ''
        arr_bool = False
        count = 1
        variable_nodes = []
        variable_nodes.append(AST.Variable(self.current_token, id))
        self.accept(tokens.ID)
        while self.current_token.type == tokens.COMMA:
            self.accept(tokens.COMMA)
            variable_nodes.append(AST.Variable(self.current_token, id))
            self.accept(tokens.ID)
        if self.current_token.type == tokens.LBRACKET:
            self.accept(tokens.LBRACKET)
            if self.current_token.type == tokens.INT:
                count = self.current_token.value
                self.accept(tokens.INT)
                if self.current_token.type == tokens.RBRACKET:
                    self.accept(tokens.RBRACKET)
                    arr_bool = True
        else:
            arr_bool = False
        type_node = self.typespec(arr_bool, count)
        variable_declarations = [
            AST.VariableDeclaration(variable_node, type_node) for variable_node in variable_nodes
        ]
        return variable_declarations

    def typespec(self, arr_bool, count_array):
        """
        TypeSpec ->  ""int" | "string"

        """
        if arr_bool:
            token = self.current_token
            if self.current_token.type == tokens.INT:
                self.accept(tokens.INT)
                return AST.Type(token, True, count_array)
            if self.current_token.type == tokens.STRING:
                self.accept(tokens.STRING)
                return AST.Type(token, True, count_array)
            self.error('Unexpected token type %s in type_spec function' % self.current_token.type)
        else:
            token = self.current_token
            if self.current_token.type == tokens.INT:
                self.accept(tokens.INT)
                return AST.Type(token, False, count_array)
            if self.current_token.type == tokens.STRING:
                self.accept(tokens.STRING)
                return AST.Type(token, False, count_array)
            self.error('Unexpected token type %s in type_spec function' % self.current_token.type)

    def factor(self):
        """
          Factor : "+" Factor
           | "-" Factor
           | "int"
           | "string"
           | LPAREN Expr RPAREN
           | Variable
        """
        token = self.current_token
        if token.type == tokens.INT:
            self.accept(tokens.INT)
            return AST.Number(token)
        if token.type == tokens.PLUS:
            self.accept(tokens.PLUS)
            node = AST.UnaryOperator(token, self.factor())
            return node
        if token.type == tokens.MINUS:
            self.accept(tokens.MINUS)
            node = AST.UnaryOperator(token, self.factor())
            return node
        if token.type == tokens.LPAREN:
            self.accept(tokens.LPAREN)
            node = self.expr()
            self.accept(tokens.RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def term(self):
        """
        Term: Factor (("*" | "/") Factor)*
        """
        node = self.factor()

        while self.current_token.type in (tokens.MULTIPLY, tokens.DIVIDE):
            token = self.current_token
            if token.type == tokens.MULTIPLY:
                self.accept(tokens.MULTIPLY)
            elif token.type == tokens.DIVIDE:
                self.accept(tokens.DIVIDE)
            node = AST.BinaryOperator(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        """
        Expr: Term (("+" | "-") Term)*
        """
        node = self.term()

        while self.current_token.type in (tokens.PLUS, tokens.MINUS):
            token = self.current_token
            if token.type == tokens.PLUS:
                self.accept(tokens.PLUS)
            elif token.type == tokens.MINUS:
                self.accept(tokens.MINUS)
            node = AST.BinaryOperator(left=node, op=token, right=self.term())
        return node


    def compstatement(self):
        """CompStatement -> StatementList"""
        nodes = self.statementlist()

        root = AST.Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statementlist(self):
        """
        StatementList -> Statement
               | Statement ";" StatementList
        """
        node = self.statement()
        results = [node]
        while self.current_token.type == tokens.SEMI:
            self.accept(tokens.SEMI)
            results.append(self.statement())
        if self.current_token.type == tokens.ID:
            self.error('Unexpected token type %s in statement_list function'.format(self.current_token.type))

        return results

    def statement(self):
        """
        Statement ->  CompStatement
          | (AssigAtatement|CallStmt)
          | PrintStatement
          | ScanStatement
          | IfStmt
          | WhileStmt
          | CallStmt
          | Empty
        """
        node = None
        # if self.current_token.type == tokens.VAR or self.current_token.type == tokens.FUNCTION:
        #     self.error("Please declaration at the beginning of the block")
        if self.current_token.type == tokens.ID:

            node = self.assigatatement()
        elif self.current_token.type == tokens.PRINT:
            node = self.printstatement()
        elif self.current_token.type == tokens.SCAN:
            node = self.scanstatement()
        elif self.current_token.type == tokens.IF:
            node = self.ifstatement()
        elif self.current_token.type == tokens.FOR:
            node = self.whilestatement()
        else:
            node = self.empty()
        return node

    def ifstatement(self):
        """
        IfStmt -> "if" Condition .
        """
        self.accept(tokens.IF)
        condition_node = self.condition()
        if self.current_token.type == tokens.LBRACE:
            self.accept(tokens.LBRACE)
            block_node = self.block()
            self.accept(tokens.RBRACE)
            node = AST.IF(condition_node, block_node)
            return node

    def whilestatement(self):
        """
        WhileStmt        -> "for" Condition Block.
        """
        self.accept(tokens.FOR)
        condition_node = self.condition()
        if self.current_token.type == tokens.LBRACE:
            self.accept(tokens.LBRACE)
            block_node = self.block()
            self.accept(tokens.RBRACE)
            node = AST.WHILE(condition_node, block_node)
            return node

    def condition(self):
        """
        Condition       -> "(" Expr rel_op Expr ")" Block.
        """
        if self.current_token.type == tokens.LPAREN:
            self.accept(tokens.LPAREN)
            left = self.factor()
            op = self.realop()
            right = self.factor()
            self.accept(tokens.RPAREN)
            node = AST.Condition(left, op, right)
            return node

    def realop(self):
        """
        rel_op          -> "==" | "!=" | "<" | "<=" | ">" | ">=".
        """
        operations = {tokens.EQUAL, tokens.EQR, tokens.EQL,
                      tokens.NOTEQUAL, tokens.MORE, tokens.LESS}
        if self.current_token.type in operations:
            node = self.current_token
            self.accept(self.current_token.type)
            return node

    def stmtlist(self):
        """
        ParametrList -> Parametrs
                | Parametrs "," ParametrList
        """
        parameter_nodes = []
        parameter_nodes.append(AST.Variable(self.current_token, id))
        if self.current_token.type == tokens.ID:
            self.accept(tokens.ID)
        else:
            return []
        while self.current_token.type == tokens.COMMA:
            self.accept(tokens.COMMA)
            parameter_nodes.append(AST.Variable(self.current_token, id))
            self.accept(tokens.ID)
        return parameter_nodes

    def assigatatement(self):
        """
        AssigAtatement ->  Variable "=" Expr
        """
        parameters = []
        left = self.variable()
        token = self.current_token
        if self.current_token.type == tokens.ASSIGN:
            self.accept(tokens.ASSIGN)
            right = self.expr()
            node = AST.Assign(left, token, right)
            return node
        elif self.current_token.type == tokens.LPAREN:
            self.accept(tokens.LPAREN)
            parameters = self.stmtlist()
            self.accept(tokens.RPAREN)
            return AST.CallFunc(left, parameters)

    def printstatement(self):
        """
        PrintStatement ->  "print" Expr
        """
        token = self.current_token
        self.accept(tokens.PRINT)
        expr = self.expr()
        node = AST.Print(token, expr)
        return node

    # def scanstatement(self):
    #     """
    #     ScanStatement : "scan" "(" "&" Variable ")"
    #     """
    #     token = self.current_token
    #     self.accept(tokens.PRINT)
    #     expr = self.expr()
    #     node = AST.Print(token, expr)
    #     return node

    def variable(self):
        """
        Variable ->  identifier | identifier "[" Number "]"
        """
        # arr_bool = False
        node = []
        token = self.current_token
        id = ''
        self.accept(tokens.ID)
        if self.current_token.type == tokens.LBRACKET:
            self.accept(tokens.LBRACKET)
            if self.current_token.type == tokens.INT or self.current_token.type == tokens.ID:
                id = self.current_token.value
                self.accept(self.current_token.type)
                if self.current_token.type == tokens.RBRACKET:
                    self.accept(tokens.RBRACKET)
                    node = AST.Variable(token, id)
        else:
            node = AST.Variable(token, id)
        return node

    def empty(self):
        """An empty production"""
        return AST.NoOp()

    def parse(self):
        node = self.Program()
        if self.current_token.type != tokens.EOF:
            self.error('Expected token type EOF but got %s' % self.current_token.type)
        return node
