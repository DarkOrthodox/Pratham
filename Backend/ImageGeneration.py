import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# Define the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths to important directories
DATA_DIR = os.path.join(BASE_DIR, 'Data')
FRONTEND_FILES_DIR = os.path.join(BASE_DIR, 'Frontend', 'Files')
IMAGE_GENERATION_DATA_PATH = os.path.join(FRONTEND_FILES_DIR, 'ImageGeneration.data')

# Constants
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

def open_images(prompt):
    folder_path = DATA_DIR
    prompt_sanitized = prompt.replace(" ", "_")

    Files = [f"{prompt_sanitized}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

async def generate_images(prompt: str):
    tasks = []
    prompt_sanitized = prompt.replace(" ", "_")

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        image_filename = os.path.join(DATA_DIR, f"{prompt_sanitized}{i+1}.jpg")
        with open(image_filename, "wb") as f:
            f.write(image_bytes)

def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

if __name__ == "__main__":
    try:
        with open(IMAGE_GENERATION_DATA_PATH, "r") as f:
            Data: str = f.read()

        Prompt, Status = Data.strip().split(",")

        if Status.strip().lower() == "true":
            print("Generating Images...")
            GenerateImages(prompt=Prompt)

            with open(IMAGE_GENERATION_DATA_PATH, "w") as f:
                f.write("False,False")
    except Exception as e:
        print(f"Error: {e}")
