from vtk import *
from math import floor

# Source points
reader = vtkStructuredPointsReader()
reader.SetFileName("Wind.vtk")
reader.Update()

# Look up
colorLookUpTable = vtkLookupTable()
colorLookUpTable.SetHueRange(0.0, 0.0)
colorLookUpTable.SetValueRange(1.0, 1.0)
colorLookUpTable.SetSaturationRange(0.2, 1.0)
colorLookUpTable.SetTableRange(reader.GetOutput().GetScalarRange())


# Source plane
src = vtkPlaneSource()
src.SetXResolution(25)
src.SetYResolution(15)

bounds = reader.GetOutput().GetBounds()
src.SetOrigin(bounds[0], bounds[2], bounds[4])
src.SetPoint1(bounds[1], bounds[2], bounds[4])
src.SetPoint2(bounds[0], bounds[2], bounds[5])


# Stream line is deprecated
streamTracer = vtkStreamTracer()
streamTracer.SetSourceConnection(src.GetOutputPort())
streamTracer.SetInputConnection(reader.GetOutputPort())
streamTracer.SetMaximumPropagation(100)


# Mapper 1
mapperStreamTracer = vtkPolyDataMapper()
mapperStreamTracer.SetLookupTable(colorLookUpTable)
mapperStreamTracer.SetInputConnection(streamTracer.GetOutputPort())
mapperStreamTracer.SetScalarRange(reader.GetOutput().GetScalarRange())

# Actor 1
actorStreamTracer = vtkActor()
actorStreamTracer.SetMapper(mapperStreamTracer)
actorStreamTracer.GetProperty().SetLineWidth(2.0)
actorStreamTracer.GetProperty().SetDiffuse(1.0)
actorStreamTracer.GetProperty().SetSpecular(0)
actorStreamTracer.GetProperty().SetSpecularPower(7)
actorStreamTracer.GetProperty().SetLighting(False)
actorStreamTracer.GetProperty().SetRenderLinesAsTubes(True)
actorStreamTracer.GetProperty().SetOpacity(0.8)
actorStreamTracer.GetProperty().SetShading(False)


# Mapper 2
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

mapperOutline = vtkPolyDataMapper()
mapperOutline.SetInputConnection(outline.GetOutputPort())

#Actor 2
actorOutline = vtkActor()
actorOutline.SetMapper(mapperOutline)
actorOutline.GetProperty().SetColor(1, 1, 1)


#Renderer

renderer = vtkRenderer()

renderer.AddActor(actorStreamTracer)
renderer.AddActor(actorOutline)

renderer.SetBackground(0.1, 0.2, 0.4)
renderer.ResetCameraClippingRange()
renderer.ResetCamera();
renderer.GetActiveCamera().Zoom(1)

#Render Window

renderWin = vtkRenderWindow()
renderWin.SetWindowName("Ejercicio 2 - Corrientes de Aire")
renderWin.SetSize(640, 480)

renderWin.AddRenderer(renderer)

#Interactor

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWin)
interactor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())

#Initialize
interactor.Start()