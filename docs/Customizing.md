# FastPy customizing

### Customize operators

If you don't like how the operators look, you can change the [ops config file](../config/operators.json).

### Customize stages

For stage customization you need to inherit ```BaseClass``` of that stage and change the eponymous config file.

#### Lexing

*Config file:* [lexer.json](../config/lexer.json)

*Base interface classes:*

- Base stage class: ```BaseLexer```
- Token base class: ```BaseToken```
- Detector base class: ```BaseDetector```

*Examples:*

```python
from fastpy.lexer import BaseLexer, BaseToken, BaseDetector
from fastpy.module import Module


class MyLexer(BaseLexer):
    """Your implementation of BaseLexer interface"""

    def __init__(self, module: Module):
        """

        :param module: the module parameter contains information about the currently processed file
        """

    def lex(self) -> list[BaseToken]:
        """
        Splits the code into a list of tokens

        :return: list of tokens
        """
```

#### Parsing

*Config file:* [parser.json](../config/parser.json)

*Base interface classes:*

- Base stage class: ```BaseParser```
- Abstract Syntax Tree base class: ```BaseAST```
- Node parser class: ```BaseNodeParser```

*Examples:*

```python
from fastpy.parser import BaseParser, BaseNode, BaseAST
from fastpy.lexer import BaseToken
from fastpy.module import Module


class MyParser(BaseParser):
    """Your implementation of BaseParser interface"""

    def __init__(self,
                 module: Module,
                 tokens: list[BaseToken]):
        """
        
        :param module: the module parameter contains information about the currently processed file
        :param tokens: list of tokens - output of previous stage
        """

    def parse(self) -> BaseAST:
        """
        Parses tokens and returns an Abstract Syntax Tree
        
        :return: Abstract Syntax Tree
        """
```

#### Transpiling

*Config file:* [transpiler.json](../config/transpiler.json)

*Base interface classes:*

- Base stage class: ```BaseTranspiler```
- Base node transpiler class: ```BaseNodeTranspiler```

*Examples:*

```python
from fastpy.transpiler import BaseTranspiler
from fastpy.module import Module
from fastpy.parser import BaseAST


class MyTranspiler(BaseTranspiler):
    """Your implementation transpailer interface"""

    def __init__(self, module: Module, ast: BaseAST):
        """
        
        :param module: module: the module parameter contains information about the currently processed file
        :param ast: Abstract Syntax Tree - output of previous stage
        """

    def transpile(self) -> str:
        """
        Transpile an Abstract Syntax Tree to source C++ code
        
        :return: C++ code
        """
```