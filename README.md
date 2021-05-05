# cowin-notifier
A basic python script that can be used to check the availability of vacccine in your district. It will notify you via an email.
Checks for vaccine for next 7 days.

Usage: cowinNotifier.py [-e senderEmail][-p senderPwd][-r commaSeparatedReceiversEmail][-d districtCode]

Sample:
python cowinNotifier.py -e sender@gmail.com -p myPwd -r receiver1@gmail.com,receiver2@gmail.com -d 193

Note:
1. -e , -p and -r are necessary arguments.
2. -d district code should be specified to search within your district
3. 	To locate your district code, do the following:
	- Check for your state code, visit https://cdn-api.co-vin.in/api/v2/admin/location/states
	- Get the state_id for your state, and visit https://cdn-api.co-vin.in/api/v2/admin/location/districts/<state_id> e.g. https://cdn-api.co-vin.in/api/v2/admin/location/districts/12
4. The sender email account has to allow less secure apps to send email: https://myaccount.google.com/lesssecureapps to allow less secure apps to send email
5. Recommendation is to use a backup account to ensure complete security.