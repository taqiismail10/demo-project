# Model evaluation run results

## Environment prep

```
python -m pip install -r requirements-model-eval.txt
```

```
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 403 Forbidden'))': /simple/evaluate/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 403 Forbidden'))': /simple/evaluate/
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 403 Forbidden'))': /simple/evaluate/
WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 403 Forbidden'))': /simple/evaluate/
WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 403 Forbidden'))': /simple/evaluate/
ERROR: Could not find a version that satisfies the requirement evaluate (from versions: none)
ERROR: No matching distribution found for evaluate
```

## Command

```
python model_eval.py
```

## Output

```
Traceback (most recent call last):
  File "/workspace/demo-project/model_eval.py", line 3, in <module>
    import evaluate
ModuleNotFoundError: No module named 'evaluate'
```
