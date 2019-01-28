from classes.TCPObserver import TCPObserver
import threading
import json
from config import db


class HomeLynkController(threading.Thread, TCPObserver):
    text_color = "\033[1;31;40m "

    def __init__(self, Q):
        self.queue = Q
        threading.Thread.__init__(self)

    def update_objects(self, changed_objects):
        for j in changed_objects:
            update_objects_query = "UPDATE 'object' SET 'current_value'='{}' WHERE _rowid_='{}'".format(j["new_value"], j["id"])
            insert_event_query = "INSERT INTO 'event'('object_id','value') VALUES ('{}','{}')".format(j["id"], j["new_value"])
            db.engine.execute(update_objects_query)
            db.engine.execute(insert_event_query)

    def handle_data(self, data):
        try:
            j_data = json.loads(data.decode("utf-8"))  # Convert data to json data
        except:
            j_data = json.loads(data)

        changed_objects = []

        if 'address' in j_data:
            db_obj = db.engine.execute('SELECT * FROM object WHERE "address"="{}"'.format(j_data["address"])).first()  # Get data from database
            if j_data["address"] == db_obj["address"]:
                if str(j_data["value"]) != str(db_obj["current_value"]):
                    current_obj = {"address": db_obj["address"], \
                                   "id": db_obj["id"], \
                                   "current_value": db_obj["current_value"], \
                                   "new_value": j_data["value"]}

                    changed_objects.append(current_obj)
        else:
            for j_obj in j_data:
                print(j_obj)
                db_obj = db.engine.execute('SELECT * FROM object WHERE "address"="{}"'.format(j_obj["address"])).first() # Get data from database
                if j_obj["address"] == db_obj["address"]:
                    if str(j_obj["value"]) != str(db_obj["current_value"]):
                        current_obj = {"address": db_obj["address"], \
                                       "id": db_obj["id"], \
                                       "current_value": db_obj["current_value"], \
                                       "new_value": j_obj["value"]}

                        changed_objects.append(current_obj)

        self.update_objects(changed_objects)

        return True

    def run(self):
        while True:
            data = self.queue.get()
            self.handle_data(data)

    def notify(self, data):
        return

