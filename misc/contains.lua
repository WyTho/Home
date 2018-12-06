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
