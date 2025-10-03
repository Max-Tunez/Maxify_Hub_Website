from django.db import models
from ckeditor.fields import *
#integrating paystack
import uuid



# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=100) 
    email=models.EmailField()
    phoneNumber=models.CharField(max_length=12)
    description=models.TextField(max_length=300)

    def __str__(self) :
        return self.name
    

class Courses(models.Model):
    courseName=models.CharField(max_length=150,primary_key=True)
    image=models.ImageField(upload_to="course",blank=True,null=True)
    courseFee=models.IntegerField()
    courseDuration=models.IntegerField()
    syllabus=RichTextField(default="syllabus")
    aboutCourse=RichTextField(default="aboutCourse")
    stars=models.IntegerField(default=3)

    def __str__(self) :
        return self.courseName





class Trainer(models.Model):
    trainer_name=models.CharField(max_length=60)
    trainer_designation=models.CharField(max_length=140)
    trainer_experience=models.DecimalField(max_digits=5,decimal_places=2)
    course=models.ForeignKey(Courses,on_delete=models.SET_NULL,null=True)

    def __str__(self) :
        return self.trainer_name



class Register(models.Model):
    candidateId=models.AutoField(primary_key=True)
    firstName=models.CharField(max_length=20)
    lastName=models.CharField(max_length=20)
    fathername=models.CharField(max_length=20)
    phoneNumber=models.CharField(max_length=14)
    alternateNumber=models.CharField(max_length=14)
    email=models.EmailField(unique=True)
    collegeName=models.CharField(max_length=100)
    address=models.TextField(max_length=150)
    landmark=models.CharField(max_length=100)
    street=models.CharField(max_length=100)
    city=models.CharField(max_length=140)
    pincode=models.IntegerField()
    companyName=models.CharField(max_length=140,blank=True,null=True)
    designation=models.CharField(max_length=140)
    qualification=models.CharField(max_length=100)
    computerKnowledge=models.CharField(max_length=40)
    course=models.CharField(max_length=140)
    timestamp=models.DateTimeField(auto_now_add=True)
    trainer=models.ForeignKey(Trainer,on_delete=models.DO_NOTHING,null=True)

    def __str__(self) :
        return self.email
    


class Payments(models.Model):
    name=models.ForeignKey(Register,on_delete=models.CASCADE)
    amountPaid=models.IntegerField()
    balance=models.IntegerField(blank=True,null=True)
    status=models.CharField(max_length=20,default="Unpaid")

    def __int__(self):
        return self.name
    


class Attendance(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    date=models.DateField()
    logintime=models.TimeField()
    logouttime=models.TimeField()
    approved=models.BooleanField(default=False)

    def __str__(self):
        return self.email
    

class Blogs(models.Model):
    title=models.CharField(max_length=160)
    description=RichTextField(default="description")
    authname=models.CharField(max_length=100)
    img=models.ImageField(upload_to='blog', blank=True, null=True)
    timestamp=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title



# Paystack Integration

class Payment(models.Model):
    ref = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField()
    # amount = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ref)
