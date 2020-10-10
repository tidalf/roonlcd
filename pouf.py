import roonapi
import time

def state_callback(event, changed_items):
    print("%s: %s" %(event, changed_items))

appinfo = {
        "extension_id": "oled_info",
        "display_name": "Python library oled info for Roon",
        "display_version": "1.0.0",
        "publisher": "tidalf",
        "email": "tidalf@ematome.com"
    }
    
token = open('mytokenfile').read()
roonapid = roonapi.RoonApi(appinfo, token)
import json
# get all zones (as dict)

#for zone in roonapid.zones: 
    # if (zone.zone_id=="160155895af4376afe74c12da20fdadfc027"):
# dac_zone='160155895af4376afe74c12da20fdadfc027'
dac_zone=0

while not dac_zone:
  for zone in roonapid.zones:
      if roonapid.zones[zone]['display_name'] == "evo":
          dac_zone=zone
  time.sleep(10)
  print( "waiting for evo")
    
print(roonapid.zones[dac_zone]['now_playing']['one_line']['line1'])
# get all outputs (as dict)
# print(json.dumps(roonapid.outputs))

# receive state updates in your callback
# roonapid.register_state_callback(state_callback)


# time.sleep(100)

# save the token for next time
with open('mytokenfile', 'w') as f:
    f.write(roonapid.token)


