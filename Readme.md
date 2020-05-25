## Migration database conflicts
If you making new models or update a old one you need to do:
```
python manage.py makemigrations
python manage.py migrate
```
it will create new migration files
local check and push, I need all migration files!  
Then I will do:
```
git pull
git fetch
```
first what I should do is
```
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

## What a heck with a jinja?
It doesn't work, because jinja preinstall all urls   
and ```"{% url '' %}"``` is empty so where will be an error like that:
```
NoReverseMatch at /students/
Reverse for '' not found. '' is not a valid view function or pattern name.
```

```html
<a href="{% url '' %}" class="list-group-item">
            <h4 class="list-group-item-heading">Доступные занятия</h4>
```
Urls in templates are required
```html
<a href="{% url 'course_list' %}" class="list-group-item">
            <h4 class="list-group-item-heading">Доступные занятия</h4>
```
If you comment it, it will pesponse you an same error. So be attentive.   
```html
<!-- <a href="{% url '' %}" class="list-group-item">
            <h4 class="list-group-item-heading">Доступные занятия</h4> -->
```

#### Best regards, Ian.

If you have some good info about project please share with us below.