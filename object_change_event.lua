--	[[	# object_change_event # ]] --
-- 			88b           d88    88888888ba
-- 			888b         d888    88      "8b
-- 			88`8b       d8'88    88      ,8P
-- 			88 `8b     d8' 88    88aaaaaa8P'
-- 			88  `8b   d8'  88    88""""""8b,
-- 			88   `8b d8'   88    88      `8b
-- 			88    `888'    88    88      a8P
-- 			88     `8'     88    88888888P"
--	[[	## Made by: Maikel Bolderdijk ## 							]]	--
--	[[	## Email: maikel.bolderdijk@student.hu.nl ##	]]	--

-- [[ Send an object change to the WyTho API ]] --

--  [[  Constants support in LUA  ]]  --
--  [[  Credits: Andrejs Cainikovs]]  --
--  [[  Used as Safety measure    ]]  --
function CreateConstant(tbl)
 return setmetatable(
  {},
  {
   __index = tbl,
   __newindex = function(t, key, value)
    error("attempting to change constant " .. tostring(key) .. " to " .. tostring(value), 2)
   end
  }
 )
end

--  [[  GLOBAL CONSTANTS ]]  --
--  [[  MAKE SURE TO ALWAYS CHANGE ACCORDING TO YOUR SETUP ]] --
--  [[  API_DOCUMENTATION @ github.com/wytho/python_flask   ]]  --
local CONSTANTS = {
 API = {
  IP = "10.1.1.143",
  PORT = 5000,
  ENDPOINTS = {
   BASE = "api",
   item = "item",
   item_id = "item/%d",
   usage = "usage",
   usage_id = "usage/%d",
   event = "event",
   event_id = "event/%d",
   group = "group",
   group_id = "group/%d",
   event_call = "event_call",
   event_call_id = "event_call/%d",
   graph = "graph",
   graph_title = "graph/%s"
  },
  ENDPOINT_METHODS = {
   BASE = {""},
   item = {"GET", "POST"},
   item_id = {"GET", "POST"},
   usage = {"GET", "POST"},
   usage_id = {"GET", "POST"},
   event = {"GET", "POST"},
   event_id = {"GET"},
   group = {"GET", "POST"},
   group_id = {"GET", "PUT"},
   event_call = {"GET", "POST"},
   event_call_id = {"GET"},
   graph = {"GET"},
   graph_title = {"GET", "PUT"}
  }
 }
}
CONSTANTS = CreateConstant(CONSTANTS)

-- [[ Check if a table contains a certain value ]] --
-- [[ @param table Table that might contain the value   ]]  --
-- [[ @param val Value that should be in the table  ]]  --
local function Contains(table, val)
 for i = 1, #table do
  if table[i] == val then
   return true
  end
 end
 return false
end

-- [[ Should be self explanatory ]] --
local function GetObjectIDByAddress(address)
 query = string.format("SELECT id FROM objects WHERE address=%s", address)
 return db:getall(query)
end

-- [[ ]] --
-- [[ ]] --
function GetObjectUsages(CONSTANTS, current_object)
 if (current_object == nil) then
  log("no data. Function: CreateUsage")
 end

 if (CONSTANTS == nil) then
  log("CONSTANTS ARE NIL")
  return
 end

 if (CONSTANTS.API.IP == nil) then
  log("MISSING IP FOR API")
  return
 end

 if (CONSTANTS.API.PORT == nil) then
  log("MISSING PORT FOR API")
  return
 end

 if (CONSTANTS.API.BASE == nil) then
  log("MISSING BASE ENDPOINT")
  return
 end

 if (CONSTANTS.API.usage == nil) then
  log("MISSING usage ENDPOINT")
  return
 end

 if (Contains(CONSTANTS.API.ENDPOINT_METHODS.usage, "GET") == false) then
  log("ENDPOINT usage DOESN'T HAVE METHOD 'GET'")
  return
 end

 local http = require("socket.http")
 local ltn12 = require("ltn12")
 local json = require("json")

 local APIUrl =
  string.format(
  "http://%s:%s/%s",
  CONSTANTS.API.IP,
  CONSTANTS.API.PORT,
  CONSTANTS.API.BASE .. "/" .. CONSTANTS.API.usage
 )
 local request_body, response_body = {}

 local res, code, response_headers =
  http.request {
  url = APIUrl,
  method = "GET", -- Contains(CONSTANTS.API.ENDPOINT_METHODS.usage, 'GET')
  headers = {
   ["Content-Type"] = "application/x-www-form-urlencoded",
   ["Content-Length"] = #request_body
  },
  source = ltn12.source.string(request_body),
  sink = ltn12.sink.table(response_body)
 }

 if (code ~= 201) then
  log(string.format("API returned code %s with the following response: %s", code, res))
  return false
 else
  if (res ~= nil) then
   res = json.encode(res)
   local usages = {}
   for k, v in pairs(usages) do
    if (v["external_id"] == current_object.id) then
     usages.append(v)
    end
   end
   return usages
  else
   log("Response was empty. Function GetObjectUsages()")
   return false
  end
 end
end

--  [[ Creates an event in the database of the WyTho API by calling its endpoint ]]  --
--  [[ @param data single object data   ]]  --
--  [[ @param item_id internal LSS100100 item_id    ]]  --
function CreateEvent(CONSTANTS, current_object)
 local object_usages = GetObjectUsages(CONSTANTS, current_object)
 if (object_usages) then
  if (CONSTANTS == nil) then
   log("CONSTANTS ARE NIL")
   return
  end

  if (CONSTANTS.API.IP == nil) then
   log("MISSING IP FOR API")
   return
  end

  if (CONSTANTS.API.PORT == nil) then
   log("MISSING PORT FOR API")
   return
  end

  if (CONSTANTS.API.BASE == nil) then
   log("MISSING BASE ENDPOINT")
   return
  end

  if (CONSTANTS.API.event == nil) then
   log("MISSING event ENDPOINT")
   return
  end

  if (Contains(CONSTANTS.API.ENDPOINT_METHODS.event, "POST") == false) then
   log("ENDPOINT event DOESN'T HAVE METHOD 'POST'")
   return
  end

  local http = require("socket.http")
  local ltn12 = require("ltn12")
  local json = require("json")

  local APIUrl =
   string.format(
   "http://%s:%s/%s",
   CONSTANTS.API.IP,
   CONSTANTS.API.PORT,
   CONSTANTS.API.BASE .. "/" .. CONSTANTS.API.usage
  )
  local request_body, response_body = {}

  -- [[ TODO: EVENT_BLOCK ]] --
  local USAGE_ID = 0
  local USAGE_TYPE = ""
  -- [[ END EVENT_BLOCK ]] --

  request_body = string.format("usage_id=%s&data=%s&data_type=%s", USAGE_ID, current_object.value, USAGE_TYPE)
  local res, code, response_headers =
   http.request {
   url = APIUrl,
   method = "POST", -- Contains(CONSTANTS.API.ENDPOINT_METHODS.event, 'POST')
   headers = {
    ["Content-Type"] = "application/x-www-form-urlencoded",
    ["Content-Length"] = #request_body
   },
   source = ltn12.source.string(request_body),
   sink = ltn12.sink.table(response_body)
  }

  if (code ~= 201) then
   log(string.format("API returned code %s with the following response: %s", code, res))
  end
 else
  log("No object usages found. Function CreateEvent()")
 end
end

current_object = {
 address = "1/1/1",
 id = GetObjectIDByAddress(current_object.address),
 value = grp.getvalue(current_object.id)
}

CreateEvent(CONSTANTS, current_object)
