from .nodes import *
from .validators import *


class BaseNodeParser(ABC):
    parses: tuple[BaseNode]

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
              **extra_data) -> BaseNode:
        """Parses tokens and returns node"""


class AssignNodeParser(BaseNodeParser):
    parses = (AssignNode,)

    def validate(self,
                 tokens: list[BaseToken],
                 supposed_node_type: type[BaseNode],
                 **extra_data) -> bool:
        return check_token_types(tokens, extra_data.get('supposed_types')) \
               and check_token_names(tokens, extra_data.get('supposed_names'))

    def parse(self,
              tokens: list[BaseToken],
              supposed_node_type: type[BaseNode],
              **extra_data) -> BaseNode:
        print(tokens, "PARSE<")
