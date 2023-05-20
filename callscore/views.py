from django.shortcuts import render

# Create your views here.


def viewScores(request):

    return render(request, "allScores.html")