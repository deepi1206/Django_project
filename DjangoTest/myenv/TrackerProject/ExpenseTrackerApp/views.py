from django.shortcuts import render,redirect
from .models import Expense,Userdb
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph,Spacer
from reportlab.lib.enums import TA_CENTER

# Create your views here.
@login_required
def expense(request):
    if request.method == 'POST':
        # Handle form submission
        category = request.POST.get('category')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        monthly_budget = request.POST.get('monthlyBudget')  # Assuming your input field name is 'monthlyBudget'
        name = request.POST.get('welcomeMessage')  # Assuming you have user authentication and want to associate expenses with users
        login_name = request.session.get('loginedusername')
        print("login_name",login_name)
        user_exists = Userdb.objects.filter(user_name=login_name).values()
        print("user",user_exists)
        if user_exists is not None:
            Budget = user_exists[0]['monthly_budget']
            name =  name
            print('Budget',Budget)                  
        try:
            amount = float(amount)
            monthly_budget = float(monthly_budget) if monthly_budget else None
        except ValueError:
            # Handle invalid input
            return render(request, 'expEntrypage.html', {'error_message': 'Invalid input for amount or monthly budget'})
        datas1 = Expense.objects.filter(login_name=login_name).values()  # Filter expenses for the logged-in user
        print("datas", datas1)
        totalexp = 0 
        for i in range(len(datas1)):
            print(datas1[i]['amount'])
            totalexp+= int(datas1[i]['amount'])
        totalexp= totalexp+amount
        if totalexp > monthly_budget:
            print("totalexp",totalexp)
            return render(request, 'expEntrypage.html', {'error_message': 'Your Monthly budget is completed',"monthlyAmt" : Budget,"Name":name,'datas':datas1})             
        # return redirect('home', monthly_amt=Budget, name=name, datas=datas)
        else:
            Expense.objects.create(category=category, description=description, amount=amount, monthly_budget=monthly_budget, login_name=login_name,name=name)
            datas = Expense.objects.filter(login_name=login_name).values()  # Filter expenses for the logged-in user
            print("datas", datas)
            return render(request,'expEntrypage.html',{"monthlyAmt" : Budget,"Name":name,'datas':datas})  # Redirect to the same page to display updated data
    return render(request,'expEntrypage.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("username",username,password)
        user_exists = Userdb.objects.filter(user_name=username, user_password=password).first()
        print("user",user_exists)
        if user_exists is not None:
            Budget = user_exists.monthly_budget
            name = user_exists.name 
            print('Budget',Budget,name)
            datas = Expense.objects.filter(login_name=user_exists).values()  # Filter expenses for the logged-in user
            print("datas12", datas)     
            request.session['loginedusername'] = username  
            return render(request,'expEntrypage.html',{"monthlyAmt" : Budget,"Name":name,'datas':datas})  # Redirect to expense page after successful login
        else:
            return render(request, 'loginpage.html', {'error_message': 'Invalid username or password'})


    return render(request, 'loginpage.html')
def signup_view(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('newname')
        username = request.POST.get('newUsername')
        email = request.POST.get('email')
        password = request.POST.get('newPassword')
        monthly_budget = request.POST.get('monthlyBudget')

        # Check if the username is already taken
        if Userdb.objects.filter(user_name=username).exists():
            return render(request, 'loginpage.html', {'error_message': 'Username already exists. Please choose a different username.'})

        # Create the user
        user = Userdb.objects.create(user_name=username, g_email=email, user_password=password,monthly_budget=monthly_budget,name=name)

        # Save additional user details (monthly budget) if provided
        if monthly_budget:
            # Validate monthly budget input
            try:
                monthly_budget = float(monthly_budget)
                print("monthly_budget",monthly_budget)
            except ValueError:
                return render(request, 'loginpage.html', {'error_message': 'Invalid input for monthly budget. Please enter a valid number.'})

            # Save monthly budget for the user

        # Redirect to the login page after successful signup
        return redirect('login')

    return render(request, 'loginpage.html')



def generate_pdf(request):
    login_name = request.session.get('loginedusername')
    datas= Expense.objects.filter(login_name=login_name).values()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expenses.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Sample table data (replace with your actual data)
    table_data = []
    title_style = ParagraphStyle(name='TitleStyle', fontSize=20, textColor=colors.black, alignment=TA_CENTER)  # Set alignment to center
    title_text = "<center><b>Daily Expense Datas</b></center>"
    title = Paragraph(title_text, title_style)
    elements.append(title)

    elements.append(Spacer(1, 36))
    
    for expense in datas:
        print("expenseeee",expense)  # Assuming user has an expenses relation
        table_data.append([expense['category'], expense['description'], expense['amount'], expense['monthly_budget'],expense['name']])

    # Define table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])

    # Create table
    expense_table = Table(data=[['Category', 'Description', 'Amount', 'Monthly Budget','Name']] + table_data)
    expense_table.setStyle(style)

    # Add table to the document
    elements.append(expense_table)

    # Build PDF
    pdf.build(elements)

    return response

