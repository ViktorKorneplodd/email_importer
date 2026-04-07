# Email Importer Django Project

Система для импорта email рассылок из Excel файлов (XLSX) с последующей отправкой писем.

## Запуск проекта

```bash
python -m venv venv
source venv/bin/activate (или venv\Scripts\activate на Windows)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver