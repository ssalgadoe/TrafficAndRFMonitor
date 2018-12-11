from django.db import models

# Create your models here.

class Queues(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    device_name = models.CharField(max_length=60, blank=True, null=True)
    ip = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return(self.name + '-' + self.device_name)

class Queue_data(models.Model):
    queue = models.ForeignKey(Queues, on_delete=models.CASCADE)
    ip = models.CharField(max_length=45, blank=True, null=True)
    owner = models.CharField(max_length=45, blank=True, null=True,default='1')
    dummy = models.CharField(max_length=10, blank=True, null=True, default='1')
    b_tx = models.CharField(max_length=45, blank=True, null=True)
    b_rx = models.CharField(max_length=45, blank=True, null=True)
    p_tx = models.CharField(max_length=45, blank=True, null=True)
    p_rx = models.CharField(max_length=45, blank=True, null=True)
    drop_tx = models.CharField(max_length=45, blank=True, null=True)
    drop_rx = models.CharField(max_length=45, blank=True, null=True)
    usage_tx = models.CharField(max_length=45, blank=True, null=True)
    usage_rx = models.CharField(max_length=45, blank=True, null=True)
    time_st = models.DateTimeField(blank=True, null=True)
    mk_time = models.DateTimeField(blank=True, null=True)
    average_tx = models.CharField(max_length=45, blank=True, null=True)
    average_rx = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return('Owner:' + self.owner + ' IP: ' +self.ip + ' b_tx: ' + self.b_tx + ' b.rx: ' + self.b_rx + ' time: ' + str(self.mk_time))



