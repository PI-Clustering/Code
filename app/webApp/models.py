from django.db import models


class Benchmark(models.Model):
    id = models.AutoField(primary_key=True)
    algo_type = models.CharField(max_length=20)
    size = models.IntegerField()
    t_pre = models.DecimalField(max_digits=5, decimal_places=2)
    t_cluster = models.DecimalField(max_digits=5, decimal_places=2)
    t_write = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.algo_type + self.size


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
