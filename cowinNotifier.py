import os
import smtplib
import datetime
import requests
from time import time,ctime,sleep

# Replace below with the sender's email/password. It won't be cached anywhere. The script runs locally on your device.
senderEmail = 'sender@gmail.com'
senderPassword = 'senderPwd'

receiverList = ['receiver@gmail.com']
# Note this list can be comma separated to notify multiple people like 
# ['receiver1@gmail.com', 'receiver2@gmail.com']

# https://myaccount.google.com/lesssecureapps to allow less secure apps to send email
def sendEmail(res):
	subject = 'Vaccine Slots Available'
	body = "Following vaccines centers are found \n\n" + res
	content = """\
From: %s
To: %s 
Subject: %s
%s
""" % (senderEmail, ", ".join(receiverList), subject, body)
	print (content)

	try:
	    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	    server.ehlo()
	    server.login(senderEmail, senderPassword)
	    server.sendmail(senderEmail, receiverList, content)
	    server.close()
	    print ('Email sent to: ' + ", ".join(receiverList))
	except Exception as exc:
	    print ('Exception sending email. Exception')
	    print (exc)
	
def availableCenters(result):
	retVal = []
	centers = result['centers']
	for center in centers:
		sessions = center['sessions']
		for session in sessions:
			if session['available_capacity'] > 0:
				res = { 'name':center['name'], 'block_name':center['block_name'],'age_limit':session['min_age_limit'], 'vaccine_type':session['vaccine'] , 'date':session['date'],'available_capacity':session['available_capacity'] }
				retVal.append(res)
	return retVal			
	
def checkCenters(endPoint):
    print(ctime(time()))
    print (endPoint)
    response = requests.get(endPoint)

    if response.status_code == 200:
        result = response.json()
        jsonResult = availableCenters(result)
        if len(jsonResult) > 0:
            print ("Vaccine Slots Available")
            print('\007')
            resultStr = ""
            for center in jsonResult:
                resultStr = resultStr + center['name'] + "\n"
                resultStr = resultStr + "block:"+center['block_name'] + "\n"
                resultStr = resultStr + "vaccine count:"+str(center['available_capacity']) + "\n"
                resultStr = resultStr + "vaccine type:"+ center['vaccine_type'] + "\n"
                resultStr = resultStr + "Date:"+ center['date'] + "\n"
                resultStr = resultStr + "age_limit:"+str(center['age_limit'])+"\n"
                resultStr = resultStr + "-----------------------------------------------------\n"
            sendEmail(resultStr)
            return True
        else:
            return False
    else:
	    return False

if __name__ == '__main__':
    periodicity = 5 # check every 5 minutes
    districtCode = "193" # Code for district ambala
	# To locate your district code, do the following:
	# Check for your state, visit https://cdn-api.co-vin.in/api/v2/admin/location/states
	# Get the state_id for your state, and visit https://cdn-api.co-vin.in/api/v2/admin/location/districts/<state_id> e.g. https://cdn-api.co-vin.in/api/v2/admin/location/districts/12

    while True:
        for x in range(7):
            _date = datetime.date.today() + datetime.timedelta(days=x)
            _date = str(_date.strftime("%d/%m/%Y")).replace("/","-")
            endPoint = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + districtCode+ "&date="+ _date
            if checkCenters(endPoint) == True:
                break
            else:
                print ("Vaccine slot not available on: " + _date +"\n")
        print ("Sleeping for " + str(periodicity) + " mins")
        sleep(periodicity * 60)
        print ("Wake Up")        