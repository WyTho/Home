--	[[	# Team WyTho Data Transfer and Access Library # ]] --
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

--	[[	__Functions__ ]]

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

--	[[	Translate an SQLite query to JSON	]]	--
--	[[	Used for http(s) data transfer	]]	--
function QueryToJSON(dbQuery, filter)
    require('json')
    local dbExec = db:getall(dbQuery)

    if filter then
        dbExec = ConvertGroupAddressToString(dbExec)
    end
    local json = json.encode(dbExec)

    return json
end

--  [[  Sends a single event directly to an API ]]  --
--  [[  !Doesn't convert data to JSON ]]  --
--  [[  !Uses LUA table for request_body  ]]  --
--  [[  !Tables can only be 1 level deep  ]]  --
function SendEventToAPI(APISettings, dbData)  
  if(type(dbData) ~= 'table'      then return end
  if(APISettings.ip == nil)       then return end
  if(APISettings.port == nil)     then return end
  if(APISettings.endpoint == nil) then return end
  
  local APIUrl = APISettings.ip .. ':' .. APISettings.port .. '/' .. APISettings.endpoint
  require('socket.http')
  require('ltn12')
  
  local request_body = '[['
  local response_body = {}
  
  --  [[  Build request body ]] --
  for i,v in pairs(dbData) do    
      request_body = request_body .. i .. '=' .. v .. '&'
  end  
  
  request_body = request_body .. ']]'

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
end

--  [[  Sends a JSONString to an API  ]]  --
--  [[  !Doesn't convert data to JSON ]]  --
--  [[  !Uses string for request body ]]  --
function SendJSONtoAPI(APISettings, JSONString)
  if(type(JSONString) ~= 'string' then return end
  if(APISettings.ip == nil)       then return end
  if(APISettings.port == nil)     then return end
  if(APISettings.endpoint == nil) then return end
  
  local APIUrl = APISettings.ip .. ':' .. APISettings.port .. '/' .. APISettings.endpoint
  require('socket.http')
  require('ltn12')
  
  local request_body = JSONString
  local response_body = {}

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
end

--  [[  __Program__ ]]  --

--  [[  Make sure to change these settings  ]]  --
local APISettings = {
      ip = '0.0.0.0',
      port = '80',
      endpoint = 'api/item'
}
APISettings = CreateConstant(APISettings)

--	[[	## Following list contains all important database queries ## ]]	--
--	[[	*	SELECT name FROM sqlite_master WHERE type="table"	*	]]	--
--	[[	*	SELECT sql FROM sqlite_master *	]]	--
--	[[	*	SELECT * FROM objects WHERE name = "Z04 Gang lamp (SW)" LIMIT 1')	*	]]	--

--  [[  *   SELECT address, name, comment FROM objects  ]]  --

local dbExec = QueryToJSON('SELECT address, name, comment FROM objects',true)
dbExec = ConvertGroupAddressToString(dbExec)
SendJSONtoAPI(APISettings, dbExec)

log(dbExec)