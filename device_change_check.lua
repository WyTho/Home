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

--	[[ Converts an integer group address(36374) to a KNX address string(11/11/11)	]] --
--	[[ Used for remote controlled access	]]--
function ConvertGroupAddressToString(dbObject)
    for i, v in pairs(dbObject) do
        --	[[	3-level KNX address config	]]	--
        --	[[	main		=	0..31		XX/00/00 	]]  --
        --	[[	middle	=	0..7		00/XX/00	]] 	--
        --	[[	sub			=	0..255	00/00/XX	]]	--
        local main, middle, sub  -- Explained above
        local mainRest, middleRest  -- Needed for proper calculation
        local subMax, middleMax = 256, 8 -- See KNX address config above
        local vSet = v -- We don't want to directly edit v

        main = math.floor((v["address"] / subMax) / middleMax)
        mainRest = ((v["address"] / subMax) / middleMax) - main

        middle = math.floor(mainRest * middleMax)
        middleRest = (mainRest * middleMax) - middle

        sub = middleRest * subMax

        vSet["address"] = main .. "/" .. middle .. "/" .. sub

        dbObject[i] = vSet
    end
    return dbObject
end

--  [[  Compares two tables if they are equal regardless of index   ]]  --
--  [[  @return boolean ]]  --
--  [[  @source https://web.archive.org/web/20131225070434/http://snippets.luacode.org/snippets/Deep_Comparison_of_Two_Values_3 ]]  --
--  [[  Changed for use case by Maikel Bolderdijk   ]]  --
function isEqual(t1, t2)
    local ty1 = type(t1)
    local ty2 = type(t2)
    if ty1 ~= ty2 then
        return false
    end
    -- non-table types can be directly compared
    if ty1 ~= "table" and ty2 ~= "table" then
        return t1 == t2
    end
    -- as well as tables which have the metamethod __eq
    for k1, v1 in pairs(t1) do
        local v2 = t2[k1]
        if v2 == nil or not isEqual(v1, v2) then
            return false
        end
    end
    for k2, v2 in pairs(t2) do
        local v1 = t1[k2]
        if v1 == nil or not isEqual(v1, v2) then
            return false
        end
    end
    return true
end

--  [[  Compares two tables and returns the difference  ]]  --
--  [[  @return Changed table elements ]]  --
function GetTableDiff(t1, t2)
    local diff = {}
    for i1, v1 in pairs(t1) do
        local equal = true
        local v2 = t2[i1]
        if (type(v1) == "table") then
            for j1, w1 in pairs(v1) do
                if (w1 ~= t2[i1][j1]) and equal then
                    equal = false
                end
            end
        end
        if not equal then
            table.insert(diff, v2)
        end
    end
    return diff
end

--  [[  Sends Multiple devices to an API ]]  --
--  [[  !Converts data to JSON ]]  --
--  [[  !Uses LUA table for request_body  ]]  --
function UpdateItemsInAPI(APISettings, data)
    if (type(data) ~= "table") then
        return
    end
    if (APISettings.ip == nil) then
        return
    end
    if (APISettings.port == nil) then
        return
    end
    if (APISettings.endpoint == nil) then
        return
    end

    local http = require("socket.http")
    local ltn12 = require("ltn12")
    require("json")

    --  [[  Go through database entries updating them 1 by 1  ]]  --
    --  [[  TODO: Multiple Items at once(SUPPORT FROM API NEEDED)  ]]  --
    for i, v in pairs(data) do
        local APIUrl = string.format("http://%s:%s/%s/%s", APISettings.ip, APISettings.port, APISettings.endpoint, v.id)
        local request_body, response_body = {}

        request_body = string.format("name=%s&address=%s&comment=%s&usage_type=&usage=", v.name, v.address, v.comment)
        log(request_body)
        local res, code, response_headers =
            http.request {
            url = APIUrl,
            method = "POST",
            headers = {
                ["Content-Type"] = "application/x-www-form-urlencoded",
                ["Content-Length"] = #request_body
            },
            source = ltn12.source.string(request_body),
            sink = ltn12.sink.table(response_body)
        }

        if (code ~= 201) then
            -- TODO: Test this stuff
            log(
                string.format(
                    "ERROR IN FILE: initial_device_send: %s : API returned code %s with the following response: %s",
                    90,
                    code,
                    res
                )
            )
        -- return false
        end
    end
    return true
end

--  [[  __Implementation__  ]]  --
local APISETTINGS = {
    ip = "10.1.1.143",
    port = "5000",
    endpoint = "api/item"
}

local STORAGEDETAILS = {
    string = "device_change_check_storage"
}

APISETTINGS = CreateConstant(APISETTINGS)
STORAGEDETAILS = CreateConstant(STORAGEDETAILS)

currentDevices = db:getall("SELECT id, name, address, comment FROM objects")
currentDevices = ConvertGroupAddressToString(currentDevices)
oldDevices = storage.get(STORAGEDETAILS.string)

if (oldDevices == nil) then
    storage.set(STORAGEDETAILS.string, currentDevices)
    log("NO DEVICES EXIST YET... STORING " .. storage.get(STORAGEDETAILS.string))
else
    if not isEqual(oldDevices, currentDevices) then
        local diff = GetTableDiff(oldDevices, currentDevices)
        if UpdateItemsInAPI(APISETTINGS, diff) == true then
            storage.set(STORAGEDETAILS.string, currentDevices)
        end
    --else
    --  UpdateItemsInAPI(APISETTINGS, oldDevices) -- Return to old state
    -- end
    end
end
