local floor = {}
function sanitize(ssize)
	local part = Instance.new("Part")
	part.Anchored = true
	part.Size = ssize
	part.TopSurface = "Smooth"
	part.BottomSurface = "Smooth"
	--part.Parent = script.Parent
	return part
end

local Base = sanitize(Vector3.new(1,1,1))
Base.CFrame = CFrame.new(120, 0, 160)
	* CFrame.Angles(0, 0, 45)
local c = Base.CFrame

-- EDIT THESE
local bricksize = 3
local brickgap = 0.1
local tendrillength = 250
local size = 40
local deviation = 0.1 -- how fast each tendril goes crazy
-- EDIT THESE

for i=1, size do
	for j=1, size do
		local p = sanitize(Vector3.new(bricksize, bricksize, bricksize))
		p.CFrame = c
			* CFrame.new(j*bricksize + j*brickgap, 0, i*bricksize + i*brickgap)
		table.insert(floor, p)
	end
end

local lastpart = floor[1]
r1 = Random.new()
r2 = Random.new()
r3 = Random.new()
local p
for i=1, #floor + 1 do
	local b = floor[i]
	for j=1, tendrillength do
		local percent = bricksize / tendrillength
		local reduction = bricksize - j*percent 
		p = sanitize(Vector3.new(reduction, reduction, reduction))
		p.CFrame = lastpart.CFrame
			* CFrame.Angles(math.rad(j*deviation*r1:NextNumber(-1, 1)), math.rad(j*deviation*r2:NextNumber(-1, 1)), math.rad(j*deviation*r3:NextNumber(-1, 1)))
			* CFrame.new(0, reduction, 0)
		p.Color = Color3.new(255-(255*(j/255)),255-(255*(j/255)),255-(255*(j/255)))
		p.Parent = script.Parent
		lastpart = p
	end
	lastpart = b
end

for i=1, #floor do floor[i]:Destroy() end

