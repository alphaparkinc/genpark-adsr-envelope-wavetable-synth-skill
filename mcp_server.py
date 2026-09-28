import sys
import json
from client import ADSREnvelopeWavetableSynth

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-adsr-envelope-wavetable-synth-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "render_tone",
                    "description": "Synthesize audio waveform using ADSR envelope generator and wavetable oscillators",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "waveform": {"type": "string", "enum": ["sine", "square", "sawtooth", "triangle"], "default": "sine"},
                            "freq": {"type": "number", "default": 440.0},
                            "duration_sec": {"type": "number", "default": 0.5},
                            "attack": {"type": "number", "default": 0.05},
                            "decay": {"type": "number", "default": 0.05},
                            "sustain": {"type": "number", "default": 0.7},
                            "release": {"type": "number", "default": 0.1}
                        }
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "render_tone":
            synth = ADSREnvelopeWavetableSynth()
            data = synth.render_tone(**args)
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
