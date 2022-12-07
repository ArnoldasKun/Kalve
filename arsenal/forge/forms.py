from django import forms
from django.utils.timezone import datetime, timedelta
from . models import ArmorReview

class ArmorReviewForm(forms.ModelForm):
    def is_valid(self) -> bool:
        valid = super().is_valid()
        if valid:
            client = self.cleaned_data.get("client")
            recent_posts = ArmorReview.objects.filter(
                client=client, 
                created_at__gte=(datetime.utcnow()-timedelta(hours=1))
            )
            if recent_posts:
                return False
        return valid

    class Meta:
        model = ArmorReview
        fields = ('content', 'armor', 'client', )
        widgets = {
            'armor': forms.HiddenInput(),
            'client': forms.HiddenInput(),
        }