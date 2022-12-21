#sudo chmod 777 /dev/ttyUSB0


def is_cnx_active():
    import urllib.request
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

def updateJson(idchannel,msg,key):
    import json
    import requests
    import time

    e=[]
    url = 'https://api.thingspeak.com/channels/'+idchannel+'/bulk_update.json' # ThingSpeak server settings
    update={}
    update['created_at']=time.strftime('%Y-%m-%d %H:%M:%S',  time.gmtime(time.time()))
    canale=0
    for field in msg:
        canale=canale+1
        update['field'+str(canale)]=field
        
    message_buffer=[update]

    bulk_data = json.dumps({'write_api_key':key,'updates':message_buffer}) # Format the json data buffer
    request_headers = {"User-Agent":"mw.doc.bulk-update (Orange Pi)","Content-Type":"application/json","Content-Length":str(len(bulk_data))}
    # Make the request to ThingSpeak
    try:
        #print(request_headers)
        response = requests.post(url,headers=request_headers,data=bulk_data)
        #response = requests.post(url,data=bulk_data)
        print (response) # A 202 indicates that the server has accepted the request
    except e:
        print(e.code) # Print the error code

def updateJsonbck(idchannel,msg_bck,key):
    import json
    import requests

    e=[]
    url = 'https://api.thingspeak.com/channels/'+idchannel+'/bulk_update.json' # ThingSpeak server settings
        
    message_buffer=msg_bck

    bulk_data = json.dumps({'write_api_key':key,'updates':message_buffer}) # Format the json data buffer
    request_headers = {"User-Agent":"mw.doc.bulk-update (Orange Pi)","Content-Type":"application/json","Content-Length":str(len(bulk_data))}
    # Make the request to ThingSpeak
    try:
        #print(request_headers)
        response = requests.post(url,headers=request_headers,data=bulk_data)
        #response = requests.post(url,data=bulk_data)
        print (response) # A 202 indicates that the server has accepted the request
    except e:
        print(e.code) # Print the error code

import serial
import time
from datetime import datetime, timedelta
import telegram
import os
import json
import glob
#import numpy as np

api_key = '5056593909:AAGL1Q8PjvYgtrRFbosh-3J6cx1O5hOzknA'
giovanni_id='206547422'
pasquale_id='5037672168'
user_id =[ giovanni_id,pasquale_id]

bot = telegram.Bot(token=api_key)

port='/dev/ttyUSB0'
baudrate='9600'
msg_bck=[]

if os.path.isfile('njfile.txt')==False:
    fn=open('/home/orangepi/CR1000/njfile.txt','w')
    fn.write('1')
    fn.close()
    print('njfile creato')
    

update={}
updatebck={}
id_channel=['1800121','1800122','1663815']
ts_key=['CW3X9B4MH88D1AF1','NPGHUY19K6ARB265','X15IXDOWVC2O64VY']

com_test=False

while com_test==False:

    try:
        ser = serial.Serial(port, baudrate=baudrate , parity='N', bytesize=8, stopbits=1, timeout=2)
        com_test=True
        if is_cnx_active()==True:
            print('Serial port connected')
            try:
                for user in user_id:
                    bot.send_message(chat_id=user, text='Serial port connected')
            except:
                print('bot not active')
    except:
        com_test=False
        if is_cnx_active()==True:
            print('Serial port not connected')
            try:
                for user in user_id:
                    bot.send_message(chat_id=user, text='Serial port not connected')
            except:
                print('bot not active')
            time.sleep(15)
        
while True:

    out_byte=ser.readline()
    try:
        stringa=out_byte.decode('utf-8')

    except:
        stringa=[]
    
    # for k in range(0,2):
    #     stringa='meteo'
    #     t1=np.random.randint(50, size=4)
    #     for t in range(0,len(t1)):
    #         stringa=stringa+';'+str(t1[t])
    #     t2=np.random.randint(50, size=9)
    #     stringa=stringa+';'+'tdr'
    #     for t in range(0,len(t2)):
    #         stringa=stringa+';'+str(t2[t])
    #     t3=np.random.randint(50, size=7)
    #     stringa=stringa+';'+'tens'
    #     for t in range(0,len(t3)):
    #         stringa=stringa+';'+str(t3[t])
    
    if stringa:
        msg0=stringa.split(';')
        
        for idchannel in id_channel:
            
            if idchannel==id_channel[0]:
                if 'meteo' in msg0:
                    idx=msg0.index('meteo')
                    msg=[]
                    for k in range(1,4):
                        msg.append(msg0[idx+k])
                    update['meteo']=msg

            if idchannel==id_channel[1]:
                if 'tdr' in msg0:
                    idx=msg0.index('tdr')
                    msg=[]
                    for k in range(1,9):
                        msg.append(msg0[k+idx])
                    update['tdr']=msg
                                        
                    # for user in user_id:
                    #     bot.send_message(chat_id=user, text='TDR OK')

            if idchannel==id_channel[2]:
                if 'tens' in msg0:
                    idx=msg0.index('tens')
                    msg=[]
                    for k in range(1,7):
                        msg.append(msg0[k+idx])
                    update['tens']=msg
                    
                    # for user in user_id:
                    #     bot.send_message(chat_id=user, text='TENS OK')
                    
        if is_cnx_active()==True:
            idx=0
            for key in update:
                msg=update[key]
                updateJson(id_channel[idx],update[key],ts_key[idx])
                idx=idx+1
            stringa=[]
            update={}
            
            ftime=open('/home/orangepi/CR1000/orario.txt','w')
            ftime.write(time.strftime('%Y-%m-%d %H:%M:%S',  time.gmtime(time.time())))
            ftime.close()
            
            bckfiles=glob.glob('*.json')
            
            if len(bckfiles)>0:
                
                #print('attesa invio files...')
                time.sleep(35) #tempo di attesa necessario per il secondo invio sullo stesso canale
                #for user in user_id:
                        #bot.send_message(chat_id=user, text='send bck data...')
                
                msg_bck0=[]
                msg_bck1=[]
                msg_bck2=[]
                
                for nbckfile in bckfiles:
                    
                    if 'meteo' in nbckfile:
                        f=open(nbckfile,'r')
                        msg_bck0.append(json.load(f))
                        f.close()
                    if 'tdr' in nbckfile:
                        f=open(nbckfile,'r')
                        msg_bck1.append(json.load(f))
                        f.close()
                    if 'tens' in nbckfile:
                        f=open(nbckfile,'r')
                        msg_bck2.append(json.load(f))
                        f.close()
                    
                    os.remove(nbckfile)
                    
                updateJsonbck(id_channel[0],msg_bck0,ts_key[0])
                updateJsonbck(id_channel[1],msg_bck1,ts_key[1])
                updateJsonbck(id_channel[2],msg_bck2,ts_key[2])
                
                fn=open('/home/orangepi/CR1000/njfile.txt','w')
                fn.write('1')
                fn.close()
            
        if is_cnx_active()==False:
            
            fn=open('/home/orangepi/CR1000/njfile.txt','r')
            njfile=fn.readlines()
            fn.close()
            
            ftime=open('/home/orangepi/CR1000/orario.txt','r')
            time_bck=ftime.readlines()
            ftime.close()
            
            dt_time_bck = datetime.strptime(time_bck[0], '%Y-%m-%d %H:%M:%S') #convert string to datetime
            dt_time_bck_1=dt_time_bck+timedelta(hours=int(njfile[0]))  #add to datetime next time step 1 hour
            
            for key in update:
                updatebck['created_at']=dt_time_bck_1.strftime('%Y-%m-%d %H:%M:%S') #convert datetime to string
                msg=update[key]
                field=0
                for value in msg:
                    field=field+1
                    updatebck['field'+str(field)]=value
                
                jfile = open(key+njfile[0]+'.json', 'w')
                json.dump(updatebck,jfile)
                jfile.close()
                updatebck={}
             
            fn=open('/home/orangepi/CR1000/njfile.txt','w')
            fn.write(str(int(njfile[0])+1))
            fn.close()
                    
        stringa=[]
        print('attesa nuova lettura...')
        #time.sleep(60*5)
        os.system('shutdown -h now')
        
#ser.close()
        
        
