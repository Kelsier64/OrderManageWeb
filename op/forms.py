from django import forms
from base.models import Product,ExtendedUser
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User

class ProductForm(forms.Form):
    input_notes = forms.CharField(required=False, widget=forms.TextInput)
    quantity = forms.IntegerField(initial=0, min_value=0,required=False)
    


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["platform","product_name","release_date","suggested_price","notes",]
        labels = {
            'release_date': '發佈日期',
            'platform': '平台',
            'product_name': '產品名稱',
            'suggested_price': '建議價格',
            'notes': '備註',
        }
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'platform': forms.TextInput(attrs={'placeholder': '輸入平台','class': 'form-control'}),
            'product_name': forms.TextInput(attrs={'placeholder': '輸入產品名稱','class': 'form-control'}),
            'suggested_price': forms.NumberInput(attrs={'step': '1','class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'cols': 40,'class': 'form-control'}),
        }
    def clean_suggested_price(self):
        price = self.cleaned_data.get('suggested_price')
        if price is not None:
            if price <= 0:
                raise ValidationError('建議價格必須大於 0')
        return price

    # def clean_release_date(self):
    #     release_date = self.cleaned_data.get('release_date')
    #     if release_date is not None:
    #         if release_date < date.today():
    #             raise ValidationError('發佈日期不能是過去的日期')
    #     return release_date

    def clean(self):
        cleaned_data = super().clean()
        # 可以在這裡添加其他全局的驗證邏輯
        return cleaned_data
    
    
class RegistrationForm(forms.ModelForm):
    userName = forms.CharField(max_length=150, required=True, label='帳號', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入帳號'}))
    password = forms.CharField(required=True, label='密碼', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入密碼'}))
    class Meta:
        model = ExtendedUser
        fields = ['user_class', 'name']
        labels = {
            'user_class': '用戶類別',
            'name': '用戶名',
        }
        widgets = {
            'user_class': forms.TextInput(attrs={'placeholder': '輸入用戶類別','class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': '輸入用戶名','class': 'form-control'}),
        }
    def clean_userName(self):
        userName = self.cleaned_data.get('userName')
        if User.objects.filter(username=userName).exists():
            raise forms.ValidationError('用戶名已經存在')
        return userName

    def save(self, commit=True):
        user = User.objects.create_user(username=self.cleaned_data['userName'], password=self.cleaned_data['password'])
        extended_user = ExtendedUser(user=user, user_class=self.cleaned_data['user_class'], name=self.cleaned_data['name'])
        if commit:
            extended_user.save()
        return extended_user
    
    
    
class UserEditForm(forms.ModelForm):
    userId = forms.IntegerField(widget=forms.HiddenInput)
    userName = forms.CharField(max_length=150, required=True, label='帳號', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入帳號'}))
    password = forms.CharField(required=True, label='密碼', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入密碼'}))
    class Meta:
        model = ExtendedUser
        fields = ['user_class', 'name']
        labels = {
            'user_class': '用戶類別',
            'name': '用戶名',
        }
        widgets = {
            'user_class': forms.TextInput(attrs={'class': 'form-control','placeholder': '輸入用戶類別'}),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': '輸入用戶名'}),
        }
    def clean_userName(self):
        userId = self.cleaned_data.get('userId')
        userName = self.cleaned_data.get('userName')
        if User.objects.filter(username=userName).exclude(id=userId).exists():
            raise forms.ValidationError('用戶名已經存在')
        return userName

    def save(self, commit=True):
        user = User.objects.get(id=self.cleaned_data['userId'])
        user.username = self.cleaned_data['userName']
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        extended_user = ExtendedUser.objects.get(user=user)
        extended_user.user_class = self.cleaned_data['user_class']
        extended_user.name = self.cleaned_data['name']
        if commit:
            extended_user.save()
        return extended_user

class EditProductForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = Product
        fields = ["platform","product_name","release_date","suggested_price","notes",]
        labels = {
            'release_date': '發佈日期',
            'platform': '平台',
            'product_name': '產品名稱',
            'suggested_price': '建議價格',
            'notes': '備註',
        }
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'platform': forms.TextInput(attrs={'placeholder': '輸入平台','class': 'form-control'}),
            'product_name': forms.TextInput(attrs={'placeholder': '輸入產品名稱','class': 'form-control'}),
            'suggested_price': forms.NumberInput(attrs={'step': '1','class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'cols': 40,'class': 'form-control'}),
        }
    def clean_suggested_price(self):
        price = self.cleaned_data.get('suggested_price')
        if price is not None:
            if price <= 0:
                raise ValidationError('建議價格必須大於 0')
        return price
    
    def save(self, commit=True):
        product = Product.objects.get(id=self.cleaned_data['id'])
        product.platform = self.cleaned_data['platform']
        product.product_name = self.cleaned_data['product_name']
        product.release_date = self.cleaned_data['release_date']
        product.suggested_price = self.cleaned_data['suggested_price']
        product.notes = self.cleaned_data['notes']
        if commit:
            product.save()
        return product