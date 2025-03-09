from django import forms

from brand.models import Brand
from championship.models import Championship
from manager_game.models import PPVEvent
from matches.models import Match
from wrestler.models import Wrestler


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['match_type', 'participants', 'day_number', 'brand', 'ppv_event', 'championship']

    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game')
        super().__init__(*args, **kwargs)
        self.fields['participants'].queryset = Wrestler.objects.filter(game=game)
        self.fields['brand'].queryset = Brand.objects.filter(game=game)
        self.fields['ppv_event'].queryset = PPVEvent.objects.filter(game=game)
        self.fields['championship'].queryset = Championship.objects.filter(game=game)
        self.fields['brand'].required = False
        self.fields['ppv_event'].required = False
        self.fields['championship'].required = False

    def clean(self):
        cleaned_data = super().clean()
        participants = cleaned_data.get('participants')
        match_type = cleaned_data.get('match_type')
        day_number = cleaned_data.get('day_number')

        if participants:
            participant_count = len(participants)
            required_participants = Match().get_required_participants(match_type)
            if participant_count != required_participants:
                raise forms.ValidationError(
                    f"A {match_type} must have exactly {required_participants} participants."
                )
        if day_number is not None and day_number < 0:
            raise forms.ValidationError("Day number cannot be negative.")