from django.urls import path,re_path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('pdf/', views.some_view, name='pdf'),
    #path('plot/', views.get_image, name='plot'),
    re_path(r'plot/(.*)?', views.get_image, name='plot'),
    path(r'plotter/', views.get_plot, name='plotter'),

    path('question/add/', views.QuestionCreate.as_view(), name='question-add'),
    path('question/<int:pk>/', views.QuestionUpdate.as_view(), name='question-update'),
    path('question/<int:pk>/delete/', views.QuestionDelete.as_view(), name='question-delete'),

    path('name', views.get_name, name='get-name'),

    path('plot_k', views.get_k, name='get-k'),


]