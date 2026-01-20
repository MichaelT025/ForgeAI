# ForgeAI API Reference

## Tools

### Document Operations
| Tool | Description |
|------|-------------|
| create_new_part | Create a new blank part document |
| save_part | Save current document to specified path |

#### create_new_part
Creates a new blank part document.

**Parameters:**
- `template_path` (optional, string): Template path, or None for default

**Returns:** Success message with document info + screenshot

#### save_part
Saves the current part document to the specified file path.

**Parameters:**
- `file_path` (required, string): Full file path (e.g., "C:\\Users\\...\\MyPart.SLDPRT")

**Returns:** Success message with saved path

### Sketch Operations (all dimensions in mm)
| Tool | Description |
|------|-------------|
| create_sketch | Start a new sketch on a plane (Front/Top/Right) |
| close_sketch | Exit sketch mode |
| draw_rectangle | Draw a center rectangle |
| draw_circle | Draw a circle |
| draw_line | Draw a line between two points |
| draw_arc | Draw a three-point arc |
| draw_polygon | Draw a regular polygon |
| draw_spline | Draw a spline through specified points |

#### create_sketch
**Parameters:**
- `plane` (required, string): The plane to sketch on ("Front Plane", "Top Plane", "Right Plane")

**Returns:** Success message + screenshot

#### close_sketch
Exits sketch mode.

**Parameters:**
- None

**Returns:** Success message + screenshot

#### draw_rectangle
**Parameters:**
- `x` (optional, number): Center X in mm (default: 0)
- `y` (optional, number): Center Y in mm (default: 0)
- `width` (required, number): Width in mm
- `height` (required, number): Height in mm

**Returns:** Success message + screenshot

#### draw_circle
**Parameters:**
- `x` (optional, number): Center X in mm (default: 0)
- `y` (optional, number): Center Y in mm (default: 0)
- `radius` (required, number): Radius in mm

**Returns:** Success message + screenshot

#### draw_line
**Parameters:**
- `x1` (required, number): Start X in mm
- `y1` (required, number): Start Y in mm
- `x2` (required, number): End X in mm
- `y2` (required, number): End Y in mm

**Returns:** Success message + screenshot

#### draw_arc
**Parameters:**
- `center_x` (required, number): Center X in mm
- `center_y` (required, number): Center Y in mm
- `start_x` (required, number): Start X in mm
- `start_y` (required, number): Start Y in mm
- `end_x` (required, number): End X in mm
- `end_y` (required, number): End Y in mm

**Returns:** Success message + screenshot

#### draw_polygon
**Parameters:**
- `x` (optional, number): Center X in mm (default: 0)
- `y` (optional, number): Center Y in mm (default: 0)
- `radius` (required, number): Radius in mm
- `sides` (required, integer): Number of sides

**Returns:** Success message + screenshot

#### draw_spline
**Parameters:**
- `points` (required, list of objects): List of {x, y} coordinates in mm

**Returns:** Success message + screenshot

### Feature Operations
| Tool | Description |
|------|-------------|
| extrude | Extrude sketch (boss or cut) |
| fillet | Apply fillet to edges |
| chamfer | Apply chamfer to edges |

#### extrude
**Parameters:**
- `depth` (required, number): Depth in mm
- `operation` (optional, string): "boss" or "cut" (default: "boss")
- `direction` (optional, string): "forward", "backward", "both" (default: "forward")

**Returns:** Success message + screenshot

#### fillet
V1 applies to all edges.

**Parameters:**
- `radius` (required, number): Radius in mm

**Returns:** Success message + screenshot

#### chamfer
V1 applies to all edges.

**Parameters:**
- `distance` (required, number): Distance in mm

**Returns:** Success message + screenshot

## Resources

### model_state
URI: `solidworks://model/state`
Returns JSON with: document info, features list, sketches list, active sketch

### screenshot
URI: `solidworks://viewport/screenshot`
Returns: PNG image of current viewport

## Unit Convention
- All tool inputs accept millimeters
- Conversion to meters (SolidWorks internal) happens automatically
