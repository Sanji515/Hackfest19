from django import forms
from django.contrib.auth import authenticate, login
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
# from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator


class YourSignupForm(UserCreationForm):
    # email = forms.EmailField(max_length=200)
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    mobile_no = forms.IntegerField(validators=[MaxValueValidator(9999999999)])

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'username', 'country', 'mobile_no', 'password1','password2')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['firstname', 'lastname', 'username', 'country', 'mobile_no', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs['class'] = 'input'
        
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None



# class ProfileForm(forms.Form):
#     class Meta:
#         model = Profile
#         fields = ('firstname', 'lastname', 'phone_number')


class YourLoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super(YourLoginForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password']:
            self.fields[fieldname].widget.attrs['class'] = 'input'

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user or not user.is_active:
                raise forms.ValidationError("Sorry, that login was invalid. Please try again.")

        return super(YourLoginForm, self).clean(*args, **kwargs)

        # self.fields['password'].widget = forms.PasswordInput()
        # self.fields['username'] = forms.CharField(label='')
        # self.fields['password'] = forms.PasswordInput(label='')

        # You don't want the `remember` field?
        # if 'remember' in self.fields.keys():
        #     del self.fields['remember']

        # helper = FormHelper()
        # helper.form_show_labels = False

        # helper.layout = Layout(
        #     Field('login', placeholder = 'Email address'),
        #     Field('password', placeholder = 'Password'),
        #     FormActions(
        #         Submit('submit', 'Log me in to Cornell Forum', css_class = 'btn-primary')
        #     ),
        # )
        # self.helper = helper
