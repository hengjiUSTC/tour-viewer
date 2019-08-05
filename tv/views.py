import os
from distutils.command import register

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from geopy import Nominatim

from tv.models import Question, Choice
from tv.google_drive.display import GoogleDriveClient
from tv.util.ImageHolder import ImageHolder

STATIC_FOLDER = "tv/static/"
class IndexView(generic.ListView):
    template_name = 'tv/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'tv/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'tv/results.html'


def tv_map(request):
    print(request.GET)
    # google_client = GoogleDriveClient()
    # dirs = google_client.list_dir()
    # print(dirs)
    # for dir in dirs:
    #     images = (google_client.list_dir(dir['id']))
    #     if len(images) > 0:
    #         fd = open(images[0]['name'], 'w')
    #         google_client.download_file(images[0]['id'], fd)
    # local_path = request.GET.get('path')
    local_path = "tv/places"  # insert the path to your directory

    image_list = []
    place_list = os.listdir(STATIC_FOLDER + local_path)
    geolocator = Nominatim(user_agent="hengji")
    for place in place_list:
        images = os.listdir(os.path.join(STATIC_FOLDER + local_path, place))
        if len(images) > 0:
            tmp_image = ImageHolder()
            tmp_image.path = local_path + '/' + place
            tmp_image.filename = images[0]
            tmp_image.city = place
            location = geolocator.geocode(tmp_image.city)
            tmp_image.latitude = location.latitude
            tmp_image.longitude = location.longitude
            image_list.append(tmp_image)
            print(tmp_image.filename, tmp_image.path, tmp_image.get_image_path())
    return render_to_response('tv/map.html', {'images': image_list})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'tv/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('tv:results', args=(question.id,)))