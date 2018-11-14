--	[[	# WyTho object change checker # ]] --
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

--  [[  Constants support in LUA  ]]  --
--  [[  Credits: Andrejs Cainikovs]]  --
--  [[  Used as Safety measure    ]]  --
function CreateConstant(tbl)
    return setmetatable({}, {
        __index = tbl,
        __newindex = function(t, key, value)
            error("attempting to change constant " ..
                   tostring(key) .. " to " .. tostring(value), 2)
        end
    })
end

function __LINE__() return debug.getinfo(2, 'l').currentline end

--  [[  Sends multiple items directly to an API ]]  --
--  [[  !Converts data to JSON ]]  --
--  [[  !Uses LUA table for request_body  ]]  --
--  [[  !Tables can only be 1 level deep  ]]  --
function UpdateItemsInAPI(APISettings, dbData)  
  if(type(dbData) ~= 'table'      then return end
  if(APISettings.ip == nil)       then return end
  if(APISettings.port == nil)     then return end
  if(APISettings.endpoint == nil) then return end
  
  require('socket.http')
  require('ltn12')
  require('json')

--  [[  Go through database entries updating them 1 by 1  ]]  --
--  [[  TODO: Multiple Items at once(SUPPORT FROM API NEEDED)  ]]  --
  for i,v in pairs(dbData) do
      local APIUrl = APISettings.ip .. ':' .. APISettings.port .. '/' .. APISettings.endpoint .. '/' .. v.id
      local request_body, response_body = {}
      
      request_body = {v.name, v.address, v.comment}
      request_body = json.encode(request_body)
      
      local res, code, response_headers = http.request{
        url = APIUrl,
        method = "POST", 
        headers = 
          {
              ["Content-Type"] = "application/x-www-form-urlencoded";
              ["Content-Length"] = #request_body;
          },
          source = ltn12.source.string(request_body),
          sink = ltn12.sink.table(response_body),
      }
      
      if (code ~= 200) then
        log('device_change_check:' .. 
      end
      
  end  
end

local APISETTINGS = {
    ip = '0.0.0.0',
    port = '5000',
    endpoint = 'api/item'
}

local STORAGEDETAILS = {
    string = 'device_change_check_storage'
}

APISETTINGS = CreateConstant(APISettings)
STORAGEDETAILS = CreateConstant(STORAGEDETAILS)

--  [[  __Implementation__  ]]  --
currentDevices = db:getall('SELECT id, name, address, comment FROM objects')
oldDevices = storage.get(STORAGEDETAILS.string)
if (oldDevices == nil) then 
  storage.set(STORAGEDETAILS.string)
else
  if(currentDevices ~= oldDevices) then
    
  end
end
