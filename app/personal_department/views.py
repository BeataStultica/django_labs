from django.http import HttpResponse
from .models import Person
from django.template import loader
from django.shortcuts import redirect


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


def get_persons_list(request):
    persons = Person.objects.all()

    template = loader.get_template('persons.html')
    context = {'persons': persons}

    return HttpResponse(template.render(context, request))


def get_persons_by_id(request, person_id):
    person = Person.objects.get(pk=person_id)

    template = loader.get_template('person_detail.html')
    context = {
        'person': person,
    }

    return HttpResponse(template.render(context, request))


def create_person(request):
    if request.method == 'GET':
        template = loader.get_template('create_person.html')

        return HttpResponse(template.render({}, request))

    elif request.method == 'POST':

        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        position = request.POST.get("position", "")
        bio = request.POST.get("bio", "")
        responsibilities = request.POST.get("responsibilities", "")
        orders = request.POST.get("orders", "")

        person = Person.objects.create(first_name=first_name, last_name=last_name, position=position, bio=bio, responsibilities=responsibilities, orders=orders)

        return redirect('person-detail', person_id=person.pk)


def update_person_by_id(request, person_id):
    if request.method == 'GET':
        person = Person.objects.get(pk=person_id)

        template = loader.get_template('person_update.html')
        context = {'person': person}

        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        person = Person.objects.get(pk=person_id)

        person.first_name = request.POST.get("first_name", "")
        person.last_name = request.POST.get("last_name", "")
        person.position = request.POST.get("position", "")
        person.bio = request.POST.get("bio", "")
        person.responsibilities = request.POST.get("responsibilities", "")
        person.orders = request.POST.get("orders", "")

        person.save()

        return redirect('person-detail', person_id=person.pk)


def delete_person_by_id(request, person_id):
    person = Person.objects.get(pk=person_id)
    person.delete()

    return redirect('persons-list')


def get_about_info(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render({}, request))
