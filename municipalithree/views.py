from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response, Http404, redirect
from google.appengine.api import users
import json
from django.conf import settings
from forms import ComplaintForm,PhoneAuthForm
from models import Complaint, PhoneAuth
from twilio import twiml
from twilio.rest import TwilioRestClient
import random
from django.conf import settings
from google.appengine.ext import db
import re
#from stemming.porter2 import stem
#from itertools import product
import string

def home(request):
    '''
        This is the landing page for Municipalithree where all the complaints can be searched and browsed
    '''
    user = users.get_current_user()
    complaints = Complaint.all()
    if user:
      if user.email() == settings.SUPERUSER_EMAIL_ID:
        return redirect(settings.SITE_URL + 'dashboard/')      
    else:
      login_url = users.create_login_url(settings.SITE_URL)
    return render_to_response("index.html", locals(), context_instance=RequestContext(request))

def image(request):
    '''
        This is the landing page for Municipalithree where all the complaints can be searched and browsed
    '''
    image = Complaint.get_by_id(int(request.GET.get('id',0))).photo
    response = HttpResponse(image,mimetype="image")
    return response

def submit(request):
    '''
        This view handles all the communications with the Mobile app
    '''
    if request.method == "POST":
      complaint_form = ComplaintForm(data=request.POST)
      if complaint_form.is_valid():
        submitted=1
        complaint = complaint_form.save(commit=False)
        complaint.status = "submitted"
        photo = request.GET.get('photo',None)
        complaint.photo = db.Blob(photo)
        complaint.save()
      else:
        submitted=0;
        return render_to_response("complaintweb.html", locals(), context_instance=RequestContext(request))
      complaint_form = ComplaintForm()
      return render_to_response("complaintweb.html", locals(), context_instance=RequestContext(request))
    else:
      complaint_form = ComplaintForm()
      return render_to_response("complaintweb.html", locals(), context_instance=RequestContext(request))

def api(request):
    '''
        This view handles all the communications with the Mobile app
    '''
    complaint_form = ComplaintForm(data=request.GET)
    if complaint_form.is_valid():
      submitted=1
      complaint = complaint_form.save(commit=False)
      complaint.status = "submitted"
      complaint.save()
    else:
      submitted=0;
      return HttpResponse("Failed! Please try again later.")
    return HttpResponse("Success!")

def auth(request):
    '''
        This view handles auth-flow for the Mobile app
    '''
    if request.method == "POST":
      auth_form = PhoneAuthForm(data=request.POST)
      if auth_form.is_valid():
        imei = auth_form.cleaned_data['imei']
        code = auth_form.cleaned_data['code']
        auth = PhoneAuth.all().filter("imei =",imei)
        for a in auth:
          if a.code == code:
            return HttpResponse("Success")
        return HttpResponse("Not found!")
      else:
        pass
    else:
      auth_form = PhoneAuthForm(data=request.GET)
      if auth_form.is_valid():
        code = str(int(random.random()*10000))
        auth = auth_form.save(commit=False)
        auth.code = code
        auth.save()
        account_sid = "AC25686c73aef12ab314a1a5389cff6738"
        auth_token = "0f6cbf7f0e1f29bbe02fbe315991d2c3" 
        client = TwilioRestClient(account_sid, auth_token)
        rv = client.sms.messages.create(to=auth.phno,
                                        from_="+14439880196",
                                        body="Your confirmation code is " + code + " -Municipalithree.")
      else:
        raise Http404()
      return HttpResponse("Success")

def browse(request):
    '''
        This is the landing page for Municipalithree where all the complaints can be searched and browsed
    '''
#    user = users.get_current_user()
    complaints = Complaint.all()
#    if user:
#        logout_url = users.create_logout_url(settings.SITE_URL)
#    else:
#        login_url = users.create_login_url(settings.SITE_URL)
    return render_to_response("browse.html", locals(), context_instance=RequestContext(request))
    
def stats(request):
    '''
      This view handles the Stats page for Municipalithree.
    '''
#    user = users.get_current_user()
    complaints = Complaint.all()
#    if user:
#        logout_url = users.create_logout_url(settings.SITE_URL)
#    else:
#        login_url = users.create_login_url(settings.SITE_URL)
    return render_to_response("stats.html", locals(), context_instance=RequestContext(request))

def dashboard(request):
    user = users.get_current_user()
    if user:
      if user.email() == settings.SUPERUSER_EMAIL_ID:
        logout_url = users.create_logout_url(settings.SITE_URL)
        complaints = Complaint.all()
        return render_to_response("dashboard.html", locals(), context_instance=RequestContext(request))
    else:
      return redirect(settings.SITE_URL)

def browsers(request):
    if request.method == "POST":
      pass
    else:
      complaints = Complaint.all()
      data = [{"id":idx+1, "title":c.title, "desc":c.desc, "loc":c.add, "status":c.status, "remarks":c.remarks} for idx,c in enumerate(complaints)]
      response = {"id":-1,"fieldErrors":[],"sError":"","aaData":data}
    return HttpResponse(json.dumps(response),mimetype='application/json')

def checkSimilarity(string1, string2):
    exclude = string.punctuation
    strtok1 = (''.join(ch for ch in string1 if ch not in exclude)).split(' ')
    strtok2 = (''.join(ch for ch in string2 if ch not in exclude)).split(' ')
    score = 0.0
    for s1 in strtok1:
      for s2 in strtok2:
        if s1 == s2:
          score += 1.0
    return score/(len(strtok1)+len(strtok2))
    

'''
def stemwords(inString):
    outString = []
    for idx,s in enumerate(inString.split(' ')):
        temp = stem(s)
        if len(temp) > 2 :
          outString.append(temp)
    return outString

def aggregate(complaint):
    complaints = Complaint.all()
    scores = []
    exclude = set(string.punctuation)
    for c in complaints:
      s = ''.join(ch for ch in c.title if ch not in exclude)
      c_tokenized = stemword(s)
      s = ''.join(ch for ch in complaint.title if ch not in exclude)
      complaint_tokenized = stemwords(s)
      print c_tokenized
      print complaint_tokenized
'''
