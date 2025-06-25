
function sanitize(ssize)
	local part = Instance.new("Part")
	part.Anchored = true
	part.Size = ssize
	part.TopSurface = "Smooth"
	part.BottomSurface = "Smooth"
	part.Parent = script.Parent
	return part
end

local Base = sanitize(Vector3.new(1,1,1))
Base.Position = Vector3.new(80, 50, -130)

local c = Base.CFrame

-- EDIT THESE
local boxsize = 50
local limbsize = 5
local num = 10
-- EDIT THESE

local degree = 360 / num
local reference = sanitize(Vector3.new(1,1,1))
reference.Position = Base.Position
local obs = boxsize
Base.Transparency = 1
reference.Transparency = 1
local color = 255 / num
for j = 1, num do -- Creates many boxes
	local var = boxsize / limbsize
	
	for i = 1, 4 do -- Creates one box
		wait()
		local p = sanitize(Vector3.new(var, 2*boxsize + var, var))
		p.CFrame = reference.CFrame
			* CFrame.Angles(0, math.rad(i*90), 0)
			* CFrame.new(boxsize, 0, boxsize) -- Hypotenuse instead?
		wait()
		local p1 = sanitize(Vector3.new(var, var, 2*boxsize + var))
		p1.CFrame = reference.CFrame
			* CFrame.Angles(0, 0, math.rad(i*90) )
			* CFrame.new(boxsize, boxsize, 0) -- Hypotenuse instead?
		wait()
		local p2 = sanitize(Vector3.new(2*boxsize + var, var, var))
		p2.CFrame = reference.CFrame
			* CFrame.Angles(math.rad(i*90), 0, 0)
			* CFrame.new(0, boxsize, boxsize) -- Hypotenuse instead?
		
		p.Color = Color3.fromRGB(255 - j*color, 255 - j*color, 255 - j*color)
		p1.Color = Color3.fromRGB(255 - j*color, 255 - j*color, 255 - j*color)
		p2.Color = Color3.fromRGB(255 - j*color, 255 - j*color, 255 - j*color)
	end
	boxsize = math.sqrt(math.pow(boxsize, 2) + math.pow(boxsize, 2)) / 2
	reference.CFrame = c
		* CFrame.Angles(math.rad(j*degree), 0, 0)
end

Base:Destroy()
reference:Destroy()
