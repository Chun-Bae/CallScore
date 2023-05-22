import copy

def transformChartData(allScore):
    newScore = {}

    for i in range(len(allScore.keys())):

        newScore[i] = {"Name":"","Course": [], "CreditHours": [], "Grade": [], "Score": [], "GradePoints": [], "TotalGrade": 0,"AvgScore": 0, "AvgGradePoints": 0 }

        newScore[i]["Name"] = allScore[i]["name"]
        newScore[i]["Course"] = [subject for subject in allScore[i]["semester"]["subject"]]
        newScore[i]["CreditHours"] = [credit for credit in allScore[i]["semester"]["credit"]]
        newScore[i]["Grade"] = [grade for grade in allScore[i]["semester"]["grade"]]
        newScore[i]["Score"] = [score for score in allScore[i]["semester"]["score"]]
        newScore[i]["GradePoints"] = [rating for rating in allScore[i]["semester"]["rating"]]
        newScore[i]["TotalGrade"] = allScore[i]["figure"]["acq_creidt"]
        newScore[i]["AvgScore"] = allScore[i]["figure"]["r_scores_avg"]
        newScore[i]["AvgGradePoints"] = allScore[i]["figure"]["rating_avg"]

    return newScore