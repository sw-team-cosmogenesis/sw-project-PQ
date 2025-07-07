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


#游客模型
class GuestUser(models.Model):

    id = models.BigIntegerField(primary_key=True, editable=False)  # 雪花ID主键

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, help_text="由前端生成，作为前后端通信的索引")

    created_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(auto_now=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    registered_user = models.ForeignKey(
        RegisteredUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="guest_profiles"
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = next(generator)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"GuestUser ({self.uuid})"

#演讲模型
class Presentation(models.Model):
    """
    演讲/课程 模型
    代表一次演讲、一堂课或一次分享会。
    演讲者可创建多个 Presentation，每个演讲对应多个 PopQuiz。
    """

    id = models.BigIntegerField(primary_key=True, editable=False)  # 雪花主键

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # 外部引用安全ID

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


#题目模型
class PopQuiz(models.Model):

    id = models.BigIntegerField(primary_key=True, editable=False)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

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
