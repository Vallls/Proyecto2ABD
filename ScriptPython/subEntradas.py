import ssl
import sys
import paho.mqtt.client
import psycopg2
import pandas
import numpy
import matplotlib
import json

connn = psycopg2.connect(host = 'localhost', user= 'postgres', password ='27450917', dbname= 'Compras_Sambil')
conn = psycopg2.connect(host = 'localhost', user= 'postgres', password ='27450917', dbname= 'Entradas_Sambil')
con = psycopg2.connect(host = 'localhost', user= 'postgres', password ='27450917', dbname= 'Mesas_Sambil') 

def mcAdress(a):
    cur = connn.cursor()
    sql = '''INSERT INTO mcadress (mcadress,nombre,apellido,telefono,sexo,edad,cedula) VALUES ( %s, %s, %s, %s, %s, %s, %s);'''
    cur.execute(sql, (a["mcadress"],a["nombre"],a["apellido"],a["telefono"],a["sexo"],a["edad"],a["cedula"]))
    connn.commit()

def mcAdress2(a):
    cur = conn.cursor()
    sql = '''INSERT INTO mcadress (mcadress,nombre,apellido,telefono,sexo,edad,cedula) VALUES ( %s, %s, %s, %s, %s, %s, %s);'''
    cur.execute(sql, (a["mcadress"],a["nombre"],a["apellido"],a["telefono"],a["sexo"],a["edad"],a["cedula"]))
    conn.commit()

def mcAdress3(a):
    cur = con.cursor()
    sql = '''INSERT INTO mcadress (mcadress,nombre,apellido,telefono,sexo,edad,cedula) VALUES ( %s, %s, %s, %s, %s, %s, %s);'''
    cur.execute(sql, (a["mcadress"],a["nombre"],a["apellido"],a["telefono"],a["sexo"],a["edad"],a["cedula"]))
    con.commit()

def sensor_mcadress(a):
    cur = conn.cursor()
    sql = '''INSERT INTO sensor_mcadress (mcadress,idsensor,fecha_hora) VALUES ( %s, %s, %s);'''
    cur.execute(sql, (a["mcadress"],a["idsensor"],a["fecha_hora"]))
    conn.commit()

def sensor_mcadress2(a):
    cur = con.cursor()
    sql = '''INSERT INTO sensor_mcadress (mcadress,idsensor,fecha_hora) VALUES ( %s, %s, %s);'''
    cur.execute(sql, (a["mcadress"],a["idsensor"],a["fecha_hora"]))
    con.commit()

def sensor_usuario(a):
    cur = conn.cursor()
    sql = '''INSERT INTO sensor_usuario (idsensor,fecha_hora,edad,sexo) VALUES ( %s, %s, %s, %s);'''
    cur.execute(sql, (a["idsensor"],a["fecha_hora"],a["edad"],a["sexo"]))
    conn.commit()

def sensor_usuario2(a):
    cur = con.cursor()
    sql = '''INSERT INTO sensor_usuario (idsensor,fecha_hora,edad,sexo) VALUES ( %s, %s, %s, %s);'''
    cur.execute(sql, (a["idsensor"],a["fecha_hora"],a["edad"],a["sexo"]))
    con.commit()

def on_connect(client, userdata, flags, rc):    
    print('conectado (%s)' % client._client_id)
    client.subscribe(topic='sambil/#', qos = 0)        

def on_message(client, userdata, message):   
    a = json.loads(message.payload)
    print(a)
    print('------------------------------')
    if a['nombre'] == '':
        if a['edad'] != '':
            sensor_usuario(a)
            sensor_usuario2(a)
        else:
            sensor_mcadress(a)
            sensor_mcadress2(a)
    else:
        mcAdress(a)
        mcAdress2(a)
        mcAdress3(a)
        sensor_mcadress(a)
        sensor_mcadress2(a)
        
    

def main():
    client = paho.mqtt.client.Client()
    client.on_connect = on_connect
    client.message_callback_add('sambil/sensores/entrada', on_message)
    client.connect(host='localhost')
    client.loop_forever()


if __name__ == '__main__':
	main()
	sys.exit(0)