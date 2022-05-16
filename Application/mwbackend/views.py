from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from azure.storage.blob import BlobServiceClient
import datetime

azure_conn_string = "DefaultEndpointsProtocol=https;AccountName=imagesstoragesuperhero;AccountKey=pDHER3XVErQzE71GGNiiCUTyH8aaSifOuu1/LY2PGEpLP0+dA+uZ+H10wCrwRn79dYfGPkKlF06D+AStHPY+9w==;EndpointSuffix=core.windows.net"
azure_photo_container = "savedimages"

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
        print(request.FILES)
        print(request)
        for file in request.FILES.getlist('images'):
            print(file)
            try:
                container_client.upload_blob(file.name, file)
            except Exception as e:
                print(e)
                print("[ERROR]Failed to upload photo to Azure Blob")
                return HttpResponse("[ERROR]Upload failed")

        return HttpResponse()
    else:
        return HttpResponseNotAllowed()  