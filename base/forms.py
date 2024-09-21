from django import forms
from django.contrib.auth import authenticate
class LoginForm(forms.Form):
    username = forms.CharField(label="帳號",max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入帳號'}))
    password = forms.CharField(label="密碼", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '請輸入密碼'}))
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("帳號或密碼錯誤")
            self.cleaned_data['user'] = user

        return cleaned_data