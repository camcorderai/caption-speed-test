import time, sys, os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

# OPENAI
client = OpenAI(os.getenv("OPENAI_API_KEY"))

# INPUTS
model_id = "gpt-4-vision-preview"

image_path = (
    sys.argv[1]
    if len(sys.argv) > 2
    else "https://replicate.delivery/pbxt/IqiPBXiSDTHbjN61b809YMPWCB4OBkxXPGmqEiKA7K1pyErB/yud.png"
)

prompt = sys.argv[2] if len(sys.argv) > 3 else "describe this image"

# MAIN

try:
    start_time = time.time()
    print(f"Model: {model_id}")
    
    results = client.chat.completions.create(
      model=model_id,
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": prompt},
            {
              "type": "image_url",
              "image_url": {
                "url": image_path,
                "detail": "low"
              },
            },
          ],
        }
      ],
      max_tokens=300,
    )
    
    end_time = time.time()
    
    print()
    print(f"Model: {model_id}")
    print("Start time: ", time.strftime("%I:%M:%S %p", time.localtime(start_time)))
    print("End time: ", time.strftime("%I:%M:%S %p", time.localtime(end_time)))
    print(f"Total time: {round(end_time - start_time, 1)}s")
        
    print()
    
    print(results.choices[0].message.content)
    
except Exception as e:
    print(f"Error: {e}")
