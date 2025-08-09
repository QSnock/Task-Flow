from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from boards.models import Board, BoardMember
from tasks.models import Task

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает тестовые данные для Task Flow'

    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных...')

        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Тест',
                'last_name': 'Пользователь'
            }
        )

        if created:
            user.set_password('test123')
            user.save()
            self.stdout.write('Создан user: test_user (пароль: test123)')

        board, created = Board.objects.get_or_create(
            title='Тестовая доска',
            owner=user,
            defaults={
                'description': 'Это тестовая доска'
            }
        )

        if created:
            self.stdout.write(f'Создана доска: {board.title}')

            BoardMember.objects.create(
                board=board,
                user=user,
                role='owner'
            )

        test_tasks = [
            {
                'title': 'Настроить проект',
                'description': 'Настроить базовую структуру Django проекта',
                'status': 'done'
            },
            {
                'title': 'Создать модели',
                'description': 'Создать модели для досок и задач',
                'status': 'done'
            },
            {
                'title': 'Добавить аутентификацию',
                'description': 'Реализовать страницы входа и регистрации',
                'status': 'in_progress'
            },
            {
                'title': 'Создать доску',
                'description': 'Разработать интерфейс доски с колонками',
                'status': 'review'
            },
            {
                'title': 'Добавить drag & drop',
                'description': 'Реализовать перетаскивание задач',
                'status': 'todo'
            },
            {
                'title': 'Управление участниками',
                'description': 'Добавить возможность приглашения по email',
                'status': 'todo'
            }
        ]

        for i, task_data in enumerate(test_tasks):
            task, created = Task.objects.get_or_create(
                title=task_data['title'],
                board=board,
                defaults={
                    'description': task_data['description'],
                    'status': task_data['status'],
                    'creator': user,
                    'assignee': user if i % 2 == 0 else None,
                    'position': i
                }
            )

            if created:
                self.stdout.write(
                    f'Создана задача: {task.title} ({task.status})'
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Тестовые данные созданы!\n'
                f'Пользователь: test_user (пароль: test123)\n'
                f'Доска: {board.title}\n'
                f'Задач создано: {board.tasks.count()}'
            )
        )
