# Описание проекта Django

> В проекте сейчас используется библиотека pdfkit и wkhtmltopdf

## Прочее
https://www.youtube.com/watch?v=3eYWOsfCncc&t=759s
https://www.w3schools.com/django/django_ref_filter.php

## Изучить
https://www.youtube.com/watch?v=DYxjL0K3Hwk&list=PLQAt0m1f9OHvGM7Y7jAQP8TKbBd3up4K2

## Документации и Cтатьи
### Документация комад Django
https://getkt.com/2022/12/10/django-django-admin-command-reference/

### MD
https://skillbox.ru/media/code/yazyk-razmetki-markdown-shpargalka-po-sintaksisu-s-primerami/

### СSS
https://yandex.ru/video/preview/18430246097696583971
https://stackoverflow.com/questions/14676613/how-to-import-google-web-font-in-css-file
https://itfy.org/threads/python-django-kak-ukazat-lokalnye-shrifty.2708/

### Fonts
https://fonts.google.com/selection/embed

### Static File
https://www.youtube.com/watch?v=IrUG07namQ8

### Классы ListView
https://yandex.ru/video/preview/7058180514876708295

### PDF
https://pythonguides.com/convert-html-page-to-pdf-using-django/
https://www.cyberforum.ru/python-django/thread3091633.html
https://www.meziantou.net/generate-pdf-files-using-an-html-template-and-playwright.htm
https://dzen.ru/a/X1aHYLcgRwnw1xkH
pdfkit 
https://pythoncircle.com/post/470/generating-and-returning-pdf-as-response-in-django/

### Bootstap
https://getbootstrap.ru/docs/5.1/components/dropdowns/

### Статьи Django
https://habr.com/ru/articles/242261/

### Проподают css стили
https://qna.habr.com/q/858245

## Решение проблем

1) Cохранил параметр migration: 
https://www.youtube.com/watch?v=of4St7HvMHs
2) Изменение переменной:
https://www.youtube.com/watch?v=lCHAN-YPtAg
3) Увеличение размера кода:
https://ru.stackoverflow.com/questions/1229896/Как-увеличить-текст-кода-или-размер-окна-в-pycharm
4) Настройка окружения
https://stackoverflow.com/questions/47124297/commanderror-you-appear-not-to-have-the-psql-program-installed-or-on-your-pat 
5) ОТЧЁТ
https://github.com/DocRaptor/html-to-pdf-templates/blob/main/source/estimate/estimate.html

````
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
{{app_report}}
<hr>
{{app_report.description|linebreaks}}
{{app_report.logo}}
<br>
{{app_report.logo.url}}
<br>
{{app_report.logo.path}}
<br>
{{app_report.created_at}}
<br>
{{app_report.updated_at}}
<br>
<img src="media/{{app_report.logo}}" height='200px'>
</body>
</html>
````

6) незагрузка CSS ФАЙЛА - причина неправильный формат

````
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = [os.path.join(BASE_DIR, 'media')]
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
````

7) POST AND GET
https://www.youtube.com/watch?v=wzZiONbtwiA
https://yandex.ru/video/preview/2198961803011279516
8) Исправлен имя переменной app и вставлен ссылка и цикл "{% url 'app:pdf-view' reports.pk %}"
9) https://pythonguides.com/convert-html-page-to-pdf-using-django/
10) Настройка статических файлов


## Примеры отчётов:
![Изображение](https://ppt.ru/fls/97469/resize/1obrazec-otcheta1-width961.jpg "Логотип Markdown")

Участники - сотрудника на кого создается отчёт
Ответственный - это тот кто создал отчёт

select_type_staff = 'Александра Сидорова' 

Вы можете использовать различные языки программирования или инструменты для преобразования формата даты и времени. Например, в Python можно использовать библиотеку `datetime`. Вот пример кода:

```python
from datetime import datetime

# Входная строка с датой и временем
input_date = "March 27, 2024, 8:35 p.m."

# Преобразование строки в объект datetime
dt_object = datetime.strptime(input_date, "%B %d, %Y, %I:%M %p")

# Форматирование объекта datetime в требуемый формат
output_date = dt_object.strftime("%d %B %Y года")

print(output_date)
```

Этот код преобразует входную строку `"March 27, 2024, 8:35 p.m."` в объект `datetime`, а затем форматирует его в формат `"30 марта 2024 года"`.

Google.generativeai

```python
import google.generativeai as genai

genai.configure(api_key='')

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat()
# response = model.generate_content('Please summarise this document: ...')
response = chat.send_message("Hello")

print(response.text)
```
## Документация AI

__Gemini API: быстрый старт с Python__
https://ai.google.dev/tutorials/python_quickstart

__Поиск документов с вложениями__
https://ai.google.dev/examples/doc_search_emb

__Обучение классификатора текста с использованием вложений__
https://ai.google.dev/examples/train_text_classifier_embeddings

__Помощник по кодированию__
https://ai.google.dev/examples/pipet-code-agent?hl=ru

__Gemini API: вызов функций с помощью Pytho__
https://ai.google.dev/tutorials/function_calling_python_quickstart

__Gemini API: настройка быстрого запуска с помощью Python__
https://ai.google.dev/tutorials/tuning_quickstart_python

__Gemini API: быстрый старт с Python__
https://ai.google.dev/tutorials/python_quickstart

```

SyntaxError: incomplete input
>>> model = genai.get_model('models/chat-bison-001') 
>>> import pprint
>>> pprint.pprint(model)
Model(name='models/chat-bison-001',
      base_model_id='',
      version='001',
      display_name='PaLM 2 Chat (Legacy)',
      description='A legacy text-only model optimized for chat convers
ations',
      input_token_limit=4096,
      output_token_limit=1024,
      supported_generation_methods=['generateMessage', 'countMessageTo
kens'],
      temperature=0.25,
      top_p=0.95,
      top_k=40)
>>> model = genai.get_model('models/gemini-pro')            
>>> pprint.pprint(model)                         
Model(name='models/gemini-pro',
      base_model_id='',
      version='001',
      display_name='Gemini 1.0 Pro',
      description='The best model for scaling across a wide range of t
asks',
      input_token_limit=30720,
      output_token_limit=2048,
      supported_generation_methods=['generateContent', 'countTokens'],
      temperature=0.9,
      top_p=1.0,
      top_k=1)
>>>

```

__Модели Близнецов__
https://ai.google.dev/models/gemini?hl=ru

__Примеры ботов__
https://ai.google.dev/examples?keywords=embed&hl=ru

__Оперативные стратегии проектирования__
https://ai.google.dev/docs/prompt_best_practices?hl=ru

> Обобщите этот текст. Текст: Квантовый компьютер использует квантово-механические явления для выполнения вычислений экспоненциально быстрее, чем любой современный традиционный компьютер. В очень крошечных масштабах физическая материя действует и как частицы, и как волны, и квантовые вычисления используют специальное оборудование для усиления этого поведения. Принципы работы квантовых устройств выходят за рамки классической физики. При масштабном развертывании квантовые компьютеры могут использоваться в самых разных приложениях, таких как: в сфере кибербезопасности для взлома существующих методов шифрования и помощи исследователям в создании новых, в метеорологии для разработки более эффективных прогнозов погоды и т. д. Однако нынешний уровень техники квантовые компьютеры по-прежнему в значительной степени экспериментальны и непрактичны.
> Приводить примеры
> Отдающие предпочтение кратким ответам.
> Использование примеров, чтобы показать модели шаблон, которому следует следовать, более эффективно, чем использование примеров, чтобы показать модели антипаттерн, которого следует избегать.

 

````
Краткое содержание:

Включение примеров подсказок в подсказку помогает модели научиться реагировать.
Приведите модельные примеры шаблонов, которым следует следовать, а не примеры шаблонов, которых следует избегать.
Поэкспериментируйте с количеством включенных подсказок. В зависимости от модели слишком мало примеров неэффективно для изменения поведения модели. Слишком большое количество примеров приводит к переобучению модели.

````


Регулярные выражения в Python от простого к сложному. Подробности, примеры, картинки, упражнения
https://habr.com/ru/articles/349860/
Python – конвертировать список словарей в JSON
https://www.geeksforgeeks.org/python-convert-list-of-dictionaries-to-json/
Встроенные типы 
https://docs.python.org/3/library/stdtypes.html
Как Фильтровать Наборы Запросов Django — 15 Примеров Для Начинающих
https://ctrlzblog.com/django-queryset-filter-15-examples/


