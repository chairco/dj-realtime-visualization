#films/forms.py
from django import forms


class DashForm(forms.Form):  
  start = forms.DateTimeField()
  end = forms.DateTimeField()