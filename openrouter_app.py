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
SECURITY_PROMPT = f"""
Act as a professional Security Operations Center (SOC) Analyst. 
Analyze the provided image ({image_filename}) and provide a structured security report.

1. TIMESTAMPS & SOURCE:
   - Identify the Camera ID (e.g., CAM 2).
   - Record the exact date and time shown in the overlay.

2. SUBJECT IDENTIFICATION:
   - Identify all people in the frame. 
   - For the individual in uniform: Identify the agency name visible on their clothing (e.g., 'POLICE'). Note if they are armed or carrying equipment (handcuffs, radio, notebook).
   - For the civilians: Describe their attire, physical build, and demeanor.

3. BEHAVIORAL ANALYSIS:
   - Describe the interaction. Is it a confrontational, cooperative, or investigative scene?
   - Note specific gestures. (e.g., "The male in the brown jacket is pointing toward the camera/house.")
   - Is anyone taking notes or using a mobile device?

4. ANOMALY DETECTION:
   - Identify any objects that are out of place.
   - Are there vehicles visible in the background? If so, provide color and type.
   - Identify any potential security vulnerabilities visible (e.g., open windows, unsecure perimeter).

5. RISK ASSESSMENT:
   - Categorize this event: [Routine/Authorized], [Suspicious], or [Emergency].
   - Provide a 1-sentence summary of what is happening for a security log.
"""

    analyze_local_security_image(TARGET_FILE, SECURITY_PROMPT)

if __name__ == "__main__":
    main()
