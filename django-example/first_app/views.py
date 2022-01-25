from django.shortcuts import render

def first_view(request):
    render (request, '', {
        'foo': 'bar'
    })