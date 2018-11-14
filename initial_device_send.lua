--	[[	# Initial device send script # ]] --
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

--	[[ Converts an integer group address(36374) to a KNX address string(11/11/11)	]] --
--	[[ Used for remote controlled access	]]--
function ConvertGroupAddressToString(dbObject)
    for i, v in pairs(dbObject) do
        --	[[	3-level KNX address config	]]	--
        --	[[	main		=	0..31		XX/00/00 	]]  --
        --	[[	middle	=	0..7		00/XX/00	]] 	--
        --	[[	sub			=	0..255	00/00/XX	]]	--
        local main, middle, sub -- Explained above
        local mainRest, middleRest -- Needed for proper calculation
        local subMax, middleMax = 256, 8 -- See KNX address config above
        local vSet = v -- We don't want to directly edit v

        main = math.floor( (v['address'] / subMax) / middleMax)
        mainRest = ( (v['address'] / subMax) / middleMax ) - main

        middle = math.floor(mainRest * middleMax)
        middleRest = (mainRest * middleMax) - middle

        sub = middleRest * subMax

        vSet['address'] = main .. '/' .. middle .. '/' .. sub

        dbObject[i] = vSet
    end
    return dbObject
end

--  [[  Sends Multiple devices to an API ]]  --
--  [[  !Converts data to JSON ]]  --
--  [[  !Uses LUA table for request_body  ]]  --
function SendItemsToAPI(APISettings, data)  
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
      local APIUrl = string.format('%s:%s/%s', APISettings.ip, APISettings.port,APISettings.endpoint)
      local request_body, response_body = {}
      
      request_body = {v.id, v.name, v.address, v.comment}
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
      
      if (code ~= 201) then
        -- TODO: Test this stuff
        log(string.format('ERROR IN FILE: initial_device_send: %s : API returned code %d with the following response: %s', __LINE__(), code, res))
        -- return false
      end
  end
  return true
end

--  [[  __Implementation__  ]]  --
local APISettings = {
      ip = '0.0.0.0',
      port = '80',
      endpoint = 'api/item'
}
APISettings = CreateConstant(APISettings)

devices = db:getall('SELECT id, name, address, comment FROM object')
devices = ConvertGroupAddressToString(devices)
SendItemsToAPI(APISETTINGS, devices) -- needs error checking



