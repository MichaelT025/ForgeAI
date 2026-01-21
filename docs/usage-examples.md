# Usage Examples

This guide shows how to use ForgeAI through Claude Desktop to create SolidWorks parts using natural language.

## Prerequisites
- ForgeAI server configured in Claude Desktop (see [Getting Started](./getting-started.md))
- SolidWorks running or set to auto-launch

## Basic Workflow

### 1. Creating a Simple Box

This example demonstrates the core workflow of creating a part, adding a sketch, extruding it, and applying fillets.

**User**: Create a new part and make a 100x50mm rectangle on the front plane

**Claude**: I'll create a new part and draw the rectangle.
- `create_new_part()`
- `create_sketch(plane="Front Plane")`
- `draw_rectangle(center_x=0, center_y=0, width=100, height=50)`
- `close_sketch()`

✓ Created new part document
✓ Created sketch on Front Plane
✓ Drew 100x50mm rectangle centered at origin
[Screenshot showing the rectangle]

**User**: Extrude it 25mm

**Claude**: I'll extrude the sketch to a depth of 25mm.
- `extrude(depth=25, operation="boss")`

✓ Extruded sketch 25mm
[Screenshot showing the 3D box]

**User**: Add 5mm fillets to all edges

**Claude**: I'll apply the fillets to the edges of the box.
- `fillet(radius=5)`

✓ Applied 5mm fillets to 12 edges
[Screenshot showing filleted box]

**User**: Save it as MyPart.SLDPRT

**Claude**: I'll save the part to your specified path.
- `save_part(file_path="C:\Users\...\MyPart.SLDPRT")`

✓ Saved as MyPart.SLDPRT

### 2. Working with Sketches

You can create complex geometry by combining different sketch entities on various planes.

**Examples of sketch commands:**

- **Circles**: "Draw a 20mm radius circle at the origin"
  - `draw_circle(center_x=0, center_y=0, radius=20)`
- **Lines**: "Draw a line from 0,0 to 50,50"
  - `draw_line(x1=0, y1=0, x2=50, y2=50)`
- **Polygons**: "Create a 6-sided polygon with a 30mm radius"
  - `draw_polygon(center_x=0, center_y=0, radius=30, sides=6)`

Always ensure you have an active sketch on a plane before drawing these entities.

### 3. Demo Scenario: Filleted Box

This is the standard 5-step demonstration for ForgeAI V1.

1. **Create new part**: Start a fresh SolidWorks part document.
2. **Rectangle sketch 100x50mm**: Create a sketch on the Front Plane and draw the base rectangle.
3. **Extrude 25mm**: Turn the 2D sketch into a 3D block.
4. **Add 5mm fillets**: Smooth all 12 edges of the block.
5. **Save as demo.SLDPRT**: Save the final result.

## Tips
- All dimensions should be in millimeters (mm). ForgeAI handles internal unit conversion automatically.
- Always create a part document before attempting any sketch or feature operations.
- Close sketches before applying features like extrude or cut.
- Screenshots are returned after each modifying operation for visual confirmation. If a screenshot doesn't appear, you can request one by asking "Show me the current model".
