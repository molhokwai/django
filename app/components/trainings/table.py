from django_unicorn.components import UnicornView
from app.models import TrainingCourse, TrainingCourseSession, TaskStatus


class TableView(UnicornView):
    TaskStatusEnum = TaskStatus