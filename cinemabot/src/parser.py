from kinopoisk import movie
from src import config
from imdb import IMDb


class Helper_imdb:
    def parse_query(self, text):
        """
        Returns brief search results from imdb
        Number of results is set by LIST_LENGTH constant in config.py
        """

        def err_msg(text):
            """
            To return error when nothing is found
            """
            return config.ERR_IMDB_MSG.format(text)

        def remove_non_movies(movie):
            """
            IMDB base contains porn and videogames,
            so we need to filter it from search results.
            Maybe some other garbage too, just didn't find it yet.
            :param movie: movie object
            :return: boolean
            """
            return movie.data['kind'] not in ['video game', 'adult']

        m = IMDb()
        movie_list = m.search_movie(text)
        if not movie_list:
            return err_msg(text)
        output_text = "Your search \"{}\" revealed these movies\n" \
                      "Tap on the IMDB id to see more\n".format(text)
        movies = list(filter(remove_non_movies, movie_list))
        counter = 1
        for item in movies[:config.LIST_LENGTH]:
            data = item.data
            title = data['title']
            year = data.get("year", "Year unknown")
            id = item.movieID
            if data['kind'] in ["tv series", "miniseries"]:
                title = "".join((title, " (TV series)\t"))
            if "akas" in data:
                title = "".join((title, " ({})".format(data['akas'][0])))
            output_text = "".join((output_text, "{}) {}\n[{}\t/id{}] ️\n"
                                   .format(str(counter), title, year, id)))
            counter += 1
        return output_text

    def parse_id(self, film_id):
        """
        To find description on Kinopoisk, store full output, title and picture
        :param film_id: string
        """
        m = IMDb()
        film = m.get_movie(film_id)
        title = film['title']
        title = title
        id = film_id
        if (film['kind'] in ["tv series", "miniseries"]):
            title = "".join((title, " (TV series)"))
        year = film.get('year', 'Year unknown')
        if film.get('genres'):
            genre = film['genres'][0]
        else:
            genre = "Genre unknown"
        if film.get('countries'):
            countries = ". ".join(film['countries'][:3])
        else:
            countries = "Country unknown"
        output = "".join((title, ",\t [{}, {}, {}] \n".format(year, genre, countries)))
        if film.get('akas'):
            output = "".join((output, "(Alternative title: {})\n".format(film['akas'][0])))
        if film.get('rating'):
            output = "".join((output, "Rating: {}\n".format(film['rating'])))
        if film.get('runtimes'):
            output = "".join((output, "⌛️ {} min.\n".format(film['runtimes'][0])))
        if film.get('genres'):
            genres = ", ".join(film['genres'])
            output = "".join((output, "Genres: {}\n".format(genres)))
        if film.get('cast'):
            actors = ', '.join(map(lambda x: x['name'], film['cast'][:5]))
            output = "".join((output, "Starring: {}, ...\n".format(actors)))
        if film.get('directors'):
            directors = ', '.join(map(lambda x: x['name'], film['directors']))
            output = "".join((output, "Directed by: {}\n".format(directors)))
        if film.get('plot outline'):
            synopsis = film['plot outline']
            output = "".join((output, "Plot: {}\n".format(synopsis)))
        if film.get('cover url'):
            photo = film['full-size cover url']
        return output, photo, title


class Helper_kinopoisk:
    def parse_query(self, text):
        """
        Returns brief search results from kinopoisk
        Number of results is set by LIST_LENGTH constant in config.py
        """

        def err_msg(text):
            """
            To return error when nothing is found
            """
            return config.ERR_KINOPOISK_MSG.format(text)

        m = movie.Movie()
        movie_list = m.objects.search(text)
        if not movie_list:
            return err_msg(text)
        output_text = "По запросу \"{}\" найдено:\n"\
            "(Нажми на ссылку, чтобы узнать больше)\n".format(text)
        counter = 1
        for item in movie_list[:config.LIST_LENGTH]:
            title = item.title
            year = item.year
            rating = item.rating or "Нет рейтинга"
            id = item.id
            if item.series:
                title = "".join((title, " (сериал)\t"))
            if item.title_en:
                title = "".join((title, " ({})".format(item.title_en)))
            output_text = "".join((output_text, "{}) {}\n[Год: {}\tРейтинг:️ {}]\n/id{} ️\n"
                                   .format(str(counter), title, year, rating, id)))
            counter += 1
        return output_text

    def parse_id(self, film_id):
        """
        To find description on Kinopoisk, store full output, title and picture
        :param film_id: string
        """
        film = movie.Movie(id=str(film_id))
        film.get_content("main_page")
        film.get_content("posters")
        title = film.title
        id = str(film_id)
        year = film.year or "Год неизвестен"
        if film.genres:
            genre = film.genres[0]
        else:
            genre = "Жанр неизвестен"
        if film.countries:
            countries = ". ".join(film.countries[:3])
        else:
            countries = "Страна неизвестна"
        output = "{},\t [{}, {}, {}] \n".format(title, year, genre, countries)
        if film.title_en:
            output = "".join((output, "\n(Оригинальное название: {})\n".format(film.title_en)))
            # title_en actually gets original title, not English title!
        if film.rating is not None:
            output = "".join((output, "Рейтинг️ {}\n".format(film.rating)))
        if film.runtime is not None:
            output = "".join((output, "⌛ {} мин.\n".format(film.runtime)))
        if film.actors:
            actors = ', '.join(map(lambda x: x.name, film.actors[:5]))  # 5 actors is enough!
            output = "".join((output, "В ролях: {}.\n".format(actors)))
        if (len(film.directors) == 1):
            output = "".join((output, "Режиссер: {}.\n".format(film.directors[0])))
        elif (len(film.directors) > 1):
            directors = ", ".join(map(lambda x: x.name, film.directors))
            output = "".join((output, "Режиссеры: {}.\n".format(directors)))
        if film.plot:
            plot = ". ".join(film.plot.split('.'))
            output = "".join((output, "Сюжет: {}\n".format(plot)))
        photo = "https://st.kp.yandex.net/images/film_big/{}.jpg".format(id)
        return output, photo, title


class Parser:
    """
    Class works with two types of inputs.
    1) parse_text method calls the Kinopoisk API and returns a brief description of
    1-6 movies.
    2) parse_id method calls the Kinopoisk API to show additional info and poster
    """

    def __init__(self, search_type):
        self.output = ""
        self.photo = None
        self.type = search_type  # Set the search source (IMDB or Kinopoisk)
        self.helpers = {'imdb': Helper_imdb, 'kinopoisk': Helper_kinopoisk}
        self.title = ""

    def set_type(self, type):
        """
        Sets the search tipe
        :param type: string ('imdb' or 'kinopoisk')
        """
        self.type = type

    def parse_query(self, query):
        """
        Calls one of to methods to return several brief search results to choose from
        :param query: search (string)
        :return: search result (string)
        """
        helper = self.helpers[self.type]()
        return helper.parse_query(query)

    def parse_id(self, id):
        """
        Calls one of to methods to store full output
        :param query: id (string)
        """
        helper = self.helpers[self.type]()
        self.output, self.photo, self.title = helper.parse_id(id)
