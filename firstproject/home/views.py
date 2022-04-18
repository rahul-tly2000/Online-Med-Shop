from datetime import datetime
from os import abort
from django.shortcuts import render, redirect
from django.http import  HttpResponseRedirect
from django.contrib import messages
from functools import wraps

from .forms import EmployeeForm, LoginForm, MedicineForm

from django.contrib.auth.models import auth
from .models import Medicine, Purchase, User

# Create your views here.

def admin_only(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        current_user = request.user
        username = current_user.username
        if username != 'admin':
            return HttpResponseRedirect('Permission denied')
        return f(request, *args, **kwargs)
    return wrap


def emp_only(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        current_user = request.user
        if current_user.is_employee != 1 or current_user.is_approved != 1:
            return HttpResponseRedirect('Permission denied')
        return f(request, *args, **kwargs)
    return wrap

def login_required(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        current_user = request.user
        if current_user.is_user != 1 or current_user.is_approved != 1:
            return HttpResponseRedirect('Permission denied')
        return f(request, *args, **kwargs)
    return wrap

def home(request):
    med_obj = Medicine.objects.all()
    return render(request, 'home.html', {'med_obj' : med_obj, 'alert':''}) 

def reg(request):
    form = EmployeeForm()
    if request.method == 'POST':
        employeeForm = EmployeeForm(request.POST)
        if employeeForm.is_valid():
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone_number = request.POST['phone_number']
            username = request.POST['username']
            age = request.POST['age']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            position = request.POST['choose']      
            email = request.POST['email']
            if password==confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken')
                elif User.objects.filter(email=email).exists():
                        messages.info(request, 'Email Taken')
                else:
                    user = User.objects.create_user(password=password, email=email, first_name=first_name, last_name=last_name, age=age, phone_number=phone_number, username=username)
                    user.save()
                    user_obj = User.objects.get(email=email)
                    if position == 'User':
                        user_obj.is_user = 1
                    else:
                        user_obj.is_employee = 1
                    user_obj.save()
                    messages.info(request, 'Waiting for Admin approval')           
                    return redirect('../login/')
            else:
                messages.info(request, 'Password not match')
    return render(request, 'register.html', {'form':form})

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            messages.info(request, 'Unauthorized account!!!')
            return HttpResponseRedirect('../login')
        else:
            user_obj = User.objects.get(username=username)

            if username=='admin' and password=='123':
                auth.login(request, user)
                return redirect(admin)
            elif user_obj.is_user == 1 and user_obj.is_approved == 1:
                auth.login(request, user)
                request.session['name'] = username
                return redirect(user_)
            elif user_obj.is_employee==1 and user_obj.is_approved==1:
                auth.login(request, user)
                request.session['name'] = username
                return redirect(employee)
            else:
                messages.info(request, 'Unauthorized account!!!')

    return render(request, 'login.html', {'form':form})

def logout(request):
    auth.logout(request)
    return redirect(home)

############  admin  #############

@admin_only
def admin(request):
    return render(request, 'admin.html')

@admin_only
def emp_data(request):
    emp_obj = User.objects.filter(is_employee = 1, is_approved = 1).all()
    return render(request, 'emp_data.html', {'emp_obj':emp_obj})

@admin_only
def emp_req(request):
    emp_obj = User.objects.filter(is_employee = 1, is_approved = 0).all()
    
    return render(request, 'emp_req.html', {'emp_obj':emp_obj})

@admin_only
def emp_approve(request, id):
    emp_obj = User.objects.filter(id=id).first()
    emp_obj.is_approved = 1
    emp_obj.save()
    return redirect(emp_req)

@admin_only
def emp_reject(request, id):
    emp_obj = User.objects.filter(id=id).first()
    emp_obj.delete
    return redirect(emp_req)

@admin_only
def emp_edit(request, id):
    emp_obj = User.objects.filter(id=id).first()
    if request.method == 'POST':
        emp_obj.first_name = request.POST['first_name']
        emp_obj.last_name = request.POST['last_name']
        emp_obj.username = request.POST['username']
        emp_obj.email = request.POST['email']
        emp_obj.age = request.POST['age']
        emp_obj.phone_number = request.POST['phone_number']
        emp_obj.salary = request.POST['salary']
        emp_obj.save()
        return redirect(emp_data)
    return render(request, 'emp_edit.html', {'emp_obj':emp_obj})

@admin_only
def emp_remove(request, id):
    emp_obj = User.objects.filter(id=id).first()
    emp_obj.delete()
    return redirect(emp_data)

@admin_only
def approve_stock(request):
    med_obj = Medicine.objects.all()
    needy_med = []
    for med in med_obj:
        if med.requested_stock > 0:
            needy_med.append(med)
    return render(request, 'admin_approve_stock.html', {'med_obj':needy_med})

@admin_only
def reject_med(request, id):
    med_obj = Medicine.objects.filter(id=id).first()
    med_obj.requested_stock = 0
    med_obj.save()
    return redirect(approve_stock)

@admin_only
def verify_stock(request, id):
    med_obj = Medicine.objects.filter(id=id).first()
    med_obj.verify_stock += med_obj.requested_stock
    med_obj.save()
    med_obj.requested_stock = 0
    med_obj.save()
    return redirect(approve_stock)

############  employee  #############

@emp_only
def employee(request):
    current_user = request.user
    return render(request, 'employee.html', {'user':current_user})

@emp_only
def medicine_data(request):
    med_obj = Medicine.objects.all()
    app_med = []
    for med in med_obj:
        if med.verify_stock > 0:
            app_med.append(med)
    return render(request, 'medicine_data.html', {'medicine_obj':med_obj, 'approve_med':app_med})


@emp_only
def approved_med(request, id):
    med_obj = Medicine.objects.filter(id=id).first()
    med_obj.stock += med_obj.verify_stock
    med_obj.save()
    med_obj.verify_stock = 0
    med_obj.save()
    return redirect(medicine_data)

@emp_only 
def medicine(request):
    form = MedicineForm()
    if request.method == 'POST':
        medicineForm = MedicineForm(request.POST)
        if medicineForm.is_valid():
            medicineForm.save()
            return redirect(employee)
    return render(request, 'medicine.html', {'form':form})

@emp_only
def edit_med(request, id):
    med_obj = Medicine.objects.filter(id=id).first()
    if request.method == 'POST':
        med_obj.name = request.POST['name']
        med_obj.price = request.POST['price']
        med_obj.discription = request.POST['discription']
        med_obj.photo_link = request.POST['link']
        med_obj.save()
        return redirect(medicine_data)
    return render(request, 'edit_med.html', {'med_obj': med_obj})


@emp_only
def req_more(request, id):
    med_obj = Medicine.objects.filter(id=id).first()
    if request.method == 'POST':
        req_stock = request.POST['req_stock']
        med_obj.requested_stock += int(req_stock)
        med_obj.save()
        return redirect(medicine_data)
    return render(request, 'req.html', {'med_obj':med_obj})

@emp_only
def user_data(request):
    user_obj = User.objects.filter(is_user = 1, is_approved = 1).all()
    unauth_user_obj = User.objects.filter(is_user = 1, is_approved = 0).all()
    return render(request, 'user_data.html', {'user_obj':user_obj, 'unauth_user_obj':unauth_user_obj})

@emp_only
def user_reject(request, id):
    user_obj = User.objects.filter(id=id).first() 
    user_obj.delete()
    return redirect(user_data)

@emp_only
def user_approve(request, id):
    user_obj = User.objects.filter(id=id).first()
    user_obj.is_approved = 1
    user_obj.save()
    return redirect(user_data)

@emp_only
def user_edit(request, id):
    user_obj = User.objects.filter(id=id).first()
    if request.method == 'POST':
        user_obj.first_name = request.POST['first_name']
        user_obj.last_name = request.POST['last_name']
        user_obj.username = request.POST['username']
        user_obj.email = request.POST['email']
        user_obj.age = request.POST['age']
        user_obj.phone_number = request.POST['phone_number']
        user_obj.save()
        return redirect(user_data)
    return render(request, 'user_edit.html', {'user_obj':user_obj})

@emp_only
def user_remove(request, id):
    user_obj = User.objects.filter(id=id).first()
    user_obj.delete()
    return redirect(user_data)

@emp_only
def pending_purchace(request):
    purchace_obj = Purchase.objects.all()
    pending_obj = []
    for obj in purchace_obj:
        if obj.is_requested == 1:
            pending_obj.append(obj)
    return render(request, 'pending_purchace.html', {'pending_obj':pending_obj})

@emp_only
def purchace_approve(request, id):
    purchace_obj = Purchase.objects.filter(id=id).first()
    purchace_obj.is_purchced = 1
    purchace_obj.save()
    med_id = purchace_obj.medicine_id
    med_obj = Medicine.objects.filter(id=med_id).first()
    med_obj.stock -= purchace_obj.quantity
    med_obj.sell += purchace_obj.quantity
    med_obj.income += purchace_obj.price
    med_obj.save()
    purchace_obj.status = 'Completed'
    purchace_obj.is_requested = 0
    purchace_obj.save()
    return redirect(pending_purchace)

@emp_only
def purchace_reject(request, id):
    purchace_obj = Purchase.objects.filter(id=id).first()
    purchace_obj.is_reject = 1
    purchace_obj.is_requested = 0
    purchace_obj.status = 'Rejected'
    purchace_obj.save()
    return redirect(pending_purchace)

@emp_only
def profile_emp(request, id):
    emp_obj = User.objects.filter(id=id).first()
    return render(request, 'profile_emp.html', {'emp':emp_obj})

@emp_only
def purchase_history_all(request):
    purchase_obj = Purchase.objects.filter()
    return render(request, 'purchase_history_all.html', {'purchase_obj': purchase_obj})


############  user  #############

@login_required
def user_(request):
    current_user = request.user
    med_obj = Medicine.objects.all()
    cart_obj = Purchase.objects.filter(is_cart=1, user_id=current_user.id)
    purchase_obj = []
    cart_list = []
    tot_price = 0
    if cart_obj:
        for obj in cart_obj:
            med = Medicine.objects.filter(id=obj.medicine_id).first()
            cart_list.append(med)
            purchase_obj.append(obj)
            tot_price += obj.price

    return render(request, 'user.html', {'user':current_user, 'med_obj':med_obj, 'cart_item':cart_list, 'purchase_obj':cart_obj, 'tot_price':tot_price})

@login_required
def add_to_cart(requset, id):
    med_obj = Medicine.objects.filter(id=id).first()
    cart_obj = Purchase.objects.filter(is_cart=1 , medicine_id=id).first()
    
        
    if cart_obj:
        cart_obj.quantity +=1
        cart_obj.price += med_obj.price
        cart_obj.save()
    else:
        current_user = requset.user
        user_id = current_user.id
        user_name = current_user.username
        tot_price = med_obj.price
        date_= datetime.now()
        new_purchace = Purchase(user_id=user_id, medicine_id=id, name=med_obj.name, username=user_name, is_requested=0, is_cart=1, price=tot_price, date=date_)
        new_purchace.save()
    return redirect(user_)

@login_required
def cart_update(request, id, p):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        if quantity < 1:
            quantity = 1
        purchase_obj = Purchase.objects.filter(id=id).first()
        med_obj = Medicine.objects.filter(id = purchase_obj.medicine_id).first()
        if quantity > med_obj.stock:
            messages.info(request, f'"{med_obj.name}" only {med_obj.stock} left')           
            return redirect(user_)
        purchase_obj.quantity = quantity
        purchase_obj.price = p * quantity
        purchase_obj.save()
    return redirect(user_)

@login_required
def cart_remove(request, id):
    purchase_obj = Purchase.objects.filter(id=id)
    purchase_obj.delete()
    return redirect(user_)

@login_required
def purchase(request, id):
    cart_obj = Purchase.objects.filter(user_id=id, is_cart=1)
    for obj in cart_obj:
        obj.is_requested = 1
        obj.status = 'Pending'
        obj.is_cart = 0
        obj.save()
    return redirect(user_)

@login_required
def available_med(request):
    med_obj = Medicine.objects.all()
    avl_med = []
    for med in med_obj:
        if med.stock > 0:
            avl_med.append(med)
    return render(request, 'available_med.html', {'med_obj':avl_med})

@login_required
def purchace_history(request):
    current_user = request.user
    id = current_user.id
    purchace_obj = Purchase.objects.filter(user_id=id, is_clear_byUser=0, is_requested=0, is_cart=0).all()
    pending_obj = Purchase.objects.filter(user_id=id, is_clear_byUser=0, is_requested=1).all()
    return render(request, 'purchace_history.html', {'purchace_obj':purchace_obj[::-1], 'pending_obj':pending_obj[::-1]})

@login_required
def clear_one(request, id):
    user_id = request.user.id
    purchace_obj = Purchase.objects.filter(id=id).first()
    if purchace_obj.is_requested == 1:
        purchace_obj.delete()
    else:
        purchace_obj.is_clear_byUser = 1
        purchace_obj.save()
    return redirect(purchace_history)

@login_required
def clear_all(request, id):
    purchace_obj = Purchase.objects.filter(user_id=id, is_requested=0)
    print(purchace_obj)
    for obj in purchace_obj:
        obj.is_clear_byUser = 1
        obj.save()
    return redirect(purchace_history)

@login_required
def clear_all_order(request, id):
    purchace_obj = Purchase.objects.filter(user_id=id, is_requested=1)
    print(purchace_obj)
    for obj in purchace_obj:
        obj.delete()
    return redirect(purchace_history)

@login_required
def profile(request, id):
    user_obj = User.objects.filter(id=id).first()
    return render(request, 'profile.html', {'user':user_obj})


def tryy(request):
    return render(request, 'try.html')