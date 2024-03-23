from django.db import models

# Create your models here.
class Expense(models.Model):
    name= models.CharField(max_length=100,default='unknown')
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # New column added
    login_name = models.CharField(max_length=100,default='unknown')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
class Userdb(models.Model):
    name= models.CharField(max_length=100,default='unknown')
    user_name = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)
    g_email = models.CharField(max_length=100,default='unknown')
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # New column added

    def __str__(self):
        return self.user_name
