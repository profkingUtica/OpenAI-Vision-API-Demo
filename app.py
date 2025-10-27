"""
OpenAI Vision API Demo
Demonstrates image analysis using GPT-4 Vision
Useful for security camera analysis, document scanning, and visual threat detection
"""

import os
import base64
import json
from openai import OpenAI
from pathlib import Path

def encode_image_to_base64(image_path):
    """
    Encode a local image file to base64 string
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        str: Base64 encoded image string
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found: {image_path}")
    except Exception as e:
        raise Exception(f"Error encoding image: {str(e)}")


def analyze_image_from_url(image_url, prompt="What's in this image?", detail="auto"):
    """
    Analyze an image from a URL using OpenAI Vision API
    
    Args:
        image_url (str): URL of the image to analyze
        prompt (str): Question or instruction about the image
        detail (str): "low", "high", or "auto" - affects token usage and analysis depth
    
    Returns:
        dict: Response containing analysis and metadata
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = OpenAI(api_key=api_key)
    
    try:
        print(f"Analyzing image from URL...")
        print(f"Prompt: '{prompt}'")
        print(f"Detail level: {detail}\n")
        
        response = client.chat.completions.create(
            model="gpt-4o",  # or "gpt-4-turbo" or "gpt-4o-mini" for different capabilities
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
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
            max_tokens=1000
        )
        
        # Display raw JSON response
        print("=" * 60)
        print("RAW API RESPONSE (JSON):")
        print("=" * 60)
        
        response_dict = {
            'id': response.id,
            'model': response.model,
            'created': response.created,
            'choices': [
                {
                    'index': choice.index,
                    'message': {
                        'role': choice.message.role,
                        'content': choice.message.content
                    },
                    'finish_reason': choice.finish_reason
                }
                for choice in response.choices
            ],
            'usage': {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            }
        }
        
        print(json.dumps(response_dict, indent=2))
        print("=" * 60 + "\n")
        
        return {
            'success': True,
            'analysis': response.choices[0].message.content,
            'model': response.model,
            'tokens_used': response.usage.total_tokens,
            'prompt_tokens': response.usage.prompt_tokens,
            'completion_tokens': response.usage.completion_tokens
        }
        
    except Exception as e:
        print(f"✗ Error analyzing image: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


def analyze_image_from_file(image_path, prompt="What's in this image?", detail="auto"):
    """
    Analyze a local image file using OpenAI Vision API
    
    Args:
        image_path (str): Path to local image file
        prompt (str): Question or instruction about the image
        detail (str): "low", "high", or "auto"
    
    Returns:
        dict: Response containing analysis and metadata
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = OpenAI(api_key=api_key)
    
    try:
        print(f"Analyzing local image: {image_path}")
        print(f"Prompt: '{prompt}'")
        print(f"Detail level: {detail}\n")
        
        # Encode image to base64
        base64_image = encode_image_to_base64(image_path)
        
        # Determine image type from file extension
        file_ext = Path(image_path).suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_types.get(file_ext, 'image/jpeg')
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
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
        
        # Display raw JSON response
        print("=" * 60)
        print("RAW API RESPONSE (JSON):")
        print("=" * 60)
        
        response_dict = {
            'id': response.id,
            'model': response.model,
            'created': response.created,
            'choices': [
                {
                    'index': choice.index,
                    'message': {
                        'role': choice.message.role,
                        'content': choice.message.content
                    },
                    'finish_reason': choice.finish_reason
                }
                for choice in response.choices
            ],
            'usage': {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            }
        }
        
        print(json.dumps(response_dict, indent=2))
        print("=" * 60 + "\n")
        
        return {
            'success': True,
            'analysis': response.choices[0].message.content,
            'model': response.model,
            'tokens_used': response.usage.total_tokens,
            'prompt_tokens': response.usage.prompt_tokens,
            'completion_tokens': response.usage.completion_tokens
        }
        
    except Exception as e:
        print(f"✗ Error analyzing image: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


def analyze_multiple_images(image_sources, prompt="Compare these images"):
    """
    Analyze multiple images in a single request
    
    Args:
        image_sources (list): List of image URLs or file paths
        prompt (str): Question or instruction about the images
    
    Returns:
        dict: Response containing analysis
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = OpenAI(api_key=api_key)
    
    try:
        print(f"Analyzing {len(image_sources)} images...")
        print(f"Prompt: '{prompt}'\n")
        
        # Build content array with text prompt and images
        content = [{"type": "text", "text": prompt}]
        
        for source in image_sources:
            if source.startswith('http://') or source.startswith('https://'):
                # URL image
                content.append({
                    "type": "image_url",
                    "image_url": {"url": source}
                })
            else:
                # Local file
                base64_image = encode_image_to_base64(source)
                file_ext = Path(source).suffix.lower()
                mime_types = {
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.png': 'image/png',
                    '.gif': 'image/gif',
                    '.webp': 'image/webp'
                }
                mime_type = mime_types.get(file_ext, 'image/jpeg')
                
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{base64_image}"
                    }
                })
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=1500
        )
        
        print("✓ Analysis complete\n")
        
        return {
            'success': True,
            'analysis': response.choices[0].message.content,
            'tokens_used': response.usage.total_tokens
        }
        
    except Exception as e:
        print(f"✗ Error analyzing images: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


def main():
    """
    Main demonstration function with cybersecurity-relevant examples
    """
    print("=" * 60)
    print("OpenAI Vision API Demo")
    print("=" * 60 + "\n")
    
    # Example 1: Analyze image from URL
    print("EXAMPLE 1: Analyzing image from URL")
    print("-" * 60)
    
    # Using a sample image URL (replace with your own)
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    
    result = analyze_image_from_url(
        image_url=image_url,
        prompt="Describe this image in detail. What are the key elements?",
        detail="auto"
    )
    
    if result['success']:
        print("\nANALYSIS RESULT:")
        print("-" * 60)
        print(result['analysis'])
        print(f"\nTokens used: {result['tokens_used']}")
        print(f"  - Prompt tokens: {result['prompt_tokens']}")
        print(f"  - Completion tokens: {result['completion_tokens']}")
    
    print("\n" + "=" * 60)
    
    # Example 2: Security-focused analysis
    print("\nEXAMPLE 2: Security-focused image analysis")
    print("-" * 60)
    print("(Uncomment and provide a local image path to test)\n")
    
    # Uncomment to use with a local image:
     result = analyze_image_from_file(
         image_path="security_image.jpeg",
         prompt="Analyze this security camera image. Describe any people, vehicles, or suspicious activity visible.",
         detail="high"
     )
     
     if result['success']:
         print("\nSECURITY ANALYSIS:")
         print("-" * 60)
         print(result['analysis'])
    
    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
