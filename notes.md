# Teaching Notes for Cybersecurity Students:
"""
KEY CONCEPTS FOR CYBERSECURITY:

1. Vision API Capabilities:
   - Object detection and identification
   - Text extraction (OCR) from images
   - Scene understanding and description
   - Face detection (but not identification)
   - Document analysis

2. Cybersecurity Use Cases:
   - Security camera footage analysis
   - Phishing email screenshot analysis
   - Malware/suspicious interface detection
   - ID document verification
   - Network diagram analysis
   - Code screenshot analysis
   - Threat intelligence from visual sources

3. Detail Levels:
   - "low": 512x512, fewer tokens (~85 tokens)
   - "high": Detailed tile analysis, more tokens (~170 tokens per 512x512 tile)
   - "auto": API decides based on image size

4. Token Costs:
   - Base tokens: Text in your prompt
   - Image tokens: Depends on size and detail level
   - gpt-4o: ~$2.50/1M input tokens, ~$10/1M output tokens
   - Images can use 100-1000+ tokens depending on resolution

5. Privacy & Security Considerations:
   - Images sent to OpenAI for processing
   - Do NOT send: PII, classified info, sensitive credentials
   - OpenAI may use data for model improvement (check data usage policy)
   - Consider on-premise solutions for sensitive material
   - Be aware of data retention policies

6. Input Validation:
   - Verify image file types and sizes
   - Sanitize file paths to prevent directory traversal
   - Implement file size limits to prevent abuse
   - Validate URLs to prevent SSRF attacks

7. Supported Formats:
   - PNG, JPEG, WEBP, non-animated GIF
   - Max file size: 20MB
   - For base64: encode efficiently, consider file size impact

8. Error Handling:
   - Handle rate limits (429 errors)
   - Manage invalid image formats
   - Deal with network timeouts
   - Handle API key issues

EXERCISE IDEAS:
- Analyze phishing email screenshots to identify red flags
- Process security camera feeds for threat detection
- Extract network topology from diagram images
- Analyze malware UI to understand functionality
- OCR credentials from screenshots (ethical hacking scenarios)
"""
