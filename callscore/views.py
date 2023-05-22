from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.


def viewScores(request):
    newScore = request.session.get('newScore')
    if newScore is None:
        return redirect("/")

    return render(request, "viewScores.html", {'newScore': newScore})