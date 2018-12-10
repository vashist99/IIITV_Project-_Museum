from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import View
from django.db.models import Count
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from App.forms import LoginForm, RegisterForm

from App.forms import LoginForm, RegisterForm, ProjectForm
from App.models import Project


def index(request):
    projects=Project.objects.all().order_by('-date')
    return render(request, 'index.html',{'projects':projects})

def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, './project_detail.html', {'project': project})

def leaderboard(request):
    projects = Project.objects.all().annotate(like_count=Count('likes')).order_by('-like_count')
    return render(request, 'leaderboard.html', {'projects': projects})

def liked(request, pk):
    project = Project.objects.get(pk=pk)

    try:
        user = project.likes.get(pk=request.user.id)
        if user:
            project.likes.remove(user)
    except:
        project.likes.add(request.user)

    return redirect('App:project-detail', pk=pk)

def delete(request, pk):
    Project.objects.get(pk=pk).delete()
    return redirect('App:index')

class ProjectFormView(View):
    form_class = ProjectForm
    template_name = 'form_project.html'

    # sends query and form on request
    def get(self, request):
        form = self.form_class(None)
        print(form)
        return render(request, self.template_name,
                      {'form': form})

    # authenticates user request
    def post(self, request):

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            # print(project.faculty.email)
            subject = "Invitation for being mentor"
            content = "Hey,\n" + str(project.member.username) + " has invited you to be the mentor for project" + str(project.project_name) + "!"
            from_email = project.member.email
            # to = [project.faculty.email,]
            # msg = EmailMessage(subject, content, from_email, to)
            print(subject)
            print(content)
            # msg.send()
            return redirect('/')
        else:
            messages.error(request, "Incorrect credentials")
            return render(request, self.template_name, {'form': form})



class LoginFormView(View):
    """Uses the LoginForm created in forms.py and handles 'GET' 'POST' requests
        from form_register.html """
    form_class = LoginForm
    template_name = 'form_login.html'

    # sends query and form on request
    def get(self, request):
        form = self.form_class(None)
        print(form)
        return render(request, self.template_name,
                      {'form': form})

    # authenticates user request
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect('/')
            else:
                messages.error(request, "Incorrect Credentials")
                return redirect('App:login')
        else:
            messages.error(request, "Incorrect credentials")
            return render(request, self.template_name, {'form': form})


class RegisterFormView(View):
    """Uses the RegisterForm created in forms.py and handles 'GET' 'POST' requests
        from form_register.html """
    form_class = RegisterForm
    template_name = 'form_register.html'

    # sends query and form on request
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name,
                      {'form': form})

    # stores data to database on request and authenticates the user
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            user.set_password(password)
            if password == confirm_password:
                user.save()
                messages.success(request, "Registered Successfully")
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('/')
            else:
                messages.error(request, "Incorrect credentials")
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, "Incorrect credentials")
            return render(request, self.template_name, {'form': form})


def signout(request):
    """logs out the user on request"""
    logout(request)
    return redirect('App:index')

def AboutUs(request):
    return render(request,'aboutus.html')
