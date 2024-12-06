import requests
import json
import time
import base64
import os

meshy_credentials = "meshy_keys.json"
with open(meshy_credentials, "r") as meshy_keys:
    meshy_tokens = json.load(meshy_keys)

api_key = meshy_tokens['Authorization']

#image ---> base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

#path -----> image 
image_path = os.path.join(os.getcwd(), "images", "paddington.jpg")  # Combine the current working directory with the "images" folder and the image name
base64_image = encode_image_to_base64(image_path)

image_data = f"data:image/jpeg;base64,{base64_image}"

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
    model_urls = task_details.get("model_urls", {})
    thumbnail_url = task_details.get("thumbnail_url", "")
    print(f"FBX URL: {model_urls.get('fbx')}")
    print(f"OBJ URL: {model_urls.get('obj')}")
    print(f"GLB URL: {model_urls.get('glb')}")
    print(f"Thumbnail URL: {thumbnail_url}")

    fbx_model = model_urls.get('fbx')
    return fbx_model



def main():
    try:
        task_id = create_task(image_data, api_key)
        task_details = wait_for_completion(task_id, api_key)
        returned_model = return_model(task_details)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
