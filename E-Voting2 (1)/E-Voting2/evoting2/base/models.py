from django.db import models
from django.contrib.auth.models import User

class VoterID(models.Model):

    STATUS_CHOICES = (
        ('active', 'active'),
        ('blocked', 'blocked')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voterid = models.CharField(max_length=255, default='No Voter ID found')
    name = models.CharField(max_length=255, default='John Doe')
    parents_name = models.CharField(max_length=500, default='Papa John Doe')
    age = models.PositiveIntegerField(default=18)
    mobile_number = models.PositiveBigIntegerField(default=9000448844)
    address = models.CharField(max_length=500, default='XYZ, street no 52, UP, 2011150')
    profile_pic = models.ImageField(upload_to='profile_pic', default='default.png')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    def __str__(self):
        return self.voterid

class OTP(models.Model):
    otp = models.CharField(max_length=5, default='00000')
    
    def __str__(self):
        return self.otp

class Candidate(models.Model):
    first_name = models.CharField(max_length=255, default="John")
    last_name = models.CharField(max_length=255, default="Doe")
    party_name = models.CharField(max_length=255, default="NOTA")
    profile_pic = models.ImageField(upload_to='image', default='image/default.png')

    def __str__(self):
        return self.first_name + " " + self.last_name



class Election(models.Model):
    STATUS_CODE = (
        ('ongoing', 'ongoing'),
        ('done', 'done')
    )
    name = models.CharField(max_length=255, default="No Data")
    candidates = models.ManyToManyField(Candidate)
    status = models.CharField(max_length=20, choices=STATUS_CODE ,default="ongoing")
    def __str__(self):
        return self.name

class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=255,default="No Data")

    def __str__(self):
        return self.voter_id