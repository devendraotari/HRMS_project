from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import get_template
# from django.contrib.auth.models import
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, EmployeeForm, LeaveConfForm, EmpNotifyForm, LoginForm, CustomUserLoginForm
from .models import Employee, Leave, Notify, Emails, Compose, ViewMail, ContactsDetails
from django.template import Context
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            htmly = get_template('Email.html')
            d = {'username': username}
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text / html")
            # msg.send()

            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'title': 'reqister here'})

# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             form = login(request, user)
#             messages.success(request, f' welcome {username} !!')
#             return redirect('home')
#         else:
#             messages.info(request, f'account done not exit plz sign in')
#     form = AuthenticationForm()
#     return render(request, 'login_two_columns.html', {'form': form, 'title': 'log in'})

@csrf_exempt
def login_view(request):
    print("redirecting to home page")
    if request.method == 'POST':
        print("in post method")
        print(request.POST)
        form = CustomUserLoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(email=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        if form.is_valid():
            print("in form is_valid()")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            print("user authentication done")
            if user is not None:
                login(request, user)
                messages.success(request, f' welcome {user.username} !!')
                print("redirecting to home page")
                return redirect('home')
            else:
                print("user not found")
                messages.info(request, f' {user.username} does not exists !!')
                return redirect('login')
        else:
            print("form invalid ")
            messages.info(request, f'account does not exit plz sign in')
            return redirect('login')
    else:
        print("get method")
        form = CustomUserLoginForm()
        return render(request, 'login_two_columns.html', {'form': form, 'title': 'log in'})



def forgot_password(request):
    return render(request, 'forgot_password.html')


def home(request):
    emp = User.objects.all()
    print("HOME_________000000--------")
    return render(request, 'index.html', {'emp': emp})


def add_employee(request):
    emp = Employee.objects.all()
    # return render(request, 'addemployee.html',{'emp':emp})
    context = {}
    form = EmployeeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    context['emp'] = emp
    context['form'] = form
    return render(request, 'addemployee.html', context)


def add_categories(request):
    if request.method == "GET":
        form = EmployeeForm()
        return render(request, 'addemployee.html', {"form": form})
    else:
        # save code
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                pass
        return redirect(add_employee)


def delete(request, pk):
    d = Employee.objects.filter(id=pk)
    d.delete()
    return redirect(add_employee)


# def edit(request, id):
#     if (request.method == "GET"):
#         d = Employee.objects.get(id=id)
#         return render(request, 'edit.html', {'emp': d})
#
#     elif (request.method == "POST"):
#         id = request.POST.get("id")
#         d = Employee.objects.get(id=id)
#         form = CategoryForm(request.POST, instance=d)
#         if form.is_valid():
#             form.save()
#         return redirect(add_employee)


def apply_leave(request):
    emp = Leave.objects.all()
    # return render(request, 'application leave.html',{'emp':emp})
    context = {}
    form = LeaveConfForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    context['emp'] = emp
    context['form'] = form
    return render(request, 'application leave.html', context)


def add_leave(request):
    if request.method == "GET":
        form = LeaveConfForm()
        return render(request, 'application leave.html', {"form": form})
    else:
        # save code
        form = LeaveConfForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                pass
        return redirect(apply_leave)


def mailbox(request):
    emp = Emails.objects.all()
    return render(request, 'mailbox.html', {'emp': emp})


def mail_detail(request):
    emp = ViewMail.objects.all()
    return render(request, 'mail_detail.html', {'emp': emp})


def mail_compose(request):
    emp = Compose.objects.all()
    return render(request, 'mail_compose.html', {'emp': emp})


def cardcustom(request):
    return render(request, 'cardcustom.html')


def widgets(request):
    return render(request, 'widgets.html')


def notifications(request):
    emp = Notify.objects.all()
    # return render(request, 'notifications.html',{'emp':emp})
    context = {}
    form = EmpNotifyForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    context['emp'] = emp
    context['form'] = form
    return render(request, 'notifications.html', context)


def addnotifications(request):
    if request.method == "GET":
        form = EmpNotifyForm()
        return render(request, 'notifications.html', {"form": form})
    else:
        # save code
        form = EmpNotifyForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                pass
        return redirect(notifications)


def delete_N(request, id):
    d = Notify.objects.filter(id=id)
    d.delete()
    return redirect(notifications)


# def edit_N(request, id):
#     if (request.method == "GET"):
#         d = Notify.objects.get(id=id)
#         return render(request, 'edit.html', {'emp': d})
#
#     elif (request.method == "POST"):
#         id = request.POST.get("id")
#         d = Notify.objects.get(id=id)
#         form = CategoryForm(request.POST, instance=d)
#         if form.is_valid():
#             form.save()
#         return redirect(notifications)


def contacts(request):
    emp = ContactsDetails.objects.all()
    return render(request, 'contacts.html', {'emp': emp})
