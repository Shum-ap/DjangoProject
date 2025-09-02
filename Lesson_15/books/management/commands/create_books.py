# books/management/commands/create_books.py
from django.core.management.base import BaseCommand
from books.models import Book
import random
from datetime import date

# Списки для генерации случайных данных
TITLES = [
    "1984", "Война и мир", "Гарри Поттер", "Мастер и Маргарита", "Преступление и наказание",
    "Алые паруса", "Три товарища", "О дивный новый мир", "Фаренгейт 451", "Мы", "День триффидов",
    "Посторонний", "Шум и ярость", "Над пропастью во ржи", "Цветы для Элджернона", "Солярис",
    "Сталкер", "451 градус по Фаренгейту", "Моби Дик", "Остров сокровищ"
]

AUTHORS = [
    "Джордж Оруэлл", "Лев Толстой", "Дж. К. Роулинг", "Михаил Булгаков", "Фёдор Достоевский",
    "Александр Грин", "Эрих Мария Ремарк", "Олдос Хаксли", "Рэй Брэдбери", "Евгений Замятин",
    "Джон Уиндем", "Альбер Камю", "Уильям Фолкнер", "Джером Сэлинджер", "Дэниел Киз",
    "Станислав Лем", "Братья Стругацкие", "Герман Мелвилл", "Роберт Стивенсон", "Ричард Мэтьюсон"
]


class Command(BaseCommand):
    help = 'Создаёт 10 случайных книг'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Количество книг для создания'
        )

    def handle(self, *args, **options):
        count = options['count']
        created_count = 0

        for _ in range(count):
            title = random.choice(TITLES)
            author = random.choice(AUTHORS)
            year = random.randint(1800, 2025)
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # чтобы избежать ошибок с 29-31
            published_date = date(year, month, day)

            book, created = Book.objects.get_or_create(
                title=title,
                author=author,
                defaults={'published_date': published_date}
            )

            if created:
                created_count += 1
                self.stdout.write(f"✅ Книга: '{book.title}' — {book.author}, {book.published_date}")
            else:
                self.stdout.write(f"⚠️ Уже существует: '{book.title}' — {book.author}")

        self.stdout.write(
            self.style.SUCCESS(f'Успешно создано {created_count} новых книг из {count} запрошенных.')
        )
