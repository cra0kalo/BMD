# (BMD) Binary Model Data - File Format

![BMD Logo](https://github.com/cra0kalo/BMD/blob/main/docs/images/logo.png?raw=true)

The BMD file format is a byproduct I created in 2013 to help me manage 3d mesh data extracted from various sources. It's derived from Valve Software's SMD (StudioMDL Data) file format. The idea was to have a bare bones very simple binary file format to store mesh data that had the ability to contain skinning information and bone data.

## Features

* Simple straight forward file format which contains the basic core components like an primitive list
* Can contain multiple meshes
* Ability to store an amature (skeleton rig)
* Deformation/Skinning information (how the bones deform change the mesh)
* Material list (Information on how the mesh is textured)
* Ability to store meta data

## Whats included?

### Noesis Plugin
**plugins\Noesis\fmt_BinaryModelData_bmd.py**
Is a plugin for a popular model viewer called [Noesis](https://richwhitehouse.com/index.php?content=inc_projects.php&showproject=91).

### 010Editor Template
**plugins\010Editor\BMD_Format.bt**
Used by my favrioute hex editor [010Editor](https://www.sweetscape.com/010editor) to help visualize the file format.

### 3DSMax Plugin
**plugins\3DSMax\2012\BMDImport.dli**
Dated 3DSMax 2012 plugin for importing/exporting the file format.

### BMDConvert

Located at: **tools\bmdconvert.exe** is a tool you can use to test convert some files to the BMD file format.
```
Usage: bmdconvert -f [FormatType] -x [UpAxis] --src path/to/source path/to/out
Format Types: OBJ,SMD
Axis: Y or Z
Example: bmdconvert -f OBJ -x Z --src O:/geom/Teapot.obj O:/geom/cTeapot.bmd
```


## Improvements & Ideas

* Store more information about the mesh (PBR materials?)
* Compress triangle list or reference same value vertex floats
* ?? (You can help decide)

## Examples

![Screenshot](https://github.com/cra0kalo/BMD/blob/main/docs/images/screenshot1.png?raw=true)
