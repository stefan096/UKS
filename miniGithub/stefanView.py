from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from miniGithub.models import Project

def detail(request, project_id):
    #return HttpResponse("You're looking at question %s." % question_id)

    # try:
    #     project = Project.objects.get(pk=question_id)
    # except Project.DoesNotExist:
    #     raise Http404("project does not exist")
    # return render(request, 'miniGithub/detail.html', {'project': project})

    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'miniGithub/detail.html', {'project': project})