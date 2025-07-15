# PyDial - AI-Powered Phone Calls

PyDial is a Python-based tool that enables AI-powered phone calls using SignalWire's API. It supports background audio playback during calls and customizable voice settings.

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with the following configuration:

```env
# SignalWire API Configuration
SIGNALWIRE_API_KEY=your_api_key_here
SIGNALWIRE_PROJECT_ID=your_project_id_here
SIGNALWIRE_PHONE_NUMBER=your_signalwire_phone_number  # No + prefix needed

# Target Phone Number (number being called)
TARGET_PHONE_NUMBER=target_phone_number_here  # No + prefix needed

# Voice Configuration
SIGNALWIRE_VOICE_GENDER=female  # Options: female, male
SIGNALWIRE_VOICE_LOCALE=en-US  # Options: en-US, en-GB, en-AU

# Background Audio Configuration (optional)
# SIGNALWIRE_BACKGROUND_AUDIO_URL=https://example.com/path/to/audio.mp3
# SIGNALWIRE_BACKGROUND_VOLUME=-20  # Volume in dB, default: -20
```

## Usage

1. Set up your environment variables as shown above
2. Run the script:
   ```bash
   python main.py
   ```
3. Follow the interactive prompts to:
   - Enter your name (who you're calling as)
   - Enter the contact's name
   - Specify the call objective
   - Add any additional context
4. Confirm the call details to initiate the call

## Features

- AI-powered phone conversations
- Background audio support during calls
- Customizable voice settings (gender and locale)
- Interactive CLI interface
- Rich terminal output with call status and details

## Voice Options

Available voice configurations:

### Female Voices
- US English: Joanna-Neural (en-US)
- British English: Amy (en-GB)
- Australian English: Olivia (en-AU)

### Male Voices
- US English: Matthew (en-US)
- British English: Brian (en-GB)
- Australian English: Russell (en-AU)

## Background Audio

You can add background audio to your calls by setting the following environment variables:

- `SIGNALWIRE_BACKGROUND_AUDIO_URL`: URL to your audio file (MP3 format recommended)
- `SIGNALWIRE_BACKGROUND_VOLUME`: Volume level in dB (default: -20)

The background audio will play continuously during the call while the AI speaks.

## Error Handling

The script includes comprehensive error handling for:
- Missing environment variables
- Invalid API credentials
- Failed API calls
- Invalid phone numbers
- Network issues

## Dependencies

See `requirements.txt` for a full list of dependencies 