dofile_once("mods/__noitatoolhelper/files/scripts/json.lua")
dofile_once("data/scripts/perks/perk_list.lua")
dofile_once("data/scripts/lib/utilities.lua")
dofile_once("data/scripts/gun/gun_enums.lua")
dofile_once("data/scripts/gun/gun_actions.lua")
dofile_once("data/scripts/magic/fungal_shift.lua")


function dump(o)
    if type(o) == 'table' then
       local s = '{ '
       for k,v in pairs(o) do
          if type(k) ~= 'number' then k = '"'..k..'"' end
          s = s .. '['..k..'] = ' .. dump(v) .. ','
       end
       return s .. '} '
    else
       return tostring(o)
    end
end

function exists(file)
   local ok, err, code = os.rename(file, file)
   if not ok then
      if code == 13 then
         -- Permission denied, but it exists
         return true
      end
   end
   return ok, err
end

function lines_from(file)
    if not exists(file) then return {} end
    local lines = {}
    for line in io.lines(file) do 
        lines[#lines + 1] = line
    end
    return lines
end

local function shuffle_table( t )
	assert( t, "shuffle_table() expected a table, got nil" )
	local iterations = #t
	local j
	
	for i = iterations, 2, -1 do
		j = Random(1,i)
		t[i], t[j] = t[j], t[i]
	end
end
function table.contains(t, element)
    for _, value in pairs(t) do
      if value == element then
        return true
      end
    end
    return false
  end

function OnPlayerSpawned(a)
    if not exists(noitaToolsDir .. "/data.json") then
        f = io.open(noitaToolsDir .. "/data.json", "w")
        f:write("{}")
        f:close()
        data = {}
    else
        data = json.decode(table.concat(lines_from(noitaToolsDir .. "/data.json"), ""))
    end

    data["perkAssets"] = {}
    data["spellAssets"] = {}
    data["fungalMaterialsFrom"] = {}
    data["fungalMaterialsTo"] = {}
    data["activeMods"] = ModGetActiveModIDs()

    -- PERKS
    for i, v in ipairs(perk_list) do
        new = {}
        new["image"] = v.ui_icon
        new["name"] = v.ui_name
        new["id"] = v.id
        new["default"] = v.not_in_default_perk_pool == nil or not v.not_in_default_perk_pool
        new["stackable"] = v.stackable ~= nil and v.stackable
        new["maxInPerkPool"] = (v.max_in_perk_pool ~= nil and v.max_in_perk_pool or false)
        new["stackableMax"] = (v.stackable_maximum ~= nil and v.stackable_maximum or false)
        new["stackableRare"] = (v.stackable_is_rare ~= nil and v.stackable_is_rare or false)
        new["stackableReappearRate"] = (v.stackable_how_often_reappears ~= nil and v.stackable_how_often_reappears or false)
        
        table.insert(data["perkAssets"], new)
    end

    -- SPELLS/WANDS
    for i, v in ipairs(actions) do
        new = {}
        new["image"] = v.sprite
        new["id"] = v.id
        new["name"] = v.name
        new["spawnProbability"] = v.spawn_probability
        new["spawnLevel"] = v.spawn_level
        new["type"] = v.type
        new["price"] = v.price

        table.insert(data["spellAssets"], new)
    end

    -- FUNGAL
    for i, v in ipairs(materials_from) do
        new = {}
        new["probability"] = v.probability
        new["materials"] = v.materials
        new["name_material"] = (v.name_material ~= nil and v.name_material else v.materials[0])

        table.insert(data["fungalMaterialsFrom"])
    end

    for i, v in ipairs(materials_to) do
        new = {}
        new["probabilty"] = v.probability
        new["material"] = v.material

        table.insert(data["fungalMaterialsTo"])
    end
  

    f = io.open(noitaToolsDir .. "/data.json", "w")
    f:write(json.encode(data))
    f:close()
end
