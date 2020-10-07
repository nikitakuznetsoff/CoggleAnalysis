from django import forms


class TaskForm(forms.Form):
    title = forms.CharField(max_length=80)
    about = forms.CharField(widget=forms.Textarea)
    file_table = forms.FileField()
    service = forms.CharField()

    # correct_work = forms.URLField()
    text_keys = forms.CharField()
    correct_work = forms.URLField(required=False)
    # keys = forms.CharField(required=False)

    table_name = forms.CharField(required=False)
    names_column = forms.CharField(required=False)
    links_column = forms.CharField(required=False)
    start_row = forms.CharField(required=False)
