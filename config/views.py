from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.cache import never_cache


from module.getScore import getStudentScore
from module.processingScore import transformChartData


def login(request):
    if request.method == "POST" and request.session['post'] is False:
        request.session['post'] = True
        # migration migrates를 해야 session table이 생성됨
        request.session['studentID'] = request.POST["studentid"]
        request.session['passwd'] = request.POST["passwd"]

        return redirect('loading')

    request.session['post'] = False
    return render(request, "login.html")

@never_cache
def loading(request):
    if request.session.get('post') is True:
        return render(request, "loading.html")

    return redirect('/')

@csrf_exempt
def get_score(request):
    if request.method == 'POST' and request.session.get('post') is True:
        request.session['post'] = False
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

    return JsonResponse({})