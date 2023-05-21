from django.shortcuts import render

# Create your views here.


def viewScores(request):
    newScore = request.session.get('newScore')
    return render(request, "viewScores.html", {'newScore': newScore})