from django.db import models

# Create your models here.
class SearchRecord(models.Model):
    query = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Add fields to store search results
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    volume_24h = models.DecimalField(max_digits=15, decimal_places=2)
    volume_change_24h = models.DecimalField(max_digits=10, decimal_places=2)
    circulating_supply = models.DecimalField(max_digits=20, decimal_places=2)
    total_supply = models.DecimalField(max_digits=20, decimal_places=2)
    max_supply = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    fully_diluted_market_cap = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"SearchRecord for '{self.query}'"