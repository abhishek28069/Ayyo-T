import json, random
from supabase import create_client
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

url = "https://zakntpuxbdegdkyvdzkw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpha250cHV4YmRlZ2RreXZkemt3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODEyODIyNjEsImV4cCI6MTk5Njg1ODI2MX0.qJp48cSwfb0QKFOE-TAB22yJN_m6rU6kK5Ers_GgcHM"
supabase = create_client(url, key)

# send in blue setup (smtp)
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'


def getGroups():
     response = supabase.table('sensor_registry').select('group_name', count="exact").execute()
     data = dict(response)['data']
     data = list(set([x['group_name'] for x in data]))
     count = len(data)
     return {"count":count,"data":data}

def getTypes():
     response = supabase.table('sensor_registry').select('sensor_type', count="exact").execute()
     data = dict(response)['data']
     data = list(set([x['sensor_type'] for x in data]))
     count = len(data)
     return {"count":count,"data":data}

def getSensors(activated):
     print('Getting all sensors')
     if activated is not None:
          response = supabase.table('sensor_registry').select('*', count="exact").eq('activated',activated).execute()
     else:
          response = supabase.table('sensor_registry').select('*', count="exact").execute()
     return response

def getSensorsByGroup(group, activated):
     print('Getting sensor by group',group)
     if activated is not None:
          response = supabase.table('sensor_registry').select('*', count="exact").eq('group_name',group).eq('activated',activated).execute()
     else:
          response = supabase.table('sensor_registry').select('*', count="exact").eq('group_name',group).execute()
     return response

def getSensorsByType(type, activated):
     print('Getting sensor by type',type)
     if activated is not None:
          response = supabase.table('sensor_registry').select('*', count="exact").eq('sensor_type',type).eq('activated',activated).execute()
     else:
          response = supabase.table('sensor_registry').select('*', count="exact").eq('sensor_type',type).execute()
     return response

def getSensorsByGroupAndType(group,type, activated):
     print('Getting sensor by type',type)
     if activated is not None:
          response = supabase.table('sensor_registry').select('*', count="exact").eq('group_name',group).eq('sensor_type',type).eq('activated',activated).execute()
     else:
          response = supabase.table('sensor_registry').select('*', count="exact").eq('group_name',group).eq('sensor_type',type).execute()
     return response

def getSensorByID(sensor_id):
     print('Getting sensor by name',sensor_id)
     response, count = supabase.table('sensor_registry').select('*').eq('id',sensor_id).execute()
     if(len(response[1]) == 0):
          return {"error": True, "msg": "Sesnor Not found, Check the name"}
     data = response[1][0]
     data['error'] = False
     return data

def getLatestData(sensor_id):
     response = getSensorByID(sensor_id)
     if response['error'] == True:
          return {'error': True, 'msg':"Sensor not found, Check the name"}
     data_info = response['data_info']
     response = supabase.table('sensor_data').select('data').eq('sensor_name',response["sensor_name"]).execute()
     print('🔥')
     print(response)
     data = dict(response)['data'][-1]['data']
     return {"data_format": json.loads(data_info), "data":json.loads(data), "error": False}

def getHistoricData(row_count,sensor_id):
     response = getSensorByID(sensor_id)
     if response['error'] == True:
          return {'error': True, 'msg':"Sensor not found, Check the name"}
     data_info = response['data_info']
     response = dict(supabase.table('sensor_data').select('data',count='exact').eq('sensor_name',response["sensor_name"]).execute())
     print('👾👾👾👾',type(response))
     # print(dict(response))
     data = dict(response)['data']
     if(len(data) >= row_count):
          data = data[:row_count]
     data = [json.loads(x["data"]) for x in data]
     return {'data':data, 'data_format':json.loads(data_info), 'count':len(data), 'error': False}


def toggle_sensor(group_name, sensor_type, sensor_name):
    data, _ = (
        supabase.table("sensor_registry")
        .select("activated")
        .eq("group_name", group_name)
        .eq("sensor_type", sensor_type)
        .eq("sensor_name", sensor_name)
        .execute()
    )
    activated = "FALSE" if data[1][0]["activated"] else "TRUE"
    print("toggling",sensor_name,"to", activated)
    supabase.table("sensor_registry").update({"activated": activated}).eq(
        "group_name", group_name
    ).eq("sensor_type", sensor_type).eq("sensor_name", sensor_name).execute()

def getCustomSensorsByGroup(group_name,sensors_list,counts):
     result = {}
     for i in range(len(sensors_list)):
          res = supabase.table('sensor_registry').select('id').eq('group_name',group_name).eq('sensor_type',sensors_list[i]).execute()
          res = (dict(res))['data']
          ids = [obj['id'] for obj in res]
          if(counts[i] > len(res)):
               return False
          if(len(res) == counts[i]):
               result[sensors_list[i]] = ids
          else:
               result[sensors_list[i]] = random.sample(ids, counts[i])
     return result

def getCustomGroups(requirements):
     sensor_types = list(requirements.keys())
     counts = list(requirements.values())
     group_list = getGroups()['data']
     print(group_list)
     response = {}
     for group in group_list:
          res = getCustomSensorsByGroup(group,sensor_types,counts)
          if(res != False):
               response[group] = res
     return response


def getControllersByGroup(group):
     print('Getting sensor by group',group)
     response = supabase.table('controller_registry').select('*', count="exact").eq('group_name',group).execute()
     return response

def toggle_controller(id, state):
    supabase.table("controller_registry").update({"activated": state}).eq("id", id).execute()

def send_email(to_email, subject, message):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = subject
    sender = {"name":"Abhishek","email":"abhishek28069@gmail.com"}
    html_content = "<html><body>"+message+"</body></html>"
    to = [{"email":to_email, "name": "User"}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)
    try:
        api_instance.send_transac_email(send_smtp_email)
        return True
    except ApiException as e:
        print("Exception when calling SMTPApi->sendTransacEmail: %s\n" % e)
        return False