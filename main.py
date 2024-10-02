import requests
import openai

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
        print(f"Generated caption: {caption}")
        return caption
    else:
        raise Exception(f"Failed to get image caption: {response.status_code}, {response.text}")

# Updated function to generate story using new ChatCompletion API
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

# Main function to execute the project
def main(image_path):
    # Step 1: Get caption from the image
    caption = get_image_caption(image_path)
    
    # Step 2: Generate a story from the caption
    story = generate_story_from_caption(caption)
    
    print("\nGenerated Story:\n")
    print(story)

# Run the project with an image file
if __name__ == "__main__":
    image_path = "/Users/himanshurawat/Desktop/Project 2/images.jpeg"  # Replace with your image path
    main(image_path)
