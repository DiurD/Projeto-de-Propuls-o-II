from django.db import models

class atmos(models.Model):
    alt = models.FloatField(primary_key=True)
    T0 = models.FloatField(default=288.15)
    P0 = models.FloatField(default=101325.0)
    rho0 = models.FloatField(default=1.22)
    a0 = models.FloatField(default=340.2939)
    
    def __str__(self):
        return self.alt
    
class motor(models.Model):
    name = models.TextField(max_length=20,primary_key=True)
    motor_type = models.TextField(max_length=20)
    d0 = models.FloatField()
    d1 = models.FloatField()
    d2 = models.FloatField()
    d3 = models.FloatField()
    d4 = models.FloatField()
    d5 = models.FloatField()
    d6 = models.FloatField()
    d7 = models.FloatField()
    d8 = models.FloatField()
    d9 = models.FloatField()
    lenght = models.FloatField()
    speed_in_combustion = models.FloatField()
    on_design = models.BooleanField()
    choked = models.BooleanField()
    ideal = models.BooleanField()