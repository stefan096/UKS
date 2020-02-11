from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from miniGithub.models import Project, Change_Code, Problem
import re


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
                creator = commit["committer"]
                created_time = commit["timestamp"]
                commit_id = commit["id"]

                problems_strings = re.findall(r"#\d+", message)
                print(problems_strings)

                flag = False
                for one_strings in problems_strings:
                    key = int(one_strings[1:])
                    try:
                        found_problem = Problem.objects.get(pk=key)
                    except:
                        found_problem = False

                    if found_problem:
                        change_code = Change_Code.create(commit_url, commit_id, message, created_time,
                                                         creator["username"], creator["email"], project)
                        change_code.problem = found_problem
                        change_code.save()
                        flag = True

                if not flag:
                    change_code = Change_Code.create(commit_url, commit_id, message, created_time,
                                                     creator["username"], creator["email"], project)

        return HttpResponse('Succefully finished with parsing webhook')
    except:
        return HttpResponse('Exception occuer when parsing webhook')
