from django.db import models

NULLABLE = {'blank': True, 'null': True}

class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    preview = models.ImageField(upload_to='lms/preview/course', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Курс', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='lms/preview/lesson', verbose_name='Превью', **NULLABLE)
    link_to_video = models.CharField(max_length=200, verbose_name='Ссылка на видео', **NULLABLE)
