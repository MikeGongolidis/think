from django import forms


class AnswerForm(forms.Form):
    answer = forms.CharField(label='Your answer', max_length=300,widget = forms.Textarea)
