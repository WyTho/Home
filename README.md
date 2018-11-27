# Home
Home is a sub-project for team WyTho to connect devices in the Selficient house to the outside world.

The scripts inside the Home project run on the [HomeLynk LSS100100](https://www.schneider-electric.com/en/product/LSS100100/wiser-for-knx-logic-controller/) made by Schneider Electric.

This project includes scripts to read information from the LSS100100 to a connected WyTho API. Extra elements like debugging, documentation and environment is included for ease of use.

# Table of contents
- Support
- Environment setup
- Running scripts
- Security

## Support
Any issues, bugs or any other information requests can be answered by filing an issue report. For quick response it's advised to send an email to the following email address: [maikel.bolderdijk@gmail.com](mailto:maikel.bolderdijk@student.hu.nl).

## Environment Setup
For the user-guide of the LSS100100 please refer to the following guide: [User Guide-Wiser for KNX(LSS100100)](http://download.schneider-electric.com/files?p_enDocType=User+guide&p_File_Name=AR1740_EdI_User_Wiser_for_KNX_EN.pdf&p_Doc_Ref=AR1740_EdI_EN)

> Firmware version: 2.0.0

> Connected to local network(No internet connection)

> More information needs to be added

## Running scripts
All scripts follow a strict timing schedule. If you don't know how to use timing schedules on the LSS100100 please refer to the user-guide posted in [Environment Setup](Environment-Setup)

The following scripts are used with the following time schedule:
| Script | Time |
|------|-----:|
| Initial_Device_send.lua   | One time use |
| Device_Change_check.lua   | Every 5 minutes |
