from typing import Sequence, Callable, List

from .operations import Row, Mapper, Reducer, Joiner


class Graph:
    """Computational graph implementation"""

    def read_from_iter(self, name: str) -> 'Graph':
        """Construct new graph extended with operation which adds data (in form of sequence of Rows
        from 'kwargs' passed to 'run' method) into graph data-flow
        :param name: name of kwarg to use as data source
        """
        raise NotImplementedError

    def read_from_file(self, filename: str, parser: Callable[[str], Row]) -> 'Graph':
        """Construct new graph extended with operation for reading rows from file
        :param filename: filename to read from
        :param parser: parser from string to Row
        """
        raise NotImplementedError

    def map(self, mapper: Mapper) -> 'Graph':
        """Construct new graph extended with map operation with particular mapper
        :param mapper: mapper to use
        """
        raise NotImplementedError

    def reduce(self, reducer: Reducer, keys: Sequence[str]) -> 'Graph':
        """Construct new graph extended with reduce operation with particular reducer
        :param reducer: reducer to use
        :param keys: keys for grouping
        """
        raise NotImplementedError

    def sort(self, keys: Sequence[str]) -> 'Graph':
        """Construct new graph extended with sort operation
        :param keys: sorting keys (typical is tuple of strings)
        """
        raise NotImplementedError

    def join(self, joiner: Joiner, join_graph: 'Graph', keys: Sequence[str]) -> 'Graph':
        """Construct new graph extended with join operation with another graph
        :param joiner: join strategy to use
        :param join_graph: other graph to join with
        :param keys: keys for grouping
        """
        raise NotImplementedError

    def run(self, **kwargs) -> List[Row]:
        """Single method to start execution; data sources passed as kwargs"""
        raise NotImplementedError
