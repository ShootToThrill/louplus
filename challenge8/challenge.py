import re 
from datetime import datetime,timedelta
from collections import Counter

def open_parser(filename):
	with open(filename) as logfile:
		pattern = (r''
                   r'(\d+.\d+.\d+.\d+)\s-\s-\s'  # IP ??
                   r'\[(.+)\]\s'  # ??
                   r'"GET\s(.+)\s\w+/.+"\s'  # ????
                   r'(\d+)\s'  # ???
                   r'(\d+)\s'  # ????
                   r'"(.+)"\s'  # ???
                   r'"(.+)"'  # ?????
                   )
		parsers = re.findall(pattern,logfile.read())
	return parsers

def main():
	# logs = open_parser('/home/shiyanlou/Code/nginx.log')
	logs = open_parser('nginx.log')
	max_ip_count = 0
	ip_count = {}
	ip_dict = {}
	max_ip_count = 0

	url_count_404 = {}
	url_dict = {}
	max_url_count_404 = 0


	for log in logs:
		ip,_time,url,status,length,header,client = log
		utc_date = datetime.strptime(_time,'%d/%b/%Y:%H:%M:%S +0800')
		local_date = utc_date
		local_date_str = local_date.strftime('%Y%m%d')
		if local_date_str == '20170111':
			if ip not in ip_count:
				this_ip_count = 1
			else:
				this_ip_count = ip_count[ip] + 1
			ip_count[ip] = this_ip_count

			if this_ip_count > max_ip_count:
			 	max_ip_count = this_ip_count
			 	ip_dict = {ip:this_ip_count}
			elif this_ip_count == max_ip_count and ip not in ip_dict:
			 	ip_dict[ip] = this_ip_count

		if status == '404':
			if url not in url_count_404:
				this_url_count = 1
			else:
				this_url_count = url_count_404[url] +1
			url_count_404[url] = this_url_count

			if this_url_count > max_url_count_404:
				max_url_count_404 = this_url_count
				url_dict = {url:this_url_count}
			elif this_url_count == max_url_count_404 and url not in url_dict:
				url_dict[url] = this_url_count

	# url_map = [ log[2] for log in logs if log[3] == '404']
	# print(Counter(url_map))

	return ip_dict, url_dict

if __name__ == '__main__':
	# main()
	ip_dict, url_dict = main()
	print(ip_dict,url_dict)