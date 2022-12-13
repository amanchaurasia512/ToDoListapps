from django.shortcuts import render , redirect
from django.views.generic.list import ListView
from django.views.generic import CreateView ,UpdateView , DeleteView 
from .models import Task
from .form import Newuserform
from django.views.generic import FormView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView 
from django.urls import reverse_lazy   
from django.contrib.auth.mixins import LoginRequiredMixin



class Registerpage(FormView):
    template_name = 'ToDolistapp/register.html'
    form_class = Newuserform
    def form_valid(self, form): 
        user = form.save()
        if user is None:
            login(self.request , user)
        return super(Registerpage , self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('task')
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(Registerpage,self).get( *args, **kwargs)

class customlogin(LoginView):
    template_name = 'ToDolistapp/login.html'
    
    def get_success_url(self):
        return reverse_lazy('task')



class TaskList( LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'List'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    


class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    template_name = "ToDolistapp/TaskCreateView.html"
    success_url = reverse_lazy('task')
    fields = ['AddTask','Priority' ,'completed']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView,self).form_valid(form)
    
class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['AddTask','Priority' ,'completed']
    template_name = "ToDolistapp/taskupdate.html"
    success_url = reverse_lazy('task')
 
class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'List'
    success_url = reverse_lazy('task')

   
