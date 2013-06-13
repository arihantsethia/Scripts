#This code parse xml from LinkedIn API response to give public info about registered companies on LinkedIn

import oauth2 as oauth
import urlparse
import urllib
from xml.dom import minidom 

# Returns the string without non ASCII characters
def strip_non_ascii(string):
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

#Returns the value of firstchild node
def get_element_value(dom,attr):
	t = dom.getElementsByTagName(attr)
	if (len(t) and len(t[0].childNodes)):
		return t[0].childNodes[0].nodeValue
	else :
		return " Not Filled "

#Returns the dom of firstchild node
def get_element(dom,attr):
	t = dom.getElementsByTagName(attr)
	if len(t):
		return t[0]
	else :
		return dom.createElement(attr)


api_key           = "xxxxxxxxxx"
api_secret        = "xxxxxxxxxxxxxx"
consumer = oauth.Consumer(api_key, api_secret)
client = oauth.Client(consumer)
text = '"Id","Name","Company Type","Company Size","Website","Industry","Street","City","Postal Code", \n '
f = open('50000-100000.csv', 'a') 
f.write(text) 
start_id = 1
end_id = 100
for i in range(start_id,end_id) :
	temp,response = client.request("http://api.linkedin.com/v1/companies/%s:(id,name,company-type,employee-count-range,website-url,industry,locations:(is-headquarters,address),email-domains)"%(i))
	if(temp.status == 200) :
		dom = minidom.parseString(response)
		temp = '" %s ",'%(i) #LinkednID
		temp = temp + '"'+get_element_value(dom,'name')+'",' #Name
		tempDom = get_element(dom,'company-type')
		temp = temp + '"'+get_element_value(tempDom,'name')+'",' #Company Type
		tempDom =  get_element(dom,'employee-count-range')
		temp = temp + '"'+get_element_value(tempDom,'name')+'",' #Company Size
		temp = temp + '"'+get_element_value(dom,'website-url')+'",' #Website URL
		temp = temp + '"'+get_element_value(dom,'industry')+'",' #Industry
		#Locations
		#tempDom = dom.getElementsByTagName('locations')[0]
		tempDom = get_element(dom,'locations')
		tempDom	= tempDom.getElementsByTagName('location')
		for doms in tempDom	:
			if(doms.getElementsByTagName('is-headquarters')[0].childNodes[0].nodeValue== 'true'):
				temp = temp + '"'+get_element_value(doms,'street1')+'",' #Locations
				temp = temp + '"'+get_element_value(doms,'city')+'",' #Locations
				temp = temp + '"'+get_element_value(doms,'postal-code')+'",' #Locations
		emailList = dom.getElementsByTagName('email-domain')
		emails =''
		for email in emailList :
			emails = emails +email.childNodes[0].nodeValue + ' , '
		temp =  temp + '"'+emails+'",' #Email Domains
		temp = temp +',\n'   
		temp= strip_non_ascii(temp)
		f.write(temp)
		print "Successfull %s"%(i)
	else :
		print "Unsuccessfull %s"%(i)
f.close()
