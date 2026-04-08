# Email Importer Django Project

Сервис для импорта email рассылок из Excel файлов с последующей отправкой писем.

## Функциональность

- Импорт данных из Excel файла с колонками: external_id, user_id, email, subject, message
- Автоматическое предотвращение дубликатов по external_id
- Отправка писем с искусственной задержкой (5-20 секунд)
- Логирование всех отправленных писем
- Сохранение ошибок импорта в базу данных

## Запуск проекта

1. `python -m venv venv`
2. `source venv/bin/activate` (или `venv\Scripts\activate` на Windows)
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py runserver`

## Как тестировать импорт

### Подготовка тестовых данных

## Откройте терминал и выполните:
`python -c "import pandas as pd; pd.DataFrame({'external_id': ['1','2','3'], 'user_id': ['user1','user2','user3'], 'email': ['test1@example.com','test2@example.com','test3@example.com'], 'subject': ['Subject 1','Subject 2','Subject 3'], 'message': ['Message 1','Message 2','Message 3']}).to_excel('test_emails.xlsx', index=False)"`

## Запустите импорт
`python manage.py import_emails --file test_emails.xlsx`

## Ожидаемый вывод
- Обработано строк: 3
- Создано записей: 3
- Пропущено записей: 0
- Ошибочных строк: 0


## Другие тесты
 Повторный импорт (проверка дубликатов) | `python manage.py import_emails --file test_emails.xlsx` |
 Импорт без отправки писем | `python manage.py import_emails --file test_emails.xlsx --skip-sending` |
 Проверка количества записей в БД | `python manage.py shell -c "from mailing.models import ImportedEmail; print(f'Записей: {ImportedEmail.objects.count()}')"` |
 Просмотр логов отправки (Windows) | `type logs\emails.log` |
 Просмотр логов отправки (Linux/macOS) | `cat logs/emails.log` |
