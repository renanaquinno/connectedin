# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class RegistrarUsuarioForm(forms.Form):
	nome = forms.CharField(required=True)
	email = forms.EmailField(required=True)	
	senha = forms.CharField(required=True)
	telefone = forms.CharField(required=True)
	nome_empresa = forms.CharField(required=True)

	def is_valid(self): 
		valid = True

		if not super(RegistrarUsuarioForm, self).is_valid():
			self.adiciona_erro('Por favor, verifique os dados informados')
			valid = False

		user_exists = User.objects.filter(email=self.cleaned_data['email']).exists()

		if user_exists:
			self.adiciona_erro('Usuario já existente')
			valid = False
			
		return valid

	def adiciona_erro(self, message):
		errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		errors.append(message)

class RegistrarPostForm(forms.Form):
	title_post = forms.CharField(required=True)
	txt_post = forms.CharField(required=True)	
	def is_valid(self): 
		valid = True
		if not super(RegistrarPostForm, self).is_valid():
			self.adiciona_erro('Por favor, verifique os dados informados')
			valid = False
		return valid
