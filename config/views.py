from django.shortcuts import render
from django.shortcuts import redirect
from module.getScore import getStudentScore
def login(request):

    if request.method == "POST":
        studentID = request.POST["studentid"]
        passwd = request.POST["passwd"]
        context = {
            "studentID": studentID,
            "passwd" : passwd,
        }
        loading(request)
        #allScore = getStudentScore(studentID, passwd)

        return render(request,"viewScores.html",context)



    return render(request, "login.html")

def loading(request):
    return render(request, "viewScores.html")