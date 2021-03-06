#!/usr/bin/python
# -*- coding: utf-8 -*-
#from google.appengine.ext.webapp import template
import djangoforms
from models import Complaint, PhoneAuth

class ComplaintForm(djangoforms.ModelForm):
    """
    Form that allows users to submit
    suggestions for new features.
    """
    class Meta:
        model = Complaint

class PhoneAuthForm(djangoforms.ModelForm):
    """
    Form that allows users to submit
    suggestions for new features.
    """
    class Meta:
        model = PhoneAuth
