import traceback

DISCORD_WEBHOOK = Prefs['discord_webhook']

def setAPI(api):
   	global DISCORD_WEBHOOK
   	DISCORD_WEBHOOK = api

def send(message, channel=None):
    data = {
        'text': message
    }
    if channel:
        data['DISCORD_WEBHOOK'] = DISCORD_WEBHOOK
    try:
        return JSON.ObjectFromURL(DISCORD_WEBHOOK + "/slack", values=data)
    except Exception as e:
        Log.Debug("Error in send: " + e.message)
        Log.Error(str(traceback.format_exc()))  # raise last error
    return None

	
	
