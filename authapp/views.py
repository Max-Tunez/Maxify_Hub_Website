from django.shortcuts import render, redirect
from django.contrib import messages
import re
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.generic import View
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from authapp.utils import TokenGenerator,generate_token
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
import socket
#Paystack Integration
from django.http import JsonResponse
from startupapp.models import Payment
from .utils import Paystack
#Auto update payment from paystack
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json




# Create your views here.
def signup(request):
    flag = 0
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['exampleInputEmail1']
        password=request.POST['exampleInputPassword1']
        confirm_password=request.POST['exampleInputConfirmPassword1']
        print(name,email,password,confirm_password)

        if password!=confirm_password:
            messages.warning(request,"Pasword does not match")
            return redirect('/auth/signup/')
        
        if len(password)<6:
            messages.warning(request,"Password must be at least 6 characters")
            return redirect('/auth/signup/')
        
        elif not re.search("[a-z]", password):
            flag = -1

        elif not re.search("[A-Z]", password):
            flag = -1

        elif not re.search("[0-9]", password):
            flag = -1

        elif not re.search("[-_)(*^%$#@!]", password):
            flag = -1

        else:
            pass

        if(flag==0):
            try:
                if User.objects.get(username=email):
                    #returh HttpResponse("email already exist")
                    messages.info(request,"Email already exist")
                    return redirect('/auth/signup/')
                
            except Exception as identifier:
                pass

            user=User.objects.create_user(email,email,password)
            user.first_name=name
            user.is_active=False
            user.save()

            email_subject="Activate Your Account"
            message=render_to_string('activate.html', {
                'user' : user,
                'domain' : '127.0.0.1:8000',
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : generate_token.make_token(user)
            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            email_message.send()

            messages.success(request,f"Follow the link in your Gmail or copy and paste this link in a new tab to Activate your Account {message}")

            # messages.success(request,"Signup successful. Please login.")
            return redirect('/auth/login/')
        
        else:
            messages.error(request,"Invalid Password. Please follow the guideline")
            return redirect('/auth/signup/')

    return render(request,"signup.html")




class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,"Account Activation Successful. Please Login Now")
            return redirect('/auth/login/')
        else:
            return render(request,'activatefail.html')





def handleLogin(request):
    if request.method=="POST":
        username=request.POST['exampleInputEmail1']
        userpassword=request.POST['exampleInputPassword1']
        myuser=authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request, myuser)
            messages.success(request, "login successful")
            return redirect('/dashboard/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/auth/login/')
        
    return render(request,"login.html")
 
def handleLogout(request):
    logout(request)
    messages.success(request, "Logout success")
    return render(request,"login.html")

def Enroll(request):
    return render(request,"enroll.html")


class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'request-reset-email.html')
    
    def post(self,request):
        email=request.POST['email']
        if not email:
            messages.error(request, "Please enter a valid email address")
            return render(request, 'request-reset-email.html')
        # Log email to ensure we are getting the correct email
        print(f"Received email: {email}")

        user=User.objects.filter(email=email) # Use iexact for case-insensitive match
        if user.exists():
            #current_site=get_current_site(request)
            email_subject = '[Reset Your Passwprd]'
            message = render_to_string('reset-user-password.html', {
                'domain' : '127.0.0.1:8000',
                'uid' : urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token' : PasswordResetTokenGenerator().make_token(user[0]),
            })

            try:
                email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
                email_message.send()
                messages.info(request, "A password reset link has been sent to your email address.")
            except socket.timeout:
                messages.error(request, "Email server timed out. Please try again later.")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
            
            return render(request, 'request-reset-email.html')


            # email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            # email_message.send()

            # # messages.info(request, f"{message}")
            # messages.info(request, "A password reset link has been sent to your email address.")
            # return render(request,'request-reset-email.html')
        else:
            # Log message for debugging
            print(f"No user found with email: {email}")
            messages.error(request,'No Account Exist with this email')
            return render(request,'request-reset-email.html')
        

class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64' : uidb64,
            'token' : token
        }
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link is Invalid")
                return render(request,'request-reset-email.html')
            
        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'set-new-password.html',context)
    
    def post(self,request,uidb64,token):
        context={
            'uidb64' : uidb64,
            'token' : token
        }

        flag=0
        password=request.POST['exampleInputPassword1']
        confirm_password=request.POST['exampleInputConfirmPassword1']
        # print(password,confirm_password)

        if password!=confirm_password:
            messages.warning(request,"Pasword does not match")
            return render(request,'set-new-password.html',context)
        
        if len(password)<6:
            messages.warning(request,"Password must be at least 6 characters")
            return render(request,'set-new-password.html',context)
        
        elif not re.search("[a-z]", password):
            flag = -1

        elif not re.search("[A-Z]", password):
            flag = -1

        elif not re.search("[0-9]", password):
            flag = -1

        elif not re.search("[-_)(*^%$#@!]", password):
            flag = -1

        else:
            pass

        if(flag==0):
            try:
                user_id=force_text(urlsafe_base64_decode(uidb64))
                user=User.objects.get(pk=user_id)
                user.set_password(password)
                user.save()
                messages.success(request, "Password Reset Successful. Please Login with your New Password")
                return redirect('/auth/login/')
            except DjangoUnicodeDecodeError as identifier:
                messages.error(request, "Something Went Wrong")
                return render(request, "set-new-password.html",context)
            



#For PAystack Integration


def initiate_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')  # Amount in kobo
        email = request.POST.get('email')

        # Convert amount to Decimal if necessary
        try:
            amount = float(amount)
        except ValueError:
            # Handle the error or set a default value
            amount = 0.0

        # Create a new payment record
        # payment = Payments.objects.create(email=email, amount=amount)
        payment = Payment(email=email, amount=amount)
        payment.save()

        context = {
            'payment': payment,
            'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        }
        return render(request, 'make_payment.html', context)
    return render(request, 'initiate_payment.html')

def verify_payment(request, ref):
    paystack = Paystack()
    status, result = paystack.verify_payment(ref)
    if status:
        payment = Payment.objects.get(ref=ref)
        if result['amount'] == payment.amount:
            payment.verified = True
            payment.save()
            return JsonResponse({'message': 'Payment verified successfully'})
    return JsonResponse({'message': 'Payment verification failed'}, status=400)


# To auto update payment from paystack
@csrf_exempt
def paystack_webhook(request):
    if request.method == 'POST':
        event = json.loads(request.body)
        if event['event'] == 'charge.success':
            ref = event['data']['reference']
            payment = Payment.objects.get(ref=ref)
            payment.verified = True
            payment.save()
            return HttpResponse(status=200)
    return HttpResponse(status=400)
