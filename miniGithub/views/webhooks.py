from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def webhook_push(request):
    try:
        body_string = request.body.decode("utf-8")
        json_data = json.loads(body_string)
        commits = json_data['commits']
        project_url = json_data["repository"]["html_url"]
        print(project_url)
        for commit in commits:
            url_commit = commit["url"]
            message = commit["message"]
            author = commit["committer"]
            timestamp = commit["timestamp"]
            commit_id = commit["id"]
            print(url_commit)
            print(commit_id)
            print(message)
            print(author)
            print(timestamp)
        return HttpResponse('Succefully finished with parsing webhook')
    except:
        return HttpResponse('Exception occuer when parsing webhook')
