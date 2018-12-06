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
--  [[  @param tbl Table that needs to be a constant value  ]]  --
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

--  [[  Check if value n is int ]]  --
function IsInt(n)
    return n == math.floor(n)
end

--	[[ Converts an integer group address to a KNX address string(11/11/11)	]] --
--	[[ @param dbObject table with address objects	]]--
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

--  [[  Sends Multiple devices to an API ]]  --
--  [[  !Converts data to JSON ]]  --
--  [[  !Uses LUA table for request_body  ]]  --
--  [[  @param data device data from internal database]]
function SendItemsToAPI(CONSTANTS, data)
    if (type(data) ~= "table") then
        return
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

    if (CONSTANTS.API.item == nil) then
        log("MISSING item ENDPOINT")
        return
    end

    if (Contains(CONSTANTS.API.ENDPOINT_METHODS.item, "POST") == false) then
        log("ENDPOINT item DOESN'T HAVE METHOD 'POST'")
        return
    end

    local http = require("socket.http")
    local ltn12 = require("ltn12")
    local json = require("json")

    --  [[  Go through database entries adding them 1 by 1  ]]  --
    --  [[  TODO: Multiple Items at once(SUPPORT FROM API NEEDED)  ]]  --
    for i, v in pairs(data) do
        local APIUrl =
            string.format(
            "http://%s:%s/%s",
            CONSTANTS.API.IP,
            CONSTANTS.API.PORT,
            CONSTANTS.API.BASE .. "/" .. CONSTANTS.API.item
        )
        local request_body, response_body = {}

        request_body = "name=" .. v.name .. "&address=" .. v.address .. "&comment=" .. v.comment
        local res, code, response_headers =
            http.request {
            url = APIUrl,
            method = "POST", -- Contains(CONSTANTS.API.ENDPOINT_METHODS.item, 'POST')
            headers = {
                ["Content-Type"] = "application/x-www-form-urlencoded",
                ["Content-Length"] = #request_body
            },
            source = ltn12.source.string(request_body),
            sink = ltn12.sink.table(response_body)
        }

        if (code == 201) then
            if (res ~= nil) then
                res = json.decode(res)
                CreateUsage(CONSTANTS, v, res.id)
            else
                log("Response is empty: Function SendItemsToApi")
            end
        else
            log(string.format("API returned code %s with the following response: %s", code, res))
        end
    end
end

--  [[ Creates a usage in the database of the API by calling its endpoint ]]  --
--  [[ @param data single object data   ]]  --
--  [[ @param item_id internal LSS100100 item_id    ]]  --
function CreateUsage(CONSTANTS, data, item_id)
    if (data == nil) then
        log("no data. Function: CreateUsage")
    end

    if (IsInt(item_id) == false) then
        log("item_id isn't an integer. Function: CreateUsage")
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

    if (Contains(CONSTANTS.API.ENDPOINT_METHODS.usage, "POST") == false) then
        log("ENDPOINT usage DOESN'T HAVE METHOD 'POST'")
        return
    end

    --  [[ TODO: BLOCK OBJECT_SPECIFIC  ]]  --
    local CONSUMPTION_AMOUNT = -1 -- Not bound to realistic values right now
    local CONSUMPTION_TYPE = nil
    local MIN_VAL = 0
    local MAX_VAL = 100
    --  [[ END OBJECT_SPECIFIC  ]]  --

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

    -- TODO: BLOCK_OBJECT_SPECIFIC
    request_body =
        string.format(
        "item_id=%s&consumption_type=%s&consumption_amount=%s&address=%s&unit=%s&external_id=%s&min_value=%s&max_value=%s",
        item_id,
        CONSUMPTION_TYPE,
        CONSUMPTION_AMOUNT,
        data["address"],
        UNIT,
        data["id"],
        MIN_VAL,
        MAX_VAL
    )
    local res, code, response_headers =
        http.request {
        url = APIUrl,
        method = "POST", -- Contains(CONSTANTS.API.ENDPOINT_METHODS.usage, 'POST')
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
end

--  [[  __Implementation__  ]]  --
devices = db:getall("SELECT id, name, address, comment FROM objects")
devices = ConvertGroupAddressToString(devices)
SendItemsToAPI(CONSTANTS, devices) -- needs error checking
log("SEND DEVICE SCRIPT FINISHED")
