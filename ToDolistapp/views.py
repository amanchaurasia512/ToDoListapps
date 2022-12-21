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
    redirect_authenticated_user = False
    success_url = reverse_lazy('task')
    # def get_success_url(self):
    #     return reverse_lazy('task')
    
    def form_valid(self, form): 
        user = form.save()
        if user is not None:
            login(self.request , user)
        return super(Registerpage , self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(Registerpage,self).get( *args, **kwargs)
    
   

class customlogin(LoginView):
    template_name = 'ToDolistapp/login.html'
    redirect_authenticated_user = False
    
    def get_success_url(self):
        return reverse_lazy('task')



class TaskList( LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'List'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['List'] = context['List'].filter(User=self.request.user)
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

#password_reset_mail
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "ToDolistapp/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'aman.1si17cs008@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="ToDolistapp/password_reset.html", context={"password_reset_form":password_reset_form})
