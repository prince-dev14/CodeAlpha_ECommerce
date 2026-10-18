from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=150)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
