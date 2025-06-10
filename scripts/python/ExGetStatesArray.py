from load_gmat import *
import numpy as np  
from matplotlib import pyplot as plt


# Spacecraft
earthorb = gmat.Construct("Spacecraft", "EarthOrbiter") # create a spacecraft object named EarthOrbiter

# Set the coordinate system and display state type
earthorb.SetField("CoordinateSystem", "EarthMJ2000Eq")
earthorb.SetField("DisplayStateType", "Keplerian")

earthorb.SetField("X",6650.0) # km
earthorb.SetField("Y",0.0) # km
earthorb.SetField("Z",0.0) # km
earthorb.SetField("VX",0.0) # km/s
earthorb.SetField("VY",7.812754425429622) # km/s
earthorb.SetField("VZ",1.3775993988527033) # km/s


# Construct the ForceModel
fm = gmat.Construct("ForceModel", "FM")
fm.SetField("CentralBody", "Earth")

# Earth gravity model
earthgrav = gmat.Construct("GravityField")
earthgrav.SetField("BodyName","Earth")
earthgrav.SetField("PotentialFile", 'JGM2.cof')
earthgrav.SetField("Degree",70)
earthgrav.SetField("Order",70)

# Only construct the gravity model, no drag or SRP in this example
fm.AddForce(earthgrav)


# using the propagator state manager, you can get the state and derivatives from objects subject to the force model
psm = gmat.PropagationStateManager()
psm.SetObject(earthorb)

psm.BuildState()
fm.SetPropStateManager(psm)
fm.SetState(psm.GetState())

gmat.Initialize()
fm.BuildModelFromMap()
fm.UpdateInitialData()

# calcuate the derivatives 
fm.GetDerivatives(earthorb.GetState().GetState(),0)

# get the state and derivatives
print("Cartesian State Vector: ",psm.GetState().GetState())
print("Cartesian State Derivative Vector: ",fm.GetDerivativeArray())



