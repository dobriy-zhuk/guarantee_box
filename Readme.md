# Guarantee learning

## Migration database conflicts

If you making new models or update a old one you need to do:

```sh
python manage.py makemigrations
python manage.py migrate
```

it will create new migration files
local check and push, I need all migration files!  
Then I will do:

```sh
git pull
git fetch
```

first what I should do is

```sh
python manage.py migrate
```

and only that, because I don't need to do new migration files
check what you have done migrations for all apps.
[Here is an opinion on stackoveflow](https://stackoverflow.com/questions/28035119/should-i-be-adding-the-django-migration-files-in-the-gitignore-file)

## In which branch should I develop localy?

Which you want but not in master and not in test.  
You can develop in developer branch and etc.  
But you should commit and push only to developer branch.
And after code review it will be merged into test.

## What a heck with a jinja

It doesn't work, because jinja preinstall all urls
and ```"{% url '' %}"``` is empty so where will be an error like that:

```sh
NoReverseMatch at /students/
Reverse for '' not found. '' is not a valid view function or pattern name.
```

```html
<a href="{% url '' %}" class="list-group-item">
            <h4 class="list-group-item-heading">Доступные занятия</h4>
</a>
```

Urls in templates are required

```html
<a href="{% url 'course_list' %}" class="list-group-item">
            <h4 class="list-group-item-heading">Доступные занятия</h4>
</a>
```

If you comment it, it will pesponse you an same error. So be attentive.

```html
<!-- <a href="{% url '' %}" class="list-group-item">
            <h4 class="list-group-item-heading">Доступные занятия</h4>
</a> -->
```

## One more thing about jinja

It doesn't work, because jinja doesn't let quotes like this

```jinja
"{% url "some_url" %}"
```

Upper is 2 different strings  
Please do like this:

```jinja
"{% url 'some_url' %}"
```

It's string in string and jinja lets you to do that

## Live video

For starting React project you need to be in live_video directory.
And you need to install yarn on your machine as well.

```sh
yarn start
```

## Do not use numbers in function names

Wrong:

```python
def get_some_or_404(*args):
    pass
```

Good:

```python
def get_some_or_not_found_error(*args):
    pass
```

## If you have a problem with makemigrations

Look at this [article](https://devman.org/encyclopedia/django_orm/migrations_mastering/)

## What is the differense between null and blank in Django ORM and where should I user it

Look [here](https://stackoverflow.com/questions/8609192/differentiate-null-true-blank-true-in-django/8609425) for more info
Summary from url:
Good:

```python
models.ForeignKey(null=True)
models.DateTimeField(null=True) #it must be filled out in a form
models.CharField(blank=True) #stored in db as ''
```

Bad:

```python
models.DateTimeField(blank=True) # raises IntegrityError if blank
models.CharField(null=True) # NULL allowed, but will never be set as NULL
```

Шпаргалка Django ORM
Аналогия между SQL и ORM операторами

| Название         | Оператор SQL | Оператор ORM |
| ---------------- | :----------: | -----------: |
| Больше чем       | >            | `__gt`       |
| Больше или равно | =>           | `__gte`      |
| Меньше чем       | <            | `__lt`       |
| Меньше или равно | =<           | `__lte`      |
| Равно            | =            | `=`          |
| Не равно         | NOT          | `exclude`    |
| Логическое И     | AND          | `,`          |
| Ноль (ничего)    | {null}       | `None`       |
| None             |              |              |

TODO: Написать примеры использования

## How to show ManyToMany field in Django template?

Look [here](https://stackoverflow.com/questions/4270330/django-show-a-manytomanyfield-in-a-template)

## Something about corsheaders

Look [here](https://stackoverflow.com/questions/28046422/django-cors-headers-not-work)

You just need put 'corsheaders.middleware.CorsMiddleware' above all
middlewares in MIDDLEWARE variable.

## How work with datetime in jinja

Look [here](https://ourcodeworld.com/articles/read/555/how-to-format-datetime-objects-in-the-view-and-template-in-django)

```jinja
<!-- Выводит тип str -->
Месяц: {{ lesson.schedule.start_timestamp|date:'m'}}
<!-- 06 -->
День: {{ lesson.schedule.start_timestamp|date:'d' }}
<!-- 12 -->
Часы: {{ lesson.schedule.start_timestamp|date:'H' }}
<!-- 06 -->
Минуты: {{ lesson.schedule.start_timestamp|date:'i' }}
<!-- 00 -->
Все вместе: {{ lesson.schedule.start_timestamp|date:'Y-m-d H:i' }}
<!-- 2020-06-12 06:00 -->
```

`Best regards, Ian`

*If you have some good info about project please share with us below.*
