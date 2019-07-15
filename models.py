from django.db import models
from django.template.defaultfilters import slugify

class Capability(models.Model):
    name = models.CharField(primary_key=True, max_length=45)

    class Meta:
        verbose_name_plural = "Capabilities"

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(primary_key=True, max_length=45)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(primary_key=True, max_length=45)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    slug = models.SlugField(unique=True, default="")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Location, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Sector(models.Model):
    name = models.CharField(primary_key=True, max_length=45)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=45)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT)
    slug = models.SlugField(unique=True, default="")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Budget(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    jan = models.IntegerField(default=None)
    feb = models.IntegerField(default=None)
    mar = models.IntegerField(default=None)
    apr = models.IntegerField(default=None)
    may = models.IntegerField(default=None)
    jun = models.IntegerField(default=None)
    jul = models.IntegerField(default=None)
    aug = models.IntegerField(default=None)
    sep = models.IntegerField(default=None)
    oct = models.IntegerField(default=None)
    nov = models.IntegerField(default=None)
    dec = models.IntegerField(default=None)
    year = models.IntegerField(default=None)
    q1 = models.IntegerField(default=None)
    q2 = models.IntegerField(default=None)
    q3 = models.IntegerField(default=None)
    q4 = models.IntegerField(default=None)

    def save(self, *args, **kwargs):
        self.q1 = (self.jan + self.feb + self.mar)
        self.q2 = (self.apr + self.may + self.jun)
        self.q3 = (self.jul + self.aug + self.sep)
        self.q4 = (self.oct + self.nov + self.dec)
        super(Budget, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.location) + ", " + str(self.customer) + " " + str(self.year)

class Sale(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    capability = models.ForeignKey(Capability, on_delete=models.PROTECT)
    date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.customer) + ", " + str(self.location) + ", " + str(self.date)