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

## bitrix24

from app.models import CustomUser Staff, Task, Staff_Notification, Attendance_Report, Deal

````
from fast_bitrix24 import Bitrix
web = "https://b24-fecbbn.bitrix24.ru/rest/1/b5kgeg0e6gp081qy/"
b = Bitrix(web) 
````

````
res = [{k: v for k, v in d.items() if k in ['ID', 'NAME', 'LAST_NAME', 'EMAIL', 'LAST_LOGIN']} for d in b.get_all('user.get')]
user = CustomUser(first_name=res[0].get('NAME'))
user.save()
Staff(admin=user).save()
````

````
res = [{k: v for k, v in d.items() if k in ['TITLE', 'DATE_CREATE','DATE_MODIFY', 'OPENED', 'TYPE_ID', 'ASSIGNED_BY_ID', 'CLOSEDATE']} for d in b.get_all('crm.deal.list')]
user = Deal(title = res[0].get('TITLE'), CLOSEDATE = res[0].get('CLOSEDATE'), Status = res[0].get('OPENED'), DATE_MODIFY = res[0].get('DATE_MODIFY'), TYPE_ID = res[0].get('TYPE_ID'), DATE_CREATE = res[0].get('DATE_CREATE'), bitrix_staff_id = res[0].get('ASSIGNED_BY_ID')) 
user.save() 
````

````
res = [{k: v for k, v in d.items() if k in ['RESPONSIBLE_ID', 'DESCRIPTION', 'CREATED', 'LAST_UPDATED', 'COMPLETED', 'START_TIME', 'END_TIME', 'DEADLINE']} for d in b.get_all('crm.activity.list')]
user = Case(DESCRIPTION = res[0].get('DESCRIPTION'), CREATED = res[0].get('CREATED'), LAST_UPDATED = res[0].get('LAST_UPDATED'), COMPLETED = res[0].get('COMPLETED'), START_TIME = res[0].get('START_TIME'), END_TIME = res[0].get('END_TIME'), DEADLINE = res[0].get('DEADLINE'), bitrix_staff_id = CustomUser.objects.get(bitrix_staff_id=res[0].get('RESPONSIBLE_ID'))) 
user.save() 
````

python manage.py shell

CustomUser.objects.get(id=res[0].get('RESPONSIBLE_ID'))

````
>>> b.get_all('tasks.task.list', params={"select":["STATUS", "PRIORITY", "TASK_CO
NTROL", "DURATION_FACT"]})
[{'priority': '1', 'taskControl': 'N', 'durationFact': '0', 'id': '2', 'status': 
'5', 'group': [], 'subStatus': '5'}, {'priority': '1', 'taskControl': 'N', 'durat
ionFact': None, 'id': '4', 'status': '5', 'group': [], 'subStatus': '5'}, {'prior
ity': '2', 'taskControl': 'Y', 'durationFact': '0', 'id': '6', 'status': '3', 'gr
oup': [], 'subStatus': '3'}, {'priority': '1', 'taskControl': 'Y', 'durationFact'
: None, 'id': '8', 'status': '2', 'group': [], 'subStatus': '-1'}]

>>> b.get_all('tasks.task.list', params={"select":["ID", "DEADLINE", "PRIORITY", 
"DECLINE_REASON", "STATUS", "DATE_START", "CLOSED_DATE", "TIME_SPENT_IN_LOGS", "C
OMMENTS_COUNT", "TIME_ESTIMATE", "TITLE", "DESCRIPTION", "START_DATE_PLAN", "END_
DATE_PLAN", "CREATED_DATE"]})
[{'id': '2', 'deadline': '2024-04-19T19:00:00+03:00', 'priority': '1', 'dateStart
': '2024-04-02T22:18:08+03:00', 'closedDate': '2024-04-09T01:19:26+03:00', 'timeS
pentInLogs': '11', 'commentsCount': '3', 'timeEstimate': '0', 'title': 'CRM: qweq
we', 'description': '', 'startDatePlan': None, 'endDatePlan': None, 'createdDate'
: '2024-04-02T22:17:49+03:00', 'descriptionInBbcode': 'Y', 'status': '5', 'group'
: [], 'subStatus': '5'}, {'id': '4', 'deadline': '2024-04-05T19:00:00+03:00', 'pr
iority': '1', 'dateStart': '2024-04-03T19:46:05+03:00', 'closedDate': '2024-04-03
T19:46:14+03:00', 'timeSpentInLogs': None, 'commentsCount': '2', 'timeEstimate': 
'0', 'title': 'Тестовая задача', 'description': '', 'startDatePlan': None, 'endDa
tePlan': None, 'createdDate': '2024-04-03T19:43:21+03:00', 'descriptionInBbcode':
'Y', 'status': '5', 'group': [], 'subStatus': '5'}, {'id': '6', 'deadline': '202
4-04-26T19:00:00+03:00', 'priority': '2', 'dateStart': '2024-04-09T01:42:12+03:00
', 'closedDate': None, 'timeSpentInLogs': '8', 'commentsCount': '11', 'timeEstima
te': '0', 'title': 'Cделать интеграцию', 'description': 'Hello! How can I assist 
you today?\r\n\r\n', 'startDatePlan': None, 'endDatePlan': None, 'createdDate': '
2024-04-09T00:51:34+03:00', 'descriptionInBbcode': 'Y', 'status': '3', 'group': [
], 'subStatus': '3'}, {'id': '8', 'deadline': '2024-04-02T19:00:00+03:00', 'prior
ity': '1', 'dateStart': None, 'closedDate': None, 'timeSpentInLogs': None, 'comme
ntsCount': '1', 'timeEstimate': '0', 'title': 'Новая задача', 'description': 'Сде
лать разработку веб-сраницы', 'startDatePlan': None, 'endDatePlan': None, 'create
dDate': '2024-04-09T02:56:13+03:00', 'descriptionInBbcode': 'Y', 'status': '2', '
group': [], 'subStatus': '-1'}]


>>> b.get_all('tasks.task.list', params={"filter":{'subStatus':'-1'},"select":["S
TATUS"]})
[{'id': '2', 'status': '5', 'group': [], 'subStatus': '5'}, {'id': '4', 'status':
'5', 'group': [], 'subStatus': '5'}, {'id': '6', 'status': '3', 'group': [], 'su
bStatus': '3'}, {'id': '8', 'status': '2', 'group': [], 'subStatus': '-1'}]      
>>> b.get_all('tasks.task.list', params={"filter":{'subStatus':-1},"select":["STA
TUS"]})
[{'id': '2', 'status': '5', 'group': [], 'subStatus': '5'}, {'id': '4', 'status':
'5', 'group': [], 'subStatus': '5'}, {'id': '6', 'status': '3', 'group': [], 'su
bStatus': '3'}, {'id': '8', 'status': '2', 'group': [], 'subStatus': '-1'}]      
>>> b.get_all('tasks.task.list', params={"filter":{'subStatus':'-1'},"select":["S
TATUS"]})
[{'id': '2', 'status': '5', 'group': [], 'subStatus': '5'}, {'id': '4', 'status':
'5', 'group': [], 'subStatus': '5'}, {'id': '6', 'status': '3', 'group': [], 'su
bStatus': '3'}, {'id': '8', 'status': '2', 'group': [], 'subStatus': '-1'}]      
>>> b.get_all('tasks.task.list', params={"filter":{'STATUS':-1},"select":["STATUS
"]})
[{'id': '8', 'status': '2', 'group': [], 'subStatus': '-1'}]
>>> b.get_all('tasks.task.list', params={"filter":{'STATUS':-1},"select":["PRIORI
TY ","STATUS"]})
[{'id': '8', 'status': '2', 'group': [], 'subStatus': '-1'}]
>>> b.get_all('tasks.task.list', params={"filter":{'STATUS':-1},"select":["PRIORI
TY","STATUS"]})
[{'priority': '1', 'id': '8', 'status': '2', 'group': [], 'subStatus': '-1'}]


````

## Контроль задач

task.task.list

# Непросмотренная задача
'notViewed': 'N',

# Ответственный
'responsibleId': '1',

# Дата создания и изменения задачи
'createdDate': '2024-04-02T22:17:49+03:00',
'changedDate': '2024-04-09T01:19:26+03:00',

# Пользователь, последним изменивший статус задачи;
'statusChangedBy': '1',

# Ответственный за закрытие задачи,
'closedBy': '1',

# Дата начала и завершения задачи.,
'dateStart': '2024-04-02T22:18:08+03:00',
'closedDate': '2024-04-09T01:19:26+03:00',

# Время активное.
'activityDate': '2024-04-09T01:19:26+03:00',
'deadline': '2024-04-19T19:00:00+03:00',

# Индитификатор сделки
'id': '2',

# Описание
'title': 'CRM: qweqwe',
'description': '',

# Оценка;
'mark': None,

# приоритет;
'priority': '1',

PRIORITY - приоритет:
  0 - низкий;
  1 - средний;
  2 - высокий.

## Дата последнего просмотра
'viewedDate': '2024-04-09T01:19:26+03:00',

## Дата планового начала и окончания задачи
'startDatePlan': None,
'endDatePlan': None,

## Затраченное время на задачу (в секундах).,
'timeEstimate': '0',
'timeSpentInLogs': '11',

## Затрачено (план)
'durationPlan': None,
'durationFact': '0',

## Количество комментариев
'commentsCount': '3',
'serviceCommentsCount': '3',

## Ответственный
'responsible': {
  'id': '1',
  'name': 'Rock Book Book',
  'link': '/company/personal/user/1/',
  'icon': '/bitrix/images/tasks/default_avatar.png',
  'workPosition': None
},
'accomplicesData': [],
'auditorsData': [],

## Cтатус выполнения,
'status': '5',
'subStatus': '5'

REAL_STATUS - статус задачи. Константы отражающие статусы задач:
    
    STATE_NEW = 1;
    STATE_PENDING = 2;
    STATE_IN_PROGRESS = 3;
    STATE_SUPPOSEDLY_COMPLETED = 4;
    STATE_COMPLETED = 5;
    STATE_DEFERRED = 6;
    STATE_DECLINED = 7;

    СОСТОЯНИЕ НОВОЕ = 1;
    СОСТОЯНИЕ ОЖИДАНИЯ = 2;
    СОСТОЯНИЕ В ПРОЦЕССЕ = 3;
    СОСТОЯНИЕ ПРЕДПОЛОЖИТЕЛЬНО ЗАВЕРШЕНО = 4;
    СОСТОЯНИЕ ЗАВЕРШЕНО = 5;
    СОСТОЯНИЕ ОТЛОЖЕНО = 6;
    СОСТОЯНИЕ ОТКЛОНЕНО = 7;

STATUS - статус для сортировки. Аналогичен REAL_STATUS, но имеет дополнительно три мета-статуса:

    -3 - задача почти просрочена;
    -2 - не просмотренная задача;
    -1 - просроченная задача.

````
>>> b.get_all('tasks.task.list', params={"filter":{"=STATUS":'-1'}, "select":["STATUS", "RESPONSIBLE_ID"]})
[{'responsibleId': '10', 'id': '8', 'status': '2', 'group': [], 'responsi
ble': {'id': '10', 'name': 'bsa_tmp@icloud.com', 'link': '/company/person
al/user/10/', 'icon': '/bitrix/images/tasks/default_avatar.png', 'workPos
ition': None}, 'subStatus': '-1'}]

>>> b.get_all('tasks.task.list', params={"filter":{"=STATUS":'3'}, "select":["STATUS", "RESPONSIBLE_ID"]})
[{'responsibleId': '1', 'id': '6', 'status': '3', 'group': [], 'responsib
le': {'id': '1', 'name': 'Rock Book Book', 'link': '/company/personal/use
r/1/', 'icon': '/bitrix/images/tasks/default_avatar.png', 'workPosition':
 None}, 'subStatus': '3'}]
>>> len(b.get_all('tasks.task.list', params={"filter":{"=STATUS":'3'}, "s
elect":["STATUS", "RESPONSIBLE_ID"]}))
1
>>> len(b.get_all('tasks.task.list', params={"filter":{"=STATUS":'5'}, "s
elect":["STATUS", "RESPONSIBLE_ID"]}))
2
>>> len(b.get_all('tasks.task.list', params={"filter":{"=STATUS":'2'}, "s
elect":["STATUS", "RESPONSIBLE_ID"]}))
0
>>> len(b.get_all('tasks.task.list', params={"filter":{"=STATUS":'1'}, "s
elect":["STATUS", "RESPONSIBLE_ID"]}))
0
>>> len(b.get_all('tasks.task.list', params={"filter":{"=STATUS":'4'}, "s
elect":["STATUS", "RESPONSIBLE_ID"]}))
0
>>> len(b.get_all('tasks.task.list', params={"filter":{"=STATUS":'6'}, "s
elect":["STATUS", "RESPONSIBLE_ID"]}))
0
>>> len(b.get_all('tasks.task.list', params={"filter":{"=STATUS":'7'}, "s
elect":["STATUS", "RESPONSIBLE_ID"]}))
0

````

## Время time.status

# Статус текущего рабочего дня.
  'STATUS': 'CLOSED',
  Варианты значений:
  - OPENED - рабочий день идет
  - CLOSED - рабочий день закрыт
  - PAUSED - рабочий день приостановлен
  (был открыт до начала текущих календарных суток и не закрыт)

# Дата начала и дата окончания рабочего дня
'TIME_START': '2024-04-02T22:40:00+03:00',
'TIME_FINISH': '2024-04-03T07:40:00+03:00',

# Длительность рабочего день
'DURATION': '8:00:00',

# Длительность перерыва за день
'TIME_LEAKS': '00:02:01',

## Время timeman.timecontrol.reports.get

{
    'report': {
        'month_title': '������',  # Название месяца
        'date_start': '2024-04-01T00:00:00+03:00',  # Дата начала периода выборки в формате АТОМ
        'date_finish': '2024-04-30T23:59:59+03:00',  # Дата окончания периода выборки в формате АТОМ

        'days': [{
            'day_title': '01.04.2024',  # Дата рабочего дня
            'workday_complete': 'false',  # Флаг завершенности рабочего дня (true / false)

            # Продолжительность работы
            'workday_duration': 10115,  # Продолжительность рабочего дня по табелю в секундах
            'workday_duration_config': 28800,  # Необходимая продолжительность рабочего дня в секундах
            'workday_duration_final': 6914,  # Продолжительность рабочего дня по фактической выработке в секундах

            # Продолжительность перерыва
            'workday_time_leaks_user': 0,  # Продолжительность перерыва установленного пользователем в секундах
            'workday_time_leaks_real': 3201,  # Продолжительность перерыва установленного автоматической системой фиксации в секундах

            # Продолжительность сверхурочной работы
            'workday_time_leaks_final': 21886,  # Количество времени отработанных сверх положенного времени в секундах

            # Cписок записей выявленных отсутствий
            'reports': [
                {
                    'id': 459,  # Идентификатор записи
                    'type': 'TM_START',  # Тип записи
                    'date_start': '2018-08-16T14:08:35+03:00',  # Дата начала фиксации в формате АТОМ
                    'date_finish': '2018-08-16T14:08:35+03:00',  # Дата окончания фиксации в формате АТОМ
                    'duration': 0,  # Продолжительность
                    'active': False,  # Активность записи
                    'entry_id': 35,  # Идентификатор записи
                    'report_type': 'NONE',  # Тип отсутствия (work - по рабочим вопросам, private - личные дела, none - не задан, приравнивается к private).
                    'report_text': '',  # Описание причины отсутствия
                }
            ]

        }]
    },
    'user': {
        'id': 1,  # Идентификатор пользователя
        'active': True,  # Активность пользователя
        'name': 'Rock Book Book',  # Имя и фамилия пользователя
        'first_name': 'Rock Book',  # Имя пользователя
        'last_name': 'Book',  # Фамилия пользователя
        'work_position': None,  # Должность
        'last_activity_date': '2024-04-09T18:05:17+03:00'  # Дата последнего действия пользователя в формате АТОМ
    }
}

def TASKCONTROL():
    Deferred_Tasks = TaskControl.objects.filter(STATUS="6").values('bitrix_staff_id')
    Tasks_Complet = TaskControl.objects.filter(STATUS="5").values('bitrix_staff_id')
    Rework_Tasks = TaskControl.objects.filter(STATUS="7").values('bitrix_staff_id')
    Process_Tasks = TaskControl.objects.filter(STATUS="3").values('bitrix_staff_id')

    context = {
        "task": task
    }

    return None

## ПРОМТ для модели исскуственного интеллекта

 prompt = [
                    """
                    \nВступай в роли бота, который пишет {0} от третьего лица (от лица компании Эркью) по сотруднику {1}. 
                    \nВ отчёте должна содержаться детальная информация о 
                    эффективности работы cотрудника учитывая данные: анализ задач сотрудников: {2}, анализ времени работы сотрудников: {3}, 
                    анализ зконков обработанные сотрудниками: {4}, анализ обработанных сделок сотрудниками: {5}, аналих дел обработанных сотрудниками: {6}
                    \nОтчёт должен содержать заголовки: 
                    \nУспехи: детальная информация о преимуществах сотрудника {1} за {0}.
                    \nОшибки: детальная информация о недостатках работы сотрудника {1} за {0}. 
                    \nОбщий комментарий: выводы по работе сотрудника {1}.
                    \nВозможные риски: укажи возможные риски эффективности работы сотрудников организации на основе исторических данных: анализ задач сотрудника: {2}, анализ времени работы сотрудника: {3}, 
                    анализ звонков обработанные сотрудниками: {4}, анализ обработанных сделок сотрудниками: {5}, анализ дел обработанных сотрудниками: {6}
                    \nРекомендации по улучшению работы: какие статьи, книги, документацию должен прочитать сотрудник {1} организации, укажи источники.
                    \nТы должен следовать всем требованиям формирования отчёта для эффективности и контроля работы сотрудника организации. 
                    \nИнформация должна быть подробно описана в заголовках: Успехи:, Ошибки:, Общий комментарий:, Рекомендации по улучшению работы:, Возможные риски:.
                    \nФормат вывода заголовков отчёта:
                    \nУспехи: [Успех_1, Успех_2 ... Успех_N],
                    \nОшибки: [Ошибки_1, Ошибки_2 ... Ошибки_N], 
                    \nРекомендации по улучшению работы: [Рекомендация_1, Рекомендация_2 ... Рекомендация_N],
                    \nОбщий комментарий: [Общая информация].
                    \nВозможные риски: [риск_1, риск_2 ... риск_N]\n\n\n
                    """.format(select_report_type, select_type_staff, anlazing_task, anlazing_time, anlazing_call,
                               anlazing_deal, anlazing_case),
                ]
 
prompt = [
                    """
                    \nВступай в роли бота, который пишет {0} от третьего лица (от лица компании Эркью) по сотрудникам: {1}. 
                    \nВ отчёте должна содержаться детальная информация о эффективности работы cотрудников учитывая данные: 
                    анализ задач сотрудников: {2}, анализ времени работы сотрудников: {3}, анализ зконков обработанные сотрудниками: {4},
                    анализ обработанных сделок сотрудниками: {5}, аналих дел обработанных сотрудниками: {6}
                    \nОтчёт должен содержать заголовки: 
                    \nУспехи: детальная информация о преимуществах сотрудников {1} за {0}.
                    \nОшибки: детальная информация о недостатках работы сотрудников {1} за {0}. 
                    \nОбщий комментарий: выводы по работе сотрудников {1}.
                    \nВозможные риски: укажи возможные риски эффективности работы сотрудников организации на основе исторических данных: анализ задач сотрудника: {2}, анализ времени работы сотрудника: {3}, 
                    анализ звонков обработанные сотрудниками: {4}, анализ обработанных сделок сотрудниками: {5}, анализ дел обработанных сотрудниками: {6}
                    \nРекомендации по улучшению работы: какие статьи, книги, документацию должен прочитать сотрудники {1} организации, укажи источники.
                    \nСледуй всем требованиям формирования отчёта для эффективности и контроля работы сотрудников организации. 
                    \nИнформация должна быть подробно описана в заголовках: Успехи:, Ошибки:, Общий комментарий:, Рекомендации по улучшению работы:.
                    \nФормат вывода заголовков отчёта:
                    \nУспехи: [сотрудник_1, cотрудник_2 ... сотрудник_N],
                    \nОшибки: [сотрудник_1, cотрудник_2 ... сотрудник_N], 
                    \nРекомендации по улучшению работы: [сотрудник_1, cотрудник_2 ... сотрудник_N],
                    \nОбщий комментарий: [сотрудник_1, cотрудник_2 ... сотрудник_N].
                    \nВозможные риски: [риск_1, риск_2 ... риск_N]\n\n\n
                    """.format(select_report_type, customer, anlazing_task, anlazing_time, anlazing_call, anlazing_deal,
                               anlazing_case),
                ]

## получение времени в секундах

>>> TimeControl.objects.values('DURATION').first()['DURATION'].total_second
s()
7200.0
>>> TimeControl.objects.values('DURATION').first()['DURATION'].total_second
s()
7200.0
>>> first_time = time_queryset.first()       

## Звонки

меньше чем 30 секунд
callControl.objects.filter(DURATION__lt='30').values('DURATIO N')

больше чем 5 минут
callControl.objects.filter(DURATION__gt='300').values('DURATI
ON')

Прорущенные звонки 
callControl.objects.filter(CALL_FAILED_CODE='304').values() 

Джанго Шелл Плюс | Расширенная оболочка Django | Команды оболочки Django | Учебное пособие по Django Shell 
https://www.youtube.com/watch?v=kNFMpfek4Ic

нахоэжение процента
round(user_call.filter(DURATION__lt='30').count() * 100 / callControl.objects.count())

anlazing_call = {' '.join((user.first_name, user.last_name)): {
                    "calls_less_that_30_seconds": callControl.objects.filter(bitrix_staff_id=user, DURATION__lt='30', DateCreate__year=datetime.now().year, DateCreate__month=datetime.now().month).values('PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "calls_less_that_30_seconds_count": callControl.objects.filter(bitrix_staff_id=user, DURATION__lt='30', DateCreate__year=datetime.now().year, DateCreate__month=datetime.now().month).count(),
                    "calls_more_that_5_minutes": callControl.objects.filter(bitrix_staff_id=user, DURATION__gt='300', DateCreate__year=datetime.now().year, DateCreate__month=datetime.now().month).values('PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "calls_more_that_5_minutes_count": callControl.objects.filter(bitrix_staff_id=user, DURATION__gt='300', DateCreate__year=datetime.now().year, DateCreate__month=datetime.now().month).count(),
                    "total_Incoming_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='1', DateCreate__year=datetime.now().year, DateCreate__month=datetime.now().month).values('PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "total_Incoming_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='1', DateCreate__year=datetime.now().year, DateCreate__month=datetime.now().month).count(),
                    "total_outgoing_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2', DateCreate__year=datetime.now().year, DateCreate__month=datetime.now().month).values( 'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "total_outgoing_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2', DateCreate__year=datetime.now().year, DateCreate__month=datetime.now().month).count(),
                    "total_missed_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='304', DateCreate__year=datetime.now().year, DateCreate__month=datetime.now().month).values('PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "total_missed_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='304', DateCreate__year=datetime.now().year, DateCreate__month=datetime.now().month).count()} for user in users
                }

                anlazing_task = {' '.join((user.first_name, user.last_name)): {
                    "tasks_deferred": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='6', CREATED_DATE__year=datetime.now().year, CREATED_DATE__month=datetime.now().month).values('TITLE','DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE') ,
                    "tasks_deferred_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='6', CREATED_DATE__year=datetime.now().year, CREATED_DATE__month=datetime.now().month).count(),
                    "tasks_in_progress": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='3', CREATED_DATE__year=datetime.now().year, CREATED_DATE__month=datetime.now().month).values('TITLE','DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE') ,
                    "tasks_in_progress_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='3', CREATED_DATE__year=datetime.now().year, CREATED_DATE__month=datetime.now().month).count(),
                    "tasks_needs_rework": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='7', CREATED_DATE__year=datetime.now().year, CREATED_DATE__month=datetime.now().month).values('TITLE','DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE') ,
                    "tasks_needs_rework_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='7', CREATED_DATE__year=datetime.now().year, CREATED_DATE__month=datetime.now().month).count(),
                    "tasks_overdue": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='5', CREATED_DATE__year=datetime.now().year, CREATED_DATE__month=datetime.now().month).values('TITLE','DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE'),
                    "tasks_overdue_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='5', CREATED_DATE__year=datetime.now().year, CREATED_DATE__month=datetime.now().month).count(),
                } for user in users}

                anlazing_time = {' '.join((user.first_name, user.last_name)): {
                    "time": TimeControl.objects.filter(bitrix_staff_id=user, START_TIME__year=datetime.now().year, START_TIME__month=datetime.now().month).values('TIME_LEAKS', 'DURATION')
                } for user in users}
##PANDAS 

выбор столбцов
df = read_frame(qs, fieldnames=['age', 'wage', 'full_name'])

call_per_user = {(user.first_name, user.last_name): {"number_calls_less_30": callControl.objects.filter(bitrix_staff_id=user, DURATION__lt='30', DateCreate__year = datetime.now().year, DateCreate__month = datetime.now().month).values('PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'), "number_calls_more_5": callControl.objects.filter(bitrix_staff_id=user, DURATION__gt='300', DateCreate__year = datetime.now().year, DateCreate__month = datetime.now().month).values('PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'), "total_Incoming_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='1', DateCreate__year = datetime.now().year, DateCreate__month = datetime.now().month).values('PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'), "total_outgoing_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2', DateCreate__year = datetime.now().year, DateCreate__month = datetime.now().month).values('PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'), "total_missed_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='304', DateCreate__year = datetime.now().year, DateCreate__month = datetime.now().month).values('PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate')}  for user in users}
df = pd.DataFrame(call_per_user)

call_per_user_count = {(user.first_name, user.last_name): {"number_calls_less_30": callControl.objects.filter(bitrix_staff_id=user, DURATION__lt='30', DateCreate__year = datetime.now().year, DateCreate__month = datetime.now().month).count(), "number_calls_more_5": callControl.objects.filter(bitrix_staff_id=user, DURATION__gt='300', DateCreate__year = datetime.now().year, DateCreate__month = datetime.now().month).count(), "total_Incoming_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='1', DateCreate__year = datetime.now().year, DateCreate__month = datetime.now().month).count(), "total_outgoing_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2', DateCreate__year = datetime.now().year, DateCreate__month = datetime.now().month).count(), "total_missed_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='304', DateCreate__year = datetime.now().year, DateCreate__month = datetime.now().month).count()}  for user in users}
df = pd.DataFrame(call_per_user)

combined_df = pd.concat([df_notcount, df_count], axis=1)

 <form action="{% url 'chatbot_view' %}" method="POST">{% csrf_token %}
            <div class="form-group row">
                <div class="col-sm">
                    <select name="select_type_report" class="form-control">
                        <option>Отчёт не выбран</option>
                        <option>Отчет о проделанной работе за месяц</option>
                        <option>Отчет о проделанной работе за день</option>
                        <option>Отчет о проделанной работе за неделю</option>
                    </select>
                </div>
                <div class="col-sm">
                    <select name="select_type_staff" class="form-control">
                        <option>Сотрудник не выбран</option>
                        {% for i in staff %}
                        <option>{{i.admin.first_name}}&nbsp;{{i.admin.last_name}}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-sm-6">
                    <input type="submit" class="btn btn-outline-secondary mr-2" value="Cоздать отчёт">
                </div>
            </div>

<!--            <div class="mb-3">-->
<!--            <textarea class="form-control" id="exampleFormControlTextarea2"-->
<!--                      rows="3">{{response}}</textarea>-->
<!--            </div>-->
        </form>

## настройка 
<form action="{% url 'chatbot_view' %}" method="POST">{% csrf_token %}
            <div class="form-group row">
                <div class="col-sm">
                    <select name="select_type_report" class="form-control">
                        <option>Отчёт не выбран</option>
                        <option>Отчет о проделанной работе за месяц</option>
                        <option>Отчет о проделанной работе за день</option>
                        <option>Отчет о проделанной работе за неделю</option>
                    </select>
                </div>
                <div class="col-sm">
                    <select name="select_type_staff" class="form-control">
                        <option>Сотрудник не выбран</option>
                        {% for i in staff %}
                        <option>{{i.admin.first_name}}&nbsp;{{i.admin.last_name}}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-sm-6">
                    <input type="submit" class="btn btn-outline-secondary mr-2" value="Cоздать отчёт">
                </div>
            </div>

<!--            <div class="mb-3">-->
<!--            <textarea class="form-control" id="exampleFormControlTextarea2"-->

## задачи
% if current_user.user_type == '1' %}
                            {% for user, tasks_counts in tasks_per_user.items %}
                            <tr>
                                <td>{{ user.first_name }}&nbsp;{{ user.last_name }}</td>
                                <td>{{ tasks_counts.deferred_count }}</td>
                                <td>{{ tasks_counts.in_progress_count }}</td>
                                <td>{{ tasks_counts.needs_rework_count }}</td>
                                <td>{{ tasks_counts.overdue_count }}</td>
                            </tr>
                            {% endfor %}
                            {% elif current_user.user_type == '2' %}
                            {% for user, tasks_counts in tasks_per_user.items %}
                            {% if user == current_user %}
                            <tr>
                                <td>{{ user.first_name }}&nbsp;{{ user.last_name }}</td>
                                <td>{{ tasks_counts.deferred_count }}</td>
                                <td>{{ tasks_counts.in_progress_count }}</td>
                                <td>{{ tasks_counts.needs_rework_count }}</td>
                                <td>{{ tasks_counts.overdue_count }}</td>
                            </tr>
                            {% endif %}
                            {% endfor %}
                            {% endif %}
<!--                      rows="3">{{response}}</textarea>-->
<!--            </div>-->
        </form>

number_calls_less_30 = call.filter(DURATION__lt='30').count(),
number_calls_more_5 = call.filter(DURATION__gt='300').count(),
total_Incoming_calls = call.filter(CALL_TYPE='1').count(),
total_outgoing_calls = call.filter(CALL_TYPE='2').count(),
total_missed_calls = call.filter(CALL_FAILED_CODE='304').count(),
rejected_calls = call.filter(CALL_FAILED_CODE='603').count(),
busy_calls = call.filter(CALL_FAILED_CODE='486').count(),

## docker

https://stackoverflow.com/questions/46711990/error-pg-config-executable-not-found-when-installing-psycopg2-on-alpine-in-dock
https://yandex.ru/video/preview/6141758714148788816


docker-compose run web python manage.py createsuperuser 
docker-compose exec db psql -U postgres -d newproject
insert into app_bitrix24(webhook, name_webhook) values ('', 'one');
docker-compose restart web

# ai
from g4f.client import Client
client = Client()
response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]).choices[0].message.content

df = pd.DataFrame(anlazing_call)

# переделки
````
# genai.configure(api_key="AIzaSyDRK2DTmNY61tutvN2n_W51O0diOrr5ulU")
#
# generation_config = {
#     "temperature": 0.9,
#     "top_p": 1,
#     "top_k": 1,
#     "max_output_tokens": 2048,
# }
#
# safety_settings = [
#     {
#         "category": "HARM_CATEGORY_HARASSMENT",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#     },
#     {
#         "category": "HARM_CATEGORY_HATE_SPEECH",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#     },
#     {
#         "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#     },
#     {
#         "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#     },
# ]
#
# model = genai.GenerativeModel(
#     model_name="gemini-1.0-pro",
#     generation_config=generation_config,
#     safety_settings=safety_settings
# )

'''ChatGTP'''
# prompts = []

# '''Начальный системный промт'''
#
# prompts.append({"role": "system", "content": """
#     Ты являешься ботом который формирует отчёты от третьего лица (от лица компании Эркью)
#     Ты должен следовать всем требованиям формирования отчётов для эффективности и контроля
#     работы сотрудников организации. Вывод информации должен содержать заголовки [Успехи:], [Ошибки:], [Рекомендации по улучшению работы:], [Общий комментарий:].
# """})
#
# '''Промт сотрудника за месяц'''
#
# if select_type_staff == "Сотрудник не выбран":
#     prompts.append({"role": "user", "content": "Cделай {0} включая каждого сотрудников {1}".format(
#         select_report_type,
#         customer
#     )})
# else:
#     prompts.append({"role": "user", "content": "Cделай {0} по сотруднику {1}".format(
#         select_report_type,
#         select_type_staff
#     )})

# response = openai.ChatCompletion.create(
#     model="ft:gpt-3.5-turbo-0613:personal::7wZAALHG",
#     messages=prompts,
#     api_key="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",
#     max_tokens=1200,
#     temperature=0.2,
#     top_p=1,
#     frequency_penalty=0.5,
#     presence_penalty=0.5
# )

# staff = CustomUser.objects.filter(
#     id__in=Staff.objects.values_list('admin_id', flat=True)
# ).values('first_name', 'last_name')
# for i in staff:
#     customer += "{0} {1} \n".format(i['first_name'], i['last_name'])

# first_name, last_name = select_type_staff_split.split()
# user_input = request.POST.get('textPostSelect')
# print(user_input)

# from g4f.client import Client
# client = Client()
print(request)
# conversation = request.session.get('conversation', [])

# response = client.chat.completions.create(model="gpt-3.5-turbo",
#                                           messages=[
#                                               {"role": "user", "content": prompt}]
#                                           ).choices[0].message.content
# print(response)

# response = model.generate_content(prompt)

# add_new_report_emps = Attendance_Report(
#     name_report=select_report_type,
#     description=response.text
# )
# response = client.chat.completions.create(model="gpt-3.5-turbo",
#                                           messages=[
#                                               {"role": "user", "content": prompt}]
#                                           ).choices[0].message.content
# print(response)
# response = model.generate_content(prompt)

# add_new_report_emp = Attendance_Report(
#     name_report=select_report_type,
#     description=response.text,
#     staff_id=str(staff_add)
# )

# add_new_report.save()
# prompt.clear()

# add_new_report_PDF = Customer(
#     name_report=select_report_type,
# )
# add_new_report_PDF.save()

# Extract chatbot replies from the response
# chatbot_replies = [message['message']['content'] for message in response['choices'] if
#                    message['message']['role'] == 'assistant']

# Append chatbot replies to the conversation
# for reply in chatbot_replies:
#     conversation.append({"role": "assistant", "content": reply})

# Update the conversation in the session
# request.session['conversation'] = conversation
````