from django.shortcuts import render, redirect
# from .forms import signupForm, loginForm
from .models import CustomUser, Friends_record, Expense_record, Group, Group_data, Group_expense_record

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from itertools import chain
from django.db import IntegrityError
from django.urls import reverse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.
def base_view(request):
    print("Welcomm to base page")
    return render(request, "base.html", {})

def signupForm_view(request):
    
    if request.method == "POST":
        
        print("Welcomm to sign up page")
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone_no")
        
        # Check if the user already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'User already exists. Please log in.')
            # return redirect("/login_view")      
        
        else:
            user = CustomUser.objects.create_user(username, email, password, phone_no = phone_no)
            
            print(user)
            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                return redirect("/show_expenses")
            else:
                # No backend authenticated the credentials
                return redirect("/signupForm_view")

    return render(request, "signup.html")


def login_view(request):

    if request.method == "POST":
       
        print("Welcomm to login page is valid")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("/show_expenses")
        else:
            # No backend authenticated the credentials
            messages.error(request, 'User not exists. Please Sign up.')

    return render(request, "login.html")
        


def logout_view(request):
    logout(request)
    return render(request, "base.html", {})

def index_view(request):
    print("Welcomm to index page")
    if request.user.is_authenticated:

        # for add user sending a list of users.
        users = CustomUser.objects.all()  # Fetch all users from the database
        users = users.exclude(username = request.user)
        #showing the friend_list
        friend_list = Friends_record.objects.filter(uid = request.user)
        

        #showing the group_list
        group_query_set = Group.objects.filter(uid = request.user)
        other_group_list = Group_data.objects.filter(mid = request.user)
        
        group_list = list(group_query_set)
        for group in other_group_list:
            temp = Group.objects.get(gname = group.gid.gname)
            if temp not in group_list:
                group_list.append(temp)


        # just testing for git upload

        return render(request, "index.html", {'users': users, 'friend_list' : friend_list, 'group_list' : group_list})
    return redirect("/login_view")


def add_friend(request):

    if request.method == "POST":
        try:
            selected_value = request.POST.get('selected_value')

            friend_user = CustomUser.objects.get(uid = selected_value)

            friend = Friends_record(uid = request.user, f_uid = friend_user)
            friend.save()

            reverse_friend = Friends_record(uid = friend_user, f_uid = request.user)
            reverse_friend.save()

            return redirect("/index_view")

        except IntegrityError:
            messages.error(request, 'friend is already exists')
            # return render(request, "index.html", {'friend_error' : "friend is already exists"})
            return redirect("/index_view")
            # return redirect(reverse('/index_view') + '?error_message=Group name already exists')


def friend_view(request, f_uid):

    shared_user = CustomUser.objects.get(username = f_uid)

    expense_list = Expense_record.objects.filter(payer_uid = request.user, shared_uid = shared_user.uid)

    shared_user_expense_list = Expense_record.objects.filter(payer_uid = shared_user.uid, shared_uid = request.user)

    expense_list = expense_list | shared_user_expense_list

    expense_list = expense_list.order_by('date_field')
    expense_list = expense_list.order_by('time_field')

    friend_relation = Friends_record.objects.get(f_uid = shared_user.uid, uid = request.user)

    return render(request, "friend_index.html", {'friend' : f_uid, 'expense_list' : expense_list, 'owe_amount' : friend_relation.owe_amount})

def add_expense_record(request, f_uid):


    if request.method == "POST":

        s_uid = request.POST.get('friend_username')
        total_amount = request.POST.get('total_amount')
        splited_amount = int(total_amount)/2
        description = request.POST.get('description')
        date_field = request.POST.get('date_field')
        time_field = request.POST.get('time_field')

        shared_user = CustomUser.objects.get(username = s_uid)


        expense = Expense_record(payer_uid = request.user, shared_uid = shared_user, total_amount = total_amount, splited_amount = splited_amount, description = description, date_field = date_field, time_field = time_field)
        expense.save()

        friend_relation = Friends_record.objects.get(f_uid = shared_user.uid, uid = request.user)
        reverse_friend_relation = Friends_record.objects.get(f_uid = request.user, uid = shared_user.uid)

        friend_relation.owe_amount += float(splited_amount) 
        reverse_friend_relation.owe_amount -= float(splited_amount)

        friend_relation.save()
        reverse_friend_relation.save()

        
        return redirect("/friend_view/{}".format(s_uid))
    else:  # Handle GET requests (displaying the form)
        return render(request, "friend_index.html", {'friend': friend})


def add_group(request):

    if request.method == "POST":

        try:
            gname = request.POST.get('gname')
            group = Group(uid = request.user, gname = gname)
            group.save()

            group_obj = Group.objects.get(gname = gname)
            member = CustomUser.objects.get(username = request.user)

            group_data = Group_data(gid = group_obj, mid = member)
            group_data.save()
        except IntegrityError:
            # If IntegrityError is raised, redirect back to the previous page with an error message
            # return render(request, "index.html", {'error' : "Group name already exists"})
            messages.error(request, 'Group name already exists')
            # return redirect(reverse('/index_view') + '?error_message=Group name already exists')

        return redirect("/index_view")


def group_view(request, gname):

    # showing the friend list for adding into to group
    friend_list = Friends_record.objects.filter(uid = request.user)

    # fetching members from group_data
    group = Group.objects.get(gname = gname)
    members_list = Group_data.objects.filter(gid = group)
    members_list = members_list.exclude(mid = request.user)
    

    # fetching the group_exxpense_record
    # group = Group.objects.get(gname = gname)
    expense_list = Group_expense_record.objects.filter(gid = group)

    expense_list = expense_list.order_by('date_field')
    expense_list = expense_list.order_by('time_field')


    reletion_list = list()
    # fetching reletion between memberrs and user
    internal_members_list = Group_data.objects.filter(gid = group)
    internal_members_list = members_list.exclude(mid = request.user)
    for member in internal_members_list:
        x = CustomUser.objects.get(username = member.mid.username)
        temp = Friends_record.objects.get(f_uid = x.uid, uid = request.user)
        reletion_list.append(temp)

    

    print("--------")
    print(members_list)
    print("--------")
    print(request.user)

    

    return render(request, "group_index.html", {'group' : gname, 'friend_list' : friend_list, 'members_list' : members_list, 'expense_list': expense_list, 'reletion_list' : reletion_list})

def add_group_members(request, gname):

    if request.method == "POST":

        # gname = request.POST.get('gname')
        # gname = gname
        member_username = request.POST.get('selected_value')

        group = Group.objects.get(gname = gname)
        new_member = CustomUser.objects.get(username = member_username)

        group_data = Group_data(gid = group, mid = new_member)
        print("-----------------")
        print(new_member)
        

        members_list = Group_data.objects.filter(gid = group)
        members_list = members_list.exclude(mid = request.user)
        members_list = members_list.exclude(mid = new_member)
        for member in members_list:
            friend_list = Friends_record.objects.filter(uid = member.mid)

            def is_value_not_present(my_list, target_value):
                for obj in my_list:
                    print("@@@@@@@@@@@@")
                    print(obj.f_uid)
                    print(target_value)
                    if obj.f_uid == target_value:
                        return False
                return True


            if is_value_not_present(friend_list, new_member):
                friend_user = CustomUser.objects.get(username = new_member)

                friend = Friends_record(uid = member.mid, f_uid = friend_user)
                print("^^^^^^^^^^^^^^")
                print(member.mid)
                friend.save()

                reverse_friend = Friends_record(uid = friend_user, f_uid = member.mid)
                reverse_friend.save()

        group_data.save()

        
        return redirect("/group_view/{}".format(gname))


def add_group_expense_record(request, gname):

    if request.method == "POST":

        # s_uid = request.POST.get('friend_username')
        total_amount = request.POST.get('total_amount')
        description = request.POST.get('description')
        date_field = request.POST.get('date_field')
        time_field = request.POST.get('time_field')

        group = Group.objects.get(gname = gname)


        selected_members = request.POST.getlist('items')

        splited_amount = int(total_amount)/(len(selected_members)+1)

        expense = Group_expense_record(payer_uid = request.user, gid = group, total_amount = total_amount, splited_amount = splited_amount, description = description, date_field = date_field, time_field = time_field)
        expense.save()

        for member in selected_members:
                temp = CustomUser.objects.get(username = member)
                friend_relation = Friends_record.objects.get(f_uid = temp.uid, uid = request.user)
                reverse_friend_relation = Friends_record.objects.get(f_uid = request.user, uid = temp.uid)

                friend_relation.owe_amount += float(splited_amount) 
                reverse_friend_relation.owe_amount -= float(splited_amount)

                friend_relation.save()
                reverse_friend_relation.save()

        
        return redirect("/group_view/{}".format(gname))
    
    
def show_expenses(request):
    
    # expenses = Expense_record.objects.filter(payer_uid = request.user)

    expense_list = Expense_record.objects.filter(payer_uid = request.user)

    shared_user_expense_list = Expense_record.objects.filter(shared_uid = request.user)

    expense_list = expense_list | shared_user_expense_list

    expense_list = expense_list.order_by('date_field')
    # expense_list = expense_list.order_by('time_field')

   
    
    group_query_set = Group.objects.filter(uid = request.user)
    group_expense_list = list()
    for group in group_query_set:
        group_expense_list = group_expense_list + list(Group_expense_record.objects.filter(gid = group))


    return render(request, 'Dashboard.html', {'expense_list': expense_list, 'group_expense_list' : group_expense_list})
    
    
def settlement_view(request):

    if request.method == "POST":

        selected_members = request.POST.getlist('items')

        for friend in selected_members:
            temp = CustomUser.objects.get(username = friend)
            friend_relation = Friends_record.objects.get(f_uid = temp.uid, uid = request.user)
            reverse_friend_relation = Friends_record.objects.get(f_uid = request.user, uid = temp.uid)

            friend_relation.owe_amount = 0
            reverse_friend_relation.owe_amount = 0

            friend_relation.save()
            reverse_friend_relation.save()


        return redirect("settlement_view")
    
    else:
        return redirect("show_settlement_view")

    

def show_settlement_view(request):

    friend_list = Friends_record.objects.filter(uid = request.user)
    friend_list = friend_list.exclude(f_uid = request.user)

    return render(request, "settlement.html", {'friend_list' : friend_list})

