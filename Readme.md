# Лабораторна робота No1 Найпростіший Flask-додаток
## Віртуальне середовище

> python3 -m venv .venv


```bash
(.venv) bogdanpavliuk@Mac-mini-Bogdan flask_app_pavliuk % pip list
Package      Version
------------ -------
blinker      1.9.0
click        8.3.0
Flask        3.1.2
itsdangerous 2.2.0
Jinja2       3.1.6
MarkupSafe   3.0.3
pip          25.2
Werkzeug     3.1.3
```

```bash
(.venv) bogdanpavliuk@Mac-mini-Bogdan flask_app_pavliuk % flask run 
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

```bash
(.venv) bogdanpavliuk@Mac-mini-Bogdan flask_app_pavliuk % flask run 
 * Serving Flask app 'app.py'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8080
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 541-618-492
 ```

```bash
(.venv) bogdanpavliuk@Mac-mini-Bogdan flask_app_pavliuk % pip freeze > requirements.txt
```