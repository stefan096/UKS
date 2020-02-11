from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from miniGithub.models import Project, Change_Code


@csrf_exempt
def webhook_push(request):
    try:
        body_string = request.body.decode("utf-8")
        json_data = json.loads(body_string)
        commits = json_data['commits']
        project_url = json_data["repository"]["html_url"]
        project = Project.objects.get(git_repo=project_url)

        if project:
            for commit in commits:
                commit_url = commit["url"]
                message = commit["message"]
                #izvuci iz poruke da li je referenciran neki problem
                #
                creator = commit["committer"]
                created_time = commit["timestamp"]
                commit_id = commit["id"]
                comment = Change_Code.create(commit_url, commit_id, message, created_time, creator["username"], creator["email"], project)
                print(commit_id)
                print(message)
                print(creator)
        return HttpResponse('Succefully finished with parsing webhook')
    except:
        return HttpResponse('Exception occuer when parsing webhook')
