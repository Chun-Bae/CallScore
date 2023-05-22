from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from module.getScore import getStudentScore
from module.processingScore import transformChartData
def login(request):
    if request.method == "POST":
        request.session['post'] = True
        # migration migrates를 해야 session table이 생성됨
        request.session['studentID'] = request.POST["studentid"]
        request.session['passwd'] = request.POST["passwd"]

        return redirect('loading')

    return render(request, "login.html")

def loading(request):
    isPost = request.session.get('post')

    if isPost is True:
        request.session['post'] = False
        return render(request, "loading.html")

    return redirect('/')

@csrf_exempt
def get_score(request):
    if request.method == 'POST' and not request.session['post']:
        studentID = request.session.get('studentID')
        passwd = request.session.get('passwd')

        allScore = getStudentScore(studentID, passwd)
        newScore = transformChartData(allScore)

        request.session['newScore'] = newScore

        return JsonResponse({})

@csrf_exempt
def del_score(request):
    del request.session['newScore']
    del request.session['studentID']
    del request.session['passwd']
    request.session['post'] = False

    return JsonResponse({})