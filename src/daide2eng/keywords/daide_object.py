from abc import ABC, abstractmethod
from dataclasses import dataclass

from typing_extensions import get_args

from daide2eng.grammar import create_daide_grammar
from daide2eng.grammar.grammar import DAIDELevel

_grammar = create_daide_grammar(get_args(DAIDELevel)[-1], string_type="all")


@dataclass(eq=True, frozen=True)
class _DAIDEObject(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

    def __post_init__(self):
        pass