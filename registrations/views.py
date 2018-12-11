from django.shortcuts import render, get_object_or_404
from .models import Registrations, APs, Customers, Towers
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomerSerializer, ProblemSerializer




import datetime
from datetime import date, timedelta

class CustomerList(APIView):

    def get(self, request):
        queryset = Customers.objects.all()
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self):
        pass



def index(request):
    all_towers = Towers.objects.all().values()
    towers = []
    for a_ in all_towers:
        loc_id = a_['loc_id']
        id = a_['id']
        customers = Customers.objects.values("id").distinct().filter(loc_id=loc_id)
        name = a_['name']
        lat_id = a_['lat_id']
        lon_id = a_['lon_id']
        size = len(customers)
        tower = {'name':name,'id':id,'lat_id':lat_id,'lon_id':lon_id,'size':size,'loc_id':loc_id}
        towers.append(tower)
    context = {
        'all_towers': all_towers,
        'towers': list(towers)
    }
    return render(request, 'registrations/index.html',context)


def towers(request,loc_id):
    ap_list = APs.objects.values("id","name", "loc_id").distinct().filter(loc_id=loc_id).values()
    aps = []
    for a_ in ap_list:
        id = a_['id']
        name = a_['name']
        lat_id = a_['lat_id']
        lon_id = a_['lon_id']
        customers = Customers.objects.values("ap_id").filter(ap_id=id)
        size = len(customers)
        ap = {'name':name,'id':id,'lat_id':lat_id,'lon_id':lon_id,'size':size}
        aps.append(ap)

    customers = []
    rssi_list = []

    cust_list = Customers.objects.values("id","name","lat_id","lon_id","ap_id","frequency").filter(loc_id=loc_id)
    for a_ in cust_list:
        cus_id = a_['id']
        name = a_['name']
        lat_id = a_['lat_id']
        lon_id = a_['lon_id']
        ap_id = a_['ap_id']
        frequency = a_['frequency']
        #last_rec = Registrations.objects.values("rssi").filter(cust=id).order_by('-id')[:1].get()
        rssi = -70
        try:
            last_rec = Registrations.objects.values("id","rssi","mk_time","comment").filter(cust_id=cus_id).order_by('-id')[:1].get()
            rssi = int(last_rec['rssi'])
            mk_time = last_rec['mk_time']
            comment = last_rec['comment']
            mk_t = mk_time.strftime("%Y-%m-%d %H:%M")
        except Registrations.DoesNotExist:
            continue

        #size = 5
        rec_ap = APs.objects.get(pk=ap_id)
        ap_name = rec_ap.name
        client = {'size':rssi,'name': name, 'id': cus_id, 'lat_id': lat_id, 'lon_id': lon_id, 'ap_id':ap_id,'frequency':frequency}
        rssi_data = [name,rssi,frequency,ap_name,mk_t,comment]
        rssi_list.append(rssi_data)
        customers.append(client)
    rssi_list.sort(key=lambda x: x[1])

    rssi_sorted = []
    for rs in rssi_list:
        rs_d  = {'name':rs[0],'rssi':rs[1],'frequency':rs[2],'ap_name':rs[3],'mk_time':rs[4],'comment':rs[5]}
        rssi_sorted.append(rs_d)
    #customers = sorted(customers)
    context = {
        'aps': list(aps),
        'customers':list(customers),
        'rssi_list':list(rssi_sorted),
    }

    return render(request, 'registrations/towers.html',context)




def registration_data(request,ap_id):
    try:
        registrations = Registrations.objects.values("cust_name", "cust", "ap").distinct().filter(ap=ap_id)
        customers = []
        for r_ in registrations:
            cust_id = r_['cust']
            cust_name = r_['cust_name']
            rec_c = Customers.objects.get(pk=cust_id)
            rec_ap =APs.objects.get(pk=r_['ap'])
            last_rec = Registrations.objects.values("rssi").filter(cust=cust_id).order_by('-id')[:1].get()
            #customer = [cust_name, rec_c.id, rec_c.lon_id, rec_c.lat_id, rec_ap.lon_id, rec_ap.lat_id, last_rec['rssi']]
            customer = {'cust_id': rec_c.id, 'custname': cust_name,'clon_id':rec_c.lon_id, 'clat_id':rec_c.lat_id, 'rssi': last_rec['rssi'],"aplon_id":rec_ap.lon_id,"aplat_id":rec_ap.lat_id,"ap_name":rec_ap.name}
            customers.append(customer)


    except Registrations.DoesNotExist:
        raise Http404("AP Doesn't exist")
    return render(request, 'registrations/registrations.html', {'registrations': registrations, 'customers':list(customers)})


def reg_name_data(request,reg_name):

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

    try:
        registrations = Registrations.objects.filter(cust_name=reg_name).filter(mk_time__range=[d_from, d_to])
        #registrations = Registrations.objects.filter(cust_name=reg_name)

        for i,q in enumerate(registrations):
              q.uptime_sec = int(q.uptime_sec)


        filter_data = registrations.values("rssi", "ccq_rx", "ccq_tx","distance","uptime_sec")

        cust_ip =''
        cust_mac =''
        if len(registrations) > 0:
            cust_ip = registrations[0].ip
            cust_mac = registrations[0].mac

    except Registrations.DoesNotExist:
        raise Http404("AP Doesn't exist")
    context = {
        'registrations': registrations,
        'filter_data': list(filter_data),
        'reg_name':reg_name,
        'd_from': d_from,
        'd_to': d_to,
        'cust_ip':cust_ip,
        'cust_mac': cust_mac,

    }
    return render(request, 'registrations/registration_data.html', context)

def queries(request):
    active_tower = request.GET.get('active_tower')
    rssi = request.GET.get('rssi')
    counter = request.GET.get('counter')

    if not active_tower:
        active_tower = '0'
    if not rssi:
        rssi = 0
    if not counter:
        counter = 20



    try:
        if active_tower != '0':
            registrations = Registrations.objects.values("cust_name", "cust", "ap").distinct().filter(loc_id=active_tower)
        else:
            registrations = Registrations.objects.values("cust_name", "cust", "ap").distinct()

        cust_list = []
        for r_ in registrations:
            cust_id = r_['cust']
            cust_name = r_['cust_name']
            rec_c = Customers.objects.get(pk=cust_id)
            clat_id = rec_c.lat_id
            clon_id = rec_c.lon_id
            rec_ap =APs.objects.get(pk=r_['ap'])
            last_rec = Registrations.objects.values("rssi","mk_time").filter(cust=cust_id).order_by('-id')[:1].get()
            rssi = int(last_rec['rssi'])
            mk_time = last_rec['mk_time']
            mk_t = mk_time.strftime("%Y-%m-%d %H:%M")
            cust = [cust_name,rssi,rec_ap.name,rec_ap.frequency,mk_t, clat_id, clon_id]
            cust_list.append(cust)

        cust_list.sort(key=lambda x: x[1])
        cust_sorted = cust_list[:int(counter)]

        customers = []
        for rs in cust_sorted:
            rs_d  = {'name':rs[0],'rssi':rs[1],'ap':rs[2],'frequency':rs[3],'mk_time':rs[4],'lat_id':rs[5],'lon_id':rs[6]}
            customers.append(rs_d)

    except Registrations.DoesNotExist:
        raise Http404("AP Doesn't exist")

    all_towers = Towers.objects.all().values()
    towers = []
    all_tower = {'name':'ALL','id':0, 'loc_id':0}
    towers.append(all_tower)
    for a_ in all_towers:
        loc_id = a_['loc_id']
        id = a_['id']
        name = a_['name']
        tower = {'name':name,'id':id,'loc_id':loc_id}
        towers.append(tower)

    context = {
        'towers': list(towers),
        'active_tower': active_tower,
        'customers':list(customers),
        'counter':counter,
        'rssi':rssi,
    }
    return render(request,'registrations/queries.html',context)


class ProblemList(APIView):

    def get(self, request):
        active_tower = '0'
        rssi = 0
        counter = 20
        try:
            if active_tower != '0':
                registrations = Registrations.objects.values("cust_name", "cust", "ap").distinct().filter(loc_id=active_tower)
            else:
                registrations = Registrations.objects.values("cust_name", "cust", "ap").distinct()

            cust_list = []
            for r_ in registrations:
                cust_id = r_['cust']
                cust_name = r_['cust_name']
                rec_c = Customers.objects.get(pk=cust_id)
                clat_id = rec_c.lat_id
                clon_id = rec_c.lon_id
                rec_ap =APs.objects.get(pk=r_['ap'])
                last_rec = Registrations.objects.values("rssi","mk_time").filter(cust=cust_id).order_by('-id')[:1].get()
                rssi = int(last_rec['rssi'])
                mk_time = last_rec['mk_time']
                mk_t = mk_time.strftime("%Y-%m-%d %H:%M")
                cust = [cust_name,rssi,rec_ap.name,rec_ap.frequency,mk_t, clat_id, clon_id]
                cust_list.append(cust)

            cust_list.sort(key=lambda x: x[1])
            cust_sorted = cust_list[:int(counter)]

            customers = []
            for rs in cust_sorted:
                rs_d  = {'name':rs[0],'rssi':rs[1],'ap':rs[2],'frequency':rs[3],'mk_time':rs[4],'lat_id':rs[5],'lon_id':rs[6]}
                customers.append(rs_d)

        except Registrations.DoesNotExist:
            raise Http404("AP Doesn't exist")

        all_towers = Towers.objects.all().values()
        towers = []
        all_tower = {'name':'ALL','id':0, 'loc_id':0}
        towers.append(all_tower)
        for a_ in all_towers:
            loc_id = a_['loc_id']
            id = a_['id']
            name = a_['name']
            tower = {'name':name,'id':id,'loc_id':loc_id}
            towers.append(tower)

        context = {
            'towers': list(towers),
            'active_tower': active_tower,
            'customers':list(customers),
            'counter':counter,
            'rssi':rssi,
        }
        serializer = ProblemSerializer(customers, many=True)
        return Response(serializer.data)