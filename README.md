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

## Improvements & Ideas

* Store more information about the mesh (PBR materials?)
* Compress triangle list or reference same value vertex floats
* ?? (You can help decide)
