from django.shortcuts import render

# Create your views here.


def viewScores(request):
    allScore = request.session.get('allScore')
    return render(request, "viewScores.html", {'allScore': allScore})