
def transformChartData(allScore):
    newScore = {}
    s_len = len(allScore.keys())

    # 전체 학기

    newScore[0] = {"Name": "", "Course": "", "CreditHours": 0, "Grade": 0, "Score": 0, "GradePoints": 0,
                   "TotalGrade": 0, "AvgScore": 0, "AvgGradePoints": 0}

    newScore[0]["Name"] = "전체 학기"
    newScore[0]["Course"] = "-"
    newScore[0]["CreditHours"] = "-"
    newScore[0]["Grade"] = "-"
    newScore[0]["Score"] = "-"
    newScore[0]["GradePoints"] = "-"

    for semester in range(0, s_len):
        newScore[0]["TotalGrade"] += float(allScore[semester]["figure"]["acq_creidt"])
        newScore[0]["AvgScore"] += float(allScore[semester]["figure"]["r_scores_avg"])
        newScore[0]["AvgGradePoints"] += float(allScore[semester]["figure"]["acq_creidt"]) * float(allScore[semester]["figure"]["rating_avg"])

    newScore[0]["TotalGrade"] = int(newScore[0]["TotalGrade"])
    newScore[0]["AvgScore"] = round(newScore[0]["AvgScore"] / s_len, 2)
    newScore[0]["AvgGradePoints"]  = round((newScore[0]["AvgGradePoints"]/newScore[0]["TotalGrade"]),2)


    for i in range(1, s_len+1):
        newScore[i] = {"Name":"","Course": [], "CreditHours": [], "Grade": [], "Score": [], "GradePoints": [], "TotalGrade": 0,"AvgScore": 0, "AvgGradePoints": 0 }

        newScore[i]["Name"] = allScore[i-1]["name"]
        newScore[i]["Course"] = [subject for subject in allScore[i-1]["semester"]["subject"]]
        newScore[i]["CreditHours"] = [int(credit) for credit in allScore[i-1]["semester"]["credit"]]
        newScore[i]["Grade"] = [grade for grade in allScore[i-1]["semester"]["grade"]]
        newScore[i]["Score"] = [score for score in allScore[i-1]["semester"]["score"]]
        newScore[i]["GradePoints"] = [round(float(rating),1) for rating in allScore[i-1]["semester"]["rating"]]
        newScore[i]["TotalGrade"] = allScore[i-1]["figure"]["acq_creidt"]
        newScore[i]["AvgScore"] = allScore[i-1]["figure"]["r_scores_avg"]
        newScore[i]["AvgGradePoints"] = allScore[i-1]["figure"]["rating_avg"]

    print(newScore)

    return newScore