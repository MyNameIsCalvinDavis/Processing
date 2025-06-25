local center = Vector3.new(0, 0, 0)

-- EDIT THESE
local xbx = 1000
local bsize = 4
-- EDIT THESE

local floor = Instance.new("Part")
floor.Parent = script.Parent
floor.TopSurface = "Smooth"
floor.BrickColor = BrickColor.White()
floor.Size = Vector3.new(xbx, 0.2, xbx)
floor.Anchored = true

function lines(x)
	for i = 0, (xbx / bsize) do
		--wait()
		local line = Instance.new("Part")
		line.Anchored = true
		line.Parent = script.Parent
		line.BrickColor = BrickColor.Black()
		line.Size = Vector3.new(0.1, 0.2, xbx)
		if (x == 1) then
			line.CFrame = floor.CFrame
			* CFrame.new(i*bsize - (xbx / 2), 0.03, 0)
		else
			line.CFrame = floor.CFrame
			* CFrame.Angles(0, math.rad(90), 0)
			* CFrame.new(i*bsize - (xbx / 2), 0.03, 0)
		end
	end
end

lines(1)
lines(0)
