## Migration database conflicts
---
If you making new models or update a old one you need to do:
```
python manage.py makemigrations
python manage.py migrate
```
it will create new migration files
local check and push, I need all migration files!
When I will do a:
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
Best regards, Ian.