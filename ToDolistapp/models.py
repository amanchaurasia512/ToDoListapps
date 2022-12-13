from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Task(models.Model):
    HIGHPRIORITY ='HP'
    MIDPRIORITY  = 'MP'
    LOWPRRIORITY = 'LP'
    Priority_choice =[
           (HIGHPRIORITY ,'High Priority'),
           (MIDPRIORITY  , 'Mid Priority'),
           (LOWPRRIORITY , 'Low Priority')
    ]
    User= models.ForeignKey(User,on_delete=models.CASCADE ,blank=True,null=True)
    AddTask=models.CharField(max_length=50,blank=True,null=True)
    Priority=models.CharField(
        max_length=2,
        choices=Priority_choice,
        default=HIGHPRIORITY    
    )
    completed = models.BooleanField(default= False)
    created = models.DateTimeField(auto_now_add=True )   
    
    def __str__(self):
        return f'{self.AddTask} --------------{self.Priority}----------- {self.completed}'
    
    class Meta:
       ordering = ['completed']
    
        