"""
SignalWire AI Webhook Server
This server handles incoming webhook requests from SignalWire and returns LaML responses.
Run this server and expose it via ngrok or similar tunneling service.
"""

import os
from flask import Flask, request, Response
from signalwire.rest import Client
from signalwire.voice_response import VoiceResponse

app = Flask(__name__)

@app.route('/ai-agent', methods=['POST'])
def handle_ai_call():
    """
    Main AI agent endpoint - called by SignalWire when a call is initiated.
    This returns the LaML that configures the AI agent.
    """
    print("🤖 AI agent handling new incoming call")
    print(f"Request data: {request.form}")
    
    # Create the voice response
    response = VoiceResponse()
    
    # Connect to AI agent
    connect = response.connect()
    agent = connect.ai(voice='en-US-Neural2-D')
    
    # Set the post-prompt URL for call summary
    agent.post_prompt_url(f"{request.url_root}summary")
    
    # Get AI prompt from environment or use default
    ai_prompt = os.environ.get('AI_PROMPT', 
        """You are Ulya, and you are calling about a pizza order.
        Your objective is: tell the person who answers that you ordered a pizza.
        Be friendly and conversational. After delivering your message, politely end the call.
        Remember to hang up at the end of the conversation."""
    )
    
    # Configure the AI agent's prompt
    agent.prompt(
        {
            'confidence': 0.4,
            'frequency_penalty': 0.3,
        },
        ai_prompt
    )
    
    # Set post-prompt instructions for call summary
    agent.post_prompt(
        """Return a valid JSON object with the call summary by replacing the uppercase placeholders:
        {"contact_name": "CONTACT_NAME", "call_outcome": "CALL_OUTCOME", "message_delivered": "MESSAGE_DELIVERED"}"""
    )
    
    print(f"Generated LaML: {str(response)}")
    
    # Return the LaML response
    return Response(str(response), mimetype='text/xml')

@app.route('/summary', methods=['POST'])
def handle_call_summary():
    """
    Endpoint to receive call summary data from the AI agent after the call ends.
    """
    print("📞 Call summary received")
    print(f"Caller ID: {request.form.get('caller_id_number', 'Unknown')}")
    
    # Try to parse the post-prompt data
    if request.form.get('post_prompt_data.parsed'):
        print(f"Parsed summary: {request.form.get('post_prompt_data.parsed')}")
    elif request.form.get('post_prompt_data'):
        print(f"Raw summary: {request.form.get('post_prompt_data')}")
    else:
        print("No summary data received from AI agent")
    
    # Log all form data for debugging
    print("All form data:")
    for key, value in request.form.items():
        print(f"  {key}: {value}")
    
    return Response("OK", status=200)

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "SignalWire AI Webhook Server"}

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with basic info"""
    return {
        "message": "SignalWire AI Webhook Server",
        "endpoints": {
            "/ai-agent": "Main AI agent webhook (POST)",
            "/summary": "Call summary webhook (POST)", 
            "/health": "Health check (GET)"
        }
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting SignalWire AI Webhook Server on port {port}")
    print(f"🔗 Make sure to expose this server via ngrok or similar")
    print(f"📋 Your webhook URL will be: https://your-ngrok-url.ngrok.io/ai-agent")
    
    app.run(host='0.0.0.0', port=port, debug=debug)