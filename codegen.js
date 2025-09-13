function parsePrompt(prompt) {
  const text = (prompt || '').toLowerCase();

  // defaults
  let plane = 'front';
  if (text.includes('top')) plane = 'top';
  if (text.includes('right')) plane = 'right';

  // box LxWxH mm
  const boxMatch = text.match(/(\d+)\s*[x×]\s*(\d+)\s*[x×]\s*(\d+)\s*mm/);
  let L=null, W=null, H=null;
  if (boxMatch) {
    L = parseFloat(boxMatch[1]);
    W = parseFloat(boxMatch[2]);
    H = parseFloat(boxMatch[3]);
  }

  // fillet R mm
  const filletMatch = text.match(/fillet[s]?\s*(?:to)?\s*(?:all\s*edges)?\s*(\d+)\s*mm/);
  let filletR = null;
  if (filletMatch) filletR = parseFloat(filletMatch[1]);

  return { plane, L, W, H, filletR };
}

function mmToM(mm){ return (mm || 0) / 1000.0; }

/** produce only from safe templates */
function buildOperationsVB({ plane, L, W, H, filletR }) {
  const ops = [];

  // select plane
  const planeName = plane.charAt(0).toUpperCase() + plane.slice(1) + ' Plane';
  ops.push(`
' Select plane
boolstatus = model.Extension.SelectByID2("${planeName}", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
If boolstatus = False Then
  WScript.Echo "Failed to select ${planeName}"
  WScript.Quit 1
End If

' Start sketch
model.SketchManager.InsertSketch True
`);

  if (L && W) {
    const halfL = mmToM(L)/2, halfW = mmToM(W)/2;
    ops.push(`
' Draw center rectangle (±L/2, ±W/2)
Set segs = model.SketchManager.CreateCenterRectangle(0, 0, 0, ${halfL.toFixed(6)}, ${halfW.toFixed(6)}, 0)
model.SketchManager.InsertSketch True ' exit sketch
`);
  }

  if (H) {
    ops.push(`
' Extrude boss (depth in meters)
Set feat = model.FeatureManager.FeatureExtrusion2(True, False, False, 0, 0, ${mmToM(H).toFixed(6)}, 0, False, False, False, False, 0, 0, False, False, False, False, True, True, True, 0, 0, False)
If feat Is Nothing Then
  WScript.Echo "Extrude failed"
  WScript.Quit 1
End If
`);
  }

  if (filletR) {
    ops.push(`
' Select all edges and apply fillet
boolstatus = model.Extension.SelectAll()
If boolstatus = False Then
  WScript.Echo "SelectAll failed"
  WScript.Quit 1
End If
Set fil = model.FeatureManager.InsertFeatureFillet(8, ${mmToM(filletR).toFixed(6)}, 0, Nothing, Nothing, Nothing)
model.ClearSelection2 True
`);
  }

  return ops.join('\n');
}

function generateVbsFromPrompt(prompt){
  const params = parsePrompt(prompt);
  const warnings = [];
  if (!(params.L && params.W && params.H)) {
    warnings.push("Could not detect L×W×H in mm (e.g., '120x80x25 mm'). Only extrude will run if a sketch exists.");
  }

const header = `
' AISolidWorks auto-generated macro (VBScript)
On Error Resume Next
Dim swApp: Set swApp = GetObject(, "SldWorks.Application")
If Err.Number <> 0 Then
  Err.Clear
  Set swApp = CreateObject("SldWorks.Application")
End If
swApp.Visible = True

' Try to use SW's default Part template; 0 = swDefaultTemplatePart
Dim templatePath
templatePath = swApp.GetUserPreferenceStringValue(0)

' Fallback to a hardcoded template path (DOUBLE backslashes for JS)
If Len(templatePath) = 0 Then
  templatePath = "C:\\ProgramData\\SOLIDWORKS\\SOLIDWORKS 2024\\templates\\Part.prtdot"
End If

' Create new document
Dim model: Set model = swApp.NewDocument(templatePath, 0, 0, 0)
If model Is Nothing Then
  ' Print more context to the log to debug path issues
  WScript.Echo "Failed to create new document." & vbCrLf & _
               "Template tried: " & templatePath
  WScript.Quit 1
End If

' Units to mm (swUserPreferenceIntegerValue_e 121 = linear units; 2 = mm)
model.SetUserPreferenceIntegerValue 121, 2
`;

  const body = buildOperationsVB(params);

  const vbs = header + '\n' + body + '\nWScript.Echo "Done"';
  const plan = [
    `Plane: ${params.plane}`,
    params.L && params.W && params.H ? `Box: ${params.L}×${params.W}×${params.H} mm` : `Box: not fully detected`,
    params.filletR ? `Fillet: ${params.filletR} mm (all edges)` : `Fillet: none`,
  ].join('\n');

  return { plan, vbs, warnings };
}

module.exports = { generateVbsFromPrompt };
