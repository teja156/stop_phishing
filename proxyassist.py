from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException
import requests

categories = ['SSL','GOOGLE','ANANY','UK','US','NEW','SPYS_ME','PROXYSCRAPE','PROXYLIST_DOWNLOAD_HTTP']
URL = "http://copyrightform-helpcenter.tk/support/"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}



def testConnection(ip,port):
	ip_port = ip + ":" + port
	r = requests.get(URL, headers=headers, proxies={"http":ip_port,"https":ip_port})
	print(r.status_code)
	return r.status_code

def getProxyAddress():
	scrapper = Scrapper(category='ALL', print_err_trace=False)
	data = scrapper.getProxies()
	status_code = 502
	for item in data.proxies:
		print('Checking {}:{}'.format(item.ip, item.port))
		try:
			status_code = testConnection(item.ip,item.port)
		except Exception as e:
			# print("Proxy connection failed")
			pass
		if status_code == 200:
			print("Valid proxy found")
			return item.ip + ":" + item.port

	return None

# getProxyAddress()

    	

