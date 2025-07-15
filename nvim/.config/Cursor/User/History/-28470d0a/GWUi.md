# 🎵 CallHiss - AI-Powered Phone Call Assistant

CallHiss is a CLI tool that uses AI to make phone calls on your behalf. Simply provide a prompt describing what you want the AI to say, enter a phone number, and let the AI handle the conversation!

## 🌟 Features

- **CLI Interface**: Easy-to-use command line interface
- **AI-Powered Calls**: Uses SignalWire's AI agents to handle conversations
- **Natural Conversations**: AI speaks naturally and adapts to responses
- **Flexible Prompts**: Support any type of message or conversation goal
- **Call Summaries**: Get reports on how each call went

## 📋 User Stories

**Example Usage:**
```
💭 What would you like the AI to say on the call?
> call this person, tell them happy birthday! Its my mom, and tell her its from James! If she asks, im doing fine in europe.

📞 Enter the phone number to call:
> +1234567890

🎯 Ready to call +1234567890
📝 Message: call this person, tell them happy birthday! Its my mom, and tell her its from James! If she asks, im doing fine in europe.

✅ Proceed with call? (y/N): y
```

The AI will then:
1. Call the number
2. Greet the person politely
3. Deliver your message naturally
4. Handle any questions or responses
5. End the call appropriately

## 🚀 Quick Start

### Prerequisites

- **Nix** (recommended) or **Python 3.11+**
- **SignalWire Account** with:
  - Space URL
  - Project ID
  - API Token
  - Phone number
- **Public URL** for webhooks (ngrok, etc.)

### 1. Clone and Setup

```bash
git clone <your-repo>
cd callHiss

# Using Nix (recommended)
nix-shell

# Or using Python directly
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy the example config
cp config.env.example config.env

# Edit with your SignalWire credentials
nano config.env

# Source the environment
source config.env
```

**Required Variables:**
```bash
export SPACE_URL=yourspace.signalwire.com
export PROJECT_ID=your_project_id
export API_TOKEN=your_api_token
export FROM_NUMBER=+1234567890
export HOST_APP=https://your-ngrok-url.ngrok.io:3000
```

### 3. Setup Public URL (for webhooks)

SignalWire needs to reach your application via webhooks. For local development:

```bash
# Install ngrok if you haven't already
# Then expose your local port
ngrok http 3000

# Copy the https URL to your HOST_APP environment variable
export HOST_APP=https://abc123.ngrok.io
```

### 4. Run CallHiss

```bash
python call_hiss.py
```

## 🔧 Configuration

### SignalWire Setup

1. **Create Account**: Sign up at [SignalWire](https://signalwire.com)
2. **Get Credentials**: From your dashboard, note:
   - Space URL (e.g., `yourspace.signalwire.com`)
   - Project ID
   - API Token
3. **Buy Phone Number**: Purchase a phone number for outbound calls
4. **Set Webhooks**: Configure your application URL for webhooks

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SPACE_URL` | Your SignalWire space URL | `yourspace.signalwire.com` |
| `PROJECT_ID` | SignalWire Project ID | `abc123...` |
| `API_TOKEN` | SignalWire API Token | `PT...` |
| `FROM_NUMBER` | Your SignalWire phone number | `+1234567890` |
| `HOST_APP` | Public URL for webhooks | `https://abc.ngrok.io` |
| `PORT` | Local server port (optional) | `3000` |

## 💻 Usage Examples

### Basic Birthday Call
```
Prompt: "Call my mom and wish her happy birthday from James!"
```

### Business Message
```
Prompt: "Tell them the meeting is moved to 3 PM tomorrow and ask if that works for their schedule"
```

### Appointment Reminder
```
Prompt: "Remind them about their doctor's appointment tomorrow at 2 PM and ask them to confirm"
```

### Personal Check-in
```
Prompt: "Call my friend and let them know I'm thinking of them. Tell them I'm doing well in college"
```

## 📁 Project Structure

```
callHiss/
├── call_hiss.py          # Main CLI application
├── requirements.txt      # Python dependencies
├── shell.nix            # Nix development environment
├── config.env.example  # Environment variables template
├── README.md            # This file
└── example.js           # Original JavaScript example (reference)
```

## 🔍 How It Works

1. **CLI Input**: User provides a prompt and phone number
2. **Server Start**: Flask server starts to handle webhooks
3. **Call Initiation**: SignalWire API creates the call
4. **AI Agent**: When call connects, AI agent takes over
5. **Conversation**: AI follows the prompt and handles responses
6. **Summary**: Call results are logged when complete

## 🛠️ Development

### Using Nix

The `shell.nix` file provides a complete development environment:

```bash
nix-shell  # Automatically sets up Python, dependencies, and tools
```

### Manual Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python call_hiss.py
```

### Testing

For testing without making real calls, you can modify the code to use SignalWire's test credentials or webhook simulation tools.

## 🚨 Important Notes

- **Webhook URL**: Must be publicly accessible (use ngrok for local dev)
- **Phone Numbers**: Include country code (e.g., +1 for US)
- **Costs**: SignalWire charges for calls and AI usage
- **Ethics**: Only call people who consent to receive calls
- **Legal**: Follow local laws regarding automated calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

[Add your license here]

## 🆘 Support

For issues:
1. Check your environment variables
2. Verify SignalWire credentials
3. Ensure webhook URL is accessible
4. Check SignalWire dashboard for call logs

## 🙏 Acknowledgments

- Built with [SignalWire](https://signalwire.com) AI capabilities
- Inspired by the need for simple, AI-powered communication tools 