# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.

from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist as DoesNotExist
from picklefield.fields import PickledObjectField
from django.contrib.auth.models import User
from caching.base import CachingManager, CachingMixin
import datetime

class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=256)
    bio = models.CharField(max_length=256)
    pictureurl = models.CharField(max_length=256)

class party(models.Model):
    partyid = models.IntegerField(primary_key=True)
    partyref = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=256)
    abbrev = models.CharField(max_length=12)
    colour = models.CharField(max_length=12)
    wiki = models.CharField(max_length=325)

    def get_party_url(self):
        return self.wiki

    def get_party_colour(self):
        return self.colour

    def get_party_abbrev(self):
        return self.abbrev

    def get_party_textcolour(self): 
        hexy = self.colour
        red = int(hexy[1:3], 16)
        green = int(hexy[3:5], 16)
        blue = int(hexy[5:7], 16)

        if (red*0.299 + green*0.587 + blue*0.114) > 186:
            return('#000000')
        else:
            return('#ffffff')

class position(models.Model):
    posid = models.AutoField(primary_key=True)
    pid = models.ForeignKey('member')
    positionname = models.TextField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    
class datePickle(CachingMixin, models.Model):
    fullmap = PickledObjectField()
    objects = CachingManager()

class parlsess(CachingMixin, models.Model):
    parlsessid = models.CharField(max_length=8, primary_key=True)
    name = models.TextField()
    startdate=models.DateField(db_index=True)
    enddate=models.DateField(db_index=True, blank=True, null=True)
    parlnum = models.IntegerField()
    sessnum = models.IntegerField()
    duration = models.IntegerField()
    housesittings = models.IntegerField()

class datenav(CachingMixin, models.Model):
    hansarddate = models.DateField(primary_key=True)
    year = models.IntegerField(db_index=True)
    month = models.IntegerField(db_index=True)
    day = models.IntegerField(db_index=True)
    decade = models.CharField(max_length=12)
    objects = CachingManager()

    def get_fulldate(self):
        return self.hansarddate.strftime('%d %b, %Y')

    def get_decade(self):
        return self.decade

    def decades_list(self):
        return [1900,1910,1920,1930,1940,1950,1960,1970,1980,1990,2000,2010]

    def get_fullurl(self, year, month, day):
        return ('/full/'+str(year)+"/"+str(month)+"/"+str(day)+"/")

    def get_year(self):
        return self.year

    def get_month(self):
        if len(str(self.month))<=1:
            return "0"+str(self.month)
        else:
            return str(self.month)

    def get_day(self):
        if len(self.day)<=1:
            return "0"+str(self.day)
        else:
            return str(self.day)

    def get_years_list(self):
        return datenav.objects.filter(decade=self.decade).order_by('speechdate').values_list('year', flat=True).distinct()

    def get_months_list(self):
        return datenav.objects.filter(year=self.year).order_by('speechdate').values_list('month', flat=True).distinct()

    def get_days_list(self):
        return datenav.objects.filter(year=self.year).filter(month=self.month).order_by('speechdate').values_list('day', flat=True).distinct()

    def get_next_day_link(self):

        try:
            speechdate = self.get_next_by_hansarddate()

        except DoesNotExist:
            return ""

        y = str(speechdate.year)
        m = str(speechdate.month)
        d = str(speechdate.day)

        if len(m)<=1:
            m="0"+m

        if len(d)<=1:
            d="0"+d

        return ("/full/"+y+"/"+m+"/"+d+"/")


    def get_previous_day_link(self):
        try:
            speechdate = self.get_previous_by_hansarddate()

        except DoesNotExist:
            return ""

        y = str(speechdate.year)
        m = str(speechdate.month)
        d = str(speechdate.day)

        if len(m)<=1:
            m="0"+m

        if len(d)<=1:
            d="0"+d

        return ("/full/"+y+"/"+m+"/"+d+"/")


##    def get_days_dict(self):
##        daysQuery = datenav.objects.filter(year=self.year).filter(month=self.month).order_by('speechdate').values_list('day', flat=True).distinct()
##        daysDict = {}
##        for result in self.get_days_list():
##            daysDict[result]=
##            


class member(models.Model):
    pid = models.CharField(max_length=128, primary_key=True) # parlinfo member hash
    firstname = models.TextField(db_index=True)
    lastname = models.TextField(db_index=True)
    fulltitle = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=12, blank=True, null=True)
    profession = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    emailaddress = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    deceaseddate = models.DateField(blank=True, null=True)
    speakerurl = models.TextField(blank=True, null=True)
    op_slug = models.TextField(blank=True, null=True, db_index=True)
    
    def get_full_name(self):
        return (self.firstname + " " +self.lastname)

    def get_member_url(self):
        return 

    def get_static_img(self):
        '''Returns staticfile location of person's hosted picture
        If blank, links to a generic placeholder.'''
        pid = self.pid
        if pid == "":
            return ("dilipadsite/polimages/"+'unknown'+".png")
        elif pid is None:
            return ("dilipadsite/polimages/"+'unknown'+".png")
        elif pid == 'unmatched':
            return ("dilipadsite/polimages/"+'unknown'+".png")
        else:
            return ("dilipadsite/polimages/"+pid+".jpg")

    def get_personal_site(self):
        site = self.website
        if site is None:
            return ("http://www.parl.gc.ca/parlinfo/Files/Parliamentarian.aspx?Item="+self.pid+"&Language=E&Section=ALL")
        elif site=="":
            return ("http://www.parl.gc.ca/parlinfo/Files/Parliamentarian.aspx?Item="+self.pid+"&Language=E&Section=ALL")
        else:
            return site
    
class constituency(models.Model):
    '''a constituency object is an elected instance: of member, party, and riding'''
    cid = models.AutoField(primary_key=True)
    riding = models.TextField(blank=True, null=True, db_index=True)
    province = models.TextField(blank=True, null=True)
    pid = models.TextField(blank=True, null=True, db_index=True)
    partyid = models.ForeignKey('party')
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)

    def get_riding(self):
        return self.riding

    def get_position(self):
        '''Returns the position(s) that were held during this constituency period
        by this politician.'''
        position_list = []
        
        qs = position.objects.filter(pid=member.objects.get(pid=self.pid)).order_by('startdate')

        cs = self.startdate
        ce = self.enddate

        if ce is None:
            ce = datetime.datetime.now().date()
            
        for pos in qs:
            ps = pos.startdate
            pe = pos.enddate
            if pe is None:
                pe = datetime.datetime.now().date()

            if ps >= cs:
                if pe <= ce:
                    position_list.append(pos)
                elif ps <  ce and pe > ce:
                    position_list.append(pos)
            if ps < cs:
                if pe > cs and pe <= ce:
                    position_list.append(pos)
                elif pe >= ce:
                    position_list.append(pos)
        return(position_list)
            

class basehansard(CachingMixin, models.Model):
    '''base class for one statement made in the house of commons'''

    basepk = models.AutoField(primary_key=True) # new base primary key after natural sort on hid
    hid = models.TextField(blank=True, null=True) # hansard id, ie. ca.proc.d.20140529-16243.1.1.1.1
    speechdate = models.DateField(blank=True, null=True, db_index=True)
    pid = models.TextField(blank=True, null=True) # parlinfo member id hash; duplication can be removed later
    opid = models.TextField(blank=True, null=True) # open parliament-style member ID
    speakeroldname = models.TextField(blank=True, null=True) # mostly for error checking in retro documents and error-checking
    speakerposition = models.TextField(blank=True, null=True) # mostly for error checking in retro documents and error-checking
    maintopic = models.TextField(blank=True, null=True, db_index=True)
    subtopic = models.TextField(blank=True, null=True, db_index=True)
    speechtext = models.TextField(blank=True, null=True)
    speakerparty = models.TextField(blank=True, null=True, db_index=True)
    speakerriding = models.TextField(blank=True, null=True, db_index=True)
    speakername = models.TextField(blank=True, null=True, db_index=True)
    speakerurl = models.TextField(blank=True, null=True)

    objects = CachingManager()

    def get_parlinfo_id(self):
        return self.pid

    def is_topic(self):
        '''is this a topic?  used for formatting check'''
        if self.speakerposition=="topic":
            return True
        else:
            return False
        
    def is_subtopic(self):
        '''is this a subtopic?  used for formatting check'''
        if self.speakerposition=="subtopic":
            return True
        else:
            return False

    def is_modern(self):
        '''is this a post-dilipad speech?'''
        if self.speechdate >= datetime.date(1993,6,24):
            return True
        else:
            return False

    def is_stagedirection(self):
        '''is this a stagedirection?  used for formatting check'''
        if self.speakerposition=="stagedirection":
            return True
        else:
            return False

    def is_intervention(self):
        '''is this a intervention?  used for formatting check'''
        if self.speakerposition=="intervention":
            return True
        else:
            return False

    def get_party_url(self):
        try:
            x = party.objects.get(name=self.speakerparty)
            return x.get_party_url()
        
        except:
            return ("https://en.wikipedia.org/wiki/List_of_federal_political_parties_in_Canada")

    def get_party_colour(self):
        try:
            x = party.objects.get(name=self.speakerparty)
            return x.get_party_colour()
        
        except:
            return ("#777777")

    def get_party_textcolour(self):  # should remove this since it's now in party
        try:
            x = party.objects.get(name=self.speakerparty)
            return x.get_party_textcolour()
        
        except:
            return ("#ffffff")
        
    def get_party_abbrev(self):
        try:
            x = party.objects.get(name=self.speakerparty)
            return x.get_party_abbrev()
        
        except:
            return ("?")

    def get_op_id(self):
        return self.opid

    def get_display_speakerposition(self):
        x = self.speakerposition
        if x is None:
            return ""
        elif x is "":
            return x
        else:
            return ("("+x+")")

    def get_member_link(self):
        if self.pid is not None:
            return ("/members/record/"+self.pid+"/1/")
        else:
            return ("")

    def get_parlinfo_url(self):
        '''Returns parlinfo URL of person with this ID'''
        return self.speakerurl

    def get_parlinfo_url_written(self):
        '''Returns parlinfo URL of person with this ID-----
        Fix for written questions where original XML is malformed'''
        return ("http://www.parl.gc.ca/parlinfo/Files/Parliamentarian.aspx?Item="+self.opid+"&Language=E&Section=ALL")

    def get_static_img(self):
        '''Returns staticfile location of person's hosted picture
        If blank, links to a generic placeholder.'''
        pid = self.get_parlinfo_id()
        if pid == "":
            return ("dilipadsite/polimages/"+'unknown'+".png")
        elif pid is None:
            return ("dilipadsite/polimages/"+'unknown'+".png")
        elif pid == 'unmatched':
            return ("dilipadsite/polimages/"+'unknown'+".png")
        elif pid == 'intervention':
            return ("dilipadsite/polimages/"+'intervention'+".png")
        elif self.speakerposition == 'stagedirection':
            return ("dilipadsite/polimages/"+'direction'+".png")
        elif self.speakerposition == 'intervention':
            return ("dilipadsite/polimages/"+'intervention'+".png")
        else:
            return ("dilipadsite/polimages/"+pid+".jpg")

    def get_permalink_url(self):
        '''Returns a url pointing to this individual speech permalinked'''

        basepk = self.basepk
        return ("/full/permalink/"+str(basepk))
        

    def get_fullview_url(self):
        '''Returns a url pointing to this speech in its instance on a particular hansard day link at its proper anchor'''
        
        basepk = self.basepk
        speechdate = self.speechdate

        y = str(speechdate.year)
        m = str(speechdate.month)
        d = str(speechdate.day)

        if len(m)<=1:
            m="0"+m

        if len(d)<=1:
            d="0"+d

        return ("/full/"+y+"/"+m+"/"+d+"/fullview/"+str(basepk)+"/")


