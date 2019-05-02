from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from re import split as re_split

from django.contrib.auth.models import User

from .forms import AddPatientForm, RecordForm, SignUpForm, GetByPatients, EditPatient, EditNote, CalendarPickerForm, AdjustPayed

from .models import Patients, Consultations, Revenues, Unpayed

from django.urls import reverse_lazy

from django.views import generic, View

from django.contrib.auth.decorators import login_required

from django.template import loader

from django.db import connection

from datetime import datetime

# global variables
current_year = datetime.now().year


# pas sur que cela serve encore
class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

@login_required
def index(request):
    user = request.user
    form_record = RecordForm(user,initial={'payed':True})
    form_add = AddPatientForm()

    return render(request, 'jengu/index.html', {'form_add': form_add, 'form_record': form_record})


@login_required
def add_patient(request):
    user = request.user
    if request.method == 'POST':
        form_add = AddPatientForm(request.POST)
            
        if form_add.is_valid():
            form_add.clean()
            birthday = datetime.strptime(form_add["birthday"].value(), '%d/%m/%Y')

            #adding patient if NOT EXIST IN DB (get_or_create)
            d, created = Patients.objects.get_or_create(first_name= form_add["first_name"].value(), 
                last_name= form_add["last_name"].value(),
                birth_date= birthday, 
                owner = user,
                tel = form_add["tel"].value(),
                mail = form_add["mail"].value(),
                notes = form_add["notes"].value()
                )
                
            d.save()

            return redirect(request.META['HTTP_REFERER'])  

    else: 
        return HttpResponse(':\ something went wrong')
        
@login_required
def record_session(request):
    user = request.user
    if request.method == 'POST':
        form_record = RecordForm(user,request.POST)

        if form_record.is_valid():
            form_record.clean()

            # get data from form
            id_patient = form_record["Patient"].value()
                
            date = form_record["date"].value()
            if date == "":
                date = str(datetime.now())
            else: 
                date = re_split(r'\W+', date)
                date = date[2]+"-"+date[1]+"-"+date[0]+" "+date[3]+":"+date[4]
                
            patient = Patients.objects.get(id=id_patient)
                
            payed = form_record["tarif"].value()
            if payed == "":
                payed = 0
                
            # happend to db
            d = Consultations.objects.create(first_name=patient.first_name, 
                last_name= patient.last_name,
                fk_patient=patient,
                date=date,
                payed= payed, 
                owner = user
                )
                
            d.save()
                
            return HttpResponse('/thanks/')
    else:
        return HttpResponse(':\ something went wrong')
            

@login_required
def browse(request): 
    user = request.user

    if request.method == 'GET':
        form_patient = GetByPatients(user,request.GET)

        if form_patient.is_valid():
            patient_id = form_patient["Patient"].value()
            print("patient_id: ",patient_id)

            return redirect(patient_id+'/')

    return render(request, 'jengu/browse.html',{'form_patient': form_patient})

def edit_note(request, patient_id):
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            form_note = EditNote(request.POST)
            
            if form_note.is_valid():
                form_note.clean()

                patient = Patients.objects.get(id=patient_id)

                #update db
                if patient.owner_id == user.id:
                    patient.notes =form_note["notes"].value()
                    patient.save()

                    return redirect(request.META['HTTP_REFERER'])  
        else: 
            return HttpResponse(':\ something went wrong')
        
        return redirect('detail')

    else:
        return redirect('/')

@login_required
def edit_patient(request, patient_id):  
    user = request.user
    if request.method == 'POST':
        form_patient = EditPatient(request.POST)
            
        if form_patient.is_valid():
            form_patient.clean()

            patient = Patients.objects.get(id=patient_id)

            #update db
            if patient.owner_id == user.id:
                patient.tel = form_patient["tel"].value()
                patient.mail = form_patient["mail"].value()
                patient.save()
                
                return redirect(request.META['HTTP_REFERER'])  

    else: 
        return HttpResponse(':\ something went wrong')
        
    return redirect('detail')

    
# REFONTE PROGRESSIVE DE DETAIL. INTÉGRER LES REQUÊTES POST ASSOCIÉES À CETTE CLASSE EN VUE D'ÉVITER LES RÉPÉTITIONS

class Detail(View):
    def __init__(self, **kwargs):
        self.template = loader.get_template('jengu/details.html')

    def get(self,request, patient_id):
        if request.user.is_authenticated: 
            user = request.user
            patient = Patients.objects.get(id=patient_id)

            edit_patient = EditPatient(initial={'tel': patient.tel, 'mail' : patient.mail})
            edit_note = EditNote(initial={'notes':patient.notes})

            context = {
            "patient" : patient,
            "consultations" : Consultations.objects.filter(fk_patient_id=patient_id), #######
            "edit_patient": edit_patient,
            "edit_note": edit_note
            }

            if patient.owner == user: 
                return HttpResponse(self.template.render(context, request))
            else: 
                return HttpResponse("Vous ne pouvez pas accéder à cette fiche patient")

        else:
            return redirect('/')

    def post(self,request, patient_id):
        pass

class Compta(View):
    form_class = CalendarPickerForm
    template = loader.get_template("jengu/compta.html")

    def get(self,request):
        if request.user.is_authenticated: 
            user = request.user
            ca = Revenues.objects.get(owner_id=user.id)
            un = Unpayed.objects.get(owner_id=user.id)
            months = self.form_class()

            context = {
            'year' : current_year,
            'ca' : ca, 
            'un' : un,
            'months' : months,
            }

            return HttpResponse(self.template.render(context, request))

        else:
            return redirect('/')
  
    def post(self,request):
        months = self.form_class(request.POST)
        if months.is_valid():
            month_nb = months["month"].value()
            return redirect(month_nb+'/')
        
        #ICI : compta détaillé par mois: édition des éventuels impayés
class ComptaDetail(Compta):
    template = loader.get_template("jengu/comptadetail.html")
    initial = {'payed':0}
    form_class = AdjustPayed

    def get(self,request, month):
        if request.user.is_authenticated: 
            user = request.user

            adjust_form = self.form_class(initial=self.initial)
            unpayed = Consultations.objects.filter(owner_id=user.id, payed=0, date__month = month)

            context = {'unpayed' : unpayed,
                       'adjust_form' : adjust_form}

            return HttpResponse(self.template.render(context, request))

        else:
            return redirect('/')

    def post(self,request, month):
        if request.user.is_authenticated: 
            user = request.user
            adjust_form = self.form_class(request.POST)

            if adjust_form.is_valid():
                adjust_form.clean()

                consultation = Consultations.objects.get(id=request.POST["id"])

                #update db         
                if (consultation.owner_id == user.id and consultation.payed == 0.0):
                    consultation.payed = adjust_form["payed"].value()
                    consultation.save()

                    return redirect(request.META['HTTP_REFERER'])

                else: 
                    return HttpResponse(':\ something went wrong')
        else:
            return redirect('/')

class Profile(View):
    template = loader.get_template("jengu/profile.html")

    def get(self,request):
        if request.user.is_authenticated:
            user = request.user
            user = User.objects.get(username=user)

            context = {"user": user}

            return HttpResponse(self.template.render(context, request))
        else:
            return redirect('/')

    # suppression of the user by calling a stored procedure
    def post(self,request):
        if request.user.is_authenticated: 
            user = request.user
            with connection.cursor() as cursor:   
                cursor.callproc("erase_user", [user.id])
                
            #logout(request)
            return redirect('/')

        else:
            return redirect('/')

class Save(View):
    template = loader.get_template("jengu/save.html")
    
    def get(self,request):
        if request.user.is_authenticated:
            user = request.user
            full_path = request.get_full_path()

            if "?" in full_path:
                if full_path.split("?=")[1] == "patients": 
                    patient = Patients.objects.filter(owner_id=user.id)
                    context={'table' : patient}
                elif full_path.split("?=")[1] == "consultations":
                    consultation = Consultations.objects.filter(owner_id=user.id).order_by('date')
                    context={'table' : consultation}
            else: 
                context={}

            return HttpResponse(self.template.render(context, request))

        else: 
            return redirect('/')
