import subprocess, sys, os, tempfile, time

def run_code(code, timeout=8):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        wrapped = f"""
import sys, io
_buf = io.StringIO()
sys.stdout = _buf
try:
{chr(10).join('    ' + line for line in code.split(chr(10)))}
except Exception as e:
    print(f"Error: {{type(e).__name__}}: {{e}}")
sys.stdout = sys.__stdout__
print(_buf.getvalue(), end='')
"""
        f.write(wrapped)
        path = f.name
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
        elapsed = round(time.time() - t0, 3)
        err = r.stderr
        if err:
            lines = [l for l in err.split('\n') if l.strip() and 'File "' not in l and path not in l and 'Traceback' not in l]
            err = '\n'.join(lines)
        return r.stdout, err, elapsed
    except subprocess.TimeoutExpired:
        return "", "⏱️ Code timed out (infinite loop?)", timeout
    except Exception as e:
        return "", str(e), 0
    finally:
        try: os.unlink(path)
        except: pass

def check_output(code, expected_contains):
    out, err, t = run_code(code)
    combined = (out + err).lower()
    if err and 'error:' in err.lower():
        return False, out, err, t
    if not expected_contains:
        return True, out, err, t
    missing = [e for e in expected_contains if e.lower() not in combined]
    return len(missing) == 0, out, err, t
