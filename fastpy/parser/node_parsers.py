from .nodes import *
# from .validators import *
from .validators import *


class BaseNodeParser(ABC):
    """Node parser interface"""

    parses: tuple[BaseNode]  # nodes that can be parsed by this parser

    @abstractmethod
    def validate(self,
                 tokens: list[BaseToken],
                 supposed_node_type: type[BaseNode],
                 **extra_data) -> bool:
        """Checks if the tokens are suitable for parsing the current node type"""

    @abstractmethod
    def parse(self,
              tokens: list[BaseToken],
              supposed_node_type: type[BaseNode],
              parse_node_callback: callable,
              **extra_data) -> BaseNode:
        """Parses tokens and returns node"""


class UniversalNodeParser(BaseNodeParser):
    """Basic universal node parser of FastPy"""

    parses = (AssignNode, ValueNode)

    def validate(self,
                 tokens: list[BaseToken],
                 supposed_node_type: type[BaseNode],
                 **extra_data) -> bool:
        validators = extra_data.get('validators')
        if validators:
            results = []

            for validator_name, arguments in validators.items():
                result = getattr(Validators, validator_name)(tokens=tokens, **arguments)
                results.append(result)
            return all(results)

    def parse(self,
              tokens: list[BaseToken],
              supposed_node_type: type[BaseNode],
              parse_node_callback: callable,
              **extra_data) -> BaseNode:
        node_arguments = {}

        for key, value_getting_info in extra_data.items():
            value = None
            if isinstance(value_getting_info, dict):
                slice_start = value_getting_info.get('slice_start')
                value = parse_node_callback(tokens[slice_start::])
            elif isinstance(value_getting_info, int):
                value = tokens[value_getting_info]

            node_arguments.update({key: value})

        return supposed_node_type(**node_arguments)
