


local points = {}

-- EDIT THESE
local offset = Vector3.new(-180, 10, -40) -- X Y Z position of the net
local size = 180
local holespace = 2
local yMult = 8
local zoom = 15
-- EDIT THESE

for i = offset.X, offset.X + size, holespace do
	local row = {}
	for j = offset.Z, offset.Z + size, holespace do
		table.insert(row, 
			Vector3.new(i, offset.Y + yMult * math.noise(i / zoom, offset.Y / zoom, j / zoom), j)
		)
	end
	table.insert(points, row)
end

function createLine(p1, p2)
	local p = Instance.new("Part")
	local dist = (		(p1.X - p2.X)^2 + (p1.Y - p2.Y)^2 + (p1.Z - p2.Z)^2		)^0.5
	p.Position = Vector3.new(
		(p1.X + p2.X) / 2,
		(p1.Y + p2.Y) / 2,
		(p1.Z + p2.Z) / 2
	)
	p.CFrame = CFrame.new(p.Position, p2)
	p.Size = Vector3.new(0.2, 0.2, dist)
	p.TopSurface = "Smooth"
	p.BottomSurface = "Smooth"
	p.Anchored = true
	p.Parent = script.Parent
end

function makeNet(arg)
	if (arg == true) then -- square pattern
		for i = 1, #points - 1 do
			for j = 1, #points[i] - 1 do
				createLine(points[i][j], points[i+1][j])
				createLine(points[i][j], points[i][j+1])
				
			end
			wait()
		end
	end
end

makeNet(true)
