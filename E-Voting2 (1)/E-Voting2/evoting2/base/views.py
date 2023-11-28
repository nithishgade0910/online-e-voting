from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Election, Candidate, Vote, OTP, VoterID
import random
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
# Create your views here.


def user_register(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        voterID = request.POST['voter_id']
        name = request.POST['name']
        parents_name = request.POST['parents_name']
        age = request.POST['age']
        mobile_number = request.POST['mobile_number']
        address = request.POST['address']
        user_ins = User.objects.create_user(username=username, password=password, email=email)
        user_ins.save()
        VoterID.objects.create(user = user_ins, voterid = voterID, name=name, parents_name=parents_name, age=age, mobile_number=mobile_number, address=address)
        login(request, user_ins)
        user_ins.save()
        return redirect('home')
    return render(request, 'user_register.html', context)

def user_login(request):
    context = {}
    try:
        print(request.session['next_url'])
    except:
        print("NO NEXT URL")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            user_email = user.email
            rnd_str = ''.join(random.choice("0123456789") for _ in range(4))
            OTP.objects.create(otp=rnd_str)
            print(rnd_str)
            try:
                send_mail("OTP for Login", f"your OTP for logging in is {rnd_str}", "ghoshswakshwar@gmail.com", [user_email])
            except:
                pass
            login(request, user)
            return redirect('verify')
    return render(request, 'user_login.html', context)

def user_logout(request):
    logout(request)
    return redirect('home')

def verify(request):
    context = {}
    if request.method == "POST":
        otp = request.POST['otp']
        otp_ins = OTP.objects.get(otp=otp)
        if otp_ins is not None:
            try:
                next_url = request.session.get('next_url', '/')
                del request.session['next_url']
                return redirect(next_url)
            except:
                return redirect('home')
    return render(request, 'verify.html', context)

#Done
def home(request):
    context = {}
    on_going_election = Election.objects.filter(status='ongoing')
    finished_election = Election.objects.filter(status='done')
    context['on_going_elections'] = on_going_election
    context['finished_elections'] = finished_election
    return render(request, 'home.html', context)

#Done
def issue_vote(request, election_id, randomstr):
    if request.user.is_authenticated:
        curr_user = request.user
        election = Election.objects.get(id=election_id)
        all_candidates = Candidate.objects.filter(election=election)
        context = {}
        context['election'] = election
        context['all_candidates'] = all_candidates
        voter_id_ins = VoterID.objects.get(user=curr_user)
        if voter_id_ins.status == 'active':
            if request.method == 'POST':
                candidate = request.POST['candidate']
                voter_id = request.POST['voter_id']
                voter_id_ins = VoterID.objects.get(voterid = voter_id)
                if voter_id_ins is not None:
                    candidate_ins = Candidate.objects.get(id = int(candidate))
                    new_vote = Vote(election = election, candidate=candidate_ins, voter_id=voter_id)
                    new_vote.save()
                    return HttpResponse("<strong>Your Vote is successfully casted.</strong>")
                else:
                    return HttpResponse("<strong>Your Voter ID isnt found. </strong>")
        else:
            return HttpResponse("<strong>Your Voter ID is Blocked</strong>")
        return render(request, 'issue_vote.html', context)
    request.session['next_url'] = request.path
    return redirect('user_login')

#Done
def create_candidate(request):
    curr_user = request.user
    if curr_user.is_superuser:
        if  request.method == 'POST' and request.FILES:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            party_name = request.POST['party_name']
            profile_pic = request.FILES['profile_pic']
            Candidate.objects.create(first_name=first_name, last_name=last_name, party_name=party_name, profile_pic=profile_pic)
            return HttpResponse("<p>Candidate added successfully.</p>")
        return render(request, 'create_candidate.html')
    else:
        return HttpResponse("<strong>The User isnt an admin.</strong>")

#Done
def add_election(request):
    context = {}
    all_candidates = Candidate.objects.all()
    context['all_candidates'] = all_candidates
    curr_user = request.user
    if curr_user.is_superuser:
        if request.method == 'POST':
            name = request.POST['name']
            candidate_ids = request.POST.getlist('candidates')
            election = Election.objects.create(name=name)

            election.candidates.set(candidate_ids)

            return HttpResponse("<p>The Election is created.</p>")
        return render(request, 'add_election.html', context)
    else:
        return HttpResponse("<strong>The User isnt an admin.</strong>")

#Done
def add_candidate_to_election(request, election_id):
    election = Election.objects.get(id=election_id)
    all_candidates = Candidate.objects.all()

    context = {}
    curr_user = request.user
    if curr_user.is_superuser and request.method == 'POST':
        selected_candidates_ids = request.POST.getlist('candidates')
        election.candidates.set(selected_candidates_ids)
        return redirect('home')
    
    context['election'] = election
    context['all_candidates'] = all_candidates
    return render(request, 'update_candidates.html', context)

def create_election_url(request, election_id):
    rnd = ''
    for _ in range(20):
        rnd += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return HttpResponse(f"http://localhost:8000/issue_vote/{election_id}/{rnd}")

def get_result(request, election_id):
    election = Election.objects.get(id = election_id)
    all_votes = Vote.objects.filter(election=election)
    result_dict = {}
    context = {}
    for vote in all_votes:
        result_dict[vote.candidate.first_name] = result_dict.get(vote.candidate.first_name, 0) + 1
    
    top_candidate = None
    top_vote = 0
    for name, vote_ in result_dict.items():
        top_vote = max(top_vote, vote_)
        if top_vote == vote_:
            top_candidate = name
    context['winner'] = top_candidate
    context['election'] = election
    return render(request, 'results.html', context)


def candidate_profile(request, candidate_id):
    context = {}
    candidate_ins = Candidate.objects.get(id=candidate_id)
    first_name = candidate_ins.first_name
    last_name = candidate_ins.last_name
    party_name = candidate_ins.party_name
    profile_photo = candidate_ins.profile_pic
    context['first_name'] = first_name
    context['last_name'] = last_name
    context['party_name'] = party_name
    context['profile_photo'] = profile_photo
    return render(request, 'candidate_profile.html', context)

def personal_profile(request):
    context = {}
    curr_user = request.user
    if curr_user.is_authenticated:
        voter_id_ins = VoterID.objects.get(user=curr_user)
        name = voter_id_ins.name
        email = curr_user.email
        parents_name = voter_id_ins.parents_name
        age = voter_id_ins.age
        mobile_number = voter_id_ins.mobile_number
        address = voter_id_ins.address
        profile_pic = voter_id_ins.profile_picture
        context['name'] = name
        context['email'] = email
        context['parents_name'] = parents_name 
        context['age'] = age
        context['mobile_number'] = mobile_number
        context['address'] = address
        context['profile_pic'] = profile_pic
    return render(request, 'personal_profile.html', context)