from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .forms import AddPatientForm, RecordForm, SignUpForm, GetByPatients, EditPatient, EditNote, CalendarPickerForm, AdjustPayed
#from django.contrib.auth.forms import UserCreationForm
from .models import Patients, Consultations, Revenues, Unpayed

from django.urls import reverse_lazy

from django.views import generic, View

from django.views.generic import ListView

from django.template import loader

from datetime import datetime

# global variables
current_year = datetime.now().year


# pas sur que cela serve encore
class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def index(request):
    try:
        user = request.user
        form_record = RecordForm(user,initial={'payed':True})
        form_add = AddPatientForm()

        return render(request, 'jengu/index.html', {'form_add': form_add, 'form_record': form_record})
    except:
        return redirect('/')


def add_patient(request):
    try: 
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
        
        return redirect('index')

    except:
        return redirect('/')

def record_session(request):
    try:
        user = request.user
        if request.method == 'POST':
            form_record = RecordForm(user,request.POST,initial={'payed':True})

            if form_record.is_valid():
                form_record.clean()

                #adding consultation in DB
                id_patient = form_record["Patient"].value()
                patient = Patients.objects.get(id=id_patient)

                print('patient:', patient) 

                if form_record["payed"].value()==True:
                    payed = form_record["tarif"].value()
                else: 
                    payed = 0
                
                d = Consultations.objects.create(first_name=patient.first_name, 
                    last_name= patient.last_name,
                    fk_patient=patient,
                    payed= payed, 
                    owner = user
                    )
                
                d.save()
                
                return HttpResponse('/thanks/')
        else:
            return HttpResponse(':\ something went wrong')
            
    except Exception as e:
        print(e)
        return redirect('/')

def browse(request): 
    try:
        user = request.user

        if request.method == 'GET':
            form_patient = GetByPatients(user,request.GET)

            if form_patient.is_valid():
                patient_id = form_patient["Patient"].value()
                print("patient_id: ",patient_id)

                return redirect(patient_id+'/')

        return render(request, 'jengu/browse.html',{'form_patient': form_patient})
    except:
        return redirect('/')

def edit_note(request, patient_id):
    try:
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

    except:
        return redirect('/')

def edit_patient(request, patient_id):
    try: 
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

    except:
        return redirect('/')

# REFONTE PROGRESSIVE DE DETAIL. INTÉGRER LES REQUÊTES POST ASSOCIÉES À CETTE CLASSE EN VUE D'ÉVITER LES RÉPÉTITIONS

class Detail(View):
    def __init__(self, **kwargs):
        self.template = loader.get_template('jengu/details.html')

    def get(self,request, patient_id):
        try: 
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

        except:
            return redirect('/')

    def post(self,request, patient_id):
        pass

### NON, POUR LA COMPTA, ON S'ATTAQUE A AUX CLASS BASED VIEWS 
# S'APPUYER SUR https://simpleisbetterthancomplex.com/article/2017/03/21/class-based-views-vs-function-based-views.html
class Compta(View):
    form_class = CalendarPickerForm
    template = loader.get_template("jengu/compta.html")

    def get(self,request):
        try: 
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

        except:
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
        try: 
            user = request.user

            adjust_form = self.form_class(initial=self.initial)
            unpayed = Consultations.objects.filter(owner_id=user.id, payed=0, date__month = month)

            context = {'unpayed' : unpayed,
                       'adjust_form' : adjust_form}

            return HttpResponse(self.template.render(context, request))

        except:
            return redirect('/')

    def post(self,request, month):
        try: 
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
        except:
            return redirect('/')
        

    #return render(request, 'psy/compta.html')
######OLD#SHIT###############

    '''
    if request.method == 'POST':
        form_add = AddPatientForm(request.POST)

        #form_record = RecordForm(user,request.POST,initial={'payed':True})
        
        if form_add.is_valid():
            form_add.clean()
            birthday = datetime.strptime(form_add["birthday"].value(), '%d/%m/%Y')

            #adding patient if NOT EXIST IN DB (get_or_create)
            d, created = Patients.objects.get_or_create(first_name= form_add["first_name"].value(), 
                last_name= form_add["last_name"].value(),
                birth_date= birthday, 
                owner = user
                )
            
            d.save()

            return HttpResponse('/thanks/') 
    
    else:
        form_record = RecordForm(user,initial={'payed':True})
        form_add = AddPatientForm()
    '''


    '''
    def detail(request, patient_id):
    user = request.user
    patient = Patients.objects.get(id=patient_id)

    edit_patient = EditPatient(initial={'tel':patient.tel, 'mail':patient.mail})
    edit_note = EditNote(initial={'notes':patient.notes})

    template = loader.get_template('psy/details.html')
    context = {
        'patient_name': '{} {}'.format(patient.first_name, patient.last_name),
        'birth_date' : patient.birth_date,
        'phone' : patient.tel,
        'mail' : patient.mail,
        "notes" : patient.notes,
        "consultations" : Consultations.objects.filter(fk_patient_id=patient_id), #######
        "edit_patient": edit_patient,
        "edit_note": edit_note
    }

    if patient.owner == user: 
        return HttpResponse(template.render(context, request))

    else: 
        return HttpResponse("Vous ne pouvez pas accéder à cette fiche patient")
    '''