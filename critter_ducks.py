#! /usr/bin/python

import unirest, json, time

#####################################
ducksboard_key = 'EDIT ME!' #ducksboard api key, find from ducksboard portal
appId = 'EDIT ME!' #appid of crittercism registered app
access_token = 'EDIT ME!' #request access_token by using the provided client id
#####################################

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
	#for weekly view
	response = unirest.post(
	"https://push.ducksboard.com/v/482382", #enter ducksboard widget push api url
	headers={"Accept": "application/json", "Content-Type": "application/json"},
	params=json.dumps({
		"value": dau
		}),
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

	#chart view
	response = unirest.post(
		"https://push.ducksboard.com/v/490693", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": crashes
			}),
		auth=(ducksboard_key, ""))

#fetch monthly active users
"""create line chart beforehand"""
def fetch_monthly_active_users(access_token, appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/errorMonitoring/graph",
		headers={
			"Content-Type": "application/json",
			"Authorization" : "Bearer %s" % access_token
			},
		params=json.dumps({"params":{
			"graph": "mau",
			"duration": 1440,
			"appId": appId,
			}})
		)
	try:
		return response.body['data']['series'][0]['points'][0]
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_monthly_active_users')
		return None

def push_monthly_active_users(mau):
	response = unirest.post(
		"https://push.ducksboard.com/v/482056", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": mau
			}),
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
def fetch_daily_crashes_os(access_token, appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/errorMonitoring/pie",
		headers={
			"Content-Type": "application/json", 
			"Authorization" : "Bearer %s" % access_token
			},
		params=json.dumps({"params":{
				"graph": "crashes",
				"duration": 1440, 
				"groupBy": "os",
				"appId": appId
			}})
		)

	os_list = []
	try:
		for series in response.body['data']['slices']:	
			os_list.append((series['label'], series['value']))
		os_list = sorted(os_list, key=lambda x: x[1], reverse=True)[0:4]
		return map(list, zip(*os_list))
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_crashes_os')
		return [None, None]

#push daily crashes by os
def push_daily_crashes_os(os_list):
	response = unirest.post(
		"https://push.ducksboard.com/v/499410", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": os_list[1][0]
			}),
		auth=(ducksboard_key, ""))

	response = unirest.post(
		"https://push.ducksboard.com/v/499411", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": os_list[1][1]
			}),
		auth=(ducksboard_key, ""))

	response = unirest.post(
		"https://push.ducksboard.com/v/499412", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": os_list[1][2]
			}),
		auth=(ducksboard_key, ""))

	response = unirest.post(
		"https://push.ducksboard.com/v/499413", #enter ducksboard widget push api url
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
			"value": os_list[1][3]
			}),
		auth=(ducksboard_key, ""))
	#renames values for bar charts dynamically
	response = unirest.put(
 		"https://app.ducksboard.com/api/widgets/400402", #enter ducksboard widget push api url
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

#updates monthly active users
	mau = fetch_monthly_active_users(access_token, appId)
	if mau is not None:
		push_monthly_active_users(mau)
	time.sleep(1)

#updates daily service monitoring rate (error rate)
	service_list = fetch_daily_service_monitoring_rate(access_token, appId)
	if service_list is not None:
		push_daily_service_monitoring_rate(service_list)
	time.sleep(1)

#updates daily crashes by os
	os_list = fetch_daily_crashes_os(access_token, appId)
	if os_list is not None:
		push_daily_crashes_os(os_list)
	time.sleep(1)



if __name__=='__main__':
	main()