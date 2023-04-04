from django.forms import ModelForm
from .models import WatchCoin

class WatchlistForm(ModelForm):

    class Meta:
        model = WatchCoin
        fields = ['coin']