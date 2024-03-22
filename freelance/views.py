from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from freelance.models import Executor


# detailview  - принимает только одну запись из таблицы
# listview - принимает всю таблицу
# templateview -
# **kwargs - ключ-значение, не знаем сколько значений придет из базы

class MainPAgeView(TemplateView):
    template_name = 'basic/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Это главная страница проекта'
        return context

#class ExecutorListView(ListView):
    #    model = Executor
    #    tempfile_name = ('freelance/executors/executor_list.html')
#    context_object_name = 'executors'

