from collections import OrderedDict

class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class ValidType(Symbol):
    def __init__(self, name):
        super(ValidType, self).__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )


class ScopedSymbolTable():
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self._symbols = OrderedDict()
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        self._init_builtins()

    def _init_builtins(self):
        self.insert(ValidType('int'))
        self.insert(ValidType('string'))

    def __str__(self):
            h1 = 'Symbol Table'
            lines = ['\n', h1, '=' * len(h1)]
            for header_name, header_value in (
                ('Scope name', self.scope_name),
                ('Scope level', self.scope_level),
                ('Out scope', self.enclosing_scope.scope_name if self.enclosing_scope else None),
            ):
                lines.append('%-15s: %s' % (header_name, header_value))
            h2 = 'Contents'
            lines.extend([h2, '-' * len(h2)])
            lines.extend(
                ('%7s: %r' % (key, value))
                for key, value in self._symbols.items()
            )
            lines.extend(['-' * len(h2)])
            lines.append('\n')
            s = '\n'.join(lines)
            return s

    __repr__ = __str__

    def insert(self, symbol):
        # print('Inserting: %s into symbol table' % symbol.name)
        self._symbols[symbol.name] = symbol

    def lookup(self, name, current_scope_only=False):
        # print('Looking up: %s (Scope name: %s)' % (name, self.scope_name))

        symbol = self._symbols.get(name)
        if symbol is not None:
            return symbol

        if current_scope_only:
            return None

        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)
