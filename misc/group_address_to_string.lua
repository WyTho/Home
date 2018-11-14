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