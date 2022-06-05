from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from azure.storage.blob import BlobServiceClient
import datetime
import uuid
import requests
import base64
import random
from io import BytesIO
from PIL import Image
import numpy as np
from datetime import datetime

azure_conn_string = "DefaultEndpointsProtocol=https;AccountName=imagesstoragesuperhero;AccountKey=pDHER3XVErQzE71GGNiiCUTyH8aaSifOuu1/LY2PGEpLP0+dA+uZ+H10wCrwRn79dYfGPkKlF06D+AStHPY+9w==;EndpointSuffix=core.windows.net"
azure_photo_container = "generatedimages"

blob_service_client = BlobServiceClient.from_connection_string(conn_str=azure_conn_string)

try:
    container_client = blob_service_client.get_container_client(container=azure_photo_container)
    container_client.get_container_properties()
except Exception as e:
    container_client = blob_service_client.create_container(azure_photo_container)

def test(request):
    now = datetime.datetime.now()
    html = "<html><body>Time: %s.</body></html>" % now
    return HttpResponse(html)

def get_image(request):
    if request.method == 'GET':

        html_response = "<html>"
        blobs_list = container_client.list_blobs()

        for blob in blobs_list:
            blob_image = container_client.get_blob_client(blob=blob.name)
            html_response += "<img src=" + blob_image.url + " width=200 height=200></img>"
        
        html_response += "</html>"    
        
        return HttpResponse(html_response)
    else:
        return HttpResponseNotAllowed()  

@csrf_exempt
def put_image(request):
    if request.method == 'POST':
        for file in request.FILES.getlist('images'):
            try:
                container_client.upload_blob(file.name, file)
            except Exception as e:
                print(e)
                print("[ERROR]Failed to upload photo to Azure Blob")
                return HttpResponse("[ERROR]Upload failed")

        return HttpResponse()
    else:
        return HttpResponseNotAllowed()

def get_images(request, count=10):
    if request.method == 'GET':
        url_base = 'https://imagesstoragesuperhero.blob.core.windows.net/generatedimages/'
        blobs_list = container_client.list_blobs()
        res = []
        try:
            count = int(request.GET.get('count', ''))
        except:
            count = 10
        filter_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        counter = 0
        for idx, blob in enumerate(blobs_list):
            if filter_date<str(blob.creation_time):
                counter+=1
                if counter == count:
                    break
                res.append({'filename:': blob.name, 'path': url_base + blob.name})

        return JsonResponse({'images':res})
    else:
        return HttpResponseNotAllowed()


def generate_images(request):
    if request.method == 'GET':
        number_of_images = 5

        for x in range(number_of_images):
            filename = str(uuid.uuid4()) + '.png'
            headers = {"Content-Type": "application/json",
            "Authorization":"Bearer 3FThkGH2HIO7IwKEdrvN2HgInbr8R9XI",}
            data = {
                "data": random.randint(0,2**32-1),
                }
            endpoint_url = 'https://superhero-endpoint2.centralus.inference.ml.azure.com/score'
            res = requests.post(url=endpoint_url,headers=headers,json=data)
            image =  Image.fromarray(np.array(res.json(), dtype="uint8"))
            buff = BytesIO()
            image.save(buff,format="png")
            image = base64.b64encode(buff.getvalue()).decode("utf-8")
            image = base64.b64decode(image)   
            if res.status_code != 200:
                print("[ERROR]Failed to fetch image from endpoint")
                HttpResponse(503) 
            
            ##TODO check content
            try:
                container_client.upload_blob(filename, image)
                
            except Exception as e:
                print(e)
                print("[ERROR]Failed to upload photo to Azure Blob")
                return HttpResponse("[ERROR]Upload failed")
                

        return HttpResponse()
    else:
        return HttpResponseNotAllowed()

def test_endpoint(request):
    if request.method == 'GET':
        random_image = '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'
        return HttpResponse(base64.b64decode(random_image), content_type='image/png')
    else:
        return HttpResponseNotAllowed()
