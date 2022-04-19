from django.db import models

MAX_AVG_AREA = 100
MAX_AVG_VOLUME = 1000
MAX_TOTAL_WEEK_BOXES = 100
MAX_STAFF_WEEK_BOXES = 50


class Box(models.Model):
    length = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    area = models.IntegerField(default=0)
    volume = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("auth.user", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
