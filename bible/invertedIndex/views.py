from django.shortcuts import render
from invertedIndex.mainFunction import inputASV,inputKJV,inputMKJV,inputNHEB,inputRSV


# Create your views here.
def index (request) :
    return render (request, 'invertedIndex/index.html')

def indexASV (request) :
    return render (request, 'invertedIndex/ASVindex.html')

def indexKJV(request):
    return render(request, 'invertedIndex/KJVindex.html')

def indexMKJV(request):
    return render(request,'invertedIndex/MKJVindex.html')

def indexNHEB(request):
    return render(request,'invertedIndex/NHEBindex.html')

def indexRSV(request):
    return render(request, 'invertedIndex/RSVindex.html')

def preprocessingInputKJV(request):
    if request.method == 'POST' :
        textKJV = request.POST['wordKJV']
        calKJV = inputKJV.mainKJV(textKJV)
        contextKJV = {'calKJV':calKJV, 'textKJV':textKJV}
        return render(request,'invertedIndex/KJVresult.html',contextKJV)
    return render(request, 'invertedIndex/index.html')

def preprocessingInputASV(request):
    if request.method == 'POST' :
        textASV = request.POST['wordASV']
        queryASV = inputASV.processQuery(textASV)
        calASV = inputASV.mainASV(textASV)
        contextASV = {'calASV':calASV, 'textASV':textASV, 'queryASV':queryASV}
        return render(request,'invertedIndex/ASVresult.html',contextASV)
    return render(request, 'invertedIndex/index.html')

def preprocessingInputMKJV(request):
    if request.method == 'POST' :
        textMKJV = request.POST['wordMKJV']
        calMKJV = inputMKJV.mainMKJV(textMKJV)
        contextMKJV = {'calMKJV':calMKJV, 'textMKJV':textMKJV}
        return render(request,'invertedIndex/MKJVresult.html',contextMKJV)
    return render(request, 'invertedIndex/index.html')

def preprocessingInputNHEB(request):
    if request.method == 'POST' :
        textNHEB = request.POST['wordNHEB']
        calNHEB = inputNHEB.mainNHEB(textNHEB)
        contextNHEB = {'calNHEB':calNHEB, 'textNHEB':textNHEB}
        return render(request,'invertedIndex/NHEBresult.html',contextNHEB)
    return render(request, 'invertedIndex/index.html')

def preprocessingInputRSV(request):
    if request.method == 'POST' :
        textRSV = request.POST['wordRSV']
        calRSV = inputRSV.mainRSV(textRSV)
        contextRSV = {'calRSV':calRSV, 'textRSV':textRSV}
        return render(request,'invertedIndex/RSVresult.html',contextRSV)
    return render(request, 'invertedIndex/index.html')
