##Описание проекта Django

Документация команд: https://getkt.com/2022/12/10/django-django-admin-command-reference/

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

6) незагрузка CSS ФАЙЛА - причина неправильный формат
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = [os.path.join(BASE_DIR, 'media')]
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

7) POST AND GET
https://yandex.ru/video/preview/2198961803011279516
8) Исправлен имя переменной app и вставлен ссылка и цикл "{% url 'app:pdf-view' reports.pk %}"
9) 