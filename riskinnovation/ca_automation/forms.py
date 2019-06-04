from django import forms

class CAAutomation(forms.Form):
    mapping_file = forms.FileField()
    system_dump = forms.FileField()
    documents = forms.FileField()