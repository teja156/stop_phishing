from discord_webhooks import DiscordWebhooks
import pytz
from datetime import datetime 

def send_msg(status,sent,error):
	IST = pytz.timezone('Asia/Kolkata')
	datetime_ist = datetime.now(IST)
	timestamp = datetime_ist.strftime('%Y:%m:%d %H:%M:%S %Z %z')

	WEBHOOK_URL = "https://discordapp.com/api/webhooks/"
	webhook = DiscordWebhooks(WEBHOOK_URL)
	webhook.set_footer(text='-- Teja Swaroop')

	if status=="info":
		webhook.set_content(title="Report")
		webhook.add_field(name='Sent',value=sent)
		webhook.add_field(name="timestamp",value=timestamp)
	if status == "error":
		webhook.set_content(title="Error occured")
		webhook.add_field(name='Sent until here',value=sent)
		webhook.add_field(name='Error',value=error)
		webhook.add_field(name="timestamp",value=timestamp)

	try:	
		webhook.send()
		print("Message sent to discord")
	except Exception as e:
		print("Message failed to send to discord")
