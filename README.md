
![Hometho](https://github.com/wytho/home/misc/images/HomeTho.png "HomeTho Logo")
# Home
Home is a sub-project for team WyTho to connect devices in the Selficient house to the outside world.

The scripts inside the Home project run on the [HomeLynk LSS100100](https://www.schneider-electric.com/en/product/LSS100100/wiser-for-knx-logic-controller/) made by Schneider Electric.

This project includes scripts to read information from the LSS100100 to a connected WyTho API. Extra elements like debugging, documentation and environment is included for ease of use.

# Important Notices
 * Please make sure you read all documentation before changing anything
 * Transferring ownership can be done through emailing: maikel.bolderdijk@student.hu.nl
 * Please visit github.com/wytho for the full scope of our project

# Table of contents
* [Support](Support)
* [Environment Setup](Environment-setup)
* [Running Scripts](Running-scripts)
* [Debugging](Debugging)
    - [TCP Data Receiver](TCP-Data-Receiver)
    - [LSS100100 Internal Database](LSS100100-internal-database)
* [License](License)

## Support
Any issues, bugs or any other information requests can be answered by filing an issue report. For quick response it's advised to send an email to the following email address: [maikel.bolderdijk@gmail.com](mailto:maikel.bolderdijk@student.hu.nl).

## Environment Setup
For the user-guide of the LSS100100 please refer to the following guide: [User Guide-Wiser for KNX(LSS100100)](http://download.schneider-electric.com/files?p_enDocType=User+guide&p_File_Name=AR1740_EdI_User_Wiser_for_KNX_EN.pdf&p_Doc_Ref=AR1740_EdI_EN)

> Firmware version: 2.0.0 <br/>
> Connected to local network (No internet connection)<br/>
> LuaJit (Version unknown)<br/>
> In-House connected to U-Motion device

## Running Scripts
All scripts follow a strict timing schedule. If you don't know how to use timing schedules on the LSS100100 please refer to the user-guide posted in [Environment Setup](Environment-Setup)

The following scripts are used with the following time schedule:
> Initial_Device_send.lua | One time use <br/>
> Device_Change_check.lua | Every 5 minutes

## Debugging
Debugging your scripts on the LSS100100 is a pain in the ass without the right tools. <br/>

### TCP Data Receiver
At this time of writing the log() function of the LSS100100 only allows for 233 characters to be written to the log file. <br/>

In the debugging folder you can find a tool called: Data_Receiver. This application allows for receiving big TCP messages over a regular computer network.

The data receiver communicates over TCP and uses the following configuration:
> IP = Your ip address (0.0.0.0) <br/>
> PORT = 5006

__Please make sure your firewall isn't blocking TCP connections over port 5006__

If you'd like to send messages from the LSS100100 to your device via LUA scripting please implement the following function:

```LUA
-- data can be max 50000000 bytes
function sendData(data)
    YOUR_IP     = 0.0.0.0 -- Change this part
    YOUR_PORT   = 5006    -- Change this part

    local socket = require("socket") -- Note that this library isn't documented anywhere at this point of time
    local tcp = assert(socket.tcp())

    tcp:connect(YOUR_IP, YOUR_PORT);
    tcp:send(data);
    tcp::close()
end
```

### LSS100100 Internal Database
LSS100100 uses an internal SQLite database which is accessible with undocumented functionalities implemented with the scripting functionalities of the LSS100100. You can query the database by using the following function:

```LUA
db:getall(query) -- Only SQLLite queries
```

__THE ABOVE FUNCTION IS UNDOCUMENTED IN THE DOCUMENTATION OF THE LSS100100 OR ANY OTHER SCHNEIDER ELECTRIC DOCUMENTATION.__<br/>
__IT IS ADVISED TO NOT USE THIS FUNCTION IN THE FUTURE AND FIND OTHER WAYS OF RETRIEVING INFORMATION__

An example of the internal database can be found in the folder: __database__.

