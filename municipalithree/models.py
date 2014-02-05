from google.appengine.ext import db

class Complaint(db.Model):
    """
    Models a request for a Complaint
    submitted by an User
    """
    phno    = db.PhoneNumberProperty(required=True)
    name    = db.StringProperty(required=True)
    title   = db.StringProperty(required=True)
    desc    = db.TextProperty()
    loc     = db.GeoPtProperty(required=True)
    landmark= db.StringProperty()
    add     = db.StringProperty()
    status  = db.StringProperty(default='submitted',choices=set(['submitted','reviewed & forwarded','work under progress','resolved']))
    remarks = db.TextProperty()
    photo   = db.BlobProperty()

class PhoneAuth(db.Model):
    """
    Models a PhoneAuth flow
    """
    phno     = db.PhoneNumberProperty()
    imei     = db.IntegerProperty()
    time     = db.DateTimeProperty(auto_now=True) 
    code     = db.StringProperty()
