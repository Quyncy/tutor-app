from django.shortcuts import render

# Create your views here.
def index(request):
    context={'leer': 0}
    return render(request, 'user/index.html', context)