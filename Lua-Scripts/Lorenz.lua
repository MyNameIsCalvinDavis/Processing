
function map(x, in_min, in_max, out_min, out_max)
	return out_min + (x - in_min)*(out_max - out_min)/(in_max - in_min)
end

function plop(pos)
	local p = Instance.new("Part")
	p.Size = Vector3.new(2, 2, 2)
	p.Shape = "Ball"
	p.Color = Color3.fromRGB(
		map(pos.X, 0, 51, 1, 250),
		map(pos.Y, 9, 51, 1, 250),
		255
		)
	p.Anchored = true
	p.Position = pos
	p.CanCollide = false
	p.Parent = script.Parent
end

local Base = Instance.new("Part")
Base.Position = Vector3.new(0, 30, 30)
Base.Transparency = 1
Base.Anchored = true
Base.Parent = script.Parent
Base.CFrame = Base.CFrame
	* CFrame.Angles(0, 0, math.rad(-45))

local x = 0.01
local y = 0
local z = 0

local a = 10
local b = 28
local c = 8.0/3.0

local dt = 0.022

local scale = 0.6

local Ball = Instance.new("Part")
Ball.Shape = "Ball"
Ball.BrickColor = BrickColor.Black()
Ball.Size = Vector3.new(4,4,4)
Ball.Anchored = true
Ball.Parent = script.Parent
Ball.CanCollide = false
Ball.CFrame = Base.CFrame

local att0 = Instance.new("Attachment")
att0.Position = Vector3.new(0.4, 0.4, 0.4)
att0.Parent = Ball

local att1 = Instance.new("Attachment")
att1.Position = Vector3.new(-0.4, -0.4, -0.4)
att1.Parent = Ball

local trail = Instance.new("Trail")
trail.Parent = Ball
trail.Attachment0 = att0
trail.Attachment1 = att1
local color1 = Color3.new(15/255, 127/255, 254/255)
local color2 = Color3.new(0,0,0)
trail.Color = ColorSequence.new(color1, color2)
trail.Lifetime = 100
trail.Transparency = NumberSequence.new(0)

local trigger = 0
while true do
	trigger = trigger + 1
	local dx = (a * (y - x)) 		* dt
	local dy = (x * (b - z) - y) 	* dt
	local dz = (x * y - c * z)		* dt
	
	x = x + dx
	y = y + dy
	z = z + dz
	
	--print(string.format("%-.02f %-.02f %-.02f", y, y, y))
	--print(string.format("%05.2f %05.2f %05.2f", x, y, z))
	--[[
	if (trigger >= 2) then
		plop(Ball.Position)
		trigger = 0
	end
	]]

	Ball.CFrame = Base.CFrame
		* CFrame.new(x*scale, y*scale, z*scale)
	wait(0.001)
	
end
