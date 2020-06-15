# pypi
""" API for Bosch API server for Indego lawn mower """
import requests
import json
from requests.auth import HTTPBasicAuth
import logging
#from datetime import datetime

DEFAULT_URL = "https://api.indego.iot.bosch-si.com:443/api/v1/"
# CONST TAKEN FROM homeassistant.const
CONTENT_TYPE_JSON = "application/json"
#const taken from aiohttp.hdrs
CONTENT_TYPE = "Content-Type"
OFFLINE_TRESHOLD = 5

_LOGGER = logging.getLogger(__name__)
#_LOGGER.setLevel(logging.INFO)
#_LOGGER.setLevel(logging.WARNING)
#_LOGGER.setLevel(logging.CRITICAL)
#_LOGGER.setLevel(logging.ERROR)
#_LOGGER.setLevel(logging.DEBUG)

#_LOGGER.debug("---------------------------------")
#_LOGGER.debug("Start")

MOWER_STATE_DESCRIPTION_DETAILED = {
    '0'    : 'Reading status',
    '257'  : 'Charging',
    '258'  : 'Docked',
    '259'  : 'Docked - Software update',
    '260'  : 'Docked',
    '261'  : 'Docked',
    '262'  : 'Docked - Loading map',
    '263'  : 'Docked - Saving map',
    '513'  : 'Mowing',
    '514'  : 'Relocalising',
    '515'  : 'Loading map',
    '516'  : 'Learning lawn',
    '517'  : 'Paused',
    '518'  : 'Border cut',
    '519'  : 'Idle in lawn',
    '769'  : 'Returning to Dock',
    '770'  : 'Returning to Dock',
    '771'  : 'Returning to Dock - Battery low',
    '772'  : 'Returning to dock - Calendar timeslot ended',
    '773'  : 'Returning to dock - Battery temp range',
    '774'  : 'Returning to dock - requested by user/app',
    '775'  : 'Returning to dock - Lawn complete',
    '776'  : 'Returning to dock - Relocalising',
    '1025' : 'Diagnostic mode',
    '1026' : 'End of life',
    '1281' : 'Software update',
    '1537' : 'Stuck on lawn, help needed',
    '64513': 'Sleeping',
    '99999': 'Offline',
    'None' : 'None'
}

MOWER_STATE_DESCRIPTION = {
    '0'    : 'Docked',
    '257'  : 'Docked',
    '258'  : 'Docked',
    '259'  : 'Docked',
    '260'  : 'Docked',
    '261'  : 'Docked',
    '262'  : 'Docked',
    '263'  : 'Docked',
    '513'  : 'Mowing',
    '514'  : 'Mowing',
    '515'  : 'Mowing',
    '516'  : 'Mowing',
    '517'  : 'Mowing',
    '518'  : 'Mowing',
    '519'  : 'Mowing',
    '769'  : 'Mowing',
    '770'  : 'Mowing',
    '771'  : 'Mowing',
    '772'  : 'Mowing',
    '773'  : 'Mowing',
    '774'  : 'Mowing',
    '775'  : 'Mowing',
    '776'  : 'Mowing',
    '1025' : 'Diagnostic mode',
    '1026' : 'End of life',
    '1281' : 'Software update',
    '1537' : 'Stuck',
    '64513': 'Docked',
    '99999': 'Offline',
    'None' : 'None'
}


MOWER_MODEL_DESCRIPTION = {
    '3600HA2300':'Indego 1000',
    '3600HA2301': 'Indego 1200',
    '3600HA2302': 'Indego 1100',
    '3600HA2303': 'Indego 13C',
    '3600HA2304': 'Indego 10C',
    '3600HB0100': 'Indego 350',
    '3600HB0101': 'Indego 400',
    '3600HB0102': 'Indego S+ 350',
    '3600HB0103': 'Indego S+ 400',
    '3600HB0105': 'Indego S+ 350 2020',
    '3600HB0106': 'Indego S+ 400 2020',
    '3600HB0301': 'Indego M+ 700'
#    '3600HB0xxx': 'Indego M+ 700' missing model number
}

MOWER_MODEL_VOLTAGE = {
    '3600HA2300': {'min': '297','max': '369'}, # Indego 1000
    '3600HA2301': {'min': '297','max': '369'}, # Indego 1200
    '3600HA2302': {'min': '297','max': '369'}, # Indego 1100
    '3600HA2303': {'min': '297','max': '369'}, # Indego 13C
    '3600HA2304': {'min': '297','max': '369'}, # Indego 10C
    '3600HB0100': {'min': '0','max': '100'},   # Indego 350
    '3600HB0101': {'min': '0','max': '100'},   # Indego 400
    '3600HB0102': {'min': '0','max': '100'},   # Indego S+ 350
    '3600HB0103': {'min': '0','max': '100'},   # Indego S+ 400
    '3600HB0105': {'min': '0','max': '100'},   # Indego S+ 350
    '3600HB0106': {'min': '0','max': '100'},    # Indego S+ 400
    '3600HB0301': {'min': '0','max': '100'}    # Indego M+ 700
#    '3600HB0xxx': {'min': '0','max': '100'}   # Indego M+ 700
}

MOWING_MODE_DESCRIPTION = {
    'smart':    'SmartMowing',
    'calendar': 'Calendar',
    'manual':   'Manual'
}

ALERT_ERROR_CODE = {
    '104':             'Stop button pushed',
    '115':             'Mower is stuck',
    '149':             'Mower uutside perimeter cable',
    '151':             'Perimeter cable signal missing',
    'ntfy_blade_life': 'Reminder blade life'
}

class IndegoAPI():
    """Wrapper for Indego's API."""
    def __init__(self, username=None, password=None, serial=None):
        """Initialize Indego API and set headers needed later."""
        _LOGGER.info("Call IndegoAPI")
        _LOGGER.debug("---------------------------------------------------------------------------")
        _LOGGER.info("Bosch Indego API Initialization")

        _LOGGER.info    ("--- This is an information!")
        _LOGGER.warning ("--- This is an warning!")
        _LOGGER.critical("--- This is an critical!")
        _LOGGER.error   ("--- This is an error!")
        _LOGGER.debug   ("--- This is an debug!!")

        # Declaring variables in case that they are read before initialized
        self._api_url = DEFAULT_URL
        # Log in settings
        self._username = username
        self._password = password
        self._headers = {CONTENT_TYPE: CONTENT_TYPE_JSON}
        self.body = {'device': '', 'os_type': 'Android', 'os_version': '4.0', 'dvc_manuf': 'unknown', 'dvc_type': 'unknown'}
        self._jsonBody = json.dumps(self.body)
        #Properties for cached values
        self._serial = serial
        self._devices = {}

        # Empty declaration
        self._mower_state = None
        self._map_update_available = None
        self._mowed = None
        self._mowmode = None
        self._xpos = None
        self._ypos = None
        self._runtime = None
        self._mapsvgcache_ts = None
        self._svg_xPos = None
        self._svg_yPos = None
        self._mower_state_description = None
        self._mower_state_description_detailed = None
        self._total_operation = None
        self._total_charge = None
        self._total_cut = None
        self._session_operation = None
        self._session_charge = None
        self._session_cut = None
        self._email = None
        self._display_name = None
        self._language = None
        self._country = None
        self._optin = None
        self._optinapp = None
        self._alm_name = None
        self._service_counter = None
        self._needs_service = None
        self._alm_mode = None
        self._bareToolnumber = None
        self._alm_firmware_version = None
        self._model_description = None
        self._battery = None
        self._garden = None
        self._hmikeys = None
        self._battery_percent = None
        self._battery_voltage = None
        self._battery_cycles = None
        self._battery_discharge = None
        self._battery_ambient_temp = None
        self._battery_temp = None
        self._firmware_available = None
        self._mowingmode_description = None
        self._battery_percent_adjusted = None
        self._alert1_id                     = None
        self._alert1_error                  = None
        self._alert1_time                   = None
        self._alert1_friendly_description   = None
        self._alert2_id                     = None
        self._alert2_error                  = None
        self._alert2_time                   = None
        self._alert2_friendly_description   = None
        self._alert3_id                     = None
        self._alert3_error                  = None
        self._alert3_time                   = None
        self._alert3_friendly_description   = None
        #self._online                        = False
        self._online                        = True #For testing mower offline in all API calls
        self._offline = 0
        self._last_completed_mow = None
        self._next_mow = None
        
        ## Logging in
        self.login()
        
        _LOGGER.debug("--- Indego API: end __init__")

    def login(self):
        _LOGGER.info("Indego API: call login")
        _LOGGER.debug("   >>> API-call: %s", '{}{}'.format(self._api_url, 'authenticate'))
        self._login_session = requests.post(
            '{}{}'.format(self._api_url, 'authenticate'), data=self._jsonBody, headers=self._headers,
            auth=HTTPBasicAuth(self._username, self._password), timeout=30)
        _LOGGER.debug("JSON Response: " + str(self._login_session.json()))

        logindata = json.loads(self._login_session.content)
        self._contextid = logindata['contextId']
        _LOGGER.debug("self._contextid: " + self._contextid)
        self._userid = logindata['userId']
        _LOGGER.debug("self._userId: " + logindata['userId'])
        _LOGGER.debug("self._serial: " + self._serial)
        _LOGGER.debug("--- Indego API: end login")
        #self.initial_update()

    def show_vars(self):
        # For debug: writing all vars to log
        _LOGGER.info("Call show_vars")

        _LOGGER.debug("*** Catched from authenticate ***")
        _LOGGER.debug(f"self._contextid: {self._contextid}")
        _LOGGER.debug(f"self._userid: {self._userid}")
        _LOGGER.debug(f"self._serial: {self._serial}")

        _LOGGER.debug("*** self.getState ***")
        _LOGGER.debug(f"self._mower_state: {self._mower_state}")
        _LOGGER.debug(f"self._map_update_available: {self._map_update_available}")
        _LOGGER.debug(f"self._mowed: {self._mowed}")
        _LOGGER.debug(f"self._mowmode: {self._mowmode}")
        _LOGGER.debug(f"self._xPos: {self._xpos}")
        _LOGGER.debug(f"self._yPos: {self._ypos}")
        _LOGGER.debug(f"self._runtime: {self._runtime}")
        _LOGGER.debug(f"self._mapsvgcache_ts: {self._mapsvgcache_ts}")
        _LOGGER.debug(f"self._svg_xPos: {self._svg_xPos}")
        _LOGGER.debug(f"self._svg_yPos: {self._svg_yPos}")                

        # User-friendly mower state
        _LOGGER.debug("*** self.MowerStateDescription() ***")
        _LOGGER.debug(f"self._mower_state_description = {self._mower_state_description}")

        # split runtime into total        
        _LOGGER.debug("*** self.RuntimeTotal() ***")
        _LOGGER.debug(f"self._total_operation: {self._total_operation}")
        _LOGGER.debug(f"self._total_charge: {self._total_charge}")
        _LOGGER.debug(f"self._total_cut: {self._total_cut}")

        # split runtime into session
        _LOGGER.debug("*** self.RuntimeSession() ***")
        _LOGGER.debug(f"self._session_operation: {self._session_operation}")
        _LOGGER.debug(f"self._session_charge: {self._session_charge}")
        _LOGGER.debug(f"self._session_cut: {self._session_cut}")

        # self.getUsers()
        _LOGGER.debug("*** self.getUsers ***")
        _LOGGER.debug(f"self._email: {self._email}")                
        _LOGGER.debug(f"self._display_name: {self._display_name}")                
        _LOGGER.debug(f"self._language: {self._language}")                
        _LOGGER.debug(f"self._country = {self._country}")
        _LOGGER.debug(f"self._optIn = {self._optin}")
        _LOGGER.debug(f"self._optInApp = {self._optinapp}")

        # self.getGenericData()
        _LOGGER.debug("*** self.getGenericData ***")
        #_LOGGER.debug(f"self._alm_sn ignored: {self._alm_sn}")
        _LOGGER.debug(f"self._alm_name: {self._alm_name}")
        _LOGGER.debug(f"self._service_counter: {self._service_counter}")
        _LOGGER.debug(f"self._needs_service: {self._needs_service}")
        _LOGGER.debug(f"self._alm_mode: {self._alm_mode}")
        _LOGGER.debug(f"self._bareToolnumber: {self._bareToolnumber}")
        _LOGGER.debug(f"self._alm_firmware_version: {self._alm_firmware_version}")

        # User-friendly mower model
        _LOGGER.debug("*** self._model_description ***")
        _LOGGER.debug(f"self._model_description = {self._model_description}")

        # self.getOperationalData()
        _LOGGER.debug("*** self.getOperatingData ***")
        _LOGGER.debug(f"battery: {self._battery}")
        _LOGGER.debug(f"garden: {self._garden}")
        _LOGGER.debug(f"hmiKeys: {self._hmikeys}")
        _LOGGER.debug(f"self._battery_percent: {self._battery_percent}")
        _LOGGER.debug(f"self._battery_voltage: {self._battery_voltage}")
        _LOGGER.debug(f"self._battery_cycles: {self._battery_cycles}")
        _LOGGER.debug(f"self._battery_discharge: {self._battery_discharge}")
        _LOGGER.debug(f"self._battery_ambient_temp: {self._battery_ambient_temp}")
        _LOGGER.debug(f"self._battery_temp: {self._battery_temp}")

        # self.getUpdates()
        _LOGGER.debug(f"*** getUpdates() ***")
        _LOGGER.debug(f"self._firmware_available: {self._firmware_available}")
        
        # self.getLastCompletedMow()
        _LOGGER.debug(f"*** getLastCompletedMow() ***")
        _LOGGER.debug(f"self._last_completed_mow: {self._last_completed_mow}")
        
        # self.getNextMow()
        _LOGGER.debug(f"*** getNextMow() ***")
        _LOGGER.debug(f"self._next_mow: {self._next_mow}")

        # Other variables()
        _LOGGER.debug(f"*** Other variables ***")
        _LOGGER.debug(f"self._online: {self._online}")
        _LOGGER.debug(f"self._offline: {self._offline}")

        # Not updated in the getState API call
        #_LOGGER.debug("Not updated in the getState API call")        
        #_LOGGER.debug(f"self._model = {self._model}")

        _LOGGER.debug("-----Show vars end")

###########################################################
### Updating classes that updates cached data
###########################################################

    def getAlerts(self):
        _LOGGER.info("Call getAlerts")
        complete_url = 'alerts'
        #_LOGGER.debug(">>>API Call: " + complete_url)
        tmp_json = self.get(complete_url)
        self._alerts = tmp_json
        _LOGGER.debug("--- getAlerts: end")
        return tmp_json

    def getGenericData(self):
        _LOGGER.info("Call getGenericData")
        complete_url = 'alms/' + self._serial
        #_LOGGER.debug(f">>>API call: {complete_url}")
        tmp_json = self.get(complete_url)
        self._alm_name = tmp_json.get('alm_name')
        _LOGGER.debug(f"self._alm_name: {self._alm_name}")
        self._service_counter = tmp_json.get('service_counter')
        _LOGGER.debug(f"self._service_counter: {self._service_counter}")
        self._needs_service = tmp_json.get('needs_service')
        _LOGGER.debug(f"self._needs_service: {self._needs_service}")
        self._alm_mode = tmp_json.get('alm_mode')
        _LOGGER.debug(f"self._alm_mode: {self._alm_mode}")
        self._bareToolnumber = tmp_json.get('bareToolnumber')
        _LOGGER.debug(f"self._bareToolnumber: {self._bareToolnumber}")
        self._alm_firmware_version = tmp_json.get('alm_firmware_version')
        _LOGGER.debug(f"self._alm_firmware_version: {self._alm_firmware_version}")
        _LOGGER.debug("--- getGenericData: end")
        return tmp_json

    def getLastCompletedMow(self):
        _LOGGER.info("Call getLastCompletedMow")
        complete_url = 'alms/' + self._serial + '/predictive/lastcutting'
        _LOGGER.debug("Complete URL: " + complete_url)
        tmp_json = self.get(complete_url)
        tmp_datetime = tmp_json['last_mowed']
        self._last_completed_mow = self.ConvertBoschDateTime(tmp_datetime)
        _LOGGER.debug(f"tmp_json = {tmp_json}")
        _LOGGER.debug(f"last_completed_mow = {self._last_completed_mow}")
        _LOGGER.debug("--- getLastCompletedMow: end")  
        return tmp_json

    def getLocation(self):
        _LOGGER.info("Call getLocation")
        complete_url = 'alms/' + self._serial + '/predictive/location'
        Runtime_temp = self.get(complete_url)
        value = Runtime_temp
        _LOGGER.debug("--- getLocation: end")
        return value

    def getNextMow(self):
        _LOGGER.info("Call getNextMow")
        complete_url = 'alms/' + self._serial + '/predictive/nextcutting'
        _LOGGER.debug("Complete URL: " + complete_url)
        tmp_json = self.get(complete_url)
        try:
            tmp_datetime = tmp_json['mow_next']
        except:
            self._next_mow = "None"
        else:
            self._next_mow = self.ConvertBoschDateTime(tmp_datetime)
        _LOGGER.debug(f"NextMow = {self._next_mow}")
        _LOGGER.debug("--- getNextMow: end")  
        return tmp_json

    def getOperatingData(self):
        _LOGGER.info("Call getOperatingData")
        complete_url = 'alms/' + self._serial + '/operatingData'
        _LOGGER.debug(">>>API Call: " + complete_url)
        tmp_json = self.get(complete_url)
        ### Dont pay attention to runtime values as they are collected in the STATE call also
        if tmp_json:
            _LOGGER.debug(f"runtime: {tmp_json.get('runtime')}")
            self._battery = tmp_json.get('battery')
            _LOGGER.debug(f"battery: {self._battery}")
            self._garden = tmp_json.get('garden')
            _LOGGER.debug(f"garden: {self._garden}")
            self._hmikeys = tmp_json.get('hmiKeys')
            _LOGGER.debug(f"hmiKeys: {self._hmikeys}")
            self._online = True
            self._offline = 0
            _LOGGER.debug(f"Online: {self._online} - Offline count: {self._offline}")
            _LOGGER.debug("--- getOperatingData: end") 
            return tmp_json
        else:
            self._offline += 1
            #self._online = False
            _LOGGER.warning("Mower offline! Not able to get Operating Data!")    
            _LOGGER.debug("Online: " + str(self._online) + " - Offline: " + str(self._offline))
            _LOGGER.debug("self._online: " + str(self._online))
            _LOGGER.debug("--- getOperatingData: end")
            return None

    def getState(self):
        _LOGGER.info("Call getState")    
        complete_url = 'alms/' + self._serial + '/state'
        _LOGGER.debug("URL: " + complete_url)
        tmp_json = self.get(complete_url)
        if tmp_json:
            self._mower_state = tmp_json.get('state')
            _LOGGER.debug(f"self._mower_state: {self._mower_state}")
            self._map_update_available = tmp_json.get('map_update_available')
            _LOGGER.debug(f"self._map_update_available: {self._map_update_available}")    
            self._mowed = tmp_json.get('mowed')
            _LOGGER.debug(f"self._mowed: {self._mowed}")    
            self._mowmode = tmp_json.get('mowmode')
            _LOGGER.debug(f"self._mowmode: {self._mowmode}")    
            self._xpos = tmp_json.get('xPos')
            _LOGGER.debug(f"self._xPos: {self._xpos}")    
            self._ypos = tmp_json.get('yPos')
            _LOGGER.debug(f"self._yPos: {self._ypos}")    
            self._runtime = tmp_json.get('runtime')
            _LOGGER.debug(f"self._runtime: {self._runtime}")    
            self._mapsvgcache_ts = tmp_json.get('mapsvgcache_ts')
            _LOGGER.debug(f"self._mapsvgcache_ts: {self._mapsvgcache_ts}")    
            self._svg_xPos = tmp_json.get('svg_xPos')
            _LOGGER.debug(f"self._svg_xPos: {self._svg_xPos}")    
            self._svg_yPos = tmp_json.get('svg_yPos')
            _LOGGER.debug(f"self._svg_yPos: {self._svg_yPos}")
            _LOGGER.debug("--- getState end")
            return tmp_json
        else:
            _LOGGER.error("--- getState gave no value when fetching form API")
            _LOGGER.debug("--- getState end")
            return None

    def getForcedState(self):
        # Forces server to also update the location!
        _LOGGER.info("Call getForcedState")    
        complete_url = 'alms/' + self._serial + '/state' + '?forceRefresh=true'
        _LOGGER.debug("URL: " + complete_url)
        tmp_json = self.get(complete_url)
        if (self._online):
            if tmp_json:
                self._mower_state = tmp_json.get('state')
                _LOGGER.debug(f"self._mower_state: {self._mower_state}")
                self._map_update_available = tmp_json.get('map_update_available')
                _LOGGER.debug(f"self._map_update_available: {self._map_update_available}")    
                self._mowed = tmp_json.get('mowed')
                _LOGGER.debug(f"self._mowed: {self._mowed}")    
                self._mowmode = tmp_json.get('mowmode')
                _LOGGER.debug(f"self._mowmode: {self._mowmode}")    
                self._xpos = tmp_json.get('xPos')
                _LOGGER.debug(f"self._xPos: {self._xpos}")    
                self._ypos = tmp_json.get('yPos')
                _LOGGER.debug(f"self._yPos: {self._ypos}")    
                self._runtime = tmp_json.get('runtime')
                _LOGGER.debug(f"self._runtime: {self._runtime}")    
                self._mapsvgcache_ts = tmp_json.get('mapsvgcache_ts')
                _LOGGER.debug(f"self._mapsvgcache_ts: {self._mapsvgcache_ts}")    
                self._svg_xPos = tmp_json.get('svg_xPos')
                _LOGGER.debug(f"self._svg_xPos: {self._svg_xPos}")    
                self._svg_yPos = tmp_json.get('svg_yPos')
                _LOGGER.debug(f"self._svg_yPos: {self._svg_yPos}")    
                _LOGGER.debug("--- getForcedState end")        
                return tmp_json
            else:
                self._offline += 1
                #self._online = False
                _LOGGER.warning("Mower offline! Not able to get Forced State!!")    
                _LOGGER.debug("Online: " + str(self._online))
                _LOGGER.debug(f"Online: {self._online} - Offline count: {self._offline}")
                _LOGGER.debug("--- getForcedState end")        
        else:
            _LOGGER.warning("self._online set to true!")    
            _LOGGER.debug(f"Online: {self._online} - Offline count: {self._offline}")
            _LOGGER.debug("--- getForcedState end")        
            return None

    def getLongpollState(self, timeout):
        # The server attempts to "hold open" (not immediately reply to) each HTTP request, responding only when there are events to deliver.
        _LOGGER.info("Call getLongpollState")    
        laststate = 0
        _LOGGER.debug(f"self._mowerstate {self._mower_state}")  
        if (self._mower_state != None): # check if state variable is already available

            laststate = self._mower_state 
            complete_url = 'alms/' + self._serial + '/state' + '?longpoll=true&timeout=' + str(timeout) + "&last=" + str(laststate) # server will wait with answering until state data has updated values
            _LOGGER.debug("URL: " + complete_url)
            tmp_json = self.get(complete_url, timeout=timeout+10)
            if tmp_json != None:
                # Longpoll requests do only provide a limited set of status variables
                if tmp_json.get('state') != None:
                    self._mower_state = tmp_json.get('state')
                    _LOGGER.debug(f"self._mower_state: {self._mower_state}")
                if tmp_json.get('map_update_available') != None:
                    self._map_update_available = tmp_json.get('map_update_available')
                    _LOGGER.debug(f"self._map_update_available: {self._map_update_available}")    
                if tmp_json.get('mowed') != None:
                    self._mowed = tmp_json.get('mowed')
                    _LOGGER.debug(f"self._mowed: {self._mowed}")    
                if tmp_json.get('mowmode') != None:
                    self._mowmode = tmp_json.get('mowmode')
                    _LOGGER.debug(f"self._mowmode: {self._mowmode}")    
                if tmp_json.get('xPos') != None:
                    self._xpos = tmp_json.get('xPos')
                    _LOGGER.debug(f"self._xPos: {self._xpos}")    
                if tmp_json.get('yPos') != None:
                    self._ypos = tmp_json.get('yPos')
                    _LOGGER.debug(f"self._yPos: {self._ypos}")    
                if tmp_json.get('runtime') != None:
                    self._runtime = tmp_json.get('runtime')
                    _LOGGER.debug(f"self._runtime: {self._runtime}")    
                if tmp_json.get('mapsvgcache_ts') != None:
                    self._mapsvgcache_ts = tmp_json.get('mapsvgcache_ts')
                    _LOGGER.debug(f"self._mapsvgcache_ts: {self._mapsvgcache_ts}")    
                if tmp_json.get('svg_xPos') != None:
                    self._svg_xPos = tmp_json.get('svg_xPos')
                    _LOGGER.debug(f"self._svg_xPos: {self._svg_xPos}")    
                if tmp_json.get('svg_yPos') != None:
                    self._svg_yPos = tmp_json.get('svg_yPos')
                    _LOGGER.debug(f"self._svg_yPos: {self._svg_yPos}")    
            return tmp_json
        else:
            _LOGGER.warning("getLongpollState needs a getState before in order to use this API call.")                    
        _LOGGER.debug("--- getLongpollState end")        

    def getUpdates(self):
        _LOGGER.info("Call getUpdates")  
        if (self._online):
            complete_url = 'alms/' + self._serial + '/updates'
            tmp_json = self.get(complete_url)
            if (tmp_json):
                self._firmware_available = tmp_json.get('available')
                _LOGGER.debug("--- getUpdates: end")  
                return tmp_json
            else:
                _LOGGER.warning("Mower offline! Not able to get Updates!")  
                self._offline += 1
                #self._online = False
                _LOGGER.debug(f"Online: {self._online} - Offline count: {self._offline}")
        else:
            _LOGGER.warning("Mower offline!!!")    
            _LOGGER.debug("Online: " + str(self._online) + " - Offline: " + str(self._offline))
            _LOGGER.debug("End getUpdates")
            return None


    def getUsers(self):
        _LOGGER.info("Call getUsers")
        complete_url = 'users/' + self._userid
        _LOGGER.debug(">>>API Call: " + complete_url)
        tmp_json = self.get(complete_url)
        self._email = tmp_json.get('email')
        _LOGGER.debug(f"email = {self._email}")
        self._display_name = tmp_json.get('display_name')
        _LOGGER.debug(f"display_name = {self._display_name}")
        self._language = tmp_json.get('language')
        _LOGGER.debug(f"language = {self._language}")
        self._country = tmp_json.get('country')
        _LOGGER.debug(f"country = {self._country}")
        self._optin = tmp_json.get('optIn')
        _LOGGER.debug(f"optIn = {self._optin}")
        self._optinapp = tmp_json.get('optInApp')
        _LOGGER.debug(f"optInApp = {self._optinapp}")
        _LOGGER.debug(f"Value User = {tmp_json}")
        _LOGGER.debug("--- getUsers: end")
        return tmp_json

    def getNetwork(self):
        _LOGGER.debug("--- getNetwork: start")
        complete_url = 'alms/' + self._serial + '/network'
        tmp_json = self.get(complete_url)
        #value = Runtime_temp
        _LOGGER.debug(f"Result = {tmp_json}")
        _LOGGER.debug("--- getNetwork: end")
        return tmp_json

    def getConfig(self):
        _LOGGER.debug("--- getConfig: start")
        complete_url = 'alms/' + self._serial + '/config'
        Runtime_temp = self.get(complete_url)
        value = Runtime_temp
        _LOGGER.debug("--- getConfig: end")
        return value

    def getPredictiveSetup(self):
        _LOGGER.debug("--- getPredictiveSetup: start")
        complete_url = 'alms/' + self._serial + '/predictive/setup'
        Runtime_temp = self.get(complete_url)
        value = Runtime_temp
        _LOGGER.debug("--- getPredictiveSetup: end")
        return value

# 8
    def getTest(self):
        #now = datetime.now()
        #_LOGGER.debug(">>>>>>" + now.strftime("%Y-%m-%d %H:%M:%S"))    
        _LOGGER.info("Call getTest")
        complete_url = 'alms/' + self._serial + '/map'
        _LOGGER.debug("Complete URL: " + complete_url)
        tmp_json = self.get(complete_url)
        _LOGGER.debug(f"tmp_json = {tmp_json}")
        _LOGGER.debug("--- getTest: end")  
        return tmp_json

###################################################
### Functions for getting data from STATE cache

    def MowerState(self):
        if hasattr(self, '_mower_state'):
            return self._mower_state
        else:
            return None
            
    def MapUpdateAvailable(self):
        if hasattr(self, '_map_update_available'):
            return self._map_update_available
        else:
            return None

    def Mowed(self):
        if hasattr(self, '_mowed'):
            return self._mowed
        else:
            return None

    def MowMode(self):
        if hasattr(self, '_mowmode'):
            return self._mowmode
        else:
            return None

    def XPos(self):
        if hasattr(self, '_xpos'):
            return self._xpos
        else:
            return None

    def YPos(self):
        if hasattr(self, '_ypos'):
            return self._ypos
        else:
            return None

    def Runtime(self):
        if hasattr(self, '_runtime'):
            return self._runtime
        else:
            return None

    def MapSvgCacheTs(self):
        if hasattr(self, '_mapsvgcache_ts'):
            return self._mapsvgcache_ts
        else:
            return None

    def SvgxPos(self):
        if hasattr(self, '_svg_xPos'):
            return self._svg_xPos
        else:
            return None

    def SvgyPos(self):
        if hasattr(self, '_svg_yPos'):
            return self._svg_yPos
        else:
            return None

### --- User readable get functions
    def RuntimeTotal(self):
        tmp = self.Runtime()
        if (tmp):
            tmp = tmp.get('total')
            if (tmp):
                self._total_operation = round(tmp.get('operate')/100)
                self._total_operation_raw = tmp.get('operate') ### Only for testing purposes!
                self._total_charge = round(tmp.get('charge')/100)
                self._total_cut = round(self._total_operation - self._total_charge)
                return tmp
            else:
                return None
        else:
            return None

    def RuntimeSession(self):
        tmp = self.Runtime()
        if (tmp):
            tmp = tmp.get('session')
            if (tmp):
                self._session_operation = round(tmp.get('operate'))
                self._session_charge = round(tmp.get('charge'))
                self._session_cut = round(self._session_operation - self._session_charge)
                return tmp
            else:
                return None
        return None


    def MowerStateDescription(self):
        if hasattr(self, '_mower_state'):
            if str(self._mower_state) in MOWER_STATE_DESCRIPTION.keys():
                self._mower_state_description = MOWER_STATE_DESCRIPTION.get(str(self._mower_state))
            else:
                _LOGGER.warning(f"Mower State Description not in database! " + str(self._mower_state))
                self._mower_state_description = "Value not in database!"
            return self._mower_state_description
        else:
            return None
        return self._mower_state_description

    def MowerStateDescriptionDetailed(self):
        if hasattr(self, '_mower_state'):
            if str(self._mower_state) in MOWER_STATE_DESCRIPTION_DETAILED.keys():
                self._mower_state_description_detailed = MOWER_STATE_DESCRIPTION_DETAILED.get(str(self._mower_state))
            else:
                _LOGGER.warning(f"Mower State Description Detailed in database! " + str(self._mower_state))
                self._mower_state_description_detailed = "Value not in database!"
            return self._mower_state_description_detailed
        else:
            return None
        return self._mower_state_description_detailed

###################################################
### Functions for getting data from USERS cache

    def Email(self):
        if hasattr(self, '_email'):
            return self._email
        else:
            return None

    def DisplayName(self):
        if hasattr(self, '_display_name'):
            return self._display_name
        else:
            return None

    def Language(self):
        if hasattr(self, '_language'):
            return self._language
        else:
            return None

    def Country(self):
        if hasattr(self, '_country'):
            return self._country
        else:
            return None

    def OptIn(self):
        if hasattr(self, '_optin'):
            return self._optin
        else:
            return None

    def OptInApp(self):
        if hasattr(self, '_optinapp'):
            return self._optinapp
        else:
            return None

#########################################################
### Functions for getting data from SERIAL API call cache

    def Serial(self):
        return self._serial

    def AlmName(self):
        if hasattr(self, '_alm_name'):
            return self._alm_name
        else:
            return None

    def ServiceCounter(self):
        if hasattr(self, '_service_counter'):
            return self._service_counter
        else:
            return None

    def NeedsService(self):
        if hasattr(self, '_needs_service'):
            return self._needs_service
        else:
            return None

    def AlmMode(self):
        if hasattr(self, '_alm_mode'):
            return self._alm_mode
        else:
            return None

    def BareToolNumber(self):
        if hasattr(self, '_bareToolnumber'):
            return self._bareToolnumber
        else:
            return None

    def AlmFirmwareVersion(self):
        if hasattr(self, '_alm_firmware_version'):
            return self._alm_firmware_version
        else:
            return None

### --- User readable get functions

    def ModelDescription(self):
        _LOGGER.info(f"Call ModelDescription")
        if hasattr(self, '_bareToolnumber'):
            _LOGGER.debug(f"bareToolnumber = {self._bareToolnumber}")
            if str(self._bareToolnumber) in MOWER_MODEL_DESCRIPTION.keys():
                self._model_description = MOWER_MODEL_DESCRIPTION.get(str(self._bareToolnumber))
            else:
                _LOGGER.warning(f"Mower Model Description not in database! ModelMumber {self._bareToolnumber}")
                self._model_description = "Value not in database!"
            return self._model_description
        else:
            _LOGGER.error(f"ModelDescription bareToolnumber ERROR!!! = {self._bareToolnumber}")
            return None

    def ModelVoltage(self):
        if hasattr(self, '_bareToolnumber'):
            if str(self._bareToolnumber) in MOWER_MODEL_VOLTAGE.keys():
                self._model_voltage = MOWER_MODEL_VOLTAGE.get(str(self._bareToolnumber))
                return self._model_voltage
            else:
                _LOGGER.warning(f"Mower Model Voltage not in database! ModelMumber {self._bareToolnumber}")
        else:
            _LOGGER.error(f"ModelVoltage bareToolnumber ERROR!!! = {self._bareToolnumber}")
            return None
    
    def ModelVoltageMin(self):
        if hasattr(self, '_model_voltage'):
            tmp = self._model_voltage
            self._model_voltage_min = tmp['min']
            return self._model_voltage_min
        else:
            _LOGGER.error(f"ModelVoltageMin bareToolnumber ERROR!!! = {self._bareToolnumber}")
            return None

    def ModelVoltageMax(self):
        if hasattr(self, '_model_voltage'):
            tmp = self._model_voltage
            self._model_voltage_max = tmp['max']
            return self._model_voltage_max
        else:
            _LOGGER.error(f"ModelVoltageMax bareToolnumber ERROR!!! = {self._bareToolnumber}")
            return None

    def MowingModeDescription(self):
        if str(self._alm_mode) in MOWING_MODE_DESCRIPTION.keys():
            self._mowingmode_description = MOWING_MODE_DESCRIPTION.get(str(self._alm_mode))
        else:
            _LOGGER.warning(f"Mowing Mode Description not in database! Mowing Mode {self._alm_mode}")
            self._mowingmode_description = "Value not in database!"
        return self._mowingmode_description


############################################################
### Functions for getting data from OPERATING API call cache

    def Battery(self):
        if hasattr(self, '_battery') and (self._battery):
            return self._battery
        else:
            return None

    def BatteryPercent(self):
        tmp = self.Battery()
        if hasattr(self, '_battery') and (self._battery):
            self._battery_percent = tmp.get('percent')
            return self._battery_percent
        else:
            return None

    def BatteryPercentAdjusted(self):
        tmp = self.Battery()
        if hasattr(self, '_battery') and (self._battery) and (hasattr(self, '_model_voltage_max')) and (hasattr(self, '_model_voltage_min')):
            starttemp = int(self._battery_percent)
            self._battery_percent_adjusted = round((int(starttemp) - int(self._model_voltage_min)) / ((int(self._model_voltage_max) - int(self._model_voltage_min))/100))
            return self._battery_percent_adjusted
        else:
            _LOGGER.error(f"BatteryPercentAdjusted ERROR!")
            return None
    
    def BatteryVoltage(self):
        tmp = self.Battery()
        if hasattr(self, '_battery') and (self._battery):
            self._battery_voltage = tmp.get('voltage')
            return self._battery_voltage
        else:
            _LOGGER.error(f"BatteryVoltage ERROR!")
            return None

    def BatteryCycles(self):
        tmp = self.Battery()
        if hasattr(self, '_battery') and (self._battery):
            self._battery_cycles = tmp.get('cycles')
            return self._battery_cycles
        else:
            _LOGGER.error(f"BatteryCycles ERROR!")
            return None

    def BatteryDischarge(self):
        tmp = self.Battery()
        if hasattr(self, '_battery') and (self._battery):
            self._battery_discharge = tmp.get('discharge')
            return self._battery_discharge
        else:
            _LOGGER.error(f"BatteryDischarge ERROR!")
            return None

    def BatteryAmbientTemp(self):
        tmp = self.Battery()
        if hasattr(self, '_battery') and (self._battery):
            self._battery_ambient_temp = tmp.get('ambient_temp')
            return self._battery_ambient_temp
        else:
            _LOGGER.error(f"BatteryAmbientTemp ERROR!")
            return None

    def BatteryTemp(self):
        tmp = self.Battery()
        if hasattr(self, '_battery') and (self._battery):
            self._battery_temp = tmp.get('battery_temp')
            return self._battery_temp
        else:
            _LOGGER.error(f"BatteryTemp ERROR!")
            return None

    def Garden(self):
        if hasattr(self, '_garden'):
            return self._garden
        else:
            _LOGGER.error(f"Garden ERROR!")
            return None

    def HmiKeys(self):
        if hasattr(self, '_hmikeys'):
            return self._hmikeys
        else:
            _LOGGER.error(f"HmiKeys ERROR!")
            return None

############################################################
### Functions for getting data from UPDATES API call cache

    def FirmwareAvailable(self):
        if hasattr(self, '_firmware_available'):
            return self._firmware_available
        else:
            return None

############################################################
### Functions for getting data from NEXTCUTTING API call cache

    def NextMow(self):
        return self._next_mow

############################################################
### Functions for getting data from LASTCUTTING API call cache

    def LastCompletedMow(self):
        return self._last_completed_mow

############################################################
### Functions for getting data from ALERTS API call cache

    def AlertsDescription(self):
        alerts =  self._alerts
        tmp_cnt = 0
        for alert in alerts:
            tmp_cnt += 1
            tmp_code = alert['error_code']
            if (tmp_cnt == 1):
                self._alert1_id    = alert['alert_id']
                self._alert1_time  = self.ConvertBoschDateTime(alert['date']) 
                self._alert1_error = alert['error_code']
                self._alert1_friendly_description = self.FriendlyAlertErrorCode(tmp_code)
                self._alert2_id    = None
                self._alert2_time  = None
                self._alert2_error = None
                self._alert2_friendly_description = None
                self._alert3_id    = None
                self._alert3_name  = None
                self._alert3_error = None
                self._alert3_friendly_description = None
            if (tmp_cnt == 2):
                self._alert2_id  = alert['alert_id']
                self._alert2_time  = self.ConvertBoschDateTime(alert['date'])
                self._alert2_error = alert['error_code']
                self._alert2_friendly_description = self.FriendlyAlertErrorCode(tmp_code)
                self._alert3_time  = None
                self._alert3_error = None
                self._alert3_friendly_description = None
            if (tmp_cnt == 3):
                self._alert3_id  = alert['alert_id']
                self._alert3_time  = self.ConvertBoschDateTime(alert['date'])
                self._alert3_error = alert['error_code']
                self._alert3_friendly_description = self.FriendlyAlertErrorCode(tmp_code)
        return self._alerts

    def FriendlyAlertErrorCode(self, tmp):
        tmp_val = tmp

        if str(tmp_val) in ALERT_ERROR_CODE.keys():
            alert_description = ALERT_ERROR_CODE[tmp_val]
        else:
            _LOGGER.warning(f"Alert Error Code not in database! Alert Code {str(tmp_val)}")
            alert_description = "Not in database!"
        return alert_description

    def ConvertBoschDateTime(self, boshdatetime):
        return boshdatetime[0:10] + " " + boshdatetime[11:16]

### --- User readable get functions

    def AlertsCount(self):
        self._alerts_count = len(self._alerts)
        return self._alerts_count

#######################################
### Sending commands to mower
####################################### 
    def putCommand(self, command):
        _LOGGER.info("postCommand: " + command)
        if command == "mow" or command == "pause" or command == "returnToDock":
            complete_url = "alms/" + self._serial + "/state"
            _LOGGER.debug("complete_url: " + complete_url)
            data = '{"state":"' + command + '"}'
            #data: {"state":"mow"}
            temp = self.put(complete_url, data)    
            return temp
        else:
            _LOGGER.warning("postCommand " + command + " not valid!")
            return "Wrong Command!"

    def putMowMode(self, command):
        _LOGGER.info("putMowMode command: " + command)
        if command == "true" or command == "false" or command == "True" or command == "False":
            complete_url = "alms/" + self._serial + "/predictive"
            _LOGGER.debug("complete_url: " + complete_url)
            #command2 = " "enabled": enable }"
            data = '{"enabled":"' + command + '"}'
            temp = self.put(complete_url, data)    
            return temp
        else:
            _LOGGER.warning("postCommand " + command + " not valid!")
            return "Wrong Command!"

    def putPredictiveCal(self, command):
        _LOGGER.info("postCommand: " + command)
        complete_url = "alms/" + self._serial + "/predictive/calendar"
        _LOGGER.debug("complete_url: " + complete_url)
        #command2 = " "enabled": enable }"
        data = '{"enabled":"enable"}'
        data = "{'sel_cal': 1, 'cals': [{'cal': 1, 'days': [{'day': 0, 'slots': [{'En': True, 'StHr': 0, 'StMin': 0, 'EnHr': 8, 'EnMin': 0}, {'En': True, 'StHr': 20, 'StMin': 0, 'EnHr': 23, 'EnMin': 59}]}, {'day': 1, 'slots': [{'En': True, 'StHr': 0, 'StMin': 0, 'EnHr': 8, 'EnMin': 0}, {'En': True, 'StHr': 20, 'StMin': 0, 'EnHr': 23, 'EnMin': 59}]}, {'day': 2, 'slots': [{'En': True, 'StHr': 0, 'StMin': 0, 'EnHr': 8, 'EnMin': 0}, {'En': True, 'StHr': 20, 'StMin': 0, 'EnHr': 23, 'EnMin': 59}]}, {'day': 3, 'slots': [{'En': True, 'StHr': 0, 'StMin': 0, 'EnHr': 8, 'EnMin': 0}, {'En': True, 'StHr': 20, 'StMin': 0, 'EnHr': 23, 'EnMin': 59}]}, {'day': 4, 'slots': [{'En': True, 'StHr': 0, 'StMin': 0, 'EnHr': 8, 'EnMin': 0}, {'En': True, 'StHr': 20, 'StMin': 0, 'EnHr': 23, 'EnMin': 59}]}, {'day': 5, 'slots': [{'En': True, 'StHr': 0, 'StMin': 0, 'EnHr': 8, 'EnMin': 0}, {'En': True, 'StHr': 20, 'StMin': 0, 'EnHr': 23, 'EnMin': 59}]}, {'day': 6, 'slots': [{'En': True, 'StHr': 0, 'StMin': 0, 'EnHr': 23, 'EnMin': 59}]}]}]}"
        temp = self.put(complete_url, data)    
        return temp


###
# Not properly implemented yet
###

    def getPredictiveCalendar(self):
        _LOGGER.info("Call getPredictveCalendar")
        complete_url = 'alms/' + self._serial + '/predictive/calendar'
        Runtime_temp = self.get(complete_url)
        value = Runtime_temp
        _LOGGER.debug("--- getPredictveCalendar: end")
        return value

    def getUserAdjustment(self):
        # No idea what this does? Maybe adjust level settings for SmartMowing
        _LOGGER.info("Call getUserAdjustment")
        complete_url = 'alms/' + self._serial + '/predictive/useradjustment'
        Runtime_temp = self.get(complete_url)
        value = Runtime_temp
        _LOGGER.debug("--- getUserAdjustment: end")
        return value['user_adjustment']

#    def getCalendar(self):
#        _LOGGER.debug("---")
#        _LOGGER.debug("getCalendar")
#        complete_url = 'alms/' + self._serial + '/calendar'
#        Runtime_temp = self.get(complete_url)
#        value = Runtime_temp
#        return value

#    def getSecurity(self):
#        _LOGGER.debug("---")
#        _LOGGER.debug("getSecurity")
#        complete_url = 'alms/' + self._serial + '/security'
#        Runtime_temp = self.get(complete_url)
#        value = Runtime_temp
#        return value

#    def getAutomaticUpdate(self):
#        _LOGGER.debug("---")
#        _LOGGER.debug("getAutomaticUpdate")
#        complete_url = 'alms/' + self._serial + '/automaticUpdate'
#        Runtime_temp = self.get(complete_url)
#        value = Runtime_temp
#        return value

#    def getMap(self):
#        _LOGGER.debug("---")
#        print("getMap (Not implemented yet")
#        #complete_url = 'alms/' + self._serial + '/map'
#        #Runtime_temp = self.get(complete_url)
#        #value = Runtime_temp
#        value = "error"
#        return value

##########################################################################
### Basics for API calls
    def get(self, method, timeout=30):
        """Send a GET request and return the response as a dict."""
        _LOGGER.info("Call GET")
        logindata = json.loads(self._login_session.content)
        contextId = logindata['contextId']
        _LOGGER.debug("      ContextID: " + contextId)
        #Check mower online status
        if (self._offline >= 5):
            self._online = False
        else:
            self._online = True
        headers = {CONTENT_TYPE: CONTENT_TYPE_JSON, 'x-im-context-id': contextId}
        url = self._api_url + method
        _LOGGER.debug("      >>>API CALL: " + url)
        ###
        ### Test with iteration
        ###
        try_call = 0
        answer = False
        while (try_call < 5) and (answer == False): 
            try_call = try_call + 1
            _LOGGER.debug("      GET try " + str(try_call))
            try:
                response = requests.get(url, headers=headers, timeout=timeout)
            except requests.exceptions.Timeout:
                _LOGGER.error("      Failed to update Indego status. Timeout!")
                return None
            except requests.exceptions.TooManyRedirects:
                _LOGGER.error("      Failed to update Indego status. Too many redirects")
                return None
            except requests.exceptions.RequestException as e:
                _LOGGER.error("      Failed to update Indego status. Error: " + str(e))
                return None
            else:
                _LOGGER.debug("      HTTP Status code: " + str(response.status_code))
                if response.status_code == 400:
                    _LOGGER.error("      server answer: Bad Request")
                    return None
                if response.status_code == 500:
                    _LOGGER.error("      Server answer: Internal Server Error")
                    return None
                if response.status_code == 501:
                    _LOGGER.error("      Server answer: not implemented yet")
                    return None
                if response.status_code == 504:
                    _LOGGER.info("      server backend did not have an update before timeout")
                    return None
                elif response.status_code != 200:
                    _LOGGER.error("      need to call login again")
                    self.login()
                    logindata = json.loads(self._login_session.content)
                    contextId = logindata['contextId']
                    #return
                else:
                    _LOGGER.debug("      Json:" + str(response.json()))
                    response.raise_for_status()
                    _LOGGER.debug("   --- GET: end")
                    answer = True
                    return response.json()
        
        if (try_call >=5):
            _LOGGER.warning("Tried 5 times to get data but didnt succeed")
            _LOGGER.warning("Do you have the correct username, password and serial in configuration.yaml???")
        _LOGGER.debug("   --- GET: end")
    
    def put(self, url, data):
        """Send a PUT request and return the response as a dict."""
        _LOGGER.info("Call PUT")
        logindata = json.loads(self._login_session.content)
        contextId = logindata['contextId']
        headers = {CONTENT_TYPE: CONTENT_TYPE_JSON, 'x-im-context-id': contextId}
        url = self._api_url + url
        _LOGGER.debug("      >>>API CALL: " + url)
        _LOGGER.debug("      headers: " + str(headers))
        _LOGGER.debug("      data: " + str(data))
        try:
            response = requests.put(url, headers=headers, data=data, timeout=30)
        except requests.exceptions.Timeout:
            _LOGGER.error("      Failed to send data to Indego mower. Timeout!")
            return None
        except requests.exceptions.TooManyRedirects:
            _LOGGER.error("      Failed to send data to Indego mower. Too many redirects")
            return None
        except requests.exceptions.RequestException as e:
            _LOGGER.error("      Failed to send data to Indego mower. Error status: " + str(e))
            return None
        else:
            _LOGGER.error("      HTTP Status code: " + str(response.status_code))
            if response.status_code != 200:
                if response.status_code == 400:
                    _LOGGER.error("      >>>>>>>>>>>>>>>>>> Bad request! <<<<<<<<<<<<<<<<<<<<")
                elif response.status_code == 404:
                    _LOGGER.error("      >>>>>>>>>>>>>>>>>> Page not found! <<<<<<<<<<<<<<<<<<<<")
                elif response.status_code == 500:
                    _LOGGER.error("      >>>>>>>>>>>>>>>>>> Internal server error! <<<<<<<<<<<<<<<<<<<<")
                elif response.status_code == 401:
                    _LOGGER.error("      >>>>>>>>>>>>>>>>>> Unauthorized! <<<<<<<<<<<<<<<<<<<<")
                    _LOGGER.error("      need to call login again")
                    self.login()
                else:
                    _LOGGER.error("      >>>>>>>>>>>>>>>>>> Unexpected error! <<<<<<<<<<<<<<<<<<<<")
                    _LOGGER.error("      need to call login again")
                    self.login()
                return str(response.status_code)
            else:
                _LOGGER.debug("      Json:" + str(response))
                _LOGGER.debug("   --- GET: end")
                if (response.status_code == 200):
                    return "OK"
                else:
                    return str(response.status_code)
        _LOGGER.debug("   --- GET: end")
#End PYPI __init__.py