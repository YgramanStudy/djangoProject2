from django.shortcuts import render
import urllib.request, json
import urllib, json
from django.http import HttpResponse
import requests
import datetime
from django.core.cache import cache
import re






def home(request):
    print("-----home-------")
    data = cache.get('data')
    if data is None:
        print("-----cache-------")
        data = requests.get('https://interviews.bigvu.tv/course/list', auth=('bigvu', 'interview')).json()
        cache.set('data', data)
    # response = requests.get('https://interviews.bigvu.tv/course/list', auth=('bigvu', 'interview'))
    # data = response.json()
    print(data)
    try:
        data = data['result']
    except:
        pass

    for temp_course in data:
        response = requests.get('https://interviews.bigvu.tv/course/' + str(temp_course['id']), auth=('bigvu', 'interview'))
        temp_course["amount_of_videos"] = len(response.json())


    # print(data["result"])


    # return HttpResponse(data["result"])
    return render(request, "../templates/HomePage.html", {"data": data})


def course(request, question_id):
    chapters = list()

    print("-----course-------")
    course = cache.get('course')
    try:
        course = course['result'][0]
    except:
        pass
    if course:
        print(course)
        if course['id'] != question_id:
            course = requests.get('https://interviews.bigvu.tv/course/' + str(question_id),
                            auth=('bigvu', 'interview')).json()
            cache.set('course', course)

    if course is None:
        print("-----cache-------")
        course = requests.get('https://interviews.bigvu.tv/course/'+str(question_id), auth=('bigvu', 'interview')).json()
        cache.set('data', course)

    # response = requests.get('https://interviews.bigvu.tv/course/'+str(question_id), auth=('bigvu', 'interview'))
    # data = response.json()

    try:
        course = course['result'][0]
    except:
        pass


    print(course)
    for chapter in course['chapters']:
        # my_new_string = re.sub('[!?]', "", my_string)
        duration = datetime.timedelta(seconds=chapter["asset"]['resource']['duration'])

        # removes microseconds
        duration = str(duration).split('.')[0]

        # removes minutes
        duration = duration.split(":", 1)[1]

        chapter["asset"]['resource']['duration'] = duration

        chapters.append(chapter)

    default_video = course['chapters'][0]


    return render(request, "../templates/CoursePage.html", {"course": course,"default_video": default_video})
