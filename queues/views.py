from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Queues, Queue_data
import datetime
from datetime import date, timedelta

def mk_list(request):
    all_queues = Queues.objects.all()
    all_mks = Queues.objects.values("device_name").distinct()
    return render(request, 'queues/mks.html',{'all_mks': list(all_mks)})

def queue_list(request, device_name):
    all_queues = Queues.objects.values("id", "name").filter(device_name=device_name)
    #customers = Customers.objects.values("id").distinct().filter(loc_id=loc_id)
    return render(request, 'queues/queues.html',{'all_queues': all_queues})


def detail2(request,queue_id):
    try:
        queue = Queues.objects.get(pk=queue_id)
    except Queues.DoesNotExist:
        raise Http404("Queue Doesn't exist")
    return render(request, 'queues/details.html', {'queue': queue})


def detail_queue_data(request,queue_id):
    d_from = request.GET.get('d_from')
    d_to = request.GET.get('d_to')

    if d_from:
        d_from = d_from.strip()
        if d_from.count(':') < 2:
            d_from += ' 00:00:00'

        d_from = ' '.join(d_from.split())

    if d_to:
        d_to = d_to.strip()
        if d_to.count(':') < 2:
            d_to += ' 00:00:00'

        d_to = ' '.join(d_to.split())



    if not d_from:
        d_from = (datetime.datetime.today() - timedelta(1)).strftime("%Y-%m-%d %H:%M:%S")
    if not d_to:
        d_to = (datetime.datetime.today()).strftime("%Y-%m-%d %H:%M:%S")


    d_delta = datetime.datetime.strptime(d_to, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(d_from, "%Y-%m-%d %H:%M:%S")
    queue =get_object_or_404(Queues, pk=queue_id)

    #queue_data = Queue_data.objects.filter(queue=queue_id)
    try:
        queue_data = Queue_data.objects.filter(queue=queue_id).filter(mk_time__range=[d_from, d_to])
       # filter_data = Queue_data.objects.filter(queue=queue_id).filter(mk_time__range=[d_from, d_to]).values("b_rx","b_tx","usage_rx","usage_tx","dummy")
        prev_rx = int(queue_data[0].b_rx)
        prev_tx = int(queue_data[0].b_tx)
        total_rx = 0
        total_tx = 0
        usage = {}
        usage['rx'] = []
        usage['tx'] = []
        time_delta = []
        prev_time = (queue_data[0].mk_time).replace(tzinfo=None)
        for i,q in enumerate(queue_data):
            usage_rx = int(q.b_rx)- prev_rx
            usage_tx = int(q.b_tx) - prev_tx
            if usage_rx < 0: usage_rx = 0
            if usage_tx < 0: usage_tx = 0
            total_rx += usage_rx
            total_tx += usage_tx
            queue_data[i].usage_rx = usage_rx/1000
            queue_data[i].usage_tx = usage_tx/1000
            temp_t = (queue_data[i].mk_time).replace(tzinfo=None)
            temp_d = (temp_t - prev_time).total_seconds()
            if temp_d == 0:
                temp_d = 1.0
            prev_time = temp_t
            time_delta.append(temp_d)
            queue_data[i].time_st = temp_d
            ave_tx = queue_data[i].usage_tx/temp_d
            ave_rx = queue_data[i].usage_rx /temp_d
            if ave_tx < 0: ave_tx = 0.0
            if ave_rx < 0: ave_rx = 0.0
            queue_data[i].average_tx = float("{0:.2f}".format(ave_tx))
            queue_data[i].average_rx = float("{0:.2f}".format(ave_rx))

            #usage['rx'].append(usage_rx/1000)
            #usage['tx'].append(usage_tx/1000)

            usage['rx'].append(ave_rx)
            usage['tx'].append(ave_tx)


            temp_urx = float(usage_rx)/1000000
            temp_utx = float(usage_tx)/1000000
            queue_data[i].usage_rx = float("{0:.2f}".format(temp_urx))
            queue_data[i].usage_tx = float("{0:.2f}".format(temp_utx))


            prev_rx = int(q.b_rx)
            prev_tx = int(q.b_tx)

        total_rx = float(total_rx)/1000000000
        total_tx = float(total_tx) / 1000000000

        total_rx = float("{0:.4f}".format(total_rx))
        total_tx = float("{0:.4f}".format(total_tx))

        for i, q in enumerate(queue_data):
            temp_rx = float(q.b_rx)/1000000000
            temp_tx = float(q.b_tx) / 1000000000
            rx = float("{0:.2f}".format(temp_rx))
            tx = float("{0:.2f}".format(temp_tx))
            queue_data[i].b_rx = float(rx)
            queue_data[i].b_tx = float(tx)


        filter_data = queue_data.values("b_rx", "b_tx")


        context = {'is_data': True,
                   'queue_data': queue_data,
                   'filter_data':list(filter_data),
                   'queue': queue,
                   'usage': usage,
                   'total_rx':total_rx,
                   'total_tx':total_tx,
                   'd_from':d_from,
                   'd_to':d_to,
                   'time_delta':time_delta
                   }
    except:
        context = {'is_data': False,
                   'queue': queue,
                   'd_from': d_from,
                   'd_to': d_to
                   }
        #raise Http404("NO Data available for duration "+ str(d_from)+ " to " + str(d_to))
        return render(request, 'queues/queue_data.html', context)
    return render(request, 'queues/queue_data.html', context)






def index(request):
    #all_queues = Queues.objects.all()
    #return render(request, 'queues/index.html',{'all_queues': all_queues})
    return render(request,'queues/index.html')

def sample(request):
    #all_queues = Queues.objects.all()
    #return render(request, 'queues/index.html',{'all_queues': all_queues})
    return render(request,'queues/sample.csv')

def queues_js(request):
    return render(request, 'queues/queues.js')


