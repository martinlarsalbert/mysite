from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Choice, Question
from django.utils import timezone

import pdb

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """

        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
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

from reportlab.pdfgen import canvas
from django.http import HttpResponse

def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

# file charts.py
def simple(request):
    import random
    import django
    import datetime

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

import sys
from django.http import HttpResponse
import matplotlib as mpl
mpl.use('Agg') # Required to redirect locally
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import rand

import io

def get_image(request,value = 0.0):
   """
   This is an example script from the Matplotlib website, just to show
   a working sample >>>
   """
   N = 50
   x = np.random.rand(N)
   y = np.random.rand(N)
   colors = np.random.rand(N)
   area = np.pi * (15 * np.random.rand(N))**2 # 0 to 15 point radiuses
   plt.scatter(x, y, s=area, c=colors, alpha=0.5)
   if value is None:
       value = '0.0'
   plt.text(0,0,'%s' % value)
   """
   Now the redirect into the cStringIO or BytesIO object >>>
   """
   f = io.BytesIO()           # Python 3
   plt.savefig(f, format="png", facecolor=(0.95,0.95,0.95))
   plt.clf()
   """
   Add the contents of the StringIO or BytesIO object to the response, matching the
   mime type with the plot format (in this case, PNG) and return >>>
   """
   return HttpResponse(f.getvalue(), content_type="image/png")

def get_plot(request,k = 1.0):
   """
   This is an example script from the Matplotlib website, just to show
   a working sample >>>
   """

   if request.method == 'POST':
       # create a form instance and populate it with data from the request:
       k = float(request.POST['k'])

   x = np.linspace(0,1,100)
   y = x**(k)

   fig,ax = plt.subplots()
   ax.plot(x,y,'b-')
   ax.set_title('y = x^%0.2f' % k)

   """
   Now the redirect into the cStringIO or BytesIO object >>>
   """
   f = io.BytesIO()           # Python 3
   fig.savefig(f, format="png", facecolor=(0.95,0.95,0.95))
   plt.clf()
   """
   Add the contents of the StringIO or BytesIO object to the response, matching the
   mime type with the plot format (in this case, PNG) and return >>>
   """
   return HttpResponse(f.getvalue(), content_type="image/png")

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class QuestionCreate(CreateView):
    model = Question
    fields = ['question_text']

class QuestionUpdate(UpdateView):
    model = Question
    fields = ['question_text']

class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('author-list')

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import NameForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'polls/name.html', {'form': form})

from .forms import PlotForm
def get_k(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlotForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlotForm()

    return render(request, 'polls/plot_k.html', {'form': form})

def welcome(request):

    return render(request, 'polls/welcome.html')