GMAT API supports python 3.6 - 3.12
# Installation

Following the installation in the
```
*/api/API_README.txt
```
folder. 

In short, open the terminal in the GMAT/api folder,
ensure your python is initialized in the correct venv and run
```
$ python BuildApiStartupFile.py
```

Then open the load_gmat.py file in the same folder.
Replace the GmatInstall line with absolute folder of the GMAT install. 
For example on unix systems if the GMAT folder is located in the home directory:

```
GmatInstall = "~/GMAT_R2025a"
```
## Extra Step on Windows

On windows, folder paths cannot use the forward slash character "/". In order for the script to correctly find the API startup file, you must replace all forward slashes with double backward slashes.
For example, my GMAT install is located on a secondary drive (E:\GMAT_R2025a), so I have to change the GmatInstall path to use double backward slashes.

```
GmatInstall = "E:\\GMAT_R2025a"
```

GMAT should then be correctly initialized.

## Usage

The load_gmat.py file will be used to import/initialize GMAT into memory. This file needs to be placed in a location where the current python script can easily import into.
For example, say I have a repo with the current folder structure.

```
. 
├── imports/ 
│   └── load_gmat.py 
└── propagationScript.py
└── shootingMethod.py
```

In the propagationScript.py file, you initialize GMAT by calling importing the load_gmat.py file 
```
from .imports/load_gmat.py import *
```

## Notes

This import helper essentially links your current python environment to the local installation of GMAT. The API is contained in the folder:
```
*/bin/gmatpy/{PYTHONVERSION}
```


# Using the API

The API is constructed using python dynamic linked libraries, this:
 - Increases performance.
 - Obfuscates how functions are defined.

Because of this obfuscation, language servers like Pylance (intellisense) won't give function definitions or autocomplete suggestions. The two main sources of documentation are:
1. The official documentation (PDFs and help commands)
2. Example scripts (official and my custom examples)

## Official Documentation
Official documentation lives in the following files.

```
*/docs/GMAT_API_UsersGuide.pdf
*/docs/GMAT_API_Cookbook.pdf
```


Any Object can call the Help function. For example, get help on possible commands.
```
>>> import gmatpy as gmat
>>> gmat.Help()
>>> gmat.Help("Commands")
```

Or if you have an object loaded into memory, get help with the available fields
From the gmat/api folder:

```
$ python
>>> from load_gmat import *
>>> gmat.LoadScript("../samples/Ex_GEOTransfer.script")
>>> gmat.RunScript()
>>> gmat.GetRuntimeObject("DefaultSC").Help() # list all fields with the spacecraft object -- includes things like current epoch, states, coordinate system, drag coefficents, etc.
>>> gmat.GetRuntimeObject("DefaultProp").Help() # lists the current force model and numerical integrator used for propagation
```

## My Example Scripts

ExBasicEarthProp.py
- Basic Earth propagation with a full 360x360 J2, drag, and SRP showing how to define initial conditions for OE or cartesian, and getting the numerical results in cartesian.
  
ExBasicEarthPropThrust.py
- Basic Earth propagation with the addition of thrust scheduling as shown in the official documentation.
  
ExBasicEarthPropEThrust.py
- Basic Earth propagation with the addition of an electric thruster, demonstrating how to construct an electric power system compared to a chemical thruster.

ExGetStatesArray.py
- Demonstration of how to get the state and derivative vectors of an object subject to an arbitrary force model.

## Useful Tips

### Loading and Saving Scripts
A great feature of the API is being able to run a predefined GMAT script. This is useful to incase you want to config things in a GUI based manner if you are not comfortable constructing a custom script from scratch in the API.
```
>>> import gmatpy as gmat
>>> gmat.LoadScript("../samples/Ex_GEOTransfer.script")
>>> gmat.RunScript()
```

This works both ways. With a fully written Python API script, you can export to a GMAT script, loadable in the GUI.
```
from load_gmat import *
.
. {some arbitrary gmat api code}
.
gmat.SaveScript (“myScript.script”)
```
This saves the GMAT API code in the current folder the python script is run from in a format loadable by the GMAT GUI for future reference. This could be useful if you want to use the visualization tools in the GMAT GUI.

### Annoying Things
 If you have an object defined in your code, but for some reason the program does not seemingly recognize it, reiniaitize gmat.
 - For example, this code will throw an error
```
tank = gmat.Construct("ChemicalTank", "Fuel")
tank.SetField("FuelMass", 200.0)
thruster = gmat.Construct("ChemicalThruster", "Thruster")
thruster.SetField("Tank", "Fuel") 
thruster.SetField("DecrementMass", True)
thruster.SetField("C1",100)
earthorb.SetField("Tanks", "Fuel") 
earthorb.SetField("Thrusters", "Thruster")

burn = gmat.Construct("FiniteBurn", "TheBurn")
burn.SetField("Thrusters", "Thruster")
burn.SetSolarSystem(gmat.GetSolarSystem())
burn.SetSpacecraftToManeuver(earthorb)
```

```
gmatpy._py311.gmat_py.APIException: Burn Exception Thrown: FiniteBurn::Fire requires thruster named "Thruster" on spacecraft EarthOrbiter
```
 - The solution to this is reiniaitizing gmat before constructing and assigning the burn to the spacecraft.
```
tank = gmat.Construct("ChemicalTank", "Fuel")
tank.SetField("FuelMass", 200.0)
thruster = gmat.Construct("ChemicalThruster", "Thruster")
thruster.SetField("Tank", "Fuel") 
thruster.SetField("DecrementMass", True)
thruster.SetField("C1",100)
earthorb.SetField("Tanks", "Fuel") 
earthorb.SetField("Thrusters", "Thruster")

gmat.Initialize()

burn = gmat.Construct("FiniteBurn", "TheBurn")
burn.SetField("Thrusters", "Thruster")
burn.SetSolarSystem(gmat.GetSolarSystem())
burn.SetSpacecraftToManeuver(earthorb)
```
