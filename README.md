# cowin-notifier
Cowin-Notifier checks the availability of a vaccine slot for next 7 days in your district for your age and notifies you via an email.

Usage: cowinNotifier.py [-e senderEmail][-p senderPwd][-r commaSeparatedReceiversEmail][-d districtCode][-a age]

Sample Command:
python cowinNotifier.py -e sender@gmail.com -p myPwd -r receiver1@gmail.com,receiver2@gmail.com -d 193 -a 25

Note:
1. -e , -p and -r are necessary arguments.
2. -a is an optional argument. If specified, it will check for slot availablilty for your age. If not, will show for all age groups.
3. -d district code should be specified to search within your district
4. To locate your district code, do the following:
    - Check for your state code, visit https://cdn-api.co-vin.in/api/v2/admin/location/states
    - Get the state_id for your state, and visit https://cdn-api.co-vin.in/api/v2/admin/location/districts/<state_id> e.g. https://cdn-api.co-vin.in/api/v2/admin/location/districts/12
5. The sender email account has to allow less secure apps to send an email. 
    - https://myaccount.google.com/lesssecureapps
    - Recommendation is to use a backup account to ensure complete security.