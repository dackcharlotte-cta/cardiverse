import requests
import json

print("it is working")
#setting up keys for meshy 

meshy_credentials = "meshy_keys.json"
with open(meshy_credentials, "r") as meshy_keys:
    meshy_tokens = json.load(meshy_keys)


#sending the image to create 3D avator from URL image
#TODO need to figure out how to do from image file 
payload = {
     # Using data URI example
     # image_url: f'data:image/png;base64,{YOUR_BASE64_ENCODED_IMAGE_DATA}',
    "image_url": "https://www.wikihow.com/images/thumb/9/90/What_type_of_person_are_you_quiz_pic.png/728px-What_type_of_person_are_you_quiz_pic.png",
    "enable_pbr": True,
}


headers = {
    "Authorization": f"Bearer {meshy_tokens['Authorization']}"
}

response_making = requests.post(
    "https://api.meshy.ai/v1/image-to-3d",
    headers=headers,
    json=payload,
)

response_making.raise_for_status()
json_id = response_making.json()
print(json_id['result'])

task_id = json_id['result']

#returning results 
response_getting = requests.get(
    f"https://api.meshy.ai/v1/image-to-3d/{task_id}",
    headers=headers,
)
response_getting.raise_for_status()

print(response_getting.json())


