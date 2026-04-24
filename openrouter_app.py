"""
OpenRouter Local Vision Analysis
Analyzes 'security_image.jpeg' in the script's directory
"""

import os
import base64
from openai import OpenAI
from pathlib import Path

def get_client():
    """Initialize the OpenAI client configured for OpenRouter"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set. "
                         "Run: export OPENROUTER_API_KEY='your_key_here'")
    
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

def encode_image_to_base64(image_path):
    """Encode a local image file to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_local_security_image(image_filename, prompt):
    """
    Reads a local file and sends it to OpenRouter for analysis
    """
    client = get_client()
    
    # Construct the full path based on the script's location
    script_dir = Path(__file__).parent
    image_path = script_dir / image_filename

    if not image_path.exists():
        print(f"✗ Error: The file '{image_filename}' was not found in {script_dir}")
        return

    try:
        print(f"--- Starting Analysis of {image_filename} ---")
        base64_image = encode_image_to_base64(image_path)
        
        # Determine MIME type based on extension
        ext = image_path.suffix.lower()
        mime_type = "image/jpeg" if ext in ['.jpg', '.jpeg'] else "image/png"

        response = client.chat.completions.create(
            model="openai/gpt-4o",  # You can also use "google/gemini-pro-1.5-vision"
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}",
                                "detail": "high" # 'high' is better for security/detail-oriented tasks
                            }
                        }
                    ]
                }
            ]
        )

        analysis = response.choices[0].message.content
        print("\n[AI ANALYSIS]:")
        print("-" * 30)
        print(analysis)
        print("-" * 30)
        
    except Exception as e:
        print(f"✗ An error occurred during analysis: {e}")

def main():
    # Configuration
    TARGET_FILE = "security_image.jpeg"
    SECURITY_PROMPT = (
        "Analyze this security camera image. Identify any individuals, "
        "vehicles, or objects that look out of place. Provide a summary of "
        "potential security concerns."
    )

    analyze_local_security_image(TARGET_FILE, SECURITY_PROMPT)

if __name__ == "__main__":
    main()
