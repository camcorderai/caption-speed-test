import time, json, os, sys, pathlib
from dotenv import load_dotenv
load_dotenv()
from replicate.client import Client

# REPLICATE
replicate = Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

# INPUTS
model_id = (
    sys.argv[1]
    if len(sys.argv) > 1
    else "andreasjansson/blip-2"
)

image_path = (
    sys.argv[2]
    if len(sys.argv) > 2
    else "https://replicate.delivery/pbxt/IqiPBXiSDTHbjN61b809YMPWCB4OBkxXPGmqEiKA7K1pyErB/yud.png"
)

prompt = sys.argv[3] if len(sys.argv) > 3 else "describe this image"

# FUNCTIONS

# Get latest verion of Replicate model
def latest_version(model):
    versions = model.versions.list()
    return versions[0].id

# Construct VLM request
def construct_request(model_id, image_path, prompt):
    if model_id == "gfodor/instructblip":
        return {
            "top_p": 0.9,
            "prompt": prompt,
            "max_len": 200,
            "min_len": 1,
            "beam_size": 5,
            "image_path": image_path,
            "len_penalty": 1,
            "repetition_penalty": 3,
            "use_nucleus_sampling": False,
        }
    elif model_id == "andreasjansson/blip-2":
        return {
            "image": image_path,
            "caption": False,
            "question": prompt,
            "temperature": 1,
            "use_nucleus_sampling": False,
        }
    elif model_id == "cjwbw/cogvlm":
        return {
            "vqa": False,
            "image": image_path,
            "query": prompt,
        }
    elif model_id == "yorickvp/llava-13b":
        return {
            "image": image_path,
            "top_p": 1,
            "prompt": prompt,
            "max_tokens": 1024,
            "temperature": 0.2,
        }
    elif model_id == "lucataco/bakllava":
        return {"image": image_path, "prompt": prompt, "max_sequence": 512}
    else:
        return {"image": image_path, "prompt": prompt}
    return {}


# Poll Replicate prediction until complete
def poll_until_function_complete(prediction) -> dict:
    start_time = time.time()
    timeout = 900  # 15 minutes in seconds
    print(
        f"Checking for inference results for prediction {prediction.id}"
    )
    while (time.time() - start_time) < timeout:
        try:
            prediction.reload()
            status = prediction.status
            elapsed_time = int(time.time() - start_time)
            print(f"{elapsed_time}s status: {status}")
            if status == "succeeded":
                return prediction
            # Adjust wait time based on the status
            wait = 15 if status == "starting" else 0.5
            time.sleep(wait)
        except Exception as e:
            print(f"Error polling for results: {e}")
            print(prediction.error)
            break

    print("Timeout reached or an error occurred. Exiting.")
    return {}


# MAIN

try:
    start_time = time.time()
    print(f"Model: {model_id}")
    
    model = replicate.models.get(model_id)
    version = latest_version(model)
    input = construct_request(model_id, image_path, prompt)
    
    prediction = replicate.predictions.create(version=version, input=input)
    
    results = poll_until_function_complete(prediction)
    end_time = time.time()
    
    print()
    print(f"Model: {model_id}")
    print("Start time: ", time.strftime("%I:%M:%S %p", time.localtime(start_time)))
    print("End time: ", time.strftime("%I:%M:%S %p", time.localtime(end_time)))
    print(f"Total time: {round(end_time - start_time, 1)}s")
    print(f"Predict time: {round(results.metrics['predict_time'],1)}s")
        
    print()
    
    if isinstance(results.output, list):
        print("".join(results.output))
    else:
        print(results.output)
except Exception as e:
    print(f"Error: {e}")
