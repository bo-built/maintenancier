from django import forms
from shop.models import MaintenanceTask, Machine, Shop


class NameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = [
            'name',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-select',
                'autocomplete': 'off',
            }),
        }


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = [
            'name',
        ]

        labels = {
            'name': 'Machine Name',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-select',
                'autocomplete': 'off',
                'placeholder': 'Machine name ...',
            }),
        }


class MachineMaintenanceTaskForm(forms.ModelForm):
    def __init__(self, *args, machine=None, **kwargs):
        super().__init__(*args, **kwargs)
        if machine is not None:
            self.fields['machine'].initial = machine
            self.instance.machine = machine

    class Meta:
        model = MaintenanceTask
        fields = [
            'name',
            'interval',
            'description',
            'start_date',
            'machine',
        ]
        widgets = {
            'machine': forms.HiddenInput(attrs={}),
            'name': forms.TextInput(attrs={
                'class': 'form-select',
                'autocomplete': 'off',
                'placeholder': 'The name of this task ...'
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


class MachineMaintenanceTaskEditForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
            'x-model': 'draft.name',
        })
    )

    interval = forms.ChoiceField(
        choices=MaintenanceTask.INTERVAL_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'autocomplete': 'off',
            'x-model': 'draft.interval',
        })
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-select',
            'autocomplete': 'off',
            'x-model': 'draft.description',
        })
    )

    next_due_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',  # Renders native browser date picker
            'x-model': 'draft.next_scheduled.due_date',
        })
    )
