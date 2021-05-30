from django.shortcuts import render

# Create your views here.
from django.db.models import Max
from .models import user_login, disease_drug_map


def index(request):
    return render(request,'./myapp/index.html')

def about(request):
    return render(request,'./myapp/about.html')

def contact(request):
    return render(request,'./myapp/contact.html')

def admin_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='admin')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/admin_home.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, './myapp/admin_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/admin_login.html',context)


def admin_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    else:
        return render(request,'./myapp/admin_home.html')

def admin_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return admin_login(request)
    else:
        return admin_login(request)

def admin_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='admin')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/admin_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/admin_changepassword.html', context)

from .models import symptom_master

def admin_symptom_master_add(request):
    if request.method == 'POST':

        symptom_name = request.POST.get('symptom_name')

        sd = symptom_master(symptom_name=symptom_name)
        sd.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/admin_symptom_master_add.html', context)
    else:
        return render(request, './myapp/admin_symptom_master_add.html')

def admin_symptom_master_edit(request):
    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        symptom_name = request.POST.get('symptom_name')
        sd = symptom_master.objects.get(id=int(s_id))

        sd.symptom_name = symptom_name
        sd.save()
        msg = 'Record Updated'
        sd_l = symptom_master.objects.all()
        context = {'symptom_list': sd_l, 'msg': msg}
        return render(request, './myapp/admin_symptom_master_view.html', context)
    else:
        id = request.GET.get('id')
        sd = symptom_master.objects.get(id=int(id))
        context = {'symptom_name':sd.symptom_name,'s_id':sd.id}
        return render(request, './myapp/admin_symptom_master_edit.html',context)

def admin_symptom_master_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    sd = symptom_master.objects.get(id=int(id))
    sd.delete()
    msg = 'Record Deleted'
    sd_l = symptom_master.objects.all()
    context = {'symptom_list': sd_l,'msg':msg}
    return render(request, './myapp/admin_symptom_master_view.html',context)

def admin_symptom_master_view(request):

    sd_l = symptom_master.objects.all()
    context = {'symptom_list':sd_l}
    return render(request, './myapp/admin_symptom_master_view.html',context)

from .models import disease_master

def admin_disease_master_add(request):
    if request.method == 'POST':

        disease_name = request.POST.get('disease_name')
        disease_descp = request.POST.get('disease_descp')

        dm = disease_master(disease_name=disease_name,disease_descp=disease_descp)
        dm.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/admin_disease_master_add.html', context)
    else:
        return render(request, './myapp/admin_disease_master_add.html')

def admin_disease_master_edit(request):
    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        disease_name = request.POST.get('disease_name')
        disease_descp = request.POST.get('disease_descp')
        dm = disease_master.objects.get(id=int(s_id))
        dm.disease_name = disease_name
        dm.disease_descp = disease_descp
        dm.save()
        msg = 'Record Updated'
        dm_l = disease_master.objects.all()
        context = {'disease_list': dm_l, 'msg': msg}
        return render(request, './myapp/admin_disease_master_view.html', context)
    else:
        id = request.GET.get('id')
        dm = disease_master.objects.get(id=int(id))
        context = {'disease_name':dm.disease_name,'disease_descp':dm.disease_descp,'s_id':dm.id}
        return render(request, './myapp/admin_disease_master_edit.html',context)

def admin_disease_master_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    dm = disease_master.objects.get(id=int(id))
    dm.delete()
    msg = 'Record Deleted'
    dm_l = disease_master.objects.all()
    context = {'disease_list': dm_l,'msg':msg}
    return render(request, './myapp/admin_disease_master_view.html',context)

def admin_disease_master_view(request):

    dm_l = disease_master.objects.all()
    context = {'disease_list':dm_l}
    return render(request, './myapp/admin_disease_master_view.html',context)

from .models import drug_master

def admin_drug_master_add(request):
    if request.method == 'POST':

        drug_name = request.POST.get('drug_name')
        drug_details = request.POST.get('drug_details')
        company_details = request.POST.get('company_details')
        dosage_details = request.POST.get('dosage_details')

        dm = drug_master(drug_name=drug_name,drug_details=drug_details,company_details=company_details,dosage_details=dosage_details)
        dm.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/admin_drug_master_add.html', context)
    else:
        return render(request, './myapp/admin_drug_master_add.html')

def admin_drug_master_edit(request):
    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        drug_name = request.POST.get('drug_name')
        drug_details = request.POST.get('drug_details')
        company_details = request.POST.get('company_details')
        dosage_details = request.POST.get('dosage_details')

        dm = drug_master.objects.get(id=int(s_id))
        dm.drug_name = drug_name
        dm.drug_details = drug_details
        dm.company_details = company_details
        dm.dosage_details = dosage_details
        dm.save()
        msg = 'Record Updated'
        dm_l = drug_master.objects.all()
        context = {'drug_list': dm_l, 'msg': msg}
        return render(request, './myapp/admin_drug_master_view.html', context)
    else:
        id = request.GET.get('id')
        dm = drug_master.objects.get(id=int(id))
        context = {'drug_name':dm.drug_name,'drug_details':dm.drug_details,'company_details':dm.company_details,'dosage_details':dm.dosage_details,'s_id':dm.id}
        return render(request, './myapp/admin_drug_master_edit.html',context)

def admin_drug_master_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    dm = drug_master.objects.get(id=int(id))
    dm.delete()
    msg = 'Record Deleted'
    dm_l = drug_master.objects.all()
    context = {'drug_list': dm_l,'msg':msg}
    return render(request, './myapp/admin_drug_master_view.html',context)

def admin_drug_master_view(request):

    dm_l = drug_master.objects.all()
    context = {'drug_list':dm_l}
    return render(request, './myapp/admin_drug_master_view.html',context)


################### Doctor Functions

from .models import doctor_master

from django.core.files.storage import FileSystemStorage
def doctor_details_add(request):
    if request.method == 'POST':

        d_descp = request.POST.get('d_descp')
        d_qualification = request.POST.get('d_qualification')

        u_file = request.FILES['document']
        fs = FileSystemStorage()
        photo = fs.save(u_file.name, u_file)

        d_category = request.POST.get('d_category')
        #dt = datetime.today().strftime('%Y-%m-%d')
        #tm = datetime.today().strftime('%H:%M:%S')

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = '1234'
        uname=email
        status = "new"

        ul = user_login(uname=uname, passwd=password, u_type='doctor')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        dm = doctor_master(d_descp=d_descp,d_qualification=d_qualification,d_category=d_category,user_id=user_id,fname=fname, lname=lname,  contact=contact,
                               status=status,email=email)
        dm.save()

        print(user_id)
        context = { 'msg': 'Record Added'}
        return render(request, 'myapp/doctor_login.html',context)

    else:
        return render(request, 'myapp/doctor_details_add.html')

def doctor_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='doctor')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/doctor_home.html')
        else:
            msg = 'Invalid Uname or Password !!!'
            context ={ 'msg':msg }
            return render(request, './myapp/doctor_login.html',context)
    else:
        msg = ''
        context ={ 'msg':msg }
        return render(request, './myapp/doctor_login.html',context)


def doctor_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return doctor_login(request)
    else:
        return render(request,'./myapp/doctor_home.html')

def doctor_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return doctor_login(request)
    else:
        return doctor_login(request)

def doctor_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='doctor')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/doctor_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/doctor_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/doctor_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/doctor_changepassword.html', context)


def doctor_symptom_master_add(request):
    if request.method == 'POST':

        symptom_name = request.POST.get('symptom_name')

        sd = symptom_master(symptom_name=symptom_name)
        sd.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/doctor_symptom_master_add.html', context)
    else:
        return render(request, './myapp/doctor_symptom_master_add.html')

def doctor_symptom_master_edit(request):
    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        symptom_name = request.POST.get('symptom_name')
        sd = symptom_master.objects.get(id=int(s_id))

        sd.symptom_name = symptom_name
        sd.save()
        msg = 'Record Updated'
        sd_l = symptom_master.objects.all()
        context = {'symptom_list': sd_l, 'msg': msg}
        return render(request, './myapp/doctor_symptom_master_view.html', context)
    else:
        id = request.GET.get('id')
        sd = symptom_master.objects.get(id=int(id))
        context = {'symptom_name':sd.symptom_name,'s_id':sd.id}
        return render(request, './myapp/admin_symptom_master_edit.html',context)

def doctor_symptom_master_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    sd = symptom_master.objects.get(id=int(id))
    sd.delete()
    msg = 'Record Deleted'
    sd_l = symptom_master.objects.all()
    context = {'symptom_list': sd_l,'msg':msg}
    return render(request, './myapp/doctor_symptom_master_view.html',context)

def doctor_symptom_master_view(request):

    sd_l = symptom_master.objects.all()
    context = {'symptom_list':sd_l}
    return render(request, './myapp/doctor_symptom_master_view.html',context)


def doctor_disease_master_add(request):
    if request.method == 'POST':

        disease_name = request.POST.get('disease_name')
        disease_descp = request.POST.get('disease_descp')

        dm = disease_master(disease_name=disease_name,disease_descp=disease_descp)
        dm.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/doctor_disease_master_add.html', context)
    else:
        return render(request, './myapp/doctor_disease_master_add.html')

def doctor_disease_master_edit(request):
    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        disease_name = request.POST.get('disease_name')
        disease_descp = request.POST.get('disease_descp')
        dm = disease_master.objects.get(id=int(s_id))
        dm.disease_name = disease_name
        dm.disease_descp = disease_descp
        dm.save()
        msg = 'Record Updated'
        dm_l = disease_master.objects.all()
        context = {'disease_list': dm_l, 'msg': msg}
        return render(request, './myapp/doctor_disease_master_view.html', context)
    else:
        id = request.GET.get('id')
        dm = disease_master.objects.get(id=int(id))
        context = {'disease_name':dm.disease_name,'disease_descp':dm.disease_descp,'s_id':dm.id}
        return render(request, './myapp/doctor_disease_master_edit.html',context)

def doctor_disease_master_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    dm = disease_master.objects.get(id=int(id))
    dm.delete()
    msg = 'Record Deleted'
    dm_l = disease_master.objects.all()
    context = {'disease_list': dm_l,'msg':msg}
    return render(request, './myapp/doctor_disease_master_view.html',context)

def doctor_disease_master_view(request):

    dm_l = disease_master.objects.all()
    context = {'disease_list':dm_l}
    return render(request, './myapp/doctor_disease_master_view.html',context)


def doctor_drug_master_add(request):
    if request.method == 'POST':

        drug_name = request.POST.get('drug_name')
        drug_details = request.POST.get('drug_details')
        company_details = request.POST.get('company_details')
        dosage_details = request.POST.get('dosage_details')

        dm = drug_master(drug_name=drug_name,drug_details=drug_details,company_details=company_details,dosage_details=dosage_details)
        dm.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/doctor_drug_master_add.html', context)
    else:
        return render(request, './myapp/doctor_drug_master_add.html')

def doctor_drug_master_edit(request):
    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        drug_name = request.POST.get('drug_name')
        drug_details = request.POST.get('drug_details')
        company_details = request.POST.get('company_details')
        dosage_details = request.POST.get('dosage_details')

        dm = drug_master.objects.get(id=int(s_id))
        dm.drug_name = drug_name
        dm.drug_details = drug_details
        dm.company_details = company_details
        dm.dosage_details = dosage_details
        dm.save()
        msg = 'Record Updated'
        dm_l = drug_master.objects.all()
        context = {'drug_list': dm_l, 'msg': msg}
        return render(request, './myapp/doctor_drug_master_view.html', context)
    else:
        id = request.GET.get('id')
        dm = drug_master.objects.get(id=int(id))
        context = {'drug_name':dm.drug_name,'drug_details':dm.drug_details,'company_details':dm.company_details,'dosage_details':dm.dosage_details,'s_id':dm.id}
        return render(request, './myapp/doctor_drug_master_edit.html',context)

def doctor_drug_master_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    dm = drug_master.objects.get(id=int(id))
    dm.delete()
    msg = 'Record Deleted'
    dm_l = drug_master.objects.all()
    context = {'drug_list': dm_l,'msg':msg}
    return render(request, './myapp/doctor_drug_master_view.html',context)

def doctor_drug_master_view(request):

    dm_l = drug_master.objects.all()
    context = {'drug_list':dm_l}
    return render(request, './myapp/doctor_drug_master_view.html',context)

from .models import disease_drug_map
def doctor_disease_drug_map_delete(request):
    id = request.GET.get('id')
    ddm =disease_drug_map.objects.get(id=int(id))
    ddm.delete()
    disease_id = request.GET.get('disease_id')
    ddm_l = disease_drug_map.objects.filter(disease_id=int(disease_id))
    dm_l = drug_master.objects.all()
    context = {'map_list': ddm_l, 'drug_list': dm_l, 'disease_id': disease_id}
    return render(request, './myapp/doctor_disease_drug_map_view.html', context)


def doctor_disease_drug_map_view(request):
    disease_id = request.GET.get('id')
    ddm_l = disease_drug_map.objects.filter(disease_id=int(disease_id))
    dm_l=drug_master.objects.all()
    context = {'map_list':ddm_l,'drug_list':dm_l,'disease_id':disease_id}
    return render(request, './myapp/doctor_disease_drug_map_view.html',context)

def doctor_disease_drug_view(request):
    disease_id = request.GET.get('disease_id')

    dm_l = drug_master.objects.all()
    context = {'drug_list':dm_l,'disease_id':disease_id}
    return render(request, './myapp/doctor_disease_drug_view.html',context)

def doctor_disease_drug_add(request):

    disease_id = int(request.GET.get('disease_id'))
    drug_id = int(request.GET.get('drug_id'))

    ddm = disease_drug_map(disease_id=disease_id,drug_id=drug_id)
    ddm.save()
    dm_l = disease_master.objects.all()
    context = {'disease_list': dm_l,'msg': 'Record Added'}
    return render(request, './myapp/doctor_disease_master_view.html', context)

from .models import disease_symptom_map

def doctor_disease_symptom_map_delete(request):
    id = request.GET.get('id')
    ddm =disease_symptom_map.objects.get(id=int(id))
    ddm.delete()
    disease_id = request.GET.get('disease_id')
    dsm_l = disease_symptom_map.objects.filter(disease_id=int(disease_id))
    sm_l = symptom_master.objects.all()
    context = {'map_list': dsm_l, 'symptom_list': sm_l, 'disease_id': disease_id}
    return render(request, './myapp/doctor_disease_symptom_map_view.html', context)


def doctor_disease_symptom_map_view(request):
    disease_id = request.GET.get('id')
    dsm_l = disease_symptom_map.objects.filter(disease_id=int(disease_id))
    sm_l=symptom_master.objects.all()
    context = {'map_list':dsm_l,'symptom_list':sm_l,'disease_id':disease_id}
    return render(request, './myapp/doctor_disease_symptom_map_view.html',context)

def doctor_disease_symptom_view(request):
    disease_id = request.GET.get('disease_id')

    sm_l = symptom_master.objects.all()
    context = {'symptom_list':sm_l,'disease_id':disease_id}
    return render(request, './myapp/doctor_disease_symptom_view.html',context)

def doctor_disease_symptom_add(request):

    disease_id = int(request.GET.get('disease_id'))
    symptom_id = int(request.GET.get('symptom_id'))

    dsm = disease_symptom_map(disease_id=disease_id,symptom_id=symptom_id)
    dsm.save()
    dm_l = disease_master.objects.all()
    context = {'disease_list': dm_l,'msg': 'Record Added'}
    return render(request, './myapp/doctor_disease_master_view.html', context)

import os
from .disease_classification import DiseaseClassification
from project.settings import BASE_DIR

def doctor_train_model(request):
    ##########training model############
    data_file_path = os.path.join(BASE_DIR, 'data/data_set.csv')
    # os.remove(data_file_path)

    obj_list = disease_symptom_map.objects.all()
    f = open(data_file_path, "w")
    f.write('text,label')
    f.write("\n")
    for obj in obj_list:
        dm = disease_master.objects.get(id=obj.disease_id)
        sm = symptom_master.objects.get(id=obj.symptom_id)

        f.write(f'{sm.symptom_name},{dm.disease_name}')
        f.write("\n")
    f.close()
    data_file_path = os.path.join(BASE_DIR, 'data/data_set.csv')
    data_file_label_path = os.path.join(BASE_DIR, 'data/data_set_label.dat')
    tfid_file_path = os.path.join(BASE_DIR, 'data/data_set_tfid.dat')
    model_file_path = os.path.join(BASE_DIR, 'data/data_set_svm.model')

    obj = DiseaseClassification()
    txt_result = obj.text_processing(data_file_path, data_file_label_path)
    obj.train_model(txt_result, tfid_file_path, model_file_path, 'svm')
    context = {'msg':'Training done and model created'}
    return render(request, './myapp/doctor_train_model.html', context)
    ################

def doctor_doctor_query_view(request):
    user_id = int(request.session['user_id'])
    dm = doctor_master.objects.get(user_id=user_id)
    udq_l = user_doctor_query.objects.filter(doctor_id=dm.id)
    dp_l = doctor_prescription.objects.filter(doctor_id=dm.id)
    dm_l = doctor_master.objects.all()
    dpl = {}
    for dp in dp_l:
        dpl[int(dp.status)] = dp.prescription

    context = {'query_list': udq_l, 'doctor_list': dm_l, 'prescription_list': dpl}
    return render(request, './myapp/doctor_doctor_query_view.html', context)


def doctor_doctor_query_search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        user_id = int(request.session['user_id'])
        dm = doctor_master.objects.get(user_id=user_id)
        udq_l = user_doctor_query.objects.filter(doctor_id=dm.id,query__contains=query)
        dp_l = doctor_prescription.objects.filter(doctor_id=dm.id)
        dm_l = doctor_master.objects.all()
        dpl = {}
        for dp in dp_l:
            dpl[int(dp.status)] = dp.prescription
        context = {'query_list': udq_l, 'doctor_list': dm_l, 'prescription_list': dpl}
        return render(request, './myapp/doctor_doctor_query_view.html', context)
    else:
        context = {}
        return render(request, './myapp/doctor_doctor_query_search.html', context)

def doctor_doctor_query_search2(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        user_id = int(request.session['user_id'])
        dm = doctor_master.objects.get(user_id=user_id)
        udq_l = user_doctor_query.objects.filter(doctor_id=dm.id,dt=query)
        dp_l = doctor_prescription.objects.filter(doctor_id=dm.id)
        dm_l = doctor_master.objects.all()
        dpl = {}
        for dp in dp_l:
            dpl[int(dp.status)] = dp.prescription
        context = {'query_list': udq_l, 'doctor_list': dm_l, 'prescription_list': dpl}
        return render(request, './myapp/doctor_doctor_query_view.html', context)
    else:
        context = {}
        return render(request, './myapp/doctor_doctor_query_search2.html', context)

def doctor_doctor_query_update(request):
    if request.method == 'POST':
        s_id = request.POST.get('s_id')

        reply = request.POST.get('reply')
        r_dt = datetime.today().strftime('%Y-%m-%d')
        r_tm = datetime.today().strftime('%H:%M:%S')
        prescription = request.POST.get('prescription')
        udq = user_doctor_query.objects.get(id=int(s_id))
        udq.reply = reply
        udq.r_dt = r_dt
        udq.t_tm = r_tm
        udq.save()

        dp = doctor_prescription.objects.get(status=str(s_id))
        dp.prescription = prescription
        dp.save()

        user_id = int(request.session['user_id'])
        dm = doctor_master.objects.get(user_id=user_id)
        udq_l = user_doctor_query.objects.filter(doctor_id=dm.id)
        dp_l = doctor_prescription.objects.filter(doctor_id=dm.id)
        dm_l = doctor_master.objects.all()
        dpl = {}
        for dp in dp_l:
            dpl[int(dp.status)] = dp.prescription

        context = {'query_list': udq_l, 'doctor_list': dm_l, 'prescription_list': dpl}
        return render(request, './myapp/doctor_doctor_query_view.html', context)

    else:
        s_id = request.GET.get('id')

        context = { 's_id': s_id}
        return render(request, './myapp/doctor_doctor_query_update.html', context)


################# User Functions
from .models import user_details
def user_details_add(request):
    if request.method == 'POST':

        addr1 = request.POST.get('addr1')
        addr2 = request.POST.get('addr2')
        addr3 = request.POST.get('addr3')
        #dt = datetime.today().strftime('%Y-%m-%d')
        #tm = datetime.today().strftime('%H:%M:%S')

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = '1234'
        uname=email
        status = "new"

        ul = user_login(uname=uname, passwd=password, u_type='user')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = user_details(user_id=user_id,fname=fname, lname=lname, gender=gender, pin=pin, contact=contact,
                               status=status,email=email,dob=dob,addr1=addr1,
                          addr2=addr2,addr3=addr3)
        ud.save()

        print(user_id)
        context = { 'msg': 'Record Added'}
        return render(request, 'myapp/user_login.html',context)

    else:
        return render(request, 'myapp/user_details_add.html')

def user_login_check(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='user')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/user_home.html')
        else:
            msg = 'Invalid Uname or Password !!!'
            context ={ 'msg':msg }
            return render(request, './myapp/user_login.html',context)
    else:
        msg = ''
        context ={ 'msg':msg }
        return render(request, './myapp/user_login.html',context)


def user_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return user_login_check(request)
    else:
        return render(request,'./myapp/user_home.html')

def user_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return user_login_check(request)
    else:
        return user_login_check(request)

def user_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='doctor')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/user_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/user_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/user_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/user_changepassword.html', context)

from datetime import datetime
from .models import user_doctor_query
from .models import doctor_prescription

def user_doctor_query_add(request):
    if request.method == 'POST':

        doctor_id = request.POST.get('doctor_id')
        query = request.POST.get('query')

        reply = ' '
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        r_dt = ' '
        r_tm = ' '
        user_id = int(request.session['user_id'])
        prescription = ' '
        status='new'
        if doctor_id == str(0) :
            print(query)
            ####################PREDICTION##############
            obj = DiseaseClassification()
            result = obj.input_text_processing(query)
            data_file_path = os.path.join(BASE_DIR, 'data/data_set.csv')
            data_file_label_path = os.path.join(BASE_DIR, 'data/data_set_label.dat')
            tfid_file_path = os.path.join(BASE_DIR, 'data/data_set_tfid.dat')
            model_file_path = os.path.join(BASE_DIR, 'data/data_set_svm.model')

            model = obj.load_data(model_file_path)
            Tfidf_vect = obj.load_data(tfid_file_path)
            p = obj.get_prediction(model, result, Tfidf_vect)
            label = obj.load_data(data_file_label_path)
            label = sorted(label)
            print(f'result = {label[p[0]]}')
            final_label = label[p[0]]
            dm = disease_master.objects.get(disease_name=final_label)
            reply = f'{dm.disease_name} - {dm.disease_descp}'
            ddm_l = disease_drug_map.objects.filter(disease_id=dm.id)
            for ddm in ddm_l:
                dm =drug_master.objects.get(id=ddm.drug_id)
                print(prescription)
                prescription = prescription + f'{dm.drug_name}-{dm.drug_details},'
            r_dt =dt
            r_tm =tm
            ############################
            udq = user_doctor_query(doctor_id=int(doctor_id), query=query, reply=reply, dt=dt,
                                    tm=tm, r_dt=r_dt, r_tm=r_tm, user_id=user_id, status=status)
            udq.save()

            query_id = user_doctor_query.objects.all().aggregate(Max('id'))['id__max']
            dp = doctor_prescription(prescription=prescription,status=str(query_id), doctor_id=doctor_id, user_id=user_id, dt=dt, tm=tm)
            dp.save()

        else:
            udq = user_doctor_query(doctor_id=int(doctor_id),query=query,reply=reply,dt=dt,
                                tm=tm,r_dt=r_dt,r_tm=r_tm,user_id=user_id,status=status )
            udq.save()

            query_id = user_doctor_query.objects.all().aggregate(Max('id'))['id__max']
            dp = doctor_prescription(prescription=prescription,status=str(query_id),doctor_id=doctor_id,user_id=user_id,dt=dt,tm=tm)
            dp.save()

        dm_l = doctor_master.objects.all()
        context = {'msg': 'Record Added','doctor_list':dm_l}
        return render(request, './myapp/user_doctor_query_add.html', context)
    else:
        dm_l = doctor_master.objects.all()
        context = { 'doctor_list': dm_l}
        return render(request, './myapp/user_doctor_query_add.html', context)


def user_doctor_query_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    udq = user_doctor_query.objects.get(id=int(id))
    dp = doctor_prescription.objects.get(status=id)
    dp.delete()
    udq.delete()
    msg = 'Record Deleted'
    user_id = int(request.session['user_id'])
    udq_l = user_doctor_query.objects.filter(user_id=user_id)
    dp_l = doctor_prescription.objects.all()
    dpl = {}
    for dp in dp_l:
        dpl[int(dp.status)] = dp.prescription
    dm_l = doctor_master.objects.all()
    context = {'query_list': udq_l,'doctor_list': dm_l,'prescription_list': dpl,'msg':msg}
    return render(request, './myapp/user_doctor_query_view.html',context)

def user_doctor_query_view(request):
    user_id = int(request.session['user_id'])
    udq_l = user_doctor_query.objects.filter(user_id=user_id)
    dp_l = doctor_prescription.objects.filter(user_id=user_id)
    dm_l = doctor_master.objects.all()
    dpl = {}
    for dp in dp_l:
        dpl[int(dp.status)] = dp.prescription

    context = {'query_list': udq_l, 'doctor_list': dm_l, 'prescription_list': dpl}
    return render(request, './myapp/user_doctor_query_view.html', context)

from .models import doctor_master
def admin_view_doctor(request):
    doctor_list = doctor_master.objects.all()
    context = {'doctor_list': doctor_list}
    return render(request, './myapp/user_view_doctor.html', context)

from .models import user_details
def admin_view_users(request):
        user_list = user_details.objects.all()
        context = {'user_list': user_list}
        return render(request, './myapp/admin_view_users.html', context)


def user_view_doctor(request):
    doctor_list = doctor_master.objects.all()
    context = {'doctor_list': doctor_list}
    return render(request, './myapp/user_view_doctor.html', context)

def user_search_doctor(request):
    if request.method == 'POST':
       query = request.POST.get('query')
       pd_l = doctor_master.objects.filter(d_category__contains=query)
       context = {'doctor_list': pd_l}
       return render(request, './myapp/user_view_doctor.html', context)
    else:
       return render(request, 'myapp/user_search_doctor.html')

from .models import doctor_appointment
from datetime import datetime
def user_book_appointment(request):
    if request.method == 'POST':
        doctor_id = request.GET.get('doctor_id')
        user_id = request.GET.get('user_id')
        dt = request.GET.get('dt')
        tm = request.GET.get('tm')
        status = request.GET.get('status')

        ud = doctor_appointment(doctor_id=doctor_id, user_id=user_id, dt=dt, tm=tm, status=status)
        ud.save()
        print(user_id)
        context = {'msg': 'Booking success'}

        return render(request, 'myapp/user_book_appointment.html', context)
    else:
      return render(request, 'myapp/user_book_appointment.html')
