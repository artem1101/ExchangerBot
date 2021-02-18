from vedis import Vedis
from enum import Enum

db_file = "database.vdb"

class States(Enum):
    """
    Vedis stores strings, which is what I need 
    """
    S_START = "0"  # Start of the dialog
    S_ENTER_CURRENCY = "1"
    S_BASE_CURRENCY = "2"



def get_current_state(user_id):
	with Vedis(db_file) as db:
		try:
			return db[user_id].decode()
		except KeyError:  # If the key doesn't exist -> to the start of the dialog
			return States.S_START.value

# save the state
def set_state(user_id, value):
    with Vedis(db_file) as db:
        try:
            db[user_id] = value
            return True
        except :
            print('Unknown value.')
            return False