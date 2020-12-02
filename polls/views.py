from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

import requests
import json

from .models import Answer, Question


def index(request):
    question = Question.objects
    context = {'question': question}
    return render(request, 'polls/index.html', context)

def detail(request):
    question = get_object_or_404(Question)
    return render(request, 'polls/detail.html', {'question': question})



def results(request, answer_id):

    answer = get_object_or_404(Answer, pk=answer_id)
    composition_dic = eval(answer.answer_composition)

    if not answer.atom_set.all(): # Avoid reprinting on page refresh
        for key,value in composition_dic.items():
            answer.atom_set.create(atom_text=key, atom_number=value)

    return render(request, 'polls/results.html', {'answer': answer})

def vote(request):
    question = get_object_or_404(Question)

    try:
        selected_molecule = request.POST['molecule']
    except KeyError:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "No molecule has been found, please enter a valid one.",
        })

    else:
        url = 'https://dwptzvjyoj.execute-api.us-east-1.amazonaws.com/dev/main'
        x = requests.post(url, data=selected_molecule)
        try:
            result = json.loads(x.text)['result']
        except:
            error_message = json.loads(x.text)
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': error_message,
            })

        else:
            a = Answer(answer_text=selected_molecule, answer_composition=repr(result))
            a.save()
            # We return an HttpResponseRedirect after successfully dealing
            # with POST data to prevent data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(a.id,)))
