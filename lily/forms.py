# coding: utf-8

from django import forms


class UserForm(forms.Form):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)


class UserModelForm(forms.ModelForm):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserModelForm, self).__init__(*args, **kwargs)


class UploadForm(forms.Form):
    photo = forms.ImageField()

    def __init__(self, *args, **kwargs):
        from .s3 import S3
        self.s3 = S3()
        super(UploadForm, self).__init__(*args, **kwargs)

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        limit = 1000 * 1024 * 12 # 12MB
        if photo.size > limit:
            raise forms.ValidationError(u'写真のサイズは10MBまでです。')
        return self.cleaned_data['photo']
