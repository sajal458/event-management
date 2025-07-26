from django import forms
from Event.models import Event

class TaskModel(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Event name",
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-2 border border-gray-300 rounded-md"
        })
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            "class": "w-full px-4 py-2 border border-gray-300 rounded-md"
        })
    )
    date = forms.DateField(
    label="Event date",
    widget=forms.SelectDateWidget(attrs={
        "class": "inline-block w-auto mx-1 px-2 py-2 border border-gray-300 rounded-md"
    })
    )
    time = forms.TimeField(
        label="Event time",
        widget=forms.TimeInput(format='%H:%M', attrs={
            "placeholder":"HH-MM",
            "class": "w-full px-4 py-2 border border-gray-300 rounded-md "
        })
    )
    location = forms.CharField(
        max_length=100,
        label="Event location",
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-2 border border-gray-300 rounded-md "
        })
    )
    category = forms.ChoiceField(
        label="Category",
        widget=forms.Select(attrs={
            
            "class": "w-full px-4 py-2 border border-gray-300 rounded-md "
        })
    )
    participant = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={
            "class": "space-y-2"
        }),
        label="Participants"
    )

    def __init__(self, *args, **kwargs):
        participant = kwargs.pop("participant", [])
        category = kwargs.pop("category", [])
        super().__init__(*args, **kwargs)
        
        self.fields["participant"].choices = [(p.id, p.name) for p in participant]
        self.fields["category"].choices = [(c.id, c.name) for c in category]
