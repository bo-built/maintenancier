from django import forms
from shop.models import MaintenanceScheduleItem, Machine


class NameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class MaintenanceScheduleItemForm(forms.ModelForm):

    machine = NameChoiceField(
        queryset=Machine.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        empty_label='General Shop',
    )

    class Meta:
        model = MaintenanceScheduleItem
        fields = [
            'machine',
            'name',
            'interval',
            'description',
            'start_date',
        ]
        widgets = {
            'machine': forms.Select(attrs={
                'class': 'form-select',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-select',
                'autocomplete': 'off',
            }),
            'interval': forms.Select(attrs={
                'class': 'form-select',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-select',
                'autocomplete': 'off',
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',  # Renders native browser date picker
            }),
        }

    def __init__(self, *args, **kwargs):
        shop = kwargs.pop('shop', None)
        super().__init__(*args, **kwargs)

        self.fields['name'].required = True
        self.fields['start_date'].required = True
        self.fields['interval'].required = True
        self.fields['machine'].required = False
        self.fields['description'].required = False

        if shop is not None:
            self.fields['machine'].queryset = Machine.objects.filter(shop=shop)
