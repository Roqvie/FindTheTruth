from django.shortcuts import render


def main_page(request):
    return render(request, 'frontend/index.html')


def person(request):
    return render(request, 'frontend/person.html')


def cat(request):
    return render(request, 'frontend/cat.html')


def about(request):
    return render(request, 'frontend/about.html')
