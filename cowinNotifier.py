import os
import sys
import smtplib
import datetime
import requests
import getopt
from time import time,ctime,sleep

G_senderEmail = ""
G_senderPassword = ""
G_receierList = ""
G_districtCode = ""

# https://myaccount.google.com/lesssecureapps to allow less secure apps to send email
def sendEmail(res):
	subject = 'Vaccine Slots Available'
	body = "Following vaccines centers are found \n\n" + res
	content = """\
From: %s
To: %s 
Subject: %s
%s
""" % (G_senderEmail, ", ".join(G_receierList), subject, body)
	print (content)

	try:
	    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	    server.ehlo()
	    server.login(G_senderEmail, G_senderPassword)
	    server.sendmail(G_senderEmail, G_receierList, content)
	    server.close()
	    print ('Email sent to: ' + ", ".join(G_receierList))
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
    userAgent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(endPoint, headers = userAgent)

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
            print ("Vaccine slot not available on: " + _date +"\n")
            return False
    else:
        print("Could not check for vaccine availability at the moment. HTTP Code: " + str(response.status_code))
        return False

def parseArgs(argv):
    global G_senderEmail, G_senderPassword,  G_receierList, G_districtCode

    usageString = 'Usage: cowinNotifier.py [-e senderEmail][-p senderPwd][-r commaSeparatedReceiversEmail][-d districtCode]' 
    try:
      opts, args = getopt.getopt(argv,"he:p:r:d:",["help","senderEmail=","senderPwd=","receiverList=","districtCode="])

    except getopt.GetoptError:
        print (usageString)
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            print (usageString)
            sys.exit(2)
        elif opt in ("-e", "--senderEmail"):
            G_senderEmail = arg
        elif opt in ("-p", "--senderPwd"):
            G_senderPassword = arg
        elif opt in ("-r", "--receiverList"):
            G_receierList = arg
        elif opt in ("-d", "--districtCode"):
            G_districtCode = arg
        else:
            print("Parameter " + opt + " is not supported")
            print(usageString)

    if (G_senderEmail == '' or G_senderPassword == '' or G_receierList == ''):
        print(usageString)
        sys.exit(3)
    if (G_districtCode == ''):
        G_districtCode = "193" # Code for district Ambala, if nothing is specified.
    G_receierList = G_receierList.split(',')
    G_receierList = [s.strip() for s in G_receierList]

    return 0

if __name__ == '__main__':
    periodicity = 5 # check every 5 minutes
    parseArgs(sys.argv[1:])	
	
    while True:
        for x in range(7):
            _date = datetime.date.today() + datetime.timedelta(days=x)
            _date = str(_date.strftime("%d/%m/%Y")).replace("/","-")
            endPoint = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + G_districtCode + "&date="+ _date
            if checkCenters(endPoint) == True:
                break
        print ("Sleeping for " + str(periodicity) + " mins")
        sleep(periodicity * 60)
        print ("Wake Up")        