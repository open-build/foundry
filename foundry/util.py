from openai import OpenAI
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.conf import settings
import re
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging

from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def preprocess_application_data(application):
    """
    Preprocess the application data to create a comprehensive summary text.
    Adjust the details as per your model's requirements.
    """
    details = [
        f"Business Description: {application['business_description']}",
        f"Legal Structure: {application['legal_structure']}",
        f"Ownership Structure: {application['ownership_structure']}",
        f"Annual Revenue: {application['annual_revenue']}",
        f"Funding Amount: {application['funding_amount']}",
        f"Outstanding Debt: {application['outstanding_debt']}",
        f"Development Stage: {application['development_stage']}",
        f"Market Demand Proof: {application['market_demand_proof']}",
        f"Marketing Strategy: {application['marketing_strategy']}",
        f"Competitive Advantage: {application['competitive_advantage']}",
        # Add more fields as necessary
    ]
    return " ".join(details)

def evaluate_startup_idea(application):
    """
    Evaluate the detailed startup application using ChatGPT for scoring based on specific criteria.
    """
    
    # Define the application summary from preprocess_application_data
    application_summary = preprocess_application_data(application)
    
    try:
        # Generate the review using ChatGPT
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Please review and evaluate the startup and business idea below:\n\n{application_summary}\n\nEvaluation Criteria:\n1. Originality\n2. Marketability\n3. Feasibility\n4. Completeness\n\nScore:",
            max_tokens=50
        )

        # Extract scores from the response
        if response.choices[0].text:
            review_text = response.choices[0].text
        else:
            review_text = "AI Failed to Summarize the Application. Please review manually."

        # Extract individual scores from the review text
        scores = review_text.split('\n')[1:]

        originality_score = float(scores[0].split(':')[-1])
        marketability_score = float(scores[1].split(':')[-1])
        feasibility_score = float(scores[2].split(':')[-1])
        completeness_score = float(scores[3].split(':')[-1])

        raise RateLimitError("You exceeded your current quota")
    except RateLimitError as e: 
        logging.error(f"Rate Limit Error: {str(e)}")
        
        scores = 0.0

        originality_score = 0.0
        marketability_score = 0.0
        feasibility_score = 0.0
        completeness_score = 0.0
        review_text = "AI Failed to Summarize the Application. Please review manually."
        
        # Send an email using SendGrid API
        message = Mail(
            from_email='foundry@buildly.io',
            to_emails='greg@buildly.io',
            subject='Open AI Rate Limit Exceeded',
            html_content='<strong>Check the Foundry</strong>')
        
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(str(e))
    return review_text, originality_score, marketability_score, feasibility_score, completeness_score

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
