from django.shortcuts import render, redirect
from geoip2.database import Reader

from .form import AppUserForm
import nmap
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import AppUsers
from .serializers import AppUsersSerializer


def register(request):
    if request.method == 'POST':
        form = AppUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Replace with your success URL
    else:
        form = AppUserForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    return render(request, 'home.html', context=dict())


def pricing(request):
    return render(request, 'pricing.html', context=dict())


def scan(request):
    formatted_scan_results = None  # Initialize the variable at the beginning
    geoip_results = None
    if request.method == 'POST':
        target = request.POST.get('target')
        nm = nmap.PortScanner()
        reader = Reader('/usr/local/share/GeoIP/GeoLite2-ASN.mmdb')
        reader_c = Reader('/usr/local/share/GeoIP/GeoLite2-City.mmdb')
        response = reader.asn(target)
        response_c = reader_c.city(target)
        try:
            scan_results = nm.scan(hosts=target, arguments='-sV')
            formatted_scan_results = json.dumps(scan_results, indent=4)  # Format the results as JSON
            try:
                geoip_results = {
                    'System_Number': response.autonomous_system_number,
                    'Organization': response.autonomous_system_organization,
                    'IP': response.ip_address,
                    "new" : response_c
                }
            except Exception as e:
                geoip_results = f"Error: {str(e)}"

        except nmap.PortScannerError as e:
            formatted_scan_results = f"Error: {str(e)}"
        except Exception as e:
            formatted_scan_results = f"Unexpected Error: {str(e)}"


    return render(request, 'scan.html', {'scan_results': formatted_scan_results, 'geoip_results': geoip_results})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import AppUsers
from .serializers import AppUsersSerializer


@api_view(['GET', 'POST'])
def appusers_list(request):
    if request.method == 'GET':
        users = AppUsers.objects.all()
        serializer = AppUsersSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AppUsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def appusers_detail(request, pk):
    try:
        user = AppUsers.objects.get(pk=pk)
    except AppUsers.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = AppUsersSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AppUsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

