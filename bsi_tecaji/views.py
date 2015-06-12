
from django.http import JsonResponse

from .forms import TecajForm
from .models import Tecaj

def get_tecaj(request):
    resp = {'status': 'fail'}

    form = TecajForm(request.GET)
    if form.is_valid():
        tecaji = list(Tecaj.objects.filter(**form.cleaned_data).values('tecaj', 'sifra', 'oznaka'))
        resp['lookup'] = form.cleaned_data
        resp['tecaji'] = tecaji
        resp['status'] = 'ok'

    return JsonResponse(resp)

