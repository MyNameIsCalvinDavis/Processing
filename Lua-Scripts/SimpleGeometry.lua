
local Base = script.Parent
local lastpart = Base
local ref = Base.CFrame
	* CFrame.new(0, 10, 0)

for i = 1, 100 do
	local basepart = Instance.new("Part")
	basepart.Parent = script.Parent
	basepart.Size = Vector3.new(1, 1, 1)
	basepart.Anchored = true
	basepart.Transparency = 1
	
	basepart.CFrame = lastpart.CFrame
		* CFrame.Angles(0, math.rad(10), 0)
		* CFrame.new(0, 1.2, 1)
	for j = 1, 50 do
		local ref = basepart.CFrame
			* CFrame.new(0, 10, 0)
		local p = Instance.new("Part")
		p.Parent = script.Parent
		p.Size = Vector3.new(0.2, 6, 0.2)
		p.Anchored = true
		p.CFrame = ref
			* CFrame.Angles(0, 0, j*math.rad(10))
			* CFrame.new(0, 10, 0)
		lastpart = p
	end
	
	lastpart = basepart
	
end
