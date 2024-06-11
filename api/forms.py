from django import forms
from .models import SearchRecord

class CryptoSearchForm(forms.Form):
    query = forms.CharField(label='Enter cryptocurrency name or symbol', max_length=100)


class UserDataForm(forms.ModelForm):
    class Meta:
        model = SearchRecord
        fields = ['name', 'symbol','price','volume_24h','volume_change_24h','circulating_supply','total_supply','max_supply','fully_diluted_market_cap']