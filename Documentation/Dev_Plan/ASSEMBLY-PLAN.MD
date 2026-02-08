# PLAN TO REFACTOR WORKBENCH TO USE PART ASSEMBLIES

Current problem is that glass panel and hardware all makes up one part that uses that same view provider and there for can not be displayed with different properties.

# Proposed change
- Glass panel and hardware(ie clamps, hinges, handles, support bars, tracks and channel) must be individual objects with there own view provider.
- Hardware can share a view provider as they all should have the same finish and material.
- Fixed panels and doors must be assemblies of a glass panel and hardware.
- Enclosures must be assemblies of Fixed panel/s and Door/s.
- Each Fixed panel and door must contain a VarSet that is used control its variables (ie dimensions, type of hardware, hardware location, type of glass)
- Models can be grouped in too folder Hardware, Glass, Enclosures.
- Things to consider ease implementing new hardware.