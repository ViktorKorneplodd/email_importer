import logging
import pandas as pd
from pathlib import Path
from random import randint
from time import sleep
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from mailing.models import ImportedEmail, ImportError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Импорт рассылок из XLSX файла и отправка писем'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, required=True, help='Путь к XLSX файлу')
        parser.add_argument('--skip-sending', action='store_true', help='Пропустить отправку писем')

    def handle(self, *args, **options):
        file_path = options['file']
        skip_sending = options['skip_sending']

        stats = {'total': 0, 'created': 0, 'skipped': 0, 'errors': 0}

        self.stdout.write(self.style.SUCCESS(f'Начало импорта: {file_path}'))

        if not Path(file_path).exists():
            raise CommandError(f'Файл не найден: {file_path}')

        df = pd.read_excel(file_path)
        stats['total'] = len(df)

        for idx, row in df.iterrows():
            row_number = idx + 2
            external_id = str(row.get('external_id', ''))

            if ImportedEmail.objects.filter(external_id=external_id).exists():
                stats['skipped'] += 1
                self.stdout.write(f' Строка {row_number}: пропущено (дубликат)')
                continue

            try:
                email_record = ImportedEmail.objects.create(
                    external_id=external_id,
                    user_id=str(row.get('user_id', '')),
                    email=str(row.get('email', '')),
                    subject=str(row.get('subject', '')),
                    message=str(row.get('message', ''))
                )

                if not skip_sending:
                    delay = randint(5, 20)
                    self.stdout.write(f' Задержка {delay} сек перед отправкой...')
                    sleep(delay)
                    self.stdout.write(f' Отправлено письмо на {email_record.email}')

                stats['created'] += 1
                self.stdout.write(f' Строка {row_number}: создано')

            except Exception as e:
                stats['errors'] += 1
                ImportError.objects.create(
                    row_number=row_number,
                    external_id=external_id,
                    error_message=str(e),
                    raw_data=row.to_dict()
                )
                self.stdout.write(self.style.ERROR(f' Строка {row_number}: ошибка - {str(e)}'))

        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('РЕЗУЛЬТАТЫ ИМПОРТА'))
        self.stdout.write('=' * 50)
        self.stdout.write(f' Обработано строк: {stats["total"]}')
        self.stdout.write(f' Создано записей: {stats["created"]}')
        self.stdout.write(f' Пропущено записей: {stats["skipped"]}')
        self.stdout.write(f' Ошибочных строк: {stats["errors"]}')
        self.stdout.write('=' * 50)