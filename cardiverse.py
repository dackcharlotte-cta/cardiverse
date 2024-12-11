import requests
import json
import time
import base64
import urllib.request
import os
from flask import session 
import json
import datetime


#setting up meshy api key 
meshy_credentials = "meshy_keys.json"
with open(meshy_credentials, "r") as meshy_keys:
    meshy_tokens = json.load(meshy_keys)

api_key = meshy_tokens['Authorization']

#creating main function to call most of other functions 
def main(filename):
    print("main: ", filename)
    try:
        #
        image_data = image_pathway(filename)
        task_id = create_task(image_data, api_key)
        task_details = wait_for_completion(task_id, api_key)
        modelname = return_model(task_details)
        print(modelname)
        return modelname
    except Exception as e:
        print(f"Error: {e}")

#image ---> base64
def encode_image_to_base64(image_path):
    #path -----> image 
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def image_pathway(filename):
    #getting name of filename is there a better way??

    image_path = os.path.join(os.getcwd(), "static", "uploads", filename) 
    base64_image = encode_image_to_base64(image_path)

    image_data = f"data:image/jpeg;base64,{base64_image}"
    return image_data



def create_task(image_data, api_key, enable_pbr=True, ai_model="meshy-4", target_polycount=30000):
    url = "https://api.meshy.ai/v1/image-to-3d"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "image_url": image_data,  # Pass the Base64 string here
        "enable_pbr": enable_pbr,
        "ai_model": ai_model,
        "target_polycount": target_polycount,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        task_id = response.json()["result"]
        print(f"Task created successfully. Task ID: {task_id}")
        return task_id
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if e.response is not None:
            print(f"Response: {e.response.json()}")
        raise

def retrieve_task(task_id, api_key):
    url = f"https://api.meshy.ai/v1/image-to-3d/{task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def wait_for_completion(task_id, api_key, interval=10, timeout=300):
    elapsed_time = 0
    while elapsed_time < timeout:
        task_details = retrieve_task(task_id, api_key)
        status = task_details["status"]
        if status == "SUCCEEDED":
            print("Task completed successfully!")
            return task_details
        elif status in ["FAILED", "EXPIRED"]:
            raise Exception(f"Task failed or expired: {task_details.get('task_error', {}).get('message', 'Unknown error')}")
        print(f"Task status: {status}. Retrying in {interval} seconds...")
        time.sleep(interval)
        elapsed_time += interval
    raise TimeoutError("Task did not complete within the timeout period.")
    

def return_model(task_details): 
    print("return_model: ", task_details)
    model_urls = task_details.get("model_urls", {})
    #thumbnail_url = task_details.get("thumbnail_url", "")
    #print(f"FBX URL: {model_urls.get('fbx')}")
    #print(f"OBJ URL: {model_urls.get('obj')}")
    print(f"GLB URL: {model_urls.get('glb')}")
    #print(f"Thumbnail URL: {thumbnail_url}")

    print(task_details)

    #trying to download image 
    #data into json 
    #json_response = json.loads(task_details.model_dump_json())
    #print(json_response)

    fbx_model_url = model_urls.get('glb')

    #route to save 
    image_dir = os.path.join(os.curdir, 'static', 'models')
    print(image_dir)
    if not os.path.isdir(image_dir):
        print('not statement: cardiverse.py 115 ')
        os.mkdir(image_dir)
    #counter 
    date_now = str(datetime.datetime.now())
    date_now = date_now.replace('.', '_').replace(':', '_')

    modelname = 'model' + date_now
    image_path = os.path.join(image_dir, modelname +'.glb') 
    print('check append date', image_path)
    #if you want to have to save image over the time, you can add a counter, maybe by getting date
    #image_url = json_repsonse['data'][0]['url']

    #generate the image, gives you a URL for image not the actual image
    generate_image = requests.get(fbx_model_url).content 

    #save image in folder
    #wb = write to binary 
    with open(image_path, 'wb') as file: 
        print('check file write.')
        file.write(generate_image) 


    #trying to download image #creating path way to folder ---- model_dir = os.path.join(os.curdir, 'static', 'models')

    #get model url for fbx 
  #  fbx_model_url = model_urls.get('glb') 
   # got_url_file = urllib.request.urlretrieve(fbx_model_url, "model1.glb")

  #  response = requests.get(fbx_model_url, stream=True)

 #   model_path = os.path.join(model_dir, 'model.glb')

 #   with open(model_path, 'wb') as file: 
 #       file.write(fbx_model)

    return modelname



#main()
