# 🔍 401 Error Diagnosis and Solution

## Problem Summary

You're experiencing a **401 Unauthorized** error when trying to use CallHiss. This means your SignalWire credentials are not working properly.

## Root Cause

The authentication is failing because one or more of these issues:

1. **Incorrect API Token** - The token in your config.env doesn't match your SignalWire account
2. **Incorrect Project ID** - The project ID doesn't exist in your SignalWire space
3. **Wrong SignalWire Space** - The credentials belong to a different space
4. **Expired/Revoked Token** - Your API token has been deactivated

## Immediate Solution

### Step 1: Get Correct Credentials

1. Go to [SignalWire Dashboard](https://signalwire.com/signin)
2. Select your space: **saorsadev**
3. Navigate to the **API** section
4. Copy the **Project ID** and **API Token**

### Step 2: Update Configuration

Edit your `config.env` file with the correct values:

```bash
# SignalWire Configuration
export SPACE_URL=saorsadev
export PROJECT_ID=your_actual_project_id_here
export API_TOKEN=your_actual_api_token_here
export FROM_NUMBER=+16144126309
```

### Step 3: Reload and Test

```bash
# Reload environment variables
source config.env

# Test credentials
python verify_credentials.py
```

### Step 4: Run CallHiss

Once verification passes:
```bash
python call_hiss.py
```

## Verification Tools Created

I've created several tools to help you troubleshoot:

1. **`verify_credentials.py`** - Quick credential check
2. **`debug_401.py`** - Comprehensive 401 error analysis  
3. **`fix_401_issue.py`** - Guided troubleshooting
4. **`TROUBLESHOOTING.md`** - Complete troubleshooting guide

## What Was Fixed

1. **Enhanced error handling** - CallHiss now checks credentials before starting
2. **Better error messages** - Clear guidance when authentication fails
3. **Debugging tools** - Multiple scripts to help identify issues
4. **Space URL formatting** - Automatic correction of space URL format
5. **Comprehensive documentation** - Step-by-step troubleshooting guide

## Next Steps

1. **Update your credentials** using the steps above
2. **Run the verification tool** to confirm everything works
3. **Start using CallHiss** for AI-powered phone calls

The 401 error should be resolved once you update your SignalWire credentials with the correct values from your dashboard. 