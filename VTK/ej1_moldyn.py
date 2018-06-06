from vtk import *
import numpy as np

# Source

points = vtkPoints()
radius = vtkFloatArray()
lines = vtkCellArray()

with open("atoms-coordinates.txt") as f:
	for line in f:
		if line.strip().startswith("#"):
			continue
		row = line.split()
		points.InsertNextPoint(float(row[0]), float(row[1]), float(row[2]))

with open("atoms-radius.txt") as f:
	for line in f:
		if line.strip().startswith("#"):
			continue
		row = line.split()
		radius.InsertNextValue(float(row[0]))

with open("atoms-connections.txt") as f:
	for lineStr in f:
		if lineStr.strip().startswith("#"):
			continue
		row = lineStr.split()
		line = vtkLine()
		line.GetPointIds().SetId(0, int(row[0]))
		line.GetPointIds().SetId(1, int(row[1]))
		lines.InsertNextCell(line)
		
linesPolyData = vtkPolyData()
linesPolyData.SetPoints(points)
linesPolyData.SetLines(lines)
linesPolyData.GetPointData().SetScalars(radius)

sphere = vtk.vtkSphereSource()
sphere.SetRadius(1)

glyph = vtkGlyph3D()
glyph.SetInputData(linesPolyData)
glyph.SetSourceConnection(0, sphere.GetOutputPort())
glyph.SetScaleFactor(0.5)

colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.SetColorSpaceToRGB()
colorTransferFunction.AddRGBPoint(0.37,1,1,1)
colorTransferFunction.AddRGBPoint(0.68,1,0,0)
colorTransferFunction.AddRGBPoint(0.739,1,0,0)
colorTransferFunction.AddRGBPoint(0.74,0,0,1)
colorTransferFunction.AddRGBPoint(0.77,0,0,1)
colorTransferFunction.AddRGBPoint(2,0,1,0)
colorTransferFunction.SetScaleToLinear()
		
#Mapper 1

mapperAtoms = vtkPolyDataMapper()
mapperAtoms.SetInputConnection(glyph.GetOutputPort())
mapperAtoms.SetColorModeToMapScalars()
mapperAtoms.SetLookupTable(colorTransferFunction)


#Actor 1

actorAtoms = vtkActor()
actorAtoms.SetMapper(mapperAtoms)
actorAtoms.GetProperty().SetDiffuse(1)


#Mapper 2

tubeFilter = vtk.vtkTubeFilter()
tubeFilter.SetInputData(linesPolyData)
tubeFilter.SetNumberOfSides(5);
tubeFilter.SetVaryRadiusToVaryRadiusOff()
tubeFilter.SetRadius(0.1)

colorTransferFunctionTube = vtk.vtkColorTransferFunction()
colorTransferFunctionTube.SetColorSpaceToRGB()
colorTransferFunctionTube.AddRGBPoint(0,1,1,1)
colorTransferFunctionTube.AddRGBPoint(2000,1,1,1)
colorTransferFunctionTube.SetScaleToLinear()

tubeMapper = vtk.vtkPolyDataMapper()
tubeMapper.SetInputConnection(tubeFilter.GetOutputPort())
tubeMapper.SetLookupTable(colorTransferFunctionTube)

#Actor 2

actorTube = vtk.vtkActor()
actorTube.SetMapper(tubeMapper)
actorTube.VisibilityOn()


#Mapper 3

outline = vtk.vtkOutlineFilter()
outline.SetInputData(linesPolyData)

mapperOutline = vtk.vtkPolyDataMapper()
mapperOutline.SetInputConnection(outline.GetOutputPort())

#Actor 3
actorOutline = vtk.vtkActor()
actorOutline.GetProperty().SetColor(0, 0, 0)
actorOutline.SetMapper(mapperOutline)


#Renderer

renderer = vtkRenderer()
renderer.AddActor(actorAtoms)
renderer.AddActor(actorTube)
renderer.AddActor(actorOutline)
renderer.SetBackground(0.4,0.4,0.4)
renderer.ResetCameraClippingRange()
renderer.ResetCamera();
renderer.GetActiveCamera().Zoom(1)
#zoom


#Render Window

renderWin = vtkRenderWindow()
renderWin.SetWindowName("Ejercicio 0")
renderWin.SetSize(640, 480)

renderWin.AddRenderer(renderer)

#random.uniform(1.5, 1.9)

#Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWin)
interactor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
#interactor.AddObserver("LeftButtonPressEvent", OnLeftClick)

#Initialize
interactor.Start()


