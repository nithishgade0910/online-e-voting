from django.contrib import admin
from .models import Vote, Candidate, Election, OTP, VoterID
# Register your models here.
admin.site.register(Vote)
admin.site.register(Candidate)
admin.site.register(Election)
admin.site.register(OTP)
admin.site.register(VoterID)
