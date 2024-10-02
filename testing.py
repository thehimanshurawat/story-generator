import requests
import openai
import tkinter as tk
from tkinter import filedialog, Text
from PIL import ImageTk, Image

# Set up Azure Image Captioning API credentials
azure_image_caption_endpoint = "https://aimultiser979867857.cognitiveservices.azure.com/"
azure_image_caption_key = "af41c07c58894d25882d885b0954cf43"

# Set up OpenAI API credentials
openai.api_key = "2558fb7b74aa49f58474e5a160a99fd3"
openai.api_base = "https://openai0878675.openai.azure.com/"
openai.api_type = "azure"
openai.api_version = "2023-05-15"  # This is the current version as of this date
deployment_name = "gpt-35-turbo-16k"

# Function to get image caption from Azure
def get_image_caption(image_path):
    headers = {
        'Ocp-Apim-Subscription-Key': azure_image_caption_key,
        'Content-Type': 'application/octet-stream'
    }
    params = {
        'visualFeatures': 'Description',
        'language': 'en'
    }
    
    with open(image_path, 'rb') as image_data:
        response = requests.post(
            azure_image_caption_endpoint + "vision/v3.0/analyze",
            headers=headers,
            params=params,
            data=image_data
        )
        
    if response.status_code == 200:
        data = response.json()
        caption = data['description']['captions'][0]['text']
        return caption
    else:
        raise Exception(f"Failed to get image caption: {response.status_code}, {response.text}")

# Function to generate story using ChatCompletion API
def generate_story_from_caption(caption):
    prompt = f"Write a detailed 500-word story based on the following caption: {caption}"

    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes creative stories."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,  # Adjust token limit to achieve ~500 words
        temperature=0.7
    )
    
    story = response['choices'][0]['message']['content']
    return story

# Function to handle image upload and display caption and story
def upload_image():
    global img_label
    
    # Ask the user to select an image file
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    
    if file_path:
        # Load and display the image
        img = Image.open(file_path)
        img = img.resize((250, 250), Image.Resampling.LANCZOS)  # Updated to use LANCZOS
        
        img_tk = ImageTk.PhotoImage(img)
        
        img_label.config(image=img_tk)
        img_label.image = img_tk
        
        # Get the caption
        caption = get_image_caption(file_path)
        caption_text.delete(1.0, tk.END)
        caption_text.insert(tk.END, caption)
        
        # Generate the story
        story = generate_story_from_caption(caption)
        story_text.delete(1.0, tk.END)
        story_text.insert(tk.END, story)

# Create the GUI using Tkinter
root = tk.Tk()
root.title("Image Caption and Story Generator")

# Create a frame for the image
image_frame = tk.Frame(root)
image_frame.pack(pady=10)

img_label = tk.Label(image_frame)
img_label.pack()

# Create a button to upload an image
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

# Create text boxes for caption and story
caption_label = tk.Label(root, text="Generated Caption:")
caption_label.pack()

caption_text = Text(root, height=2, width=50)
caption_text.pack(pady=10)

story_label = tk.Label(root, text="Generated Story:")
story_label.pack()

story_text = Text(root, height=20, width=50)
story_text.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
