from django import forms
from shop.models import MaintenanceScheduleItem, Machine, Shop


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


class MaintenanceScheduleItemForm(forms.ModelForm):

    machine = NameChoiceField(
        queryset=Machine.objects.none(),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'autofocus': True,
        }),
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


class MachineMaintenanceScheduleItemForm(forms.ModelForm):
    def __init__(self, *args, machine=None, **kwargs):
        super().__init__(*args, **kwargs)
        if machine is not None:
            self.fields['machine'].initial = machine
            self.instance.machine = machine

    class Meta:
        model = MaintenanceScheduleItem
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
