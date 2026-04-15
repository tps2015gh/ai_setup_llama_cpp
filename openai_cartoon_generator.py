#!/usr/bin/env python3
"""
OpenAI Cartoon Generator - Generate cartoon images using OpenAI's DALL-E API
This script uses your OPENAI_API_KEY and OPENAI_API_PATH to generate the 4-frame cartoon.
"""

import os
import openai
import time
import json
from pathlib import Path

def test_openai_connection():
    """Test if OpenAI API is accessible."""
    try:
        # Set up OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        api_base = os.getenv('OPENAI_API_BASE')

        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment variables")
            return False

        # Initialize OpenAI client
        if api_base:
            openai.api_base = api_base
        openai.api_key = api_key
        
        # Test connection with a simple request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print(f"✅ OpenAI connection successful! Model: {response.model}")
        return True
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")
        return False

def get_image_generation_models():
    """Get available image generation models."""
    try:
        # For DALL-E, we typically use specific model names
        # Common DALL-E models: "dall-e-2", "dall-e-3"
        models = ["dall-e-2", "dall-e-3"]
        print("Available image generation models:")
        for i, model in enumerate(models, 1):
            print(f"  {i}. {model}")
        return models
    except Exception as e:
        print(f"Error getting models: {e}")
        return ["dall-e-3"]  # Default fallback

def generate_cartoon_frames():
    """Generate the 4 cartoon frames using DALL-E."""
    
    # Check if OpenAI is accessible
    if not test_openai_connection():
        print("\nPlease set your OPENAI_API_KEY and OPENAI_API_PATH environment variables.")
        print("Example: set OPENAI_API_KEY=your_key_here")
        print("         set OPENAI_API_PATH=https://api.openai.com/v1")
        return
    
    # Get available models
    models = get_image_generation_models()
    
    # Select DALL-E 3 as default (best quality)
    selected_model = "dall-e-3"
    if "dall-e-3" not in models:
        selected_model = models[0] if models else "dall-e-3"
    
    print(f"\nUsing model: {selected_model}")
    
    # Frame prompts optimized for DALL-E
    frames = [
        {
            "title": "The Old Way",
            "prompt": "Cartoon comic strip panel, exhausted programmer with wild hair and dark circles, messy desk with 10 coffee cups, tangled cables, sticky notes everywhere, computer screen showing complex nested code with 'TODO: fix this mess', wearing 'I ❤️ Stack Overflow' t-shirt, humorous exaggerated expression, clean white background, professional cartoon style, high detail, 4k"
        },
        {
            "title": "The AI Revelation",
            "prompt": "Cartoon comic strip panel, same programmer now excited and upright, looking at laptop screen with friendly robot AI assistant saying 'I can help!' in speech bubble, neat desk with one coffee cup and small green plant, bright lighting, smiling expression, modern office setting, clean lines, vibrant colors, professional cartoon illustration"
        },
        {
            "title": "Over-Reliance Disaster",
            "prompt": "Cartoon comic strip panel, programmer confidently typing 'Make it work' into AI interface, chaos ensuing: fluffy cat walking on keyboard, robot arm pouring coffee directly into computer tower, rocket launching through office window, programmer with shocked expression, exaggerated comedy style, vibrant colors, clean cartoon lines"
        },
        {
            "title": "The Balanced Approach",
            "prompt": "Cartoon comic strip panel, programmer and AI assistant as friendly colleagues at separate desks, AI pointing at clean well-commented code, programmer smiling and thinking, whiteboard with 'Understand → Ask → Review → Deploy', organized desk with plants, professional but friendly atmosphere, modern tech office, clean cartoon illustration"
        }
    ]
    
    # Create output directory
    output_dir = Path("./ai_cartoon_output")
    output_dir.mkdir(exist_ok=True)
    
    print(f"\nGenerating {len(frames)} cartoon frames...")
    print("This may take 1-2 minutes per image...")
    
    # Generate each frame
    for i, frame in enumerate(frames, 1):
        print(f"\nGenerating Frame {i}: {frame['title']}")
        
        try:
            # Call DALL-E API
            response = openai.Image.create(
                prompt=frame["prompt"],
                n=1,
                size="1024x1024",
                model=selected_model,
                response_format="url"
            )
            
            # Get image URL
            image_url = response['data'][0]['url']
            print(f"✓ Generated image URL: {image_url}")
            
            # Save image info
            image_info = {
                "frame_number": i,
                "title": frame["title"],
                "prompt": frame["prompt"],
                "image_url": image_url,
                "model_used": selected_model,
                "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Save to file
            with open(output_dir / f"frame_{i}_info.json", "w") as f:
                json.dump(image_info, f, indent=2)
            
            print(f"✓ Saved frame {i} info to: {output_dir}/frame_{i}_info.json")
            
            # Note: To download the image, you'd need to use requests to fetch the URL
            # This script saves the URL for you to download later
            
        except Exception as e:
            print(f"❌ Error generating frame {i}: {e}")
            print("Continuing to next frame...")
    
    print(f"\n🎉 Generation complete!")
    print(f"Check './ai_cartoon_output/' for frame information files.")
    print("To download the images, use the URLs in the JSON files with a tool like wget or curl.")

def main():
    """Main function."""
    print("=" * 60)
    print("🎨 OpenAI Cartoon Generator")
    print("Generates 4-frame cartoon about AI-era programming")
    print("=" * 60)
    
    # Check environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    api_base = os.getenv('OPENAI_API_BASE')
    
    print(f"API Key: {'✓ Set' if api_key else '✗ Not set'}")
    print(f"API Base: {api_base or 'Not set'}")
    
    if not api_key:
        print("\n⚠️  Please set your environment variables first:")
        print("   set OPENAI_API_KEY=your_actual_api_key")
        print("   set OPENAI_API_BASE=https://api.openai.com/v1  # or your custom endpoint")
        return
    
    # Ask user to confirm
    print("\nWould you like to proceed with generating the cartoon frames?")
    print("(This will use your OpenAI API credits)")
    
    response = input("Enter 'yes' to proceed, or any other key to exit: ").lower().strip()
    if response == 'yes':
        generate_cartoon_frames()
    else:
        print("Exiting. Run this script again when ready.")

if __name__ == "__main__":
    main()