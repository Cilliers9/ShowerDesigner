# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the ShowerDesigner workbench.

"""
Panel spacing and constraint validation for shower enclosures.

This module provides functions for validating panel spacing, alignment,
and distribution to ensure proper shower enclosure assembly.
"""

import FreeCAD as App
from typing import List, Tuple, Optional


# Spacing constants (all in millimeters)
MIN_PANEL_SPACING = 2  # Minimum gap for seals
MAX_PANEL_SPACING = 10  # Maximum gap for waterproofing
STANDARD_SPACING = 6  # Typical for frameless enclosures
MIN_WALL_CLEARANCE = 5  # Minimum clearance from wall
STANDARD_WALL_CLEARANCE = 10  # Standard clearance from wall


def validateSpacing(panel1, panel2, min_spacing: float = MIN_PANEL_SPACING, 
                    max_spacing: float = MAX_PANEL_SPACING) -> Tuple[bool, str, float]:
    """
    Check if spacing between two panels is within acceptable range.
    
    This function calculates the minimum distance between two panels and
    validates it against spacing requirements for proper sealing and waterproofing.
    
    Args:
        panel1: First glass panel object
        panel2: Second glass panel object
        min_spacing: Minimum acceptable spacing (default: MIN_PANEL_SPACING)
        max_spacing: Maximum acceptable spacing (default: MAX_PANEL_SPACING)
    
    Returns:
        tuple: (is_valid, message, actual_spacing)
            - is_valid: True if spacing is acceptable
            - message: Description of the validation result
            - actual_spacing: Calculated spacing in mm
    
    Example:
        >>> is_valid, msg, spacing = validateSpacing(panel1, panel2)
        >>> if not is_valid:
        >>>     print(f"Invalid spacing: {msg}")
    """
    try:
        # Get panel bounding boxes
        bb1 = panel1.Shape.BoundBox
        bb2 = panel2.Shape.BoundBox
        
        # Calculate minimum distance between bounding boxes
        # Check X axis
        x_gap = 0
        if bb1.XMax < bb2.XMin:
            x_gap = bb2.XMin - bb1.XMax
        elif bb2.XMax < bb1.XMin:
            x_gap = bb1.XMin - bb2.XMax
        
        # Check Y axis
        y_gap = 0
        if bb1.YMax < bb2.YMin:
            y_gap = bb2.YMin - bb1.YMax
        elif bb2.YMax < bb1.YMin:
            y_gap = bb1.YMin - bb2.YMax
        
        # Check Z axis
        z_gap = 0
        if bb1.ZMax < bb2.ZMin:
            z_gap = bb2.ZMin - bb1.ZMax
        elif bb2.ZMax < bb1.ZMin:
            z_gap = bb1.ZMin - bb2.ZMax
        
        # Panels are touching/overlapping in some direction
        if x_gap == 0 and y_gap == 0 and z_gap == 0:
            # Check if panels are actually overlapping
            x_overlap = not (bb1.XMax < bb2.XMin or bb2.XMax < bb1.XMin)
            y_overlap = not (bb1.YMax < bb2.YMin or bb2.YMax < bb1.YMin)
            z_overlap = not (bb1.ZMax < bb2.ZMin or bb2.ZMax < bb1.ZMin)
            
            if x_overlap and y_overlap and z_overlap:
                return False, "Panels are overlapping", 0.0
            
            # Panels are touching - this is the actual gap
            # Find which dimension has the gap
            if x_gap == 0 and (y_overlap and z_overlap):
                spacing = min(abs(bb1.XMax - bb2.XMin), abs(bb2.XMax - bb1.XMin))
            elif y_gap == 0 and (x_overlap and z_overlap):
                spacing = min(abs(bb1.YMax - bb2.YMin), abs(bb2.YMax - bb1.YMin))
            elif z_gap == 0 and (x_overlap and y_overlap):
                spacing = min(abs(bb1.ZMax - bb2.ZMin), abs(bb2.ZMax - bb1.ZMin))
            else:
                spacing = 0.0
        else:
            # Panels are separated - use minimum non-zero gap
            gaps = [g for g in [x_gap, y_gap, z_gap] if g > 0]
            spacing = min(gaps) if gaps else 0.0
        
        # Validate spacing
        if spacing < min_spacing:
            return False, f"Spacing too small: {spacing:.2f}mm (minimum: {min_spacing}mm)", spacing
        elif spacing > max_spacing:
            return False, f"Spacing too large: {spacing:.2f}mm (maximum: {max_spacing}mm)", spacing
        else:
            return True, f"Spacing acceptable: {spacing:.2f}mm", spacing
            
    except Exception as e:
        return False, f"Error calculating spacing: {str(e)}", 0.0


def checkPanelCollision(panel1, panel2, tolerance: float = 0.1) -> Tuple[bool, str]:
    """
    Check if two panels are colliding (overlapping).
    
    Args:
        panel1: First glass panel object
        panel2: Second glass panel object
        tolerance: Overlap tolerance in mm (default: 0.1mm)
    
    Returns:
        tuple: (is_colliding, message)
            - is_colliding: True if panels overlap
            - message: Description of collision status
    
    Example:
        >>> is_colliding, msg = checkPanelCollision(panel1, panel2)
        >>> if is_colliding:
        >>>     print("Warning: Panels are overlapping!")
    """
    try:
        bb1 = panel1.Shape.BoundBox
        bb2 = panel2.Shape.BoundBox
        
        # Check for overlap in all three dimensions
        x_overlap = not (bb1.XMax + tolerance < bb2.XMin or bb2.XMax + tolerance < bb1.XMin)
        y_overlap = not (bb1.YMax + tolerance < bb2.YMin or bb2.YMax + tolerance < bb1.YMin)
        z_overlap = not (bb1.ZMax + tolerance < bb2.ZMin or bb2.ZMax + tolerance < bb1.ZMin)
        
        is_colliding = x_overlap and y_overlap and z_overlap
        
        if is_colliding:
            return True, f"Panels '{panel1.Label}' and '{panel2.Label}' are overlapping"
        else:
            return False, "No collision detected"
            
    except Exception as e:
        return False, f"Error checking collision: {str(e)}"


def autoAlign(panels: List, alignment_type: str, reference_panel = None) -> bool:
    """
    Align multiple panels along a specified edge or center.
    
    Args:
        panels: List of glass panel objects to align
        alignment_type: Type of alignment:
            - 'top': Align top edges
            - 'bottom': Align bottom edges  
            - 'center_vertical': Align vertical centers
            - 'left': Align left edges
            - 'right': Align right edges
            - 'center_horizontal': Align horizontal centers
        reference_panel: Panel to align to (uses first panel if None)
    
    Returns:
        bool: True if alignment was successful
    
    Example:
        >>> panels = [panel1, panel2, panel3]
        >>> autoAlign(panels, 'top')  # Align all panels to same top height
    """
    if not panels:
        App.Console.PrintWarning("No panels provided for alignment\n")
        return False
    
    if len(panels) < 2:
        App.Console.PrintWarning("Need at least 2 panels for alignment\n")
        return False
    
    try:
        # Use first panel as reference if none specified
        ref_panel = reference_panel if reference_panel else panels[0]
        ref_bb = ref_panel.Shape.BoundBox
        
        for panel in panels:
            if panel == ref_panel:
                continue
            
            bb = panel.Shape.BoundBox
            current_pos = panel.Position
            
            # Calculate new position based on alignment type
            if alignment_type == 'top':
                # Align top edges (Z max)
                new_z = ref_bb.ZMax - (bb.ZMax - bb.ZMin)
                panel.Position = App.Vector(current_pos.x, current_pos.y, new_z)
                
            elif alignment_type == 'bottom':
                # Align bottom edges (Z min)
                panel.Position = App.Vector(current_pos.x, current_pos.y, ref_bb.ZMin)
                
            elif alignment_type == 'center_vertical':
                # Align vertical centers
                ref_center_z = (ref_bb.ZMax + ref_bb.ZMin) / 2
                panel_height = bb.ZMax - bb.ZMin
                new_z = ref_center_z - (panel_height / 2)
                panel.Position = App.Vector(current_pos.x, current_pos.y, new_z)
                
            elif alignment_type == 'left':
                # Align left edges (X min)
                panel.Position = App.Vector(ref_bb.XMin, current_pos.y, current_pos.z)
                
            elif alignment_type == 'right':
                # Align right edges (X max)
                panel_width = bb.XMax - bb.XMin
                new_x = ref_bb.XMax - panel_width
                panel.Position = App.Vector(new_x, current_pos.y, current_pos.z)
                
            elif alignment_type == 'center_horizontal':
                # Align horizontal centers
                ref_center_x = (ref_bb.XMax + ref_bb.XMin) / 2
                panel_width = bb.XMax - bb.XMin
                new_x = ref_center_x - (panel_width / 2)
                panel.Position = App.Vector(new_x, current_pos.y, current_pos.z)
                
            else:
                App.Console.PrintWarning(f"Unknown alignment type: {alignment_type}\n")
                return False
        
        # Recompute to update geometry
        if panels[0].Document:
            panels[0].Document.recompute()
        
        App.Console.PrintMessage(f"Aligned {len(panels)} panels using '{alignment_type}'\n")
        return True
        
    except Exception as e:
        App.Console.PrintError(f"Error during alignment: {str(e)}\n")
        return False


def distributeEvenly(panels: List, total_width: float, axis: str = 'X', 
                     start_position: float = 0.0) -> bool:
    """
    Distribute panels evenly across a specified width.
    
    This function calculates equal spacing between panels and positions them
    accordingly. Useful for creating uniform panel layouts.
    
    Args:
        panels: List of glass panel objects to distribute
        total_width: Total width to distribute panels across (in mm)
        axis: Axis along which to distribute ('X' or 'Y')
        start_position: Starting position on the axis (default: 0.0)
    
    Returns:
        bool: True if distribution was successful
    
    Example:
        >>> panels = [panel1, panel2, panel3]
        >>> distributeEvenly(panels, 3000, axis='X')  # Distribute across 3000mm
    """
    if not panels:
        App.Console.PrintWarning("No panels provided for distribution\n")
        return False
    
    if len(panels) < 2:
        App.Console.PrintWarning("Need at least 2 panels for distribution\n")
        return False
    
    try:
        # Calculate total panel width
        total_panel_width = 0
        panel_widths = []
        
        for panel in panels:
            bb = panel.Shape.BoundBox
            if axis == 'X':
                width = bb.XMax - bb.XMin
            elif axis == 'Y':
                width = bb.YMax - bb.YMin
            else:
                App.Console.PrintError(f"Invalid axis: {axis}. Use 'X' or 'Y'\n")
                return False
            
            panel_widths.append(width)
            total_panel_width += width
        
        # Calculate spacing between panels
        available_space = total_width - total_panel_width
        
        if available_space < 0:
            App.Console.PrintError(
                f"Panels too wide for total width. "
                f"Total panel width: {total_panel_width:.2f}mm, "
                f"Available: {total_width:.2f}mm\n"
            )
            return False
        
        # Spacing between panels (n panels = n-1 gaps)
        num_gaps = len(panels) - 1
        spacing = available_space / num_gaps if num_gaps > 0 else 0
        
        # Check if spacing is within acceptable range
        if spacing < MIN_PANEL_SPACING:
            App.Console.PrintWarning(
                f"Calculated spacing ({spacing:.2f}mm) is less than minimum ({MIN_PANEL_SPACING}mm)\n"
            )
        elif spacing > MAX_PANEL_SPACING:
            App.Console.PrintWarning(
                f"Calculated spacing ({spacing:.2f}mm) exceeds maximum ({MAX_PANEL_SPACING}mm)\n"
            )
        
        # Position panels
        current_position = start_position
        
        for i, panel in enumerate(panels):
            current_pos = panel.Position
            
            if axis == 'X':
                panel.Position = App.Vector(current_position, current_pos.y, current_pos.z)
                current_position += panel_widths[i] + spacing
            elif axis == 'Y':
                panel.Position = App.Vector(current_pos.x, current_position, current_pos.z)
                current_position += panel_widths[i] + spacing
        
        # Recompute to update geometry
        if panels[0].Document:
            panels[0].Document.recompute()
        
        App.Console.PrintMessage(
            f"Distributed {len(panels)} panels across {total_width}mm "
            f"with {spacing:.2f}mm spacing\n"
        )
        return True
        
    except Exception as e:
        App.Console.PrintError(f"Error during distribution: {str(e)}\n")
        return False


def getPanelGap(panel1, panel2, axis: str = 'X') -> Optional[float]:
    """
    Calculate the gap between two panels along a specific axis.
    
    Args:
        panel1: First glass panel object
        panel2: Second glass panel object
        axis: Axis to measure gap along ('X', 'Y', or 'Z')
    
    Returns:
        float: Gap distance in mm, or None if panels overlap
    
    Example:
        >>> gap = getPanelGap(panel1, panel2, axis='X')
        >>> print(f"Gap between panels: {gap}mm")
    """
    try:
        bb1 = panel1.Shape.BoundBox
        bb2 = panel2.Shape.BoundBox
        
        if axis == 'X':
            if bb1.XMax < bb2.XMin:
                return bb2.XMin - bb1.XMax
            elif bb2.XMax < bb1.XMin:
                return bb1.XMin - bb2.XMax
            else:
                return None  # Overlapping
                
        elif axis == 'Y':
            if bb1.YMax < bb2.YMin:
                return bb2.YMin - bb1.YMax
            elif bb2.YMax < bb1.YMin:
                return bb1.YMin - bb2.YMax
            else:
                return None  # Overlapping
                
        elif axis == 'Z':
            if bb1.ZMax < bb2.ZMin:
                return bb2.ZMin - bb1.ZMax
            elif bb2.ZMax < bb1.ZMin:
                return bb1.ZMin - bb2.ZMax
            else:
                return None  # Overlapping
        else:
            App.Console.PrintError(f"Invalid axis: {axis}. Use 'X', 'Y', or 'Z'\n")
            return None
            
    except Exception as e:
        App.Console.PrintError(f"Error calculating gap: {str(e)}\n")
        return None


def snapToGrid(panel, grid_size: float = 50.0) -> bool:
    """
    Snap a panel's position to a grid for easier alignment.
    
    Args:
        panel: Glass panel object to snap
        grid_size: Grid spacing in mm (default: 50mm)
    
    Returns:
        bool: True if snap was successful
    
    Example:
        >>> snapToGrid(panel, grid_size=100)  # Snap to 100mm grid
    """
    try:
        current_pos = panel.Position
        
        # Snap each coordinate to nearest grid point
        snapped_x = round(current_pos.x / grid_size) * grid_size
        snapped_y = round(current_pos.y / grid_size) * grid_size
        snapped_z = round(current_pos.z / grid_size) * grid_size
        
        panel.Position = App.Vector(snapped_x, snapped_y, snapped_z)
        
        if panel.Document:
            panel.Document.recompute()
        
        App.Console.PrintMessage(
            f"Snapped panel '{panel.Label}' to grid "
            f"({snapped_x}, {snapped_y}, {snapped_z})\n"
        )
        return True
        
    except Exception as e:
        App.Console.PrintError(f"Error snapping to grid: {str(e)}\n")
        return False
