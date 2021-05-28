import requests

url = "http://data.ecan.govt.nz/data/133/Water/Consent%20Irrigation%20Restrictions/CSV?RecordNo=CRC205005&Today=17%2F05%2F2021"
req = requests.get(url)
urlContent = req.content
csv_file = open('../downloaded.csv', 'wb')
csv_file.write(urlContent)
csv_file.close()
