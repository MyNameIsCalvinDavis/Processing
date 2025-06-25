
function calculateHorizontalDistance(part1, part2)
	local x1 = part1.Position.X
	local x2 = part2.Position.X
	local z1 = part1.Position.Z
	local z2 = part2.Position.Z
	
	return math.pow(    math.pow((x2 - x1), 2) + math.pow((z2 - z1), 2)   , 0.5)
end

function sigmoid(x)
	return 1 / (1 + math.exp(-x))
end

function inverseSigmoid(x)
	return 60*(1 - (sigmoid(1*x - 8)))
end

function absolute(x)
	return math.abs(x) + 2
end

function negAbsolute(x)
	return -math.abs(x) + 30
end

function step(x)
	if x < 6 then
		return 30
	end
	return 0
end

function Exec()
	script.Parent.ClickDetector:Destroy()
	
	
	local Base = script.Parent
	local c = Base.CFrame
	local blocksize = 2 -- EDIT THIS
	local floor = {}
	
	-- First create a grid of blocks
	for i = 1, 20 do
		for j = 1, 20 do
			local p = Instance.new("Part")
			p.Size = Vector3.new(blocksize, 1, blocksize)
			p.Parent = script.Parent
			p.Anchored = true
			p.CFrame = Base.CFrame
				* CFrame.new(i*blocksize, 0, j*blocksize)
			p.Color = Color3.new(i*123, j*235, j*774)
			
			table.insert(floor, p)
		end
	end
	
	-- Create the rising platform
	for i = 1, 60 do
		Base.CFrame = Base.CFrame
			* CFrame.new(0, 0.5, 0)
		wait()
	end
	
	-- main loop
	-- EDIT THIS
	local p = workspace:FindFirstChild("WATCHAMACOLITE").Head
	while true do
		
		for i = 1, #floor do
			local y = calculateHorizontalDistance(floor[i], p)
			local x = inverseSigmoid(y) -- made with the help of Desmos
			--local x = absolute(y)
			--local x = negAbsolute(y)
			--local x = step(y)
			
			floor[i].Size = Vector3.new(blocksize, 1 + x, blocksize)

		end
		wait()
	end
end


script.Parent.ClickDetector.mouseClick:connect(Exec)
