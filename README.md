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