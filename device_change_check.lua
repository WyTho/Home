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

--  [[ Compares 2 tables(t1, t2) and returns the differences ]]  --
--  [[ @return table with differences ]]  --
function GetTableDiff(t1,t2)
  if type(t1) ~= 'table' or type(t2) ~= 'table' then return false end
  
  local diff = {}
  
  -- Simple diff here, speed is Log(n)  
  for i, v in pairs(t1) do
    if t1[i] ~= t2[i] then
      diff.insert(t1[i])
    end    
  end
  return diff
end

--  [[  Updates multiple items in an API ]]  --
--  [[  !Converts data to JSON ]]  --
--  [[  !Uses LUA table for request_body  ]]  --
function UpdateItemsInAPI(APISettings, data)  
  if(type(data) ~= 'table'      then return end
  if(APISettings.ip == nil)       then return end
  if(APISettings.port == nil)     then return end
  if(APISettings.endpoint == nil) then return end
  
  require('socket.http')
  require('ltn12')
  require('json')

--  [[  Go through database entries updating them 1 by 1  ]]  --
--  [[  TODO: Multiple Items at once(SUPPORT FROM API NEEDED)  ]]  --
  for i,v in pairs(data) do
      local APIUrl = string.format('%s:%s/%s/%d', APISettings.ip, APISettings.port,APISettings.endpoint,v.id)
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
        -- TODO: Test this stuff
        log(string.format('ERROR IN FILE: device_change_check: %s : API returned code %d with the following response: %s', __LINE__(), code, res))
      end
  end
  return true
end

--  [[  __Implementation__  ]]  --
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

currentDevices = db:getall('SELECT id, name, address, comment FROM objects')
oldDevices = storage.get(STORAGEDETAILS.string)
if (oldDevices == nil) then 
  storage.set(STORAGEDETAILS.string)
else
  if(currentDevices ~= oldDevices) then
    local diff = GetTableDiff(currentDevices, oldDevices)
    if UpdateItemsInAPI(APISETTINGS, diff) == true then
      storage.set(STORAGEDETAILS.string, currentDevices)
    else
      UpdateItemsInAPI(APISETTINGS, oldDevices) -- Return to old state
    end
  end
end
