from django.shortcuts import *
from django.views.generic import *
from django.contrib import messages
from startupapp.models import *


# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phoneNo=request.POST.get('num')
        desc=request.POST.get('desc')
        query=Contact(name=name,email=email,phoneNumber=phoneNo,description=desc)
        query.save()
        messages.success(request,"Thank you for contacting us. We will get back to you soon...")
        return render(request,"contact.html")
    return render(request,"contact.html")


def courses(request):
    courses=Courses.objects.all()
    context={"Courses":courses}
    return render(request,"courses.html",context)

def course(request,id):
    course=Courses.objects.filter(courseName=id)
    context={"course":course}
    return render(request,"course.html",context)

def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login Or Register with us")
        return redirect("/auth/login/")
    courses=Courses.objects.all()
    context={"courses":courses}

    #if the form is submitted, the code below should work

    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        dadName=request.POST.get('fathername')
        phone=request.POST.get('phone')
        alternateNumber=request.POST.get('alternateNumber')
        email=request.POST.get('email')
        college=request.POST.get('college')
        addr=request.POST.get('addr')
        landmark=request.POST.get('landmark')
        street=request.POST.get('street')
        pcode=request.POST.get('pcode')
        city=request.POST.get('city')
        companyname=request.POST.get('companyname')
        Designation=request.POST.get('Designation')
        Qualification=request.POST.get('Qualification')
        cknowledge=request.POST.get('cknowledge')
        scourse=request.POST.get('scourse')
        ccourse=request.POST.get('ccourse')

        emailPresent=Register.objects.filter(email=email)
        if emailPresent:
            messages.error(request,"Email already Exist")
            return redirect('/enroll/')
        
        if scourse==ccourse:
            pass

        else:
            messages.error(request,"Please Select a Valid Course")
            return redirect('/enroll/')
        
        query=Register(firstName=fname,lastName=lname,fathername=dadName,phoneNumber=phone,alternateNumber=alternateNumber,email=email,collegeName=college,address=addr,landmark=landmark,street=street,city=city,pincode=pcode,companyName=companyname,designation=Designation,qualification=Qualification,computerKnowledge=cknowledge,course=scourse)
        #print (query.candidateId)
        query.save()
        messages.success(request,"Enrollment Success")
        return redirect('/candidateprofile/')
    
    return render(request,"enroll.html", context)

def candidateprofile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login to View your Profile")
        return redirect("/auth/login")
    
    currentuser=request.user.username
    print(currentuser)
    details=Register.objects.filter(email=currentuser)

# Initialize paymentstats with default values
    paymentstats = {
        "paymentstatus": "",
        "amount": 0,
        "balance": 0
    }

# Initialize attendanceStats
    attendanceStats = []


    payment=Payments.objects.all()
    # paymentstatus=""
    # amount=0
    # balance=0
    for j in payment:
        if str(j.name)==currentuser :
            
            paymentstatus=j.status
            amount=j.amountPaid
            balance=j.balance

        
            paymentstats={"paymentstatus":paymentstatus,"amount":amount,"balance":balance}

            attendanceStats=Attendance.objects.filter(email=currentuser)

    context={"details":details,"status":paymentstats,"attendanceStats":attendanceStats}

    return render(request,"candidateprofile.html", context)

#--------------------------------------------------------------------------
# def candidateprofile(request):
#     if not request.user.is_authenticated:
#         messages.warning(request, "Please Login to View your Profile")
#         return redirect("/auth/login")
    
#     currentuser = request.user.username
#     print(currentuser)
#     details = Register.objects.filter(email=currentuser)
    
#     payment = Payments.objects.all()
#     paymentstatus = ""
#     amount = 0
#     balance = 0
#     payment_found = False
    
#     for j in payment:
#         if str(j.name) == currentuser:
#             paymentstatus = j.status
#             amount = j.amountPaid
#             balance = j.balance
#             payment_found = True
#             break  # Assuming there's only one matching payment entry per user
           
    
#     if payment_found:
#         paymentstats = {"paymentstatus": paymentstatus, "amount": amount, "balance": balance}
#     else:
#         paymentstats = {"paymentstatus": "N/A", "amount": 0, "balance": 0}

#     context = {"details": details, "status": paymentstats}
    
#     return render(request, "candidateprofile.html", context)
#-----------------------------------------------------------------------


def candidateupdate(request,id):
    data=Register.objects.get(candidateId=id)
    courses=Courses.objects.all()
    context={"data":data,"courses":courses}
    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        dadName=request.POST.get('fathername')
        phone=request.POST.get('phone')
        alternateNumber=request.POST.get('alternateNumber')
        college=request.POST.get('college')
        addr=request.POST.get('addr')
        landmark=request.POST.get('landmark')
        street=request.POST.get('street')
        pcode=request.POST.get('pcode')
        city=request.POST.get('city')
        companyname=request.POST.get('companyname')
        Designation=request.POST.get('Designation')
        Qualification=request.POST.get('Qualification')
        scourse=request.POST.get('scourse')

        edit=Register.objects.get(candidateId=id)
        edit.firstName=fname
        edit.lastName=lname
        edit.fathername=dadName
        edit.phoneNumber=phone
        edit.alternateNumber=alternateNumber
        edit.collegeName=college
        edit.address=addr
        edit.landmark=landmark
        edit.street=street
        edit.city=city
        edit.pincode=pcode
        edit.companyName=companyname
        edit.designation=Designation
        edit.qualification=Qualification
        edit.course=scourse

        edit.save()
        messages.success(request,"Data Update Successful...")
        return redirect("/candidateprofile/")
    
    return render(request,"updatecandidate.html", context)




def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login to Fill your Attendance")
        return redirect("/auth/login/")
    
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        date=request.POST.get('date')
        logintime=request.POST.get('logintime')
        logouttime=request.POST.get('logouttime')
        query=Attendance(name=name,email=email,date=date,logintime=logintime,logouttime=logouttime)
        query.save()
        messages.success(request,"Applied successfully, please wait for the approval")
        return redirect("/candidateprofile/")
    return render(request, "attendance.html")


def search(request):
    query = request.GET.get('search', '')  # Use get() to avoid KeyError
    if len(query) > 100:
        allPosts = Courses.objects.none()
    else:
        allPosts = Courses.objects.filter(courseName__icontains=query)
    
    if allPosts.count() == 0:
        messages.warning(request, "No Search Results")
    
    params = {'allPosts': allPosts, 'query': query}
    return render(request, "search.html", params)


def dashboard(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login to View your Profile")
        return redirect("/auth/login")
    
    currentuser=request.user.username
    print(currentuser)
    details=Register.objects.filter(email=currentuser)

# Initialize paymentstats with default values
    paymentstats = {
        "paymentstatus": "",
        "amount": 0,
        "balance": 0
    }

# Initialize attendanceStats
    attendanceStats = []


    payment=Payments.objects.all()
    # paymentstatus=""
    # amount=0
    # balance=0
    for j in payment:
        if str(j.name)==currentuser :
            
            paymentstatus=j.status
            amount=j.amountPaid
            balance=j.balance

        
            paymentstats={"paymentstatus":paymentstatus,"amount":amount,"balance":balance}

            attendanceStats=Attendance.objects.filter(email=currentuser)

    context={"details":details,"status":paymentstats,"attendanceStats":attendanceStats}

    return render(request,"dashboard.html", context)


def handleblog(request):
    posts = Blogs.objects.all()#.order_by('-timestamp')
    context = {"posts": posts}
    return render(request, "blog.html", context)

