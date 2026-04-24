"""
OpenRouter Vision API Demo
Demonstrates image analysis using GPT-4 Vision via OpenRouter
Useful for security camera analysis, document scanning, and visual threat detection
"""

import os
import base64
import json
from openai import OpenAI
from pathlib import Path

def get_client():
    """Initialize the OpenAI client configured for OpenRouter"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")
    
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

def encode_image_to_base64(image_path):
    """Encode a local image file to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found: {image_path}")
    except Exception as e:
        raise Exception(f"Error encoding image: {str(e)}")


def analyze_image_from_url(image_url, prompt="What's in this image?", detail="auto"):
    """Analyze an image from a URL using OpenRouter"""
    client = get_client()
    
    try:
        print(f"Analyzing image from URL...")
        print(f"Prompt: '{prompt}'")
        print(f"Detail level: {detail}\n")
        
        response = client.chat.completions.create(
            model="openai/gpt-4o",  # OpenRouter uses provider/model format
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                                "detail": detail
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000,
            extra_headers={
                "HTTP-Referer": "https://your-app-url.com", # Optional
                "X-Title": "Vision Demo",                    # Optional
            }
        )
        
        # Extract response data
        analysis = response.choices[0].message.content
        
        return {
            'success': True,
            'analysis': analysis,
            'model': response.model,
            'tokens_used': response.usage.total_tokens,
            'prompt_tokens': response.usage.prompt_tokens,
            'completion_tokens': response.usage.completion_tokens
        }
        
    except Exception as e:
        print(f"✗ Error analyzing image: {str(e)}")
        return {'success': False, 'error': str(e)}


def analyze_image_from_file(image_path, prompt="What's in this image?", detail="auto"):
    """Analyze a local image file using OpenRouter"""
    client = get_client()
    
    try:
        print(f"Analyzing local image: {image_path}")
        
        base64_image = encode_image_to_base64(image_path)
        file_ext = Path(image_path).suffix.lower()
        mime_types = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp'}
        mime_type = mime_types.get(file_ext, 'image/jpeg')
        
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}",
                                "detail": detail
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        return {
            'success': True,
            'analysis': response.choices[0].message.content,
            'model': response.model,
            'tokens_used': response.usage.total_tokens
        }
        
    except Exception as e:
        print(f"✗ Error analyzing image: {str(e)}")
        return {'success': False, 'error': str(e)}


def main():
    """Main demonstration function"""
    print("=" * 60)
    print("OpenRouter Vision API Demo")
    print("=" * 60 + "\n")
    
    # Example 1: URL Analysis
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    
    result = analyze_image_from_url(
        image_url=image_url,
        prompt="Describe this image in detail. What are the key elements?"
    )
    
    if result['success']:
        print("\nANALYSIS RESULT:")
        print("-" * 60)
        print(result['analysis'])
        print(f"\nTokens used: {result['tokens_used']}")
    
    print("\n" + "=" * 60)
    print("Demo Complete!")

if __name__ == "__main__":
    main()
