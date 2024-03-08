import openai
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.conf import settings
import re


def evaluate_startup_application(startup_application: dict) -> dict:
    # Ensure OpenAI API key is available
    openai.api_key = settings.OPENAI_API_KEY
    
    # Send description to OpenAI API for analysis
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Choose an appropriate engine for your task
            prompt=f"Provide an evaluation of this startup idea: {startup_application} give me a score based on originality, marketability, feasibility, and completeness as well as a summary.",
            max_tokens=1024,  # Adjust based on needs
            n=1,
            stop=None,
            temperature=0.5
        )
        
        # Simulate analysis of the response to calculate scores
        # Replace this with actual analysis logic based on the response
        try:
            analysis = analyze_ai_response(response)
        except Exception as e:
            # Handle the error here
            print(f"An error occurred: {e}")
            # Other error handling code if 
        
        # Return calculated scores
        return JsonResponse(analysis)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def analyze_ai_response(response):
    """
    Parses the structured response from the OpenAI API based on the given prompt.
    The function extracts scores for originality, marketability, feasibility,
    and completeness, as well as a summary from the text.
    """
    text = response.choices[0].text.strip()

    # Initialize a dictionary to hold the scores and summary
    analysis = {
        'originality_score': 0.0,
        'marketability_score': 0.0,
        'feasibility_score': 0.0,
        'completeness_score': 0.0,
        'summary': "",
    }

    # Regex patterns to find scores and summary in the response
    score_pattern = r"originality: (\d\.\d+)|marketability: (\d\.\d+)|feasibility: (\d\.\d+)|completeness: (\d\.\d+)"
    summary_pattern = r"summary: (.+)"
    
    # Extract scores using regex
    matches = re.finditer(score_pattern, text, re.IGNORECASE)
    for match in matches:
        if match.group(1):
            analysis['originality_score'] = float(match.group(1))
        elif match.group(2):
            analysis['marketability_score'] = float(match.group(2))
        elif match.group(3):
            analysis['feasibility_score'] = float(match.group(3))
        elif match.group(4):
            analysis['completeness_score'] = float(match.group(4))

    # Extract summary using regex
    summary_match = re.search(summary_pattern, text, re.IGNORECASE)
    if summary_match:
        analysis['summary'] = summary_match.group(1).strip()  # Ensure whitespace is removed

    return analysis
