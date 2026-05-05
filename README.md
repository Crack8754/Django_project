Для запуску серверу використовуйте ті команди по черзі:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process,
venv\Scripts\activate,
python manage.py runserver,
