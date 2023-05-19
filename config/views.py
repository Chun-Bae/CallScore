from django.shortcuts import render
from module.getScore import getStudentScore
def login(request):
    if request.method == "POST":
        studentID = request.POST["studentid"]
        passwd = request.POST["passwd"]
        print(studentID)
        print(passwd)
        getStudentScore(studentID, passwd)



    return render(request, "login.html")