from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class PlotForm(forms.Form):
    k = forms.FloatField(label='k',widget=forms.NumberInput(attrs={'onchange': 'form.submit();'}))
    x_min = forms.FloatField(label='x_min',widget=forms.NumberInput(attrs={'onchange': 'form.submit();'}))
    x_max = forms.FloatField(label='x_max',widget=forms.NumberInput(attrs={'onchange': 'form.submit();'}))
    N = forms.IntegerField(label='N',min_value=2,widget=forms.NumberInput(attrs={'onchange': 'form.submit();'}))

