# Коллекция тестов для проектов YaNews и YaNote

В репозитории собраны тесты для двух Django-проектов:

- **YaNews** — сервис новостей с комментариями;
- **YaNote** — сервис личных заметок.

Для каждого проекта написаны тесты, проверяющие доступность страниц (роутинг),
содержимое страниц (контент) и бизнес-логику приложения. Тесты покрывают
поведение проекта как для анонимных пользователей, так и для авторизованных,
включая права доступа авторов и посторонних пользователей.

## Структура репозитория

```
.
├── LICENSE                     # Лицензия MIT
├── requirements.txt            # Зависимости проекта
├── run_tests.sh                # Скрипт запуска всех проверок
├── setup.cfg                   # Конфигурация flake8
├── structure_test.py           # Проверка наличия тестов в нужных директориях
├── ya_news/                    # Проект YaNews
│   ├── manage.py
│   ├── pytest.ini              # Конфигурация pytest для YaNews
│   ├── news/                   # Приложение news
│   │   ├── pytest_tests/       # ДИРЕКТОРИЯ С ТЕСТАМИ YaNews
│   │   │   ├── conftest.py     # Фикстуры: пользователи, клиенты, новости, комментарии
│   │   │   ├── test_routes.py  # Тесты доступности и прав доступа к страницам
│   │   │   ├── test_content.py # Тесты содержимого страниц
│   │   │   └── test_logic.py   # Тесты бизнес-логики (комментарии)
│   │   └── ...
│   └── yanews/                 # Пакет конфигурации проекта YaNews
└── ya_note/                    # Проект YaNote
    ├── manage.py
    ├── pytest.ini              # Конфигурация pytest для YaNote
    ├── notes/                  # Приложение notes
    │   ├── tests/              # ДИРЕКТОРИЯ С ТЕСТАМИ YaNote
    │   │   ├── conftest.py     # Общие тестовые данные и клиенты
    │   │   ├── test_routes.py  # Тесты доступности и редиректов
    │   │   ├── test_content.py # Тесты содержимого страниц
    │   │   └── test_logic.py   # Тесты бизнес-логики (заметки)
    │   └── ...
    └── yanote/                 # Пакет конфигурации проекта YaNote
```

> **Важно.** Тесты должны лежать строго в указанных директориях:
> `ya_news/news/pytest_tests/` и `ya_note/notes/tests/`.
> Соблюдение структуры проверяет скрипт [`structure_test.py`](structure_test.py).

## Что покрывают тесты

### YaNews (`ya_news/news/pytest_tests/`)

| Файл | Что проверяется |
| --- | --- |
| [`test_routes.py`](ya_news/news/pytest_tests/test_routes.py) | Доступность главной страницы, страницы новости, страниц авторизации; права на редактирование и удаление комментария (доступно автору, недоступно чужому пользователю — `404`); редирект анонима на страницу логина |
| [`test_content.py`](ya_news/news/pytest_tests/test_content.py) | Количество новостей на главной странице (`NEWS_COUNT_ON_HOME_PAGE`), сортировка новостей по дате (сначала свежие), сортировка комментариев (сначала старые), наличие формы комментария только у авторизованных пользователей |
| [`test_logic.py`](ya_news/news/pytest_tests/test_logic.py) | Создание комментария (только авторизованным), запрет нецензурных слов, редактирование и удаление комментария только его автором |

### YaNote (`ya_note/notes/tests/`)

| Файл | Что проверяется |
| --- | --- |
| [`test_routes.py`](ya_note/notes/tests/test_routes.py) | Доступность публичных страниц, страниц авторизованного пользователя, недоступность чужих заметок (`404`) и редиректы анонимных пользователей на страницу логина |
| [`test_content.py`](ya_note/notes/tests/test_content.py) | Список заметок: автор видит свои заметки, посторонний — не видит; наличие формы `NoteForm` на страницах создания и редактирования |
| [`test_logic.py`](ya_note/notes/tests/test_logic.py) | Создание заметки авторизованным, запрет создания анонимом, автогенерация slug из заголовка при пустом slug, запрет неуникального slug, редактирование и удаление заметки только её автором |

## Требования

- Python 3.9+
- Зависимости из [`requirements.txt`](requirements.txt):

```
Django==5.1.1
flake8==7.1.1
flake8-docstrings==1.7.0
pep8-naming==0.14.1
pytest==7.1.3
pytest-django==4.9.0
pytest-lazy-fixture==0.6.3
pytest-subtests==0.13.1
pytils==0.4.1
```

## Установка и настройка окружения

```bash
# Создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Установить зависимости
pip install -r requirements.txt
```

## Запуск тестов

### Полная проверка (рекомендуется)

Из корня репозитория выполните скрипт [`run_tests.sh`](run_tests.sh) — он
последовательно запускает все проверки:

1. `flake8` — проверяет код на соответствие PEP8 (конфигурация в
   [`setup.cfg`](setup.cfg));
2. [`structure_test.py`](structure_test.py) — проверяет, что тесты
   скопированы в указанные в техническом задании директории;
3. `pytest` для проекта **YaNews**;
4. `pytest` для проекта **YaNote**.

```bash
bash run_tests.sh
```

### Запуск тестов по отдельности

```bash
# Тесты YaNews
cd ya_news
export DJANGO_SETTINGS_MODULE=yanews.settings
pytest --tb=line

# Тесты YaNote
cd ../ya_note
unset DJANGO_SETTINGS_MODULE
export DJANGO_SETTINGS_MODULE=yanote.settings
pytest --tb=line
```

### Проверка кода линтером

```bash
python -m flake8 --config=setup.cfg
```

## Примечания

- В проекте **YaNews** тесты написаны в стиле `pytest` с использованием
  фикстур и параметризации ([`conftest.py`](ya_news/news/pytest_tests/conftest.py)).
- В проекте **YaNote** тесты написаны в стиле `unittest` — классы наследуют
  `django.test.TestCase` и используют `assertEqual`, `assertRedirects`,
  `assertFormError` и т. д. Запускает их тот же раннер `pytest` (встроенная
  интеграция pytest с unittest). Общие тестовые данные вынесены в модуль
  [`conftest.py`](ya_note/notes/tests/conftest.py) — он не содержит
  pytest-фикстур, а используется как источник констант и базового класса.

## Лицензия
Проект распространяется под лицензией [MIT](LICENSE).

---

**Автор тестов:** [oleshey](https://github.com/oleshey)

Данный проект создан на основе задания учебного курса [Яндекс.Практикум](https://practicum.yandex.ru/). Цель проекта — отработка практических навыков и демонстрация подхода к решению поставленной задачи.
