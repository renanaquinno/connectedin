# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from django.views.generic.base import View
from usuarios.forms import *
from django.contrib.auth.models import User
from perfis.models import *
from django.shortcuts import redirect

# Create your views here.

class RegistrarUsuarioView(View):

	def get(self, request):
		return render(request, 'registrar.html')

	def post(self, request):
		form = RegistrarUsuarioForm(request.POST)

		if (form.is_valid()) :
			dados = form.cleaned_data

			usuario = User.objects.create_user(dados['nome'],
						   dados['email'],
						   dados['senha'])

			perfil = Perfil(nome = usuario.username, 
							nome_empresa = dados['nome_empresa'],
							telefone = dados['telefone'],
							usuario = usuario)
			perfil.save()
			return redirect('index')
		
		return render(request, 'registrar.html', {'form': form})

		
class RegistrarPostView(View):
	def post(self, request):
		form = RegistrarPostForm(request.POST)

		if (form.is_valid()) :
			dados = form.cleaned_data
			perfil = Perfil.objects.get(usuario=self.request.user)
			post = Postagem(title_post = dados['title_post'],txt_post = dados['txt_post'], perfil= perfil)
			post.save()
			return redirect('index')
		
		return render(request, 'postagem.html', {'form': form})
