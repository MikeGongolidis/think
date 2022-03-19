from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .models import Question,Answer
from django.shortcuts import render
from django.contrib.auth.models import User
from think.forms import AnswerForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages


import random

# Create your views here.

class HomeView(LoginRequiredMixin,TemplateView):
    template_name = "home.html"
    form_class = AnswerForm
    success_url = ''
    
    def get_random_question(self,username):
        """
        Goal: Get randomly one question that the user has not answered 
        Logic: 
            1. Get all the question ids
            2. Get our user
            3. Get all the answers of a specific user
            4. Find the questions that the users have not answered by comparing the question ids with 1
            5. If there are unanswered questions, pick one randomly and return it.
            6. Otherwise return a message that the user has no other questions left.
        """
        questions = Question.objects.all()
        questions2 = Question.objects.all().values('question_id')
        user = User.objects.get(username=username)
        answers = Answer.objects.filter(user=user).values('question_id')
        #answered_questions = Question.objects.get(question_id=answers)
        ff = list(questions2.difference(answers).iterator())
        # If there are questions available to show
        if len(ff) > 0:
            one = random.choice(ff)
            ask_him_question = Question.objects.get(question_id=one['question_id'])
        else:
            one = 'empty'
            ask_him_question = {}
            ask_him_question['question_text'] = 'empty'

        return ask_him_question

    def get(self, request, *args, **kwargs):

        username = request.user.get_username()

        ask_him_question = self.get_random_question(username)

        #our_questions =  Question.objects.all().exclude(question_id=answers.values('question'))
        return render(request, self.template_name, {'qq': ask_him_question, 'form': self.form_class, "form_success": None }) 
    
    def post(self, request, *args, **kwargs):
        
        username = User.objects.get(username=request.user)
        data = request.POST
        dic = {}
        for key in data:
           dic[key] = data[key]
        
        answer = dic['answer']
        question_id = dic["question_id"]
        question = Question.objects.get(question_id=question_id)
        
        answer = Answer(
            user = username,
            question_id=question,
            answer_text = answer
        )
        answer.save()

        ask_him_question = self.get_random_question(username)

        return render(request, self.template_name, {'qq': ask_him_question, 'form':self.form_class, "form_success": 1 }) 


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        data = {'form_login': AuthenticationForm(), 'form_signup': UserCreationForm()}
        return render(request, self.template_name, data) 

    def post(self, request, *args, **kwargs):
        if request.POST.get('form_type') == 'login':
            #login_form = AuthenticationForm(request.POST) # What does it do?

            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('home'))
            else:
                data = {
                    'form_login': AuthenticationForm(),
                    'form_signup': UserCreationForm(),
                    "message": 'Invalid login credentials'
                }
                return render(request, self.template_name, data) 

        elif request.POST.get('form_type') == 'signup':
            signup_form = UserCreationForm(request.POST) #what does this do?

            if signup_form.is_valid():
                signup_form.save()
                username = signup_form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')
                data = {
                    'form_login': AuthenticationForm(),
                    'form_signup': UserCreationForm(),
                    "message": 'Successfully created user'
                }
                return render(request, self.template_name, data) 
            else:
                data = {
                    'form_login': AuthenticationForm(),
                    'form_signup': UserCreationForm(),
                    "message": 'Invalid signup credentials'
                }
                return render(request, self.template_name, data) 
