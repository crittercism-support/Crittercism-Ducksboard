#! /usr/bin/python

import unirest, json, time, datetime

#####################################
ducksboard_key = 'EDIT ME!' #ducksboard api key, find from ducksboard portal
appId = 'EDIT ME!' #appid of crittercism registered app
access_token = 'EDIT ME!' #request access_token by using the provided client id
#####################################

#fetch Crittercism API start datetime for data requested
def get_start_time(response):
	if isinstance(response, unirest.UnirestResponse):
		response = response.body
	try:
		start_time = response['data']['start']
		start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
		return start_time
	except KeyError as e:
		print 'Error: Could not access %s in %s.' % (str(e), 'get_start_time')
		return None

#fetch daily app loads
"""please create counters widget beforehand"""
def fetch_daily_appLoads(access_token, appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/errorMonitoring/graph",
		headers={
			"Content-Type": "application/json",
			"Authorization" : "Bearer %s" % access_token
			},
		params=json.dumps({"params":{
			"graph": "appLoads",
			"duration": 1440,
			"appId": appId,
			}})
		)
	try:
		return response.body['data']['series'][0]['points'][0]
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_app_loads')
		return  None

#push daily app loads
def push_daily_appLoads(appLoads):
	response = unirest.post(
		"https://push.ducksboard.com/v/480100", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": appLoads
			}),
		auth=(ducksboard_key, ""))
		
#fetch daily active users
"""please create counters widget and area graph beforehand"""
def fetch_daily_active_users(access_token, appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/errorMonitoring/graph",
		 headers={
			"Content-Type": "application/json",
			"Authorization": "Bearer %s" % access_token
		},
		params=json.dumps({"params":{
			"graph": "dau",
			"duration": 1440,
			"appId": appId
			}})
		)
	try:
		return response.body['data']['series'][0]['points'][0]
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_app_loads')
		return None

#push daily active users
def push_daily_active_users(dau):
	#for 24 hour view
	response = unirest.post(
		"https://push.ducksboard.com/v/480127", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": dau
			}),
		auth=(ducksboard_key, ""))

#fetch daily active users graph view
response = unirest.post(
	"https://developers.crittercism.com:443/v1.0/errorMonitoring/graph",
	 headers={
		"Content-Type": "application/json",
		"Authorization": "Bearer %s" % access_token
	},
	params=json.dumps({"params":{
		"graph": "dau",
		"duration": 10080,
		"appId": appId
		}})
	)
start_time = get_start_time(response)
try:
	dau = response.body['data']['series'][0]['points']
except KeyError as e:
	print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_app_loads')
	dau = None

#push daily active users graph view
date = start_time
for i, dau in zip(range(30), dau):
		date += datetime.timedelta(days=1)
		start_time = int((date - datetime.datetime(1970, 1, 1)).total_seconds())

		response = unirest.post(
			"https://push.ducksboard.com/v/482382", #enter ducksboard widget push api url
			headers={"Accept": "application/json", "Content-Type": "application/json"},
			params=json.dumps([{
				"value": dau,
				"timestamp" : start_time
			}]),
			auth=(ducksboard_key, ""))

#fetch daily crash percent
"""please create gauges meter beforehand""" 
def fetch_daily_crash_percent(access_token, appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/errorMonitoring/graph",
		headers={
			"Content-Type": "application/json",
			"Authorization": "Bearer %s" % access_token
			},
		params=json.dumps({"params":{
			"value_type": "percent",
			"graph": "crashPercent",
			"duration": 1440,
			"appId": appId
			}})
		)
	try:
		crash_rate = float(response.body['data']['series'][0]['points'][0])
		return crash_rate / 100
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_crash_percent')
		return None
		
#push daily crash percent
def push_daily_crash_percent(crash_rate):
	response = unirest.post(
		"https://push.ducksboard.com/v/480953", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": crash_rate
			}),
		auth=(ducksboard_key, ""))
		
#fetch daily app crashes
"""create  counters widget and area graph beforehand"""
def fetch_daily_app_crashes(access_token,appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/errorMonitoring/graph",
		headers={
			"Content-Type": "application/json",
			"Authorization": "Bearer %s" % access_token
			},
		params=json.dumps({"params":{
			"graph": "crashes",
			"duration": 1440,
			"appId": appId
			}})
		)
	try:
		return response.body['data']['series'][0]['points'][0]
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_app_crashes')
		return None

#push daily app crashes
def push_daily_app_crashes(crashes):
	response = unirest.post(
		"https://push.ducksboard.com/v/480957", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": crashes
			}),
		auth=(ducksboard_key, ""))

#fetch 30 days app crashes
response = unirest.post(
	"https://developers.crittercism.com:443/v1.0/errorMonitoring/graph",
	headers={
		"Content-Type": "application/json",
		"Authorization": "Bearer %s" % access_token
		},
	params=json.dumps({"params":{
		"graph": "crashes",
		"duration": 43200,
		"appId": appId
		}})
	).body

start_time = get_start_time(response)
try:
	crashes = response['data']['series'][0]['points']
except KeyError as e:
	print 'Error: Could not access %s in %s.' % (str(e), 'get_monthly_active_users')
	crashes = None

date = start_time

#push 30 days app crashes
for i, crashes in zip(range(30), crashes):
		date += datetime.timedelta(days=1)
		start_time = int((date - datetime.datetime(1970, 1, 1)).total_seconds())

		response = unirest.post(
			"https://push.ducksboard.com/v/490693", #enter ducksboard widget push api url
			headers={"Accept": "application/json", "Content-Type": "application/json"},
			params=json.dumps([{
				"value": crashes,
				"timestamp" : start_time
			}]),
			auth=(ducksboard_key, ""))

#fetch monthly active users
response = unirest.post(
	"https://developers.crittercism.com:443/v1.0/errorMonitoring/graph",
	headers={
		"Content-Type": "application/json",
		"Authorization" : "Bearer %s" % access_token
		},
	params=json.dumps({"params":{
		"graph": "mau",
		"duration": 43200,
		"appId": appId,
		}})
	)
start_time = get_start_time(response)
try:
	mau = response.body['data']['series'][0]['points']
except KeyError as e:
	print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_monthly_active_users')
	mau = None

#push monthly active users
date = start_time
for i, mau in zip(range(30), mau):
		date += datetime.timedelta(days=1)
		start_time = int((date - datetime.datetime(1970, 1, 1)).total_seconds())

		response = unirest.post(
			"https://push.ducksboard.com/v/482056", #enter ducksboard widget push api url
			headers={"Accept": "application/json", "Content-Type": "application/json"},
			params=json.dumps([{
				"value": mau,
				"timestamp" : start_time
			}]),
			auth=(ducksboard_key, ""))

#fetch service monitoring error rate (top three offenders)
"""create bar chart beforehand"""
def fetch_daily_service_monitoring_rate(access_token, appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/performanceManagement/pie",
		headers={
			"Content-Type": "application/json",
			"Authorization": "Bearer %s" % access_token,
			},
		params=json.dumps({"params":{
			"groupBy": "service",
			"graph": "errors",
			"duration": 60,
			"appId": appId
			}})
		)
	service_list = []
	try:
		for service in response.body['data']['slices']:
			service_list.append((service['label'], service['value']))
		service_list = sorted(service_list, key=lambda x: x[1], reverse=True)[0:4]
		return map(list, zip(*service_list))
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_service_monitoring_rate')
		return [None, None]

#push service monitoring error rate (top three offenders)
def push_daily_service_monitoring_rate(service_list):
	response = unirest.post(
		"https://push.ducksboard.com/v/782", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": service_list[1][0]
			}),
		auth=(ducksboard_key, ""))

	response = unirest.post(
		"https://push.ducksboard.com/v/482375", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": service_list[1][1]
			}),
		auth=(ducksboard_key, ""))

	response = unirest.post(
		"https://push.ducksboard.com/v/482376", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": service_list[1][2]
			}),
		auth=(ducksboard_key, ""))
	
	response = unirest.post(
		"https://push.ducksboard.com/v/482377", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": service_list[1][3]
			}),
		auth=(ducksboard_key, ""))	
	#renames values for bar charts dynamically
	response = unirest.put(
	    "https://app.ducksboard.com/api/widgets/389222", #enter ducksboard widget push api url
	     headers={"Accept": "application/json", "Content-Type": "application/json"},
	     params=json.dumps({"widget":{},
		"slots":{"1": {"subtitle" : service_list[0][0]},
			"2": {"subtitle" : service_list[0][1]},
			"3": {"subtitle" : service_list[0][2]},
			"4": {"subtitle" : service_list[0][3]}
			}}),                                                                                                                                                                              
	    auth=(ducksboard_key, ""))	

#fetch daily crashes by os
"""create line chart ahead of time"""
response = unirest.post(
	"https://developers.crittercism.com:443/v1.0/errorMonitoring/pie",
	headers={
		"Content-Type": "application/json", 
		"Authorization" : "Bearer %s" % access_token
		},
	params=json.dumps({"params":{
			"graph": "crashes",
			"duration": 10080, 
			"groupBy": "os",
			"appId": appId
		}})
	)

os_list = []
start_time = get_start_time(response)
try:
	for series in response.body['data']['slices']:	
		os_list.append((series['label'], series['value']))
	os_list = sorted(os_list, key=lambda x: x[1], reverse=True)[0:4]
	os_list = map(list, zip(*os_list))
except KeyError as e:
	print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_crashes_os')
	os_list = [None, None]

#push weekly crashes by os
date = start_time
for i in range(7):
		date += datetime.timedelta(days=1)
		start_time = int((date - datetime.datetime(1970, 1, 1)).total_seconds())

		response = unirest.post(
		"https://push.ducksboard.com/v/499410",
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps([{
			"value": os_list[1][0],
			"timestamp": start_time
			}]),
		auth=(ducksboard_key, ""))

		response = unirest.post(
			"https://push.ducksboard.com/v/499411",
			headers={"Accept": "application/json", "Content-Type": "application/json"},
			params=json.dumps([{
				"value": os_list[1][1],
			"timestamp": start_time
				}]),
			auth=(ducksboard_key, ""))

		response = unirest.post(
			"https://push.ducksboard.com/v/499412",
			headers={"Accept": "application/json", "Content-Type": "application/json"},
			params=json.dumps({
				"value": os_list[1][2],
			"timestamp": start_time
				}),
			auth=(ducksboard_key, ""))

		response = unirest.post(
			"https://push.ducksboard.com/v/499413",
			headers={"Accept": "application/json", "Content-Type": "application/json"},
			params=json.dumps({
				"value": os_list[1][3],
			"timestamp": start_time
				}),
			auth=(ducksboard_key, ""))

		response = unirest.put(
 			"https://app.ducksboard.com/api/widgets/400402",
 			headers={"Accept": "application/json", "Content-Type": "application/json"},
   			params=json.dumps({"widget":{},
  				"slots":{"1": {"subtitle" : os_list[0][0]},
			"2": {"subtitle" : os_list[0][1]},
			"3": {"subtitle" : os_list[0][2]},
			"4": {"subtitle" : os_list[0][3]}
				}}),                                                                                                                                                                              
   			auth=(ducksboard_key, ""))

def main():
#updates daily app loads
	appLoads = fetch_daily_appLoads(access_token, appId)
	if appLoads is not None:
		push_daily_appLoads(appLoads)
	time.sleep(1)
	
#updates daily active users
	dau = fetch_daily_active_users(access_token, appId)
	if dau is not None:
		push_daily_active_users(dau)
	time.sleep(1)

#updates daily crash percent
	crash_rate = fetch_daily_crash_percent(access_token, appId)
	if crash_rate is not None:
		push_daily_crash_percent(crash_rate)
	time.sleep(1)
	
#updates daily app crashes
	crashes = fetch_daily_app_crashes(access_token, appId)
	if crashes is not None:
		push_daily_app_crashes(crashes)
	time.sleep(1)

#updates daily service monitoring rate (error rate)
	service_list = fetch_daily_service_monitoring_rate(access_token, appId)
	if service_list is not None:
		push_daily_service_monitoring_rate(service_list)
	time.sleep(1)


if __name__=='__main__':
	main()