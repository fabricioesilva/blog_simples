from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


class Categoria(View):
    def get(self, *args, **kwargs):
        return HttpResponse('categoria')




