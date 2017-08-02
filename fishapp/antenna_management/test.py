import serial, time
import psycopg2

hostname = 'localhost'
username = 'antoine'
password = ''
database = 'fishapp'

arduino = serial.Serial('/dev/tty.usbmodem1411', 9600, timeout=.1)
antenna_number = 1
time.sleep(2)
new_tag_constant = "<<new_tag>>"


# Simple routine to run a query on a database and print the results:
def addDetection( conn , dict) :
    cur = conn.cursor()
    cur.execute( "SELECT id, aquarium_id FROM fish_fish WHERE rfid LIKE '%s'" % dict['id'])
    #
    for data in cur.fetchall():
        print(data)
        print(dict)
        cur.execute("INSERT INTO fish_fishdetection (antenna_number, fish_id_id, aquarium_id_id, duration, nb_detection) VALUES (%d, %d, %d, %f, %d)"
                    % (antenna_number, data[0], data[1], float(dict["duration"]), int(dict["nb_detection"])))
    conn.commit()

while True:
    data = arduino.readline()
    line = data.decode("utf-8")
    if data:
        print(data)
        if new_tag_constant in line:
            elements = line[len(new_tag_constant):-2].split(";", -1)
            tag_info = {}
            for element in elements:
                tmp = element.split(":", 1)
                tag_info[tmp[0]] = tmp[1]
            myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
            addDetection(myConnection, tag_info)
            myConnection.close()
