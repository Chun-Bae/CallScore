from django.shortcuts import render

# Create your views here.


def viewScores(request):
    allScore = request.session.get('allScore')
    print("제발 나와라")
    print(allScore)
    return render(request, "viewScores.html", {'allScore': allScore})