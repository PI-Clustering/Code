from django.db import models


class Benchmark(models.Model):
    algo_type = models.CharField(max_length=20)
    data_set = models.CharField(max_length=20)
    n_iterations = models.IntegerField()
    size = models.IntegerField()
    t_pre = models.DecimalField(max_digits=5, decimal_places=2)
    t_cluster = models.DecimalField(max_digits=5, decimal_places=2)
    t_write = models.DecimalField(max_digits=5, decimal_places=2)


    def __str__(self):
        return self.algo_type + self.data_set


class DataPoint(models.Model):
    benchmark = models.ForeignKey(Benchmark, on_delete=models.CASCADE)
    iteration_no = models.IntegerField()
    ami = models.DecimalField(max_digits=5, decimal_places=3)
    f_score = models.DecimalField(max_digits=5, decimal_places=3)
    t_pre = models.DecimalField(max_digits=5, decimal_places=2)
    t_cluster = models.DecimalField(max_digits=5, decimal_places=2)
    t_write = models.DecimalField(max_digits=5, decimal_places=2)


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
