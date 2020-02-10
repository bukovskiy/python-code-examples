# FindMovieBot
@MovieFindBot
Телеграм бот для поиска фильмов (сериалов, мультиков, аниме и т. п.)

## Инструкция
1) Начать работу с ботом, введя команду /start
2) После этого появится короткая инструкция. Можно также
вызвать инструкцию командой /help.
3) В сообщении-инструкции можно выбрать источник данных 
для поиска: Кинопоиск или IMDB. Кинопоиск на практике
удобнее, однако иногда хитро блокирует запросы от бота, 
поэтому можно переключиться на IMDB.
Переключиться можно также командами /imdb или /kinopoisk
4) Ввести название фильма.
5) Появится короткий список из самых подходящих фильмов
с краткими данными (чтобы отличать один от другого).
6) Под каждым фильмом есть ссылка вида /idXXXXXX 
Если нажать на нее, бот пришлет более подробное описание фильма
с постером и ссылками на просмотр. 

##Принцип работы
Бот поддерживает класс парсера для работы с двумя API: для кинопоиска и для IMDB. 
Выбрать, с каким поиском работать, пользователь может командами /imdb или /kinopoisk, 
парсер инициализируется с соответствующим типом. 
Парсер два типа входных данных: 
1) Произвольный текст. Метод parse_query принимает строку для поиска, запрашивает информацию через API и возвращает небольшой 
список фильмов, которые подходят. К каждому фильму прилагается ссылка для полного просмотра вида /idXXXXXX, 
где XXXXXX - это id фильма в Кинопоиске или IMDB
2) ID фильма. Метод parse_id принимает id фильма, запрашивает полную информацию через API и хранит развернутое описание
фильма и постер. 

## API:

* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) - рекомендованный API для работы с Телеграм ботом
* [IMDbPy](https://imdbpy.readthedocs.io/en/latest/index.html#imdbpy) - библиотека для работы с IMDB
* [kinopoiskpy](https://github.com/ramusus/kinopoiskpy) - - библиотека для работы с Кинопоиском