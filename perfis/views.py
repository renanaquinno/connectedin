from django.shortcuts import render
from perfis.models import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
	return render(request, 'index.html',{'perfis' : Perfil.objects.all(),
										 'perfil_logado' : get_perfil_logado(request)})
@login_required
def exibir_perfil(request, perfil_id):

	#perfil = get(perfil_id)
	perfil = Perfil.objects.get(id=perfil_id)

	return render(request, 'perfil.html',
		          {'perfil' : perfil, 
				   'perfil_logado' : get_perfil_logado(request)})





@login_required
def convidar(request,perfil_id):

	perfil_a_convidar = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	
	if(perfil_logado.pode_convidar(perfil_a_convidar)):
		perfil_logado.convidar(perfil_a_convidar)
	
	return  redirect('index')

def get_perfil_logado(request):
	return request.user.perfil

@login_required
def aceitar(request, convite_id): 
	convite = Convite.objects.get(id = convite_id)
	convite.aceitar()
	return redirect('index')

@login_required
def recusar(request, convite_id): 
	convite = Convite.objects.get(id = convite_id)
	convite.recusar()
	return redirect('index')

@login_required
def desfazer(request, perfil_id):
	perfil = Perfil.objects.get(id=perfil_id)
	perfil.desfazer(get_perfil_logado(request))
	return redirect('index')

@login_required
def nova_postagem(request, perfil_id):
	perfil = Perfil.objects.get(id=perfil_id)

	return render(request, 'postagem.html',
		          {'perfil' : perfil, 
				   'perfil_logado' : get_perfil_logado(request)})



@login_required
def minhas_postagens(request, perfil_id):
	perfil = Perfil.objects.get(id=perfil_id)

	return render(request, 'time_line.html',
		          {'posts' : Postagem.objects.filter(perfil__usuario=request.user).order_by('-dt_publicacao'),
				   'perfil' : perfil, 
				   'perfil_logado' : get_perfil_logado(request)})


@login_required
def postagens_amigos(request, perfil_id):
	nome_autor = []
	contato = []
	usuario = []
	postagens_amigos = []

	perfil = Perfil.objects.get(id=perfil_id)
	posts = Postagem.objects.all().order_by('-dt_publicacao')

	for post in posts:
		nome_autor += [post.perfil.id]

	contatos = list(perfil.contatos.all())
	for i in contatos:
		contato += [i.id]

	matchItem = [x for x in contato if x in nome_autor]

	for i in range (0, len(matchItem)):
		usuario = matchItem[i]
		postagens_amigos += posts.filter(perfil_id=usuario)

	return render(request, 'time_line.html',{'posts':postagens_amigos})
				   