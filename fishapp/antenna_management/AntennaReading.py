import serial, time
import psycopg2
import math

# DB parameters
hostname = 'localhost'
username = 'antoine'
password = ''
database = 'fishapp'
new_tag_constant = "<<new_tag>>"
new_fish_constant = "<<new_fish>>"
antenna_problem_constant = "<<antenna_problem>>"
antenna_fixed_constant = "<<antenna_fixed>>"

# Settings of the antenna to listen to
aquarium_manage_list = [3, 4]
nb_tank_per_aq = {}
myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
request = "SELECT id, usbs FROM fish_aquarium WHERE id IN (%s) AND active=TRUE" % str(aquarium_manage_list)[1:-1]
cur = myConnection.cursor()
cur.execute(request)
usb_aquarium = {}
usb_aquarium_path = {}
for aquarium in cur.fetchall():
    usbs = aquarium[1].replace("\n", "").replace("\r", "").split(";")
    nb_tank_per_aq[str(aquarium[0])] = len(usbs) - 1
    for usb in usbs[:-1]:
        usb = usb
        usb_data = usb.split(":")
        usb_aquarium_path["aq_%s_ant_%s" % (aquarium[0], usb_data[0])] = usb_data[1]
        usb_available = "TRUE"
        try:
            usb_aquarium["aq_%s_ant_%s" % (aquarium[0], usb_data[0])] = serial.Serial(usb_data[1], 9600, timeout=.1)
        except serial.serialutil.SerialException:
            usb_aquarium["aq_%s_ant_%s" % (aquarium[0], usb_data[0])] = usb_data[1]
            usb_available = "FALSE"
        request = "WITH upsert AS (UPDATE fish_antenna SET usb_conection_check=%s WHERE position=%d " \
          "AND aquarium_id_id=%d RETURNING *) INSERT INTO fish_antenna (usb_conection_check, position, aquarium_id_id) " \
          "SELECT %s, %d, %d WHERE NOT EXISTS (SELECT * FROM upsert);" % (usb_available, int(usb_data[0]), int(aquarium[0]), usb_available, int(usb_data[0]), int(aquarium[0]))
        cur.execute(request)
myConnection.commit()
myConnection.close()
#arduino = serial.Serial('/dev/tty.usbmodem1411', 9600, timeout=.1)
#antenna_number = 1
time.sleep(2)
# Simple routine to run a query on a database and print the results:
def addDetection(conn, dict):
    cur = conn.cursor()
    print(dict)
    cur.execute( "SELECT id FROM fish_fish WHERE rfid LIKE '%s' AND aquarium_id=%d" % (dict['id'], dict['aquarium_id']))
    for data in cur.fetchall():
        cur.execute("INSERT INTO fish_fishdetection (antenna_number, fish_id_id, aquarium_id_id, duration, nb_detection) VALUES (%d, %d, %d, %f, %d)"
                    % (int(dict["antenna_number"]), data[0], dict['aquarium_id'], float(dict["duration"]), int(dict["nb_detection"])))
        cur.execute("SELECT id, position FROM fish_fishposition WHERE fish_id=%d ORDER BY id DESC" % data[0])
        result = cur.fetchone()
        current_position = math.floor(float(dict["antenna_number"])/2.0)
        if current_position != result[1]:
            cur.execute("INSERT INTO fish_fishposition(position, fish_id) VALUES (%d, %d)" % (current_position, data[0]))
            cur.execute("UPDATE fish_fishposition SET end_date='%s' WHERE id=%d" % (time.strftime("%Y-%m-%d %H:%M:%S"), result[0]))
        conn.commit()

# Simple routine to run a query on a database and print the results:
def addFish(conn, rfid) :
    cur = conn.cursor()
    cur.execute("INSERT INTO fish_newfish (rfid) VALUES ('%s')"
                % (rfid))
    conn.commit()

while True:
    for aquarium_id in aquarium_manage_list:
        if str(aquarium_id) in nb_tank_per_aq.keys():
            for tank_id in range(nb_tank_per_aq[str(aquarium_id)]):
                usb_path = usb_aquarium["aq_%s_ant_%s" % (aquarium_id, tank_id+1)]
                if type(usb_path) == serial.Serial:
                    try:
                        data = usb_path.readline()
                    except serial.serialutil.SerialException:
                        usb_aquarium["aq_%s_ant_%s" % (aquarium_id, tank_id+1)] = usb_aquarium_path["aq_%s_ant_%s" % (aquarium_id, tank_id+1)]
                        request = "UPDATE fish_antenna SET usb_conection_check=FALSE WHERE aquarium_id_id=%d AND position=%d" % (int(aquarium_id), int(tank_id+1))
                        myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
                        cur = myConnection.cursor()
                        cur.execute(request)
                        myConnection.commit()

                    line = data.decode("utf-8")
                    if data:
                        myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
                        if new_tag_constant in line:
                            elements = line[len(new_tag_constant):-2].split(";", -1)
                            tag_info = {}
                            for element in elements:
                                tmp = element.split(":", 1)
                                tag_info[tmp[0]] = tmp[1]
                            tag_info['antenna_number'] = tank_id + 1
                            tag_info['aquarium_id'] = aquarium_id
                            addDetection(myConnection, tag_info)
                        elif new_fish_constant in line:
                            rfid = line[len(new_fish_constant):]
                            addFish(myConnection, rfid)
                        elif antenna_problem_constant in line:
                            request = "UPDATE fish_antenna SET antenna_check=FALSE WHERE aquarium_id_id=%d AND position=%d" % (int(aquarium_id), int(tank_id+1))
                            myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
                            cur = myConnection.cursor()
                            cur.execute(request)
                            myConnection.commit()
                        elif antenna_fixed_constant in line:
                            request = "UPDATE fish_antenna SET antenna_check=TRUE WHERE aquarium_id_id=%d AND position=%d" % (int(aquarium_id), int(tank_id+1))
                            myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
                            cur = myConnection.cursor()
                            cur.execute(request)
                            myConnection.commit()
                        myConnection.close()
                else:
                    try:
                        usb_aquarium["aq_%s_ant_%s" % (aquarium_id, tank_id+1)] = serial.Serial(usb_path, 9600, timeout=.1)
                        request = "UPDATE fish_antenna SET usb_conection_check=TRUE WHERE aquarium_id_id=%d AND position=%d" % (int(aquarium_id), int(tank_id+1))
                        myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
                        cur = myConnection.cursor()
                        cur.execute(request)
                        myConnection.commit()
                    except serial.serialutil.SerialException:
                        continue
