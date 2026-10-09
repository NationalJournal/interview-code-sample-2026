from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """
    An answer option for a Question.

    A Choice may optionally carry an approximate geographic location (e.g.
    a capital city or a beach destination). When present, this is used to
    show the choice as a pin on a map alongside the poll question, before
    anyone votes. It has nothing to do with where a voter is located.
    """

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    choice_text = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.choice_text

    def has_location(self):
        return self.latitude is not None and self.longitude is not None

    @property
    def votes(self):
        """Number of responses recorded for this choice."""
        return self.responses.count()


class Response(models.Model):
    """A single vote cast for a Choice."""

    choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, related_name="responses"
    )
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote for {self.choice} at {self.voted_at:%Y-%m-%d %H:%M}"


class Category(models.Model):
    """A topical grouping for questions (e.g. "Geography", "Travel")."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
