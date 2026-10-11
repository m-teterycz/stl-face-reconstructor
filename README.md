# STL Face Reconstructor

Experimental Python implementation of ASCII and binary STL parsing with planar face reconstruction for STEP conversion.

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
* Face outer edge detection
* STEP export (only works for flat faced models)
## Planned Features

* Optional GUI
* Rounding values in actual STL files to prevent co-planar detection from failing

## Why This Project?

STL files contain only triangle meshes and lose most of the topology information present in CAD models. Reconstructing faces and topology is a challenging geometry problem and provides a useful way to learn:

* Vector mathematics
* Linear algebra
* Graph algorithms
* Computational geometry
* CAD data structures
* Python software architecture

## Project Status

This project is currently in the early late development stage. The parser is currently being worked on so that the parsed STL file can be written in STEP format. (Closed to being finished.)
The current supported types of geometry in STEP that can be written are:

* CARTESIAN_POINT
* VERTEX_POINT
* DIRECTION
* VECTOR
* LINE
* EDGE_CURVE
* ORIENTED_EDGE
* EDGE_LOOP
* FACE_OUTER_BOUND
* AXIS2_PLACEMENT_3D
* PLANE
* ADVANCED_FACE
* CLOSED_SHELL
* MANIFOLD_SOLID_BREP
* APPLICATION_CONTEXT
* APPLICATION_PROTOCOL_DEFINITION
* PRODUCT_CONTEXT
* PRODUCT
* PRODUCT_DEFINITION_FORMATION
* PRODUCT_DEFINITION_CONTEXT
* PRODUCT_DEFINITION
* PRODUCT_DEFINITION_SHAPE
* LENGTH_UNIT
* PLANE_ANGLE_UNIT
* SOLID_ANGLE_UNIT
* UNCERTAINTY_MEASURE_WITH_UNIT
* GEOMETRIC_REPRESENTATION_CONTEXT
* ADVANCED_BREP_SHAPE_REPRESENTATION
* SHAPE_DEFINITION_REPRESENTATION

## License

This project is licensed under the MIT License.
