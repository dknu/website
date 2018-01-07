from django import forms

class QueueForm(forms.Form):
    name = forms.CharField(max_length=128, required=True)
    description = forms.CharField(required=False)
    include_file = forms.BooleanField(required=False)
    include_description = forms.BooleanField(required=False)

    time_start = forms.TimeField(required=True)
    time_end = forms.TimeField(required=True)

    hidden = forms.BooleanField(required=False)

class QueueObjectForm(forms.Form):
    description = forms.CharField(required=False, max_length=64)
    file = forms.FileField(required=False)

    # Start- og sluttidspunkt
    date = forms.DateField(required=True)
    start_h = forms.CharField(required=True)
    start_m = forms.CharField(required=True)
    end_h = forms.CharField(required=True)
    end_m = forms.CharField(required=True)


