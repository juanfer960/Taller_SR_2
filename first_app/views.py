from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from .models import PREDICTION_CHART
from .models import Registry
from .models import review, business, tip, userData
from .models import Document_features,Categorie,DfReview_train,DfReview_test,Prediction
from . import forms
from first_app.forms import NewUserForm,FormName
from sklearn.model_selection import train_test_split
import pickle
from sklearn import svm
from sklearn.metrics import classification_report

# imports SR

import pandas as pd
import numpy as np

# Create your views here.

def index(request):
    return render(request,'index.html')


def login(request):
    form = NewUserForm()

    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['user']
            password = form.cleaned_data['password']

            #rs()

            predictions = Prediction.objects.filter(user_id = password, mark = 'True')[:10]

            con = 1
            dataRes_1 = []
            dataRes_2 = []
            dataRes_3 = []

            for prediction in predictions:
                busines = business.objects.filter(business_id = prediction.business_id).first()

                if(con <= 3):
                    try:
                        dataRes_1.append(busines.name)
                        con = con+1
                    except:
                        print('error')
                else:
                    if(con <=6):
                        try:
                            dataRes_2.append(busines.name)
                            con = con+1
                        except:
                            print('error')
                    else:
                        if(con <= 9):
                            try:
                                dataRes_3.append(busines.name)
                                con = con+1
                            except:
                                print('error')
                        else:
                            break

            dataRes = {'user': user, 'password': password,'dataRes_uno':dataRes_1,'dataRes_dos':dataRes_2,'dataRes_tres':dataRes_3,}

            if userValid(user,password):
                return  render(request,'basicapp/workPage.html',context=dataRes)

            else:
                data = {'user': 'null', 'password': 'null'}
                form = NewUserForm(data)
                form.is_valid()

                return render(request,'basicapp/pageError.html')

    return render(request,'basicapp/login.html',{'form':form})


def logup(request):
    form = NewUserForm()

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return render(request,'basicapp/successPage.html')
        else:
            print('ERROR FORM INVALID')

    return render(request,'basicapp/logup.html',{'form':form})


def userValid (user, password):
    try:
        User.objects.get(user = user, password =  password)
        print(User)
    except:
        return False

    return True


def singout(request):
    return render(request,'index.html')


def search(request,**kwargs):

    user = kwargs['user']
    password = kwargs['password']
    dataRes = {'user': user, 'password': password}

    return  render(request,'basicapp/search.html',context=dataRes)


def search(request,**kwargs):
    form = forms.FormSearch()

    user = kwargs['user']
    password = kwargs['password']
    dataRes = {'user': user, 'password': password,'form':form}

    return  render(request,'basicapp/search.html',context=dataRes)


def home(request,**kwargs):

    user = kwargs['user']
    password = kwargs['password']

    #rs()

    print('************************')
    print(password)
    print('************************')

    predictions = Prediction.objects.filter(user_id = password, mark = 'True')[:10]

    con = 1
    dataRes_1 = []
    dataRes_2 = []
    dataRes_3 = []

    for prediction in predictions:
        busines = business.objects.filter(business_id = prediction.business_id).first()

        if(con <= 3):
            try:
                dataRes_1.append(busines.name)
                con = con+1
            except:
                print('error')
        else:
            if(con <=6):
                try:
                    dataRes_2.append(busines.name)
                    con = con+1
                except:
                    print('error')
            else:
                if(con <= 9):
                    try:
                        dataRes_3.append(busines.name)
                        con = con+1
                    except:
                        print('error')
                else:
                    break

    dataRes = {'user': user, 'password': password,'dataRes_uno':dataRes_1,'dataRes_dos':dataRes_2,'dataRes_tres':dataRes_3,}

    return  render(request,'basicapp/workPage.html',context=dataRes)


def businessA(request,**kwargs):

    user = kwargs['user']
    password = kwargs['password']

    dataRes_1 = []
    dataRes_2 = []
    dataRes_3 = []


    business_ = business.objects.all()[:10]

    for busines in business_:
        print('***********************************************')
        print(busines.name)
        print('***********************************************')

    dataRes = {'user': user, 'password': password,'dataRes_uno':dataRes_1,'dataRes_dos':dataRes_2,'dataRes_tres':dataRes_3,}

    return  render(request,'basicapp/workPage.html',context=dataRes)


def analysis(request,**kwargs):

    user=kwargs['user']
    password=kwargs['password']

    predictions = PREDICTION_CHART.objects.filter(userId = user, prediction__isnull = False).order_by('prediction')

    dataRes_artistName = []
    dataRes_artistId = []
    dataRes_prediction = []

    for prediction in reversed(predictions):
        dataRes_artistId.append(prediction.artistId)
        dataRes_prediction.append(prediction.prediction)
        artistName = Registry.objects.filter(musicbrainzArtistId = prediction.artistId).first()
        dataRes_artistName.append(artistName.artistName)

    dataRes = {'user': user, 'password': password,'dataRes_artistName':dataRes_artistName,'dataRes_artistId':dataRes_artistId,'dataRes_prediction':dataRes_prediction}
    return  render(request,'basicapp/analysis.html',context=dataRes)


def songSerch(request,**kwargs):
    form = forms.FormSearch()
    dataRes_  = []
    user=kwargs['user']
    password=kwargs['password']
    dataRes = {}

    if request.method == 'POST':
        form = forms.FormSearch(request.POST)

        con = 0
        if form.is_valid():
            busines = business.objects.filter(city = form.cleaned_data['search'])
            for oneBusines in busines:
                predictions = Prediction.objects.filter(business_id = oneBusines.business_id, user_id = password ,mark = 'True').first()
                try:
                    predictions.user_id
                    if(con < 10):
                        dataRes_.append(oneBusines.name)
                        con = con +1
                    else:
                        break
                except:
                    print('ERROR')
                    #dataRes = {'user': user, 'password': user}

                dataRes = {'user': user, 'password': password,'form':form, 'dataRes_':dataRes_}

        return  render(request,'basicapp/search.html',context=dataRes)

    return  render(request,'basicapp/search.html',context=dataRes)


def scoreone(request,**kwargs):
    user=kwargs['user']
    password=kwargs['password']
    artist=kwargs['dataRes']
    print('************************************ UNO'+artist)
    dataRes = {'user': user, 'password': user}
    return render(request,'basicapp/infoScorePage.html',context=dataRes)


def scoretwo(request,**kwargs):
    user=kwargs['user']
    print('************************************ DOS'+user)
    dataRes = {'user': user, 'password': user}
    return render(request,'basicapp/infoScorePage.html',context=dataRes)


def scorethree(request,**kwargs):
    user=kwargs['user']
    print('************************************ TRES'+user)
    dataRes = {'user': user, 'password': user}
    return render(request,'basicapp/infoScorePage.html',context=dataRes)


def scorefour(request,**kwargs):
    user=kwargs['user']
    print('************************************ CUATRO'+user)
    dataRes = {'user': user, 'password': user}
    return render(request,'basicapp/infoScorePage.html',context=dataRes)


def scorefive(request,**kwargs):
    user=kwargs['user']
    print('************************************ CINCO'+user)
    dataRes = {'user': user, 'password': user}
    return render(request,'basicapp/infoScorePage.html',context=dataRes)

def rs():

    print('******************************************************************************************************')

    print('******************************************************************************************************')
