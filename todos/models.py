from django.db import models

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100, help_text="할 일 제목")
    content = models.TextField(help_text="할 일 내용")
    created_at = models.DateTimeField(auto_now_add=True, help_text="할 일 생성 일자")
    updated_at = models.DateTimeField(auto_now=True, help_text="할 일 수정 일자")
    is_completed = models.BooleanField(default=False, help_text="할 일 완료 여부")

    def __str__(self):
        return self.title