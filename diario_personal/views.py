from django.shortcuts import render


def home(request):
	return render(request, 'diario_personal/home.html')


def not_found(request, exception):
	return render(request, 'diario_personal/not_found.html', status=404)
