import parser
import config
import sys


def test_create_correct_parser():
    test_parser1 = parser.Parser('imdb')
    test_parser1.set_type('kinopoisk')
    assert test_parser1.type == 'kinopoisk'
    test_parser1.set_type('imdb')
    assert test_parser1.type == 'imdb'


def test_error_message():
    test_parser1 = parser.Parser('imdb')
    test_parser2 = parser.Parser('kinopoisk')
    text = 'skfjskfjshkdhkjd'
    result1 = test_parser1.parse_query(text)
    result2 = test_parser2.parse_query(text)
    assert result1 == config.ERR_IMDB_MSG.format(text)
    assert result2 == config.ERR_KINOPOISK_MSG.format(text)


def test_kinopoisk_search():
    test_parser1 = parser.Parser('kinopoisk')
    text = "Matrix"
    result = test_parser1.parse_query(text)
    assert result.startswith("По запросу \"{}\" найдено:\n".format(text) +
                             "(Нажми на ссылку, чтобы узнать больше)\n"'1) Матрица')


def test_imdb_search():
    test_parser1 = parser.Parser('imdb')
    text = "Matrix"
    result = test_parser1.parse_query(text)
    assert result.startswith("Your search \"{}\" revealed these movies\n".format(text) +
                             "Tap on the IMDB id to see more\n"+"1) The Matrix")


def test_imdb_full_output():
    test_parser1 = parser.Parser('imdb')
    test_parser1.parse_id('0133093')
    assert test_parser1.title == "The Matrix"
    assert test_parser1.output.startswith('The Matrix,	 [1999, Action, United States] ')


def test_kinopoisk_full_output():
    test_parser1 = parser.Parser('kinopoisk')
    test_parser1.parse_id('301')
    assert test_parser1.title == "Матрица"
    assert test_parser1.output.startswith('Матрица,	 [1999, фантастика, США] ')


