
function map(x, in_min, in_max, out_min, out_max)
	return out_min + (x - in_min)*(out_max - out_min)/(in_max - in_min)
end

function TorusFun()
	local Base = script.Parent -- The tubemaker block
	local radius = 50
	local sliceamount = 70 -- How many slices in a torus
	local slicedistance = 360 / sliceamount -- multiplied by sliceamount should be equal to 360
	
	for i = 1, sliceamount do -- create a circle of new base parts
		local ubase = Instance.new("Part")
		ubase.Name = "TubePart "..i -- Tubepart1, Tubepart2, ...
		ubase.Size = Vector3.new(1,1,1)
		ubase.Transparency = 1
		ubase.CanCollide = false
		ubase.Anchored = false -- anchored is false, necessary for welds to work (who knew?)
		ubase.Parent = script.Parent
		ubase.CFrame = Base.CFrame
			* CFrame.Angles(0, math.rad(i)*slicedistance, 0)
			* CFrame.new(0, 0, radius)
		
		local weldbase = Instance.new("WeldConstraint")
		weldbase.Parent = Base
		weldbase.Part0 = Base
		weldbase.Part1 = ubase
		
		for j = 1, 10 do
			local newPart = Instance.new("Part")
			newPart.Size = Vector3.new(4.5,0.5,0.5)
			--newPart.BrickColor = BrickColor.White()
			newPart.BrickColor = BrickColor.Black()
			newPart.TopSurface = "Smooth"
			newPart.BottomSurface = "Smooth"
			newPart.Parent = script.Parent:FindFirstChild("TubePart "..i, false)
			newPart.Anchored = false
			newPart.CFrame = ubase.CFrame
				* CFrame.new(0, 15, 0)
				* CFrame.Angles(math.rad(80) - math.rad(j)*15.5, 0, 0)
				* CFrame.new(0, -5, 0)
			
			local weld = Instance.new("WeldConstraint")
			weld.Parent = ubase
			weld.Part0 = ubase
			weld.Part1 = newPart
		end
	end
	
	local Ball = Instance.new("Part") -- A ball
	Ball.Size = Vector3.new(6,6,6)
	Ball.TopSurface = "Smooth"
	Ball.BottomSurface = "Smooth"
	Ball.Shape = "Ball"
	--Ball.Color = Color3.new(0,0,0)
	Ball.BrickColor = BrickColor.White()
	Ball.CFrame = Base.CFrame
		* CFrame.new(0, 20, radius)
	Ball.Parent = script.Parent
	Ball.Anchored = false
	Ball.Velocity = Vector3.new(-50,0,0)
	
	
	
	local c = Base.CFrame
	local counter = 0
	while true do
		-- follows the ball
		--Base.CFrame = CFrame.new(Base.Position, Vector3.new(Ball.Position.X, 0, Ball.Position.Z))
		
		counter = counter + 0.015
		
		Base.CFrame = c
			* CFrame.Angles(
				map(math.cos(counter), -1, 1,    math.rad(355),   math.rad(365)    ), 
				0,   
				map(math.sin(counter), -1, 1,    math.rad(355),   math.rad(365)    )      
				)
		wait(0.01)
	end
end

TorusFun()
--script.Parent.ClickDetector.mouseClick:connect(TorusFun)

