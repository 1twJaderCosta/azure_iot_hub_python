import psutil
import datetime
import time
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=IOthubnametest.azure-devices.net;DeviceId=testedevice;SharedAccessKey=YEEoSXDGu3QFZ1XegDZudxNODBRD4A6e0NuW+M7tUek="
# Define the JSON message to send to IoT Hub.
MSG_TXT = '{{"timestamp":"{timestamp}","user":"{user}","cpu_percent":{cpu_percent},"total_mem":{total_mem},"available_mem":{available_mem}}}'

def iothub_client_init():
  # Create an IoT Hub client
  client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
  return client
  
def iothub_client_telemetry_sample_run():
    try:
      client = iothub_client_init()
      print ( "Sending periodic messages, press Ctrl-C to exit" )
      client.connect()
    except Exception as ex:
      print('errr', ex)

    # Build the message with simulated telemetry values.
    timestamp = datetime.datetime.fromtimestamp(time.time()).isoformat()            
    user = psutil.users()[0].name
    mem = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent()
    total_mem = mem.total/(1024*1024*1024)
    available_mem = mem.available/(1024*1024*1024)
                
    msg_txt_formatted = MSG_TXT.format(timestamp=timestamp, user=user, cpu_percent=str(round(cpu_percent,2)), total_mem=str(round(total_mem,2)), available_mem=str(round(available_mem,2)))
    message = Message(msg_txt_formatted)

    # Add a custom application property to the message.
    # An IoT hub can filter on these properties without access to the message body.
    if cpu_percent > 80:
      message.custom_properties["cpuAlert"] = "true"
    else:
      message.custom_properties["cpuAlert"] = "false"
    # Send the message.
    print( "Sending message: {}".format(message) )
    
    client.send_message(message)
    print ( "Message successfully sent" )
    #time.sleep(1)
    client.shutdown()

    


iothub_client_telemetry_sample_run()