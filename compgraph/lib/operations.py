from abc import abstractmethod, ABC
from types import FunctionType
from typing import NewType, Dict, Any, Generator, Iterable, Tuple, Sequence

Row = NewType('Row', Dict[str, Any])
OperationResult = NewType('OperationResult', Generator[Row, None, None])


class Operation(ABC):
    @abstractmethod
    def __call__(self, rows: Iterable[Row], *args) -> OperationResult:
        pass


# Operations


class Mapper(ABC):
    """Base class for mappers"""
    @abstractmethod
    def __call__(self, row: Row) -> OperationResult:
        pass


class Map(Operation):
    def __init__(self, mapper: Mapper):
        self.mapper = mapper

    def __call__(self, rows: Iterable[Row], *args) -> OperationResult:
        pass


class Reducer(ABC):
    """Base class for reducers"""
    @abstractmethod
    def __call__(self, group_key: Tuple[str], rows: Iterable[Row]) -> OperationResult:
        pass


class Reduce(Operation):
    def __init__(self, reducer: Reducer, keys: Sequence[str]):
        self.reducer = reducer
        self.keys = keys

    def __call__(self, rows: Iterable[Row], *args) -> OperationResult:
        pass


class Sort(Operation):
    def __init__(self, keys: Sequence[str]):
        self.keys = keys

    def __call__(self, rows: Iterable[Row], *args) -> OperationResult:
        pass


class Joiner(ABC):
    """Base class for joiners"""
    def __init__(self, suffix_a: str = '_1', suffix_b: str = '_2'):
        self._a_suffix = suffix_a
        self._b_suffix = suffix_b

    @abstractmethod
    def __call__(self, keys: Sequence[str], rows_a: Iterable[Row], rows_b: Iterable[Row]) -> OperationResult:
        pass


class Join(Operation):
    def __init__(self, joiner: Joiner, keys: Sequence[str]):
        self.keys = keys
        self.joiner = joiner

    def __call__(self, rows: Iterable[Row], *args) -> OperationResult:
        pass


# Dummy operators


class DummyMapper(Mapper):
    """Yield exactly the row passed"""
    def __call__(self, row: Row) -> OperationResult:
        yield row


class FirstReducer(Reducer):
    """Yield only first row from passed ones"""
    def __call__(self, group_key: Tuple[str], rows: Iterable[Row]) -> OperationResult:
        for row in rows:
            yield row
            break


# Mappers


class FilterPunctuation(Mapper):
    """Left only non-punctuation symbols"""
    def __init__(self, column: str):
        """
        :param column: name of column to process
        """
        self.column = column

    def __call__(self, row: Row) -> OperationResult:
        pass


class LowerCase(Mapper):
    """Replace column value with value in lower case"""
    def __init__(self, column: str):
        """
        :param column: name of column to process
        """
        self.column = column

    def __call__(self, row: Row) -> OperationResult:
        pass


class Split(Mapper):
    """Split row on multiple rows by separator"""
    def __init__(self, column: str, separator: str = None):
        """
        :param column: name of column to split
        :param separator: string to separate by
        """
        self.column = column
        self.separator = separator

    def __call__(self, row: Row) -> OperationResult:
        pass


class Product(Mapper):
    """Calculates product of multiple columns"""
    def __init__(self, columns: Sequence[str], result_column: str = 'product'):
        """
        :param columns: column names to product
        :param result_column: column name to save product in
        """
        self.columns = columns
        self.result_column = result_column

    def __call__(self, row: Row) -> OperationResult:
        pass


class Filter(Mapper):
    """Remove records that don't satisfy some condition"""
    def __init__(self, condition: FunctionType):
        """
        :param condition: if condition is not true - remove record
        """
        self.condition = condition

    def __call__(self, row: Row) -> OperationResult:
        pass


class Project(Mapper):
    """Leave only mentioned columns"""
    def __init__(self, columns: Sequence[str]):
        """
        :param columns: names of columns
        """
        self.columns = columns

    def __call__(self, row: Row) -> OperationResult:
        pass


# Reducers


class TopN(Reducer):
    """Return top N by value"""
    def __init__(self, column: str, n: int):
        """
        :param column: column name to get top by
        :param n: number of top values to extract
        """
        self.column_max = column
        self.n = n

    def __call__(self, group_key: Tuple[str], rows: Iterable[Row]) -> OperationResult:
        pass


class TermFrequency(Reducer):
    """Calculate frequency of values in column"""
    def __init__(self, words_column: str, result_column: str = 'tf'):
        """
        :param words_column: name for column with words
        :param result_column: name for result column
        """
        self.words_column = words_column
        self.result_column = result_column

    def __call__(self, group_key: Tuple[str], rows: Iterable[Row]) -> OperationResult:
        pass


class Count(Reducer):
    """Count rows passed and yield single row as a result"""
    def __init__(self, column: str):
        """
        :param column: name of column to count
        """
        self.column = column

    def __call__(self, group_key: Tuple[str], rows: Iterable[Row]) -> OperationResult:
        pass


class Sum(Reducer):
    """Sum values in column passed and yield single row as a result"""
    def __init__(self, column: str):
        """
        :param column: name of column to sum
        """
        self.column = column

    def __call__(self, group_key: Tuple[str], rows: Iterable[Row]) -> OperationResult:
        pass


# Joiners


class InnerJoiner(Joiner):
    """Join with inner strategy"""
    def __call__(self, keys: Sequence[str], rows_a: Iterable[Row], rows_b: Iterable[Row]) -> OperationResult:
        pass


class OuterJoiner(Joiner):
    """Join with outer strategy"""
    def __call__(self, keys: Sequence[str], rows_a: Iterable[Row], rows_b: Iterable[Row]) -> OperationResult:
        pass


class LeftJoiner(Joiner):
    """Join with left strategy"""
    def __call__(self, keys: Sequence[str], rows_a: Iterable[Row], rows_b: Iterable[Row]) -> OperationResult:
        pass


class RightJoiner(Joiner):
    """Join with right strategy"""
    def __call__(self, keys: Sequence[str], rows_a: Iterable[Row], rows_b: Iterable[Row]) -> OperationResult:
        pass
