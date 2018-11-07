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

--	[[	## Following list contains all important database queries ## ]]	--
--	[[	*	SELECT name FROM sqlite_master WHERE type="table"	*	]]	--
--	[[	*	SELECT sql FROM sqlite_master *	]]	--
--	[[	*	SELECT * FROM objects WHERE name = "Z04 Gang lamp (SW)" LIMIT 1')	*	]]	--

local dbExec = QueryToJSON('SELECT * FROM objects WHERE name = "Z04 Gang lamp (SW)" LIMIT 1',true)

log(dbExec)