from .nodes import *
from .validators import *
from ..singleton import singleton
from ..import_tools import import_class


class BaseNodeParser(ABC):
    parses: tuple[type[BaseNode]]

    @abstractmethod
    def validate(self,
                 tokens: list[BaseToken],
                 supposed_node_type: type[BaseNode],
                 **extra_data) -> bool: ...

    @abstractmethod
    def parse(self,
              tokens: list[BaseToken],
              parse_node_clb: callable,
              supposed_node_type: type[BaseNode],
              **extra_data) -> BaseNode: ...


@singleton
class UniversalNodeParser(BaseNodeParser):
    parses = (AssignNode,)

    def validate(self,
                 tokens: list[BaseToken],
                 supposed_node_type: type[BaseNode],
                 **extra_data) -> bool:
        for method_name, method_kwargs in extra_data.get('methods').items():
            if not getattr(Validators, method_name)(
                    tokens=tokens,
                    **method_kwargs
            ):
                return False
        return True

    @staticmethod
    def _parse_value(tokens: list[BaseToken], parse_node: callable, **value_data):
        index = value_data.get('index')
        parser_class_path = value_data.get('parser_class')

        if index is not None:
            return tokens[index]

        elif parser_class_path:
            parser_class = import_class(parser_class_path)
            parser = parser_class()
            possible_node_types = tuple(
                import_class(node_class_path)
                for node_class_path in value_data.get('possible_node_classes')
            )
            tokens_slice_data = value_data.get('tokens_slice')
            slice_start = tokens_slice_data.get('start_index')
            if slice_start:
                return parse_node(
                    tokens=tokens[slice_start::],
                    possible_node_types=possible_node_types,
                    parser=parser
                )

    def parse(self,
              tokens: list[BaseToken],
              supposed_node_type: type[BaseNode],
              parse_node_clb: callable,
              **extra_data) -> BaseNode:

        node_arguments = {}
        for key, value_data in extra_data.items():
            node_arguments.update({
                key: self._parse_value(
                    tokens=tokens,
                    parse_node=parse_node_clb,
                    **value_data)
            })

        return supposed_node_type(
            **node_arguments
        )
