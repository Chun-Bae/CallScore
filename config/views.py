from django.shortcuts import render
from module.getScore import getStudentScore
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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

        request.session['allScore'] = allScore

        return JsonResponse({})
