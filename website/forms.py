from django import forms


class ImportStudentForm(forms.Form):
    file = forms.FileField()
