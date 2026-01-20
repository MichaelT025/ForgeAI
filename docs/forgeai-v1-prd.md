# ForgeAI V1 - Product Requirements Document

## Executive Summary

ForgeAI is an MCP (Model Context Protocol) server that enables natural language CAD modeling in SolidWorks through Claude Desktop. Users describe what they want to build in plain English, and ForgeAI translates those requests into SolidWorks operations.

**V1 Goal**: Deliver a functional MCP server that connects to Claude Desktop and enables core part modeling operations.

---

## Problem Statement

### Current State
- SolidWorks requires extensive training to use effectively
- Users must navigate complex menus and remember specific commands
- Rapid prototyping of simple parts is slower than it should be
- No natural language interface exists for SolidWorks

### Desired State
- Users describe parts in natural language: "Create a 100x50x25mm box with 5mm fillets"
- AI handles the translation to CAD operations
- Visual feedback confirms each step
- Iteration is conversational, not menu-driven

---

## Target Users

**Primary**: Engineers and designers who:
- Know what they want to build but find SolidWorks UI cumbersome
- Want to rapidly prototype simple-to-moderate complexity parts
- Are comfortable with conversational AI interfaces

**Secondary**: 
- Makers/hobbyists learning CAD
- Professionals wanting to speed up repetitive modeling tasks

---

## V1 Scope

### In Scope

#### Document Operations
| Operation | Description |
|-----------|-------------|
| `create_new_part` | Create a new blank part document |
| `save_part` | Save current document to specified path |

#### Sketch Operations
| Operation | Description |
|-----------|-------------|
| `create_sketch` | Start a new sketch on a plane (Front/Top/Right) |
| `close_sketch` | Exit sketch mode |
| `draw_rectangle` | Draw a center rectangle (x, y, width, height in mm) |
| `draw_circle` | Draw a circle (center x, y, radius in mm) |
| `draw_line` | Draw a line between two points |
| `draw_arc` | Draw a three-point arc |
| `draw_polygon` | Draw a regular polygon (center, radius, sides) |
| `draw_spline` | Draw a spline through specified points |

#### Feature Operations
| Operation | Description |
|-----------|-------------|
| `extrude` | Extrude sketch (boss or cut, with depth in mm) |
| `fillet` | Apply fillet to edges (radius in mm) |
| `chamfer` | Apply chamfer to edges (distance in mm) |

#### Resources (Read-Only)
| Resource | Description |
|----------|-------------|
| `model_state` | Current features, sketches, active sketch info |
| `screenshot` | Current viewport as PNG image |

### Out of Scope (V1)
- Assembly operations (multiple parts)
- Drawing/drafting operations
- Open/Close file operations (only new + save)
- Custom chat UI (Claude Desktop only)
- Multi-user or cloud features
- Advanced features (revolve, sweep, loft, patterns, holes)

---

## Technical Architecture

```
┌─────────────────┐     stdio      ┌─────────────────┐     COM API     ┌─────────────────┐
│  Claude Desktop │◄──────────────►│  ForgeAI MCP    │◄───────────────►│   SolidWorks    │
│   (AI Client)   │                │    Server       │                 │                 │
└─────────────────┘                └─────────────────┘                 └─────────────────┘
                                          │
                                          ▼
                                   ┌─────────────────┐
                                   │   Screenshots   │
                                   │   (feedback)    │
                                   └─────────────────┘
```

### Technology Stack
| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| MCP Framework | `mcp` (FastMCP) |
| COM Automation | `pywin32` |
| Data Validation | `pydantic` |
| Logging | `loguru` |
| Testing | `pytest`, `pytest-asyncio` |

### Key Design Decisions

1. **Unit Handling**: All tool inputs accept millimeters. Conversion to meters (SolidWorks internal) happens in the operations layer.

2. **Screenshot Feedback**: Every modifying operation returns a text result + screenshot for visual confirmation.

3. **Lifespan Management**: The SolidWorks COM connection is established once at server startup and reused for all operations.

4. **Error Strategy**: Descriptive error messages returned to Claude, which decides recovery approach.

---

## User Experience

### Example Conversation

```
User: Create a new part and make a 100x50mm rectangle on the front plane

Claude: I'll create a new part and draw the rectangle.
        [Calls create_new_part]
        [Calls create_sketch plane="Front Plane"]
        [Calls draw_rectangle x=0 y=0 width=100 height=50]
        [Calls close_sketch]
        
        ✓ Created new part document
        ✓ Created sketch on Front Plane
        ✓ Drew 100x50mm rectangle centered at origin
        [Screenshot showing the rectangle]

User: Extrude it 25mm

Claude: [Calls extrude depth=25 operation="boss"]
        
        ✓ Extruded sketch 25mm
        [Screenshot showing the 3D box]

User: Add 5mm fillets to all edges

Claude: [Calls fillet radius=5 edges="all"]
        
        ✓ Applied 5mm fillets to 12 edges
        [Screenshot showing filleted box]

User: Save it as MyPart.SLDPRT

Claude: [Calls save_part path="C:\Users\...\MyPart.SLDPRT"]
        
        ✓ Saved as MyPart.SLDPRT
```

---

## Functional Requirements

### FR-1: MCP Server
- **FR-1.1**: Server starts and registers with Claude Desktop via stdio transport
- **FR-1.2**: Server exposes tools matching the operations table above
- **FR-1.3**: Server exposes resources for model state and screenshots
- **FR-1.4**: Server handles connection lifecycle (startup, shutdown)

### FR-2: SolidWorks Connection
- **FR-2.1**: Connect to running SolidWorks instance
- **FR-2.2**: Optionally launch SolidWorks if not running (configurable)
- **FR-2.3**: Handle connection loss and reconnection
- **FR-2.4**: Graceful shutdown without closing SolidWorks

### FR-3: Document Operations
- **FR-3.1**: Create new blank part using default template
- **FR-3.2**: Save part to specified file path
- **FR-3.3**: Validate path is writable before save

### FR-4: Sketch Operations
- **FR-4.1**: Create sketch on Front/Top/Right plane
- **FR-4.2**: All dimensions in millimeters, converted internally
- **FR-4.3**: Exit sketch mode (close sketch)
- **FR-4.4**: Support all 6 sketch entities: rectangle, circle, line, arc, polygon, spline

### FR-5: Feature Operations
- **FR-5.1**: Extrude with boss (add material) or cut (remove material)
- **FR-5.2**: Fillet with specified radius (all edges or selection)
- **FR-5.3**: Chamfer with specified distance

### FR-6: Visual Feedback
- **FR-6.1**: Capture viewport screenshot after each modifying operation
- **FR-6.2**: Return screenshot as part of tool response
- **FR-6.3**: Store screenshots in configurable directory

### FR-7: Error Handling
- **FR-7.1**: Return descriptive error messages for failed operations
- **FR-7.2**: Include operation context in error (what was attempted)
- **FR-7.3**: Never crash the server on operation failure

---

## Non-Functional Requirements

### Performance
- Tool execution: < 5 seconds for simple operations
- Screenshot capture: < 2 seconds
- Server startup: < 10 seconds (excluding SolidWorks launch)

### Reliability
- Server handles SolidWorks connection loss gracefully
- Operations are atomic (succeed fully or fail cleanly)
- No zombie COM objects left after errors

### Testability
- Mocked unit tests run without SolidWorks
- Integration tests run with SolidWorks (marked separately)
- 80%+ code coverage for operations layer

### Maintainability
- Clear separation: MCP layer → Operations layer → COM layer
- Pydantic models for all inputs/outputs
- Comprehensive logging with loguru

---

## Success Criteria

### V1 Complete When:
1. ✓ User can create a simple part through conversation
2. ✓ All 6 sketch entities work correctly
3. ✓ Extrude, fillet, chamfer work correctly
4. ✓ Screenshots returned after each operation
5. ✓ Save part works
6. ✓ Error handling doesn't crash server
7. ✓ Both mocked and integration tests pass
8. ✓ Documentation for Claude Desktop setup

### Demo Scenario
Create this part through conversation:
1. New part
2. Rectangle sketch 100x50mm
3. Extrude 25mm
4. Add 5mm fillets
5. Save as demo.SLDPRT

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| COM connection instability | Operations fail randomly | Robust reconnection logic (already implemented) |
| Screenshot capture fails | No visual feedback | Graceful degradation - return text only |
| SolidWorks API changes | Tools break | Version check at startup, document supported versions |
| Edge selection for fillet/chamfer | User can't specify edges | V1: Apply to all edges. Future: named selection |

---

## Future Considerations (Post-V1)

- Open/close existing parts
- Assembly operations
- Drawing generation
- Revolve, sweep, loft features
- Pattern operations
- Hole wizard
- Dedicated chat UI (web or desktop)
- Voice input
- Design history / undo

---

## Appendix: Tool Schemas (Draft)

### create_new_part
```python
class CreateNewPartParams(BaseModel):
    template: Optional[str] = Field(None, description="Template path, or None for default")
```

### draw_rectangle
```python
class DrawRectangleParams(BaseModel):
    x: float = Field(0, description="Center X in mm")
    y: float = Field(0, description="Center Y in mm")
    width: float = Field(..., gt=0, description="Width in mm")
    height: float = Field(..., gt=0, description="Height in mm")
```

### extrude
```python
class ExtrudeParams(BaseModel):
    depth: float = Field(..., gt=0, description="Depth in mm")
    operation: Literal["boss", "cut"] = Field("boss")
    direction: Literal["forward", "backward", "both"] = Field("forward")
```

*(Full schemas to be finalized during implementation)*

---

*Document Version: 1.0*
*Last Updated: January 2026*
