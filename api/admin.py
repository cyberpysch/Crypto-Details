from django.contrib import admin
from .models import SearchRecord
# Register your models here.

@admin.register(SearchRecord)
class SearchRecordAdmin(admin.ModelAdmin):
    list_display = ('query', 'timestamp', 'name', 'symbol', 'price', 'volume_24h', 'volume_change_24h', 'circulating_supply', 'total_supply', 'max_supply', 'fully_diluted_market_cap')
    search_fields = ('query', 'name', 'symbol')
    list_filter = ('timestamp',)
