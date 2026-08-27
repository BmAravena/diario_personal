from django.shortcuts import render


def home(request):
	return render(request, 'diario_personal/home.html')
