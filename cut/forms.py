from django import forms
from django.forms import widgets

class userurl(forms.Form):
    address = forms.CharField(label='' , widget= forms.TextInput(attrs={'class':'addressbar' , 'id' : 'bar'}))