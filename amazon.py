import requests
from time import sleep
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from requests import get

headers = {
    'authority': 'scrapeme.live',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}


req = requests.get('https://techmaniac.in/ps5restock/discordwebhookurls.txt', headers=headers)

urlss=str(req.text).replace("\n", '').split(",")

ipadd = get('https://api.ipify.org').text
print(ipadd)

url="https://www.amazon.in/dp/B08FV5GC28/" #add your product URL here
webhook = DiscordWebhook(url=urlss) #add your webhook urls to url.txt file with "," seperating each one 



def lambda_handler(url):

    r = requests.get(url, headers=headers)
     
    if r.status_code > 500:
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("IP Blocked by Amazon. Sleeping for 60 mins.", current_time)
        embed = DiscordEmbed(title='IP Blocked ', description=" Our IP is Blocked by Amazon. Going to sleep for 30 mins. Local Time = "+ current_time +" Current IP Address = " + ipadd, color=14973201)
        webhook.add_embed(embed)
        response = webhook.execute() #send Discord Notification
        sleep(3600) #sleep for 60 mins if Amazon Blocks Our IP
        return None

    if 'Type the characters you see in this image:' in r.text:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print ("Captcha error "+ current_time +" Current IP Address = " + ipadd)
        embed = DiscordEmbed(title='Captcha Error', description=url+"Amazon Requesting captcha. Retrying in 2 minutes. Local Time = "+ current_time +" Current IP Address = "+ ipadd, color=14973201)
        webhook.add_embed(embed)
        response = webhook.execute()
        sleep(120) #sleeps for 2 mins
        return None
    
                
    if 'Currently unavailable' in r.text:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print ("Not Available on Local Time = "+ current_time +" Current IP Address = " + ipadd)
        embed = DiscordEmbed(title='Play Station 5 Still Out Of Stock :/', description=url+" is not in stock yet. Local Time = "+ current_time +" Current IP Address = "+ ipadd, color=14973201)
        webhook.add_embed(embed)
        response = webhook.execute()
        sleep(420) #retries every 7 mins to avoid Amazon IP Ban
    else:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print ("Available on "+ current_time +" Current IP Address = " + ipadd)
        print(r.text)
        print(r.status_code)
        embed = DiscordEmbed(title='Play Station 5  | Back in Stock |', description=url+" is Back In Stock @ Local Time = "+ current_time +" Current IP Address = "+ ipadd, color=14973201)
        webhook.add_embed(embed)
        response = webhook.execute() #send Discord Notification

while True:
    lambda_handler(url)