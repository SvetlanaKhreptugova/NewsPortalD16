from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm
from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'category', 'text']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")

        text = cleaned_data.get('text')
        if text == title:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
