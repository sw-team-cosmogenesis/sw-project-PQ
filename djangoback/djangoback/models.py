from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from snowflake import SnowflakeGenerator
from datetime import datetime

#调用雪花算法库
#自定义起始时间为2025.7.1 00：00：00
custom_epoch = int(datetime(2025, 7, 1, 0, 0, 0).timestamp() * 1000)
generator = SnowflakeGenerator(instance=1, epoch=custom_epoch)

#注册用户模型
class RegisteredUser(AbstractUser):
    id = models.BigIntegerField(primary_key=True, editable=False, help_text="雪花算法生成的 id ，作为主键使用")

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text="自动生成的全局唯一 UUID"
    )

    ROLE_CHOICES = (
        ('audience', 'Audience'),
        ('speaker', 'Speaker'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='audience')

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = next(generator)
        super().save(*args, **kwargs)

    def is_speaker(self):
        return self.role == 'speaker'

    def is_audience(self):
        return self.role == 'audience'

    def __str__(self):
        return f"{self.username} ({self.role})"


#演讲模型
class Presentation(models.Model):
    """
    演讲/课程 模型
    代表一次演讲、一堂课或一次分享会。
    演讲者可创建多个 Presentation，每个演讲对应多个 PopQuiz。
    """
    id = models.BigIntegerField(primary_key=True, editable=False)  # 雪花主键

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text="自动生成的全局唯一 UUID"
    )

    title = models.CharField(max_length=200, help_text="演讲标题")
    description = models.TextField(blank=True, help_text="演讲简要描述，可选")

    presenter = models.ForeignKey(
        RegisteredUser,
        on_delete=models.CASCADE,
        related_name='presentations',
        help_text="演讲者，必须为已注册用户"
    )

    scheduled_time = models.DateTimeField(null=True, blank=True, help_text="预定开始时间")
    duration_minutes = models.IntegerField(null=True, blank=True, help_text="预计时长（分钟）")

    is_active = models.BooleanField(default=True, help_text="是否处于进行中 / 可互动状态")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = next(generator)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Presentation: {self.title} by {self.presenter.username}"

# 演讲中包含的多媒体文件
class MediaFile(models.Model):

    id = models.BigIntegerField(primary_key=True, editable=False)

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text="自动生成的全局唯一 UUID"
    )

    class MediaType(models.TextChoices):
        PPT = 'ppt', 'PPT'
        VIDEO = 'video', 'Video'
        AUDIO = 'audio', 'Audio'
        IMAGE = 'image', 'Image'
        PDF = 'pdf', 'PDF'
        OTHER = 'other', 'Other'

    presentation = models.ForeignKey('Presentation', on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='media_files/')
    type = models.CharField(max_length=10, choices=MediaType.choices)
    title = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = next(generator)
        super().save(*args, **kwargs)

    def file_url(self):
        return self.file.url


#题目模型
class PopQuiz(models.Model):

    id = models.BigIntegerField(primary_key=True, editable=False)

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text="自动生成的全局唯一 UUID"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    QUESTION_TYPES = (
        ('choice', '选择题'),
        ('fill', '填空题'),
    )
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default='choice',
        help_text="题目类型：choice=选择题，fill=填空题"
    )

    question_text = models.TextField(help_text="题干文本")

    options = models.JSONField(
        null=True, blank=True,
        help_text='题目选项，格式要求为：["选项A", "选项B", "选项C"]'
    )

    correct_answers = models.JSONField(
        help_text="标准答案列表，支持多选或多个填空匹配"
    )

    is_multiple = models.BooleanField(
        default=False,
        help_text="是否为多选题，仅用于选择题"
    )


    quiz_index = models.IntegerField(
        help_text="该题在演讲中的编号，例如第 0、1、2 题"
    )

    presentation = models.ForeignKey(
        Presentation,
        on_delete=models.CASCADE,
        related_name="pop_quizzes",
        help_text="该题目所属的演讲或课程"
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = next(generator)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"PopQuiz # ({self.question_type}) for Presentation {self.presentation}"


class Answer(models.Model):
    id = models.BigIntegerField(primary_key=True, editable=False)

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text="自动生成的全局唯一 UUID"
    )

    user = models.ForeignKey(
        RegisteredUser,
        on_delete=models.CASCADE,
        related_name="answers",
        help_text="作答者"
    )

    quiz = models.ForeignKey(
        PopQuiz,
        on_delete=models.CASCADE,
        related_name="answers",
        help_text="对应的题目"
    )

    presentation = models.ForeignKey(
        Presentation,
        on_delete=models.CASCADE,
        related_name="answers",
        help_text="所属演讲"
    )

    selected_options = models.JSONField(
        help_text="作答选项（支持多选），格式如：[\"A\"] 或 [\"A\", \"C\"]"
    )

    is_correct = models.BooleanField(
        null=True,  # 可选，便于后期统一打分
        help_text="是否作答正确，可在后台评判后赋值"
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = next(generator)
        super().save(*args, **kwargs)
