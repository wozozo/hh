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

    # Unit of `limit` is MB (default 12MB)
    def __init__(self, limit=12, *args, **kwargs):
        self.limit = 1000 * 1024 * limit
        from .s3 import S3
        self.s3 = S3()
        super(UploadForm, self).__init__(*args, **kwargs)

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo.size > self.limit:
            raise forms.ValidationError('写真のサイズは %sMB までです。' % self.limit)
        return self.cleaned_data['photo']
