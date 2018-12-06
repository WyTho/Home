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
