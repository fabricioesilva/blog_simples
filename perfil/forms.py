from django import forms
from . import models
from django.contrib.auth.models import User


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ['usuario']


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirme sua senha'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 
                 'password2', 'email')
    
    def clean(self, *args, **kwargs):
        cleaned = self.cleaned_data
        validation_error_msg = {}
        
        usuario_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        usuario_db = User.objects.filter(username=usuario_data).first()
        user_do_email_db = User.objects.filter(email=email_data).first()        

        error_msg_user_exists = 'Usuário já existe.'
        error_msg_email_exists = 'E-mail já existe.'
        error_msg_password_match = 'Senhas não conferem.'
        error_msg_password_short = 'Senha menor que 6 caracteres.'
        error_msg_required_field = 'Este campo é obrigatório.'

        if self.usuario:
            if usuario_db:
                if usuario_db != self.usuario:
                    validation_error_msg['username'] = error_msg_user_exists
            
            if user_do_email_db:
                if user_do_email_db != self.usuario:
                    validation_error_msg['email'] = error_msg_email_exists
            
            if password_data:
                if password_data != password2_data:
                    validation_error_msg['password'] = error_msg_password_match
                    validation_error_msg['password2'] = error_msg_password_match
                
                if len(password_data) < 6:
                    validation_error_msg['password'] = error_msg_password_short
                    validation_error_msg['password2'] = error_msg_password_short
        else:
            if usuario_db:
                validation_error_msg['username'] = error_msg_user_exists
            
            if user_do_email_db:
                validation_error_msg['email'] = error_msg_email_exists
            
            if not password_data:
                validation_error_msg['password'] = error_msg_required_field
            
            if not password2_data:
                validation_error_msg['password2'] = error_msg_required_field

            if password_data != password2_data:
                validation_error_msg['password'] = error_msg_password_match
                validation_error_msg['password2'] = error_msg_password_match
            
            if len(password_data) < 6:
                validation_error_msg['password'] = error_msg_password_short
                validation_error_msg['password2'] = error_msg_password_short

        if validation_error_msg:
            raise forms.ValidationError(validation_error_msg)
