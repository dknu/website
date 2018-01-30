import json
from datetime import datetime, timedelta, time, date
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from printerqueue.forms import QueueForm, QueueObjectForm
from printerqueue.models import Queue, QueueObject


def index(request):




    queues = list(Queue.objects.all())[-3:] # Henter kun de tre nyeste queuene
    queue_ids = map(lambda q: {'id': q.id,
                                'intervals': (q.all_slots(day=date.today()
                                                          , open_message="Ledig")),
                               'name': q.name,
                               },
                    list(queues))

    context = {"debug":"Debug message",
               "lists": queue_ids,
               "can_reserve": True,
               }

    return render(request, 'printerqueue/landing.html', context)

def all_queues(request):
    queues = Queue.objects.all()
    context = {
        "queues": []
    }

    for queue in queues:
        objects = []

        for object in queue.queueobjects.all():
            objects.append(str(object))
        context["queues"].append({"objects":objects, "name":queue.name})

    return render(request, 'printerqueue/all.html', context)


# TODO: Kan legge in dager HS køene ikke er åpne

@permission_required('can_create_queue')
def create(request):
    if request.method == "POST":
        form = QueueForm(request.POST)

        if form.is_valid():
            form.clean()

            queue = Queue(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                include_file=form.cleaned_data["include_file"],
                include_description=form.cleaned_data["include_description"],
                allowed_time_start=form.cleaned_data["time_start"],
                allowed_time_end=form.cleaned_data["time_end"],
                hidden=form.cleaned_data["hidden"]
            )

            queue.save()

            return HttpResponseRedirect(reverse('printerqueue:show', kwargs={'queue_id':queue.id}))

        else:
            raise Http404("Invalid Form")
    else:
        form = QueueForm()
        button_message = "Submit"


        render_context = {
            'form': form,
            'button_message': button_message
        }

        return render(request, 'printerqueue/add_queue.html', render_context)


def verify_submitted(obj: QueueObject):
    queue = obj.queue
    slots = queue.get_times_for_day(obj.date)
    print(slots)

    for s,e in slots:
        if (
            obj.start >= s and
            obj.end   <= e and
            obj. start < obj.end
        ):
            return True
    return False

@login_required()
def add_to_queue(request, queue_id):
    if request.method == 'POST':
        form = QueueObjectForm(request.POST)

        if form.is_valid():
            current_user = request.user
            queue = get_object_or_404(Queue,pk=queue_id)

            start_time = time(hour=int(form.cleaned_data["start_h"]),minute=int(form.cleaned_data["start_m"]))
            end_time = time(hour=int(form.cleaned_data["end_h"]), minute=int(form.cleaned_data["end_m"]))

            object = QueueObject(
                user=current_user,
                description=form.cleaned_data["description"],
                queue=queue,
                file=form.cleaned_data["file"] if queue.include_file else None,
                date=form.cleaned_data["date"],
                start=start_time,
                end=end_time
            )

            if verify_submitted(object):
                object.save()
                return HttpResponseRedirect(reverse('printerqueue:show', kwargs={'queue_id':queue.id}))
            else:
                # TODO Send bruker tilbake til skjema med feilmelding
                return HttpResponse("The data you submittet was not valid")

        else:
            return HttpResponse(form.errors)
    else:

        form = QueueObjectForm()
        queue = get_object_or_404(Queue,pk=queue_id)

        intervals = queue.all_slots(day=date.today(), open_message="Ledig")

        context = {
            'qid':queue_id,
            'include_description':queue.include_description,
            'include_file':queue.include_file,
            'form':form,
            'intervals':intervals,
            'can_reserve': False

        }

        return render(request, 'printerqueue/add_reservation.html', context)


def open_times(slots, date):
    o_times = []

    for slot in slots:
        total = datetime.combine(date.date(), slot[1]) - datetime.combine(date.date(), slot[0])
        total_quarters = int((total.total_seconds() // 60) // 15)

        times = []
        for i in range(total_quarters):
            dt = datetime.combine(date.date(), slot[0]) + timedelta(minutes=(15 * i))
            times.append(dt)

        o_times.append(times)
    return o_times


def get_times(request,queue_id, date):
    if request.method=='GET':
        dateobj = datetime.strptime(date,"%Y-%m-%d")
        queue = get_object_or_404(Queue,pk=queue_id)

        open_slots = queue.get_times_for_day(dateobj)

        o_times = open_times(open_slots, dateobj)

        open_times_str = map(
            lambda x: ','.join(
                map(
                    lambda s: "{:02}:{:02}".format(s.time().hour, s.time().minute), x
                )
            ), o_times
        )

        options = to_time_options(o_times)

        return HttpResponse(json.dumps(options))


def to_time_options(times):
    all_times = []
    options = {'hours':[],
               'minutes':{}}
    for a in times:
        all_times+=a

    for time in all_times:
        hour = "h{:02}".format(time.time().hour)
        minute = "m{:02}".format(time.time().minute)

        if hour not in options["hours"]:
            options["hours"].append(hour)
            options["minutes"][str(hour)] = []

        if minute not in options["minutes"][str(hour)]:
            options["minutes"][str(hour)].append(minute)

    return options


def get_end_times(request, queue_id, date, time):
    if request.method == "GET":
        dateobj = datetime.strptime(date,"%Y-%m-%d")
        timeobj = datetime.strptime(time,"%H-%M").time()
        queue = get_object_or_404(Queue, pk=queue_id)

        open_slots = queue.get_times_for_day(dateobj)
        times = open_times(open_slots, dateobj)

        slot = []
        time_index = 0

        found = False
        for t in times:
            if timeobj in map(lambda x: x.time(), t):
                slot = map(lambda x: x.time(), t)

        available_times = []

        slot = list(slot)

        after = False
        for t in slot:
            if t == timeobj:
                after = True
            if after:
                available_times.append(datetime.combine(dateobj,t)+timedelta(minutes=15))

        options = to_time_options([available_times])

        return HttpResponse(json.dumps(options))


def show(request, queue_id):
    if queue_id.isalnum():
        queue = get_object_or_404(Queue, pk=queue_id)
        objects = []
        for object in queue.queueobjects.all().order_by('date','end'):
            objects.append(str(object))

        ints = queue.all_slots(day=date.today(), open_message="Ledig")

        context = {
            'name': queue.name,
            'description': queue.description,
            'objects': objects,
            'can_reserve': True,
            'qid': queue.id,
            'intervals': ints
        }

        return render(request, 'printerqueue/view.html', context)
    else:
        return HttpResponseRedirect(reverse('printerqueue:index'))


def update_queue_list(request):
    if request.method == "GET":
        try:

            ctx = {
                'queue_id':int(request.GET.queue_id),
                'date': datetime.strptime(request.GET.date, "%Y-%m-%d").date(),
                'can_reserve': bool(request.GET.reserve)
            }

            return render(request,'printerqueue/queue_data.html', ctx)
        except:
            HttpResponse("GET data not valid")
