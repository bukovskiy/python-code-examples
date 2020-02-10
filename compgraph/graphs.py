from .lib import Graph, operations


def word_count_graph(input_stream: str, text_column: str, count_column: str) -> Graph:
    """Constructs graph which counts words in text_column of all rows passed"""
    return Graph() \
        .read_from_iter(input_stream) \
        .map(operations.FilterPunctuation(text_column)) \
        .map(operations.LowerCase(text_column)) \
        .map(operations.Split(text_column)) \
        .sort([text_column]) \
        .reduce(operations.Count(count_column), [text_column]) \
        .sort([count_column, text_column])


def inverted_index_graph(input_stream: str, doc_column: str, text_column: str, result_column: str) -> Graph:
    """Constructs graph which calculates td-idf for every word/document pair"""
    raise NotImplementedError


def pmi_graph(input_stream: str, doc_column: str, text_column: str, result_column: str) -> Graph:
    """Constructs graph which gives for every document the top 10 words ranked by pointwise mutual information"""
    raise NotImplementedError


def yandex_maps_graph(input_stream_time: str, input_stream_length: str,
                      enter_time_column: str, leave_time_column: str,
                      edge_id_column: str, start_coord_column: str, end_coord_column: str,
                      weekday_result_column: str, hour_result_column: str, speed_result_column: str) -> Graph:
    """Constructs graph which measures average speed in km/h depending on the weekday and hour"""
    raise NotImplementedError
