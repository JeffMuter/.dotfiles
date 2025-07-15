# 🎵 CallHiss - AI-Powered Phone Call Assistant

CallHiss is a Python CLI tool that makes AI-powered phone calls using SignalWire and Anthropic's Claude AI. Simply describe what you want the AI to say, enter a phone number, and let the AI handle the conversation naturally!

## 🌟 Features

- **🤖 AI-Powered Conversations**: Uses Anthropic's Claude AI for intelligent, contextual responses
- **🎤 High-Quality Voice**: Neural voice synthesis (Polly.Joanna-Neural)
- **📞 Real Phone Calls**: Makes actual phone calls via SignalWire
- **💬 Natural Dialogue**: Handles back-and-forth conversations with speech recognition
- **🔧 Easy Setup**: Automated environment setup with Nix
- **🌐 Webhook Integration**: Automatic ngrok setup for local development

## 🚀 Quick Start (Nix Users)

### Prerequisites

1. **Nix** installed on your system
2. **SignalWire Account** (free trial available)
3. **Anthropic API Key** (for Claude AI)
4. **ngrok Account** (free tier works)

### Step 1: Clone and Enter Development Environment

```bash
git clone https://github.com/yourusername/callHiss.git
cd callHiss
nix-shell  # This automatically sets up everything!
```

The Nix shell will:
- ✅ Install Python 3.11 and all dependencies
- ✅ Set up ngrok authentication
- ✅ Load your configuration from `config.env`
- ✅ Create and activate a Python virtual environment

### Step 2: Create Your Configuration

Create a `config.env` file with your credentials:

```bash
# Copy the example config
cp config.env.example config.env

# Edit with your actual credentials
nano config.env
```

Fill in your actual values:

```bash
# SignalWire Configuration (get from https://signalwire.com)
export SPACE_URL=yourspace.signalwire.com
export PROJECT_ID=your-project-id-here
export API_TOKEN=your-api-token-here
export FROM_NUMBER=+12345678901  # Your SignalWire phone number

# Anthropic AI Configuration (get from https://console.anthropic.com)
export ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# ngrok Configuration (get from https://ngrok.com)
export NGROK_AUTHTOKEN=your-ngrok-token-here

# Application Settings
export HOST_APP=https://placeholder.ngrok.io  # Will be auto-updated
export PORT=3000
export AI_VOICE=Polly.Joanna-Neural
```

### Step 3: Set Up ngrok Tunnel

In a **separate terminal**:

```bash
ngrok http 3000
```

Copy the `https://` URL (e.g., `https://abc123.ngrok-free.app`) and update `HOST_APP` in your `config.env`, or use the automatic setup script:

```bash
./setup_env.sh  # Automatically detects and updates ngrok URL
```

### Step 4: Run CallHiss

```bash
source config.env  # Load your configuration
python call_hiss.py
```

You'll see:
```
🤖 Anthropic AI enabled for intelligent responses
🎤 Using voice: Polly.Joanna-Neural
🔐 Verifying SignalWire credentials...
✅ Authentication successful!
🌐 Webhook server started on https://abc123.ngrok-free.app
💭 What would you like the AI to say on the call?
```

### Step 5: Make Your First Call

```
📝 Enter your prompt (or 'quit' to exit):
> call and just say hi, ask how they're doing

📞 Enter the phone number to call (include country code, e.g., +1234567890):
> +16145551234

✅ Proceed with call? (y/N): y
```

The AI will call the number and have a natural conversation!

## 💻 Usage Examples

### Birthday Call
```
Prompt: "You're calling to wish James happy birthday from his sister Sarah. Tell him the family misses him!"
```

### Business Update
```
Prompt: "You're Annie from Pizza Hut calling to let the customer know their pizza will arrive 15 minutes early."
```

### Appointment Reminder
```
Prompt: "You're calling to remind them about their dentist appointment tomorrow at 2 PM. Ask them to confirm."
```

### Package Notification
```
Prompt: "You're Jill, Jack's assistant, calling to let them know their package is ready for pickup at the front desk."
```

## 🔧 Getting Your API Keys

### SignalWire Setup

1. **Sign up**: Go to [SignalWire.com](https://signalwire.com) and create an account
2. **Get credentials**: From your dashboard, copy:
   - **Space URL**: `yourspace.signalwire.com`
   - **Project ID**: Found in your project settings
   - **API Token**: Generate in your project settings
3. **Buy a phone number**: Purchase a number for outbound calls
4. **Verify numbers**: In trial mode, you can only call verified numbers

### Anthropic API Key

1. **Sign up**: Go to [console.anthropic.com](https://console.anthropic.com)
2. **Get API key**: Create an API key in your account settings
3. **Add credits**: Add some credits to your account for API usage

### ngrok Setup

1. **Sign up**: Go to [ngrok.com](https://ngrok.com) and create a free account
2. **Get auth token**: Copy your auth token from the dashboard
3. **Install**: ngrok is included in the Nix environment

## 🏗️ How It Works

1. **🎯 User Input**: You describe what the AI should say and provide a phone number
2. **📞 Call Initiation**: SignalWire creates an outbound call
3. **🌐 Webhook Handling**: Your local Flask server receives call events via ngrok
4. **🤖 AI Processing**: Claude AI generates contextual responses based on speech input
5. **🎤 Voice Synthesis**: Responses are converted to speech using neural voices
6. **💬 Conversation Flow**: AI maintains conversation history and responds naturally

## 📁 Project Structure

```
callHiss/
├── call_hiss.py          # Main application with Flask webhook server
├── requirements.txt      # Python dependencies
├── shell.nix            # Nix development environment (auto-setup)
├── setup_env.sh         # Automatic ngrok URL configuration
├── config.env           # Your credentials (create this file)
├── config.env.example   # Template for configuration
├── .gitignore           # Git ignore file (excludes sensitive files)
└── README.md            # This file
```

## 🔄 Version Control & GitHub Setup

### Initial Setup

The project is already initialized with Git and includes proper `.gitignore` to protect your sensitive configuration files.

### Connect to GitHub

1. **Create a new repository** on GitHub (don't initialize with README)

2. **Add the remote origin**:
```bash
git remote add origin https://github.com/yourusername/callHiss.git
```

3. **Push to GitHub**:
```bash
git push -u origin main
```

### Making Changes

```bash
# Make your changes to the code
git add .
git commit -m "✨ Add new feature: description of changes"
git push
```

### Important Notes

- ⚠️ **Never commit `config.env`** - it contains your API keys and is excluded by `.gitignore`
- ✅ **Always use `config.env.example`** to show others what configuration they need
- 🔐 **Keep your API keys secure** - they're automatically excluded from version control

## 🛠️ Advanced Configuration

### Voice Options

Change the AI voice by updating `AI_VOICE` in `config.env`:

```bash
export AI_VOICE=Polly.Joanna-Neural    # Default (female, US)
export AI_VOICE=Polly.Matthew-Neural   # Male, US
export AI_VOICE=Polly.Amy-Neural       # Female, UK
```

### Port Configuration

If port 3000 is in use, change it in `config.env`:

```bash
export PORT=3001
```

Then update your ngrok command: `ngrok http 3001`

## 🚨 Important Notes

### Trial Account Limitations
- **SignalWire Trial**: Can only call verified phone numbers
- **Costs**: SignalWire charges for calls (~$0.01-0.05/minute) and AI usage
- **Upgrade**: Remove trial limitations by adding billing to your SignalWire account

### Best Practices
- **Ethics**: Only call people who consent to receive calls
- **Legal**: Follow local laws regarding automated calls
- **Testing**: Use your own verified number for testing
- **Prompts**: Be specific about the AI's role and message

### Troubleshooting

**"Address already in use" error:**
```bash
# Kill any process using port 3000
lsof -ti:3000 | xargs kill -9
```

**"401 Authentication" error:**
- Verify your SignalWire credentials in `config.env`
- Check that your API token is current (they expire)

**"Unable to create record" error:**
- Ensure the phone number includes country code (+1 for US)
- Verify the number in your SignalWire account if using trial

**AI not responding:**
- Check that `ANTHROPIC_API_KEY` is set correctly
- Verify you have credits in your Anthropic account

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test with your own phone number
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **SignalWire**: For excellent voice API and AI capabilities
- **Anthropic**: For Claude AI that powers natural conversations
- **Nix Community**: For reproducible development environments 