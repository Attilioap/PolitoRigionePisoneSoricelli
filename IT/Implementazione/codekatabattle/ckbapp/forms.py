from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Tournament

class SignupForm(forms.Form):
    firstName = forms.CharField(max_length=255, required=True)
    lastName = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    username = forms.CharField(max_length=255, required=True)
    is_educator = forms.BooleanField(required=False)

class TournamentAdminForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = '__all__'
        widgets = {
            'educators': FilteredSelectMultiple('Educators', is_stacked=False),
            'students': FilteredSelectMultiple('Students', is_stacked=False),
        }


class PermissionGrantForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True)

class EvaluationForm(forms.Form):
    def __init__(self, battle, *args, **kwargs):
        super(EvaluationForm, self).__init__(*args, **kwargs)

        # Get teams enrolled in the battle
        teams_in_battle = battle.teams.all()

        # Add a score field for each team in the battle
        for team in teams_in_battle:
            field_name = f'team_{team.id}_score'
            self.fields[field_name] = forms.IntegerField(
                label=f'{team.name} Score',
                min_value=0,
                max_value=100
            )