from django.db import models


class Employee(models.Model):
    Employee_Name = models.CharField(max_length=20)
    Email = models.EmailField()
    Department = models.CharField(max_length=20)
    Designation = models.CharField(max_length=20)
    Salary = models.IntegerField()
    Card_status = models.CharField(max_length=20)
    Profile_picture = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.Employee_Name


class Leave(models.Model):
    From_Date = models.DateTimeField(max_length=20)
    Till_Date = models.DateTimeField(max_length=20)
    Emp_Name = models.CharField(max_length=20)
    Subject = models.CharField(max_length=100)
    Explain_Reason = models.CharField(max_length=200)
    Document = models.CharField(max_length=100)

    def __str__(self):
        return self.Emp_Name


class Notify(models.Model):
    Notification_Subject = models.CharField(max_length=200)
    Notification = models.CharField(max_length=200)
    Department = models.CharField(max_length=100)

    def __str__(self):
        return self.Notification_Subject


class Emails(models.Model):
    mail_contact = models.CharField(max_length=20)
    mail_subject = models.CharField(max_length=200)
    mail_date = models.DateField()

    def __str__(self):
        return self.mail_contact


class LeaveConf(models.Model):
    Approve = models.TextField(max_length=200)

    def __str__(self):
        return self.Approve


class Compose(models.Model):
    To = models.EmailField(max_length=20)
    Subject = models.CharField(max_length=200)
    mail_text = models.TextField(max_length=200)
    Profile_picture = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.To


class ViewMail(models.Model):
    Subject = models.CharField(max_length=200)
    Date = models.DateTimeField(max_length=200)
    From = models.EmailField(max_length=200)
    hello = models.CharField(max_length=20)
    mail_text = models.TextField(max_length=200)


class ContactsDetails(models.Model):
    Profile_picture = models.ImageField(upload_to='images/')
    Name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    twitter = models.CharField(max_length=200)
    phone = models.IntegerField()
