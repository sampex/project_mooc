from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.views import generic


from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#@login_required FIX for insecure design
# Csrf flaw
@csrf_exempt
# changing csrf_exempt to csrf_protect enables csrf protection
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Insecure Design: Lack of Authentication and Authorization Checks
    # Allow users to vote without proper authentication and authorization
    # This allows unauthorized users to manipulate the voting process
    # Implement proper authentication and authorization checks to prevent this

    try:
        # Broken access control flaw
        choice_id = request.POST.get('choice', None)
        if choice_id is None:
            raise Choice.DoesNotExist
        selected_choice = question.choice_set.get(pk=choice_id)
        #fix to it
        #selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
