from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from module.getScore import getStudentScore
from module.processingScore import transformChartData
def login(request):
    if request.method == "POST":
        # migration migrates를 해야 session table이 생성됨
        request.session['studentID'] = request.POST["studentid"]
        request.session['passwd'] = request.POST["passwd"]

        return render(request,"loading.html")

    return render(request, "login.html")


@csrf_exempt
def get_score(request):
    if request.method == 'POST':
        studentID = request.session.get('studentID')
        passwd = request.session.get('passwd')
        allScore = getStudentScore(studentID, passwd)
        del request.session['studentID']
        del request.session['passwd']
        print(allScore)
        newScore = transformChartData(allScore)
        request.session['newScore'] = newScore

        # chart를 위해 js에서 사용
        return JsonResponse({'newScore':newScore})
