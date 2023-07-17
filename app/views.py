from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View


### index
class IndexMain(View):
    def get(self, request):
        return render(request, 'index.html')