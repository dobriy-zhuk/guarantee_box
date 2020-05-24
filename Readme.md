## Migration database conflicts
---
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
---
Which you want but not in master and not in test.  
You can develop in developer branch and etc.  
But you should commit and push only to developer branch.
And after code review it will be merged into test.

Best regards, Ian.

If you have some good info about project please share with us below.