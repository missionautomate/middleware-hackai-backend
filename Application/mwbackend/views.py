from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from azure.storage.blob import BlobServiceClient
import datetime
from rest_framework.parsers import JSONParser 
from rest_framework.decorators import api_view
import psycopg2
from azure.core.exceptions import ResourceNotFoundError
import redis 
import json

redis_client = redis.StrictRedis(host="middleware-redis.redis.cache.windows.net",port=6380,db=0,password="udL1EFYhZHPUs1c18b9zdb0ywjw99sG9AAzCaEDaXdM=",ssl=True)


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


conn_string = "postgres://missionautomate:Parola1234@postgre-db-server.postgres.database.azure.com:5432/postgres"

def get_gallery(id):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    command = """
            SELECT imageurl
            FROM gallery
            WHERE googleid = 
    """
    command = f"SELECT imageurl FROM gallery WHERE googleid=\'{id}\'"
    # command += str(id)
    cursor.execute(command)
    return(cursor.fetchall())


@api_view(['POST'])
def pull_images_for_current_user(request):
    if request.method == 'POST':
        response = JSONParser().parse(request)
        google_id = response['account_id']
        base_url = "https://imagesstoragesuperhero.blob.core.windows.net/savedimages/"

        redis_key = f"{google_id}"
        img_urls = []
        if not redis_client.exists(redis_key):
            gallery = get_gallery(google_id)
            for img_url in gallery:
                img_url = base_url + img_url[0]
                redis_client.sadd(redis_key, img_url)
                img_urls.append(img_url)
        else:
            img_urls = redis_client.smembers(redis_key)
            img_urls = [img_url.decode() for img_url in img_urls]
        result = {"image_urls": img_urls}

        return HttpResponse(json.dumps(result), content_type='application/json') 
    else:
        return HttpResponseNotAllowed()


def get_image(request):
    if request.method == 'GET':

        html_response = "<html>"
        blobs_list = container_client.list_blobs()

        for blob in blobs_list:
            blob_image = container_client.get_blob_client(blob=blob.name)
            html_response += "<img src=" + blob_image.url + " width=200 height=200></img>"
        
        html_response += "</html>"    
        
        return HttpResponse()
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