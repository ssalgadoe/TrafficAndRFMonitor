from django.db import models

class Towers(models.Model):
    loc_id = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=40, blank=False, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    lon_id = models.CharField(max_length=20, blank=True, null=True)
    lat_id = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return(self.name)


class APs(models.Model):
    name = models.CharField(max_length=60, blank=False, null=True)
    ip = models.CharField(max_length=45, blank=True, null=True)
    loc_id = models.CharField(max_length=20, blank=True, null=True)
    frequency = models.CharField(max_length=45, blank=True, null=True)
    lon_id = models.CharField(max_length=45, blank=True, null=True)
    lat_id = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return(self.name)

class Customers(models.Model):
    name = models.CharField(max_length=40, blank=False, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    lon_id = models.CharField(max_length=20, blank=True, null=True)
    lat_id = models.CharField(max_length=20, blank=True, null=True)
    ap_id = models.CharField(max_length=20, blank=True, null=True)
    loc_id = models.CharField(max_length=20, blank=True, null=True)
    frequency = models.CharField(max_length=45, blank=True, null=True)


    def __str__(self):
        return(self.name)

class Registrations(models.Model):
    cust_name = models.CharField(max_length=100, blank=False, null=True)
    device_name = models.CharField(max_length=60, blank=False, null=True)
    ap = models.ForeignKey(APs, on_delete=models.CASCADE)
    loc_id = models.CharField(max_length=20, blank=True, null=True)
    cust = models.ForeignKey(Customers, on_delete=models.CASCADE)
    ip = models.CharField(max_length=45, blank=True, null=True)
    mac = models.CharField(max_length=45, blank=True, null=True)
    rssi = models.CharField(max_length=10, blank=True, null=True)
    snr = models.CharField(max_length=10, blank=True, null=True)
    ccq_tx = models.CharField(max_length=10, blank=True, null=True)
    ccq_rx = models.CharField(max_length=10, blank=True, null=True)
    uptime = models.CharField(max_length=45, blank=True, null=True)
    uptime_sec = models.CharField(max_length=45, blank=True, null=True)
    distance = models.CharField(max_length=45, blank=True, null=True)
    time_st = models.DateTimeField(blank=True, null=True)
    mk_time = models.DateTimeField(blank=True, null=True)
    extra = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=45, blank=True, null=True,default='0')
    dummy = models.CharField(max_length=10, blank=True, null=True, default='0')


    def __str__(self):
        return(self.cust_name + '-' + self.ip)