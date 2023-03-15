from django.shortcuts import render
import urllib.request, json
import urllib, json
from django.http import HttpResponse
import requests
import datetime
import re






def home(request):
    # print()
    # print("user check")
    # print(request.user.username)
    # print(request.user.id)

    # return render(request, "../templates/HomePage.html")

    # with urllib.request.urlopen("https://interviews.bigvu.tv/course/list") as url:
    #     data = json.load(url)
    #     print(data)
    response = requests.get('https://interviews.bigvu.tv/course/list', auth=('bigvu', 'interview'))
    data = response.json()
    # print(data)
    for course in data["result"]:
        response = requests.get('https://interviews.bigvu.tv/course/' + str(course['id']), auth=('bigvu', 'interview'))
        course["amount_of_videos"] = len(response.json())


    print(data["result"])


    # return HttpResponse(data["result"])
    return render(request, "../templates/HomePage.html", {"data": data["result"]})


def course(request, question_id):
    chapters = list()
    response = requests.get('https://interviews.bigvu.tv/course/'+str(question_id), auth=('bigvu', 'interview'))
    data = response.json()
    print(data)
    for chapter in data['chapters']:
        # my_new_string = re.sub('[!?]', "", my_string)
        duration = datetime.timedelta(seconds=chapter["asset"]['resource']['duration'])

        # removes microseconds
        duration = str(duration).split('.')[0]

        # removes minutes
        duration = duration.split(":", 1)[1]

        chapter["asset"]['resource']['duration'] = duration

        chapters.append(chapter)

    default_video = data['chapters'][0]


    return render(request, "../templates/CoursePage.html", {"course": data,"default_video": default_video})
