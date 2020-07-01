from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from .forms import UploadFileForm
from .extraccionKml import extraction
from api.services.validation_services import XMLValidationService


def home(request):
    template = loader.get_template('api/home.html')
    action = dict()
    if request.method == 'GET':
        action.update({'Status': 'Initialize'})
    if request.method == 'POST':
        check = request.FILES.get('file', False)
        if not check:
            action.update({'Status': 'Initialize'})
            return HttpResponse(template.render({'action': action}, request))
        action.update({'Status': 'Received'})
        myFile = request.FILES['file']
        validate = XMLValidationService()

        if not validate.validate_file_extension(myFile.name):
            action.update({'Validated Type':'No valid'})
        else:
            action.update({'Validates Type':'Passed'})
        if not validate.not_empty(myFile.read()):
            action.update({'Validated Content':'No valid'})
        else:
            action.update({'Validated Content':'Passed'})

        action.update({
            'Name': validate._name,
            'Encoding': request.POST.encoding,
            'Content type': request.content_type,
            'Validated Extension': validate._extension,
            'Content length': validate._length,
            })

    return HttpResponse(template.render({'action':action}, request))