# STL Face Reconstructor

Experimental Python implementation of ASCII and binary STL parsing with planar face reconstruction for future STEP conversion.

## Overview

This project is an exploration of computational geometry and CAD file processing. The long-term goal is to reconstruct planar faces from STL triangle meshes and eventually export a simplified STEP representation.

Rather than relying on existing CAD libraries, the project aims to implement the core algorithms manually to better understand mesh topology, vector mathematics, and geometric reconstruction.

## Current Features

* ASCII STL parsing
* Detection of triangle facets and vertices
* Basic validation of STL structure
* Internal triangle representation
* Binary STL parsing
* Coplanar face detection
* 
## Planned Features

* Face boundary reconstruction
* STEP export (experimental)
* Optional GUI
* Optional machine-learning based mesh analysis

## Why This Project?

STL files contain only triangle meshes and lose most of the topology information present in CAD models. Reconstructing faces and topology is a challenging geometry problem and provides a useful way to learn:

* Vector mathematics
* Linear algebra
* Graph algorithms
* Computational geometry
* CAD data structures
* Python software architecture

## Project Status

This project is currently in the early development stage. The parser is being expanded to support a wider range of ASCII STL files and binary STL detection.

## License

This project is licensed under the MIT License.
