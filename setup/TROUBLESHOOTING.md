# Troubleshooting setup.ipynb

Errors seen while running `setup/setup.ipynb` on Windows behind Cloudflare WARP, with the fix for each.

Cells are named by their id in the notebook file and by the first line of their code.

## 1. SSL certificate error when reading a maze page

**File:** `setup/setup.ipynb`

**Cell where it shows:** `cell-15`, `print(read_web_page("https://maze.edwarddonner.com"))`.
The request itself is made in `cell-14`, inside `read_web_page`.

**Error:**

```
SSLError: HTTPSConnectionPool(host='maze.edwarddonner.com', port=443): Max retries exceeded with url: /
(Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED]
certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1010)')))
```

**Cause:** Cloudflare WARP replaces the site's certificate with its own. Windows trusts the WARP
certificate, but Python uses its own certificate list and does not.

**Fix applied:** in `cell-07` (the imports cell), import `truststore` and call it once. Python then
uses the certificates that Windows trusts.

```python
import truststore
...
# Use the certificates Windows trusts, so HTTPS works behind Cloudflare WARP
truststore.inject_into_ssl()
```

**Why it still failed after the fix:**

- The kernel was running an older copy of `cell-07` without these lines.
- The notebook tab in VS Code had unsaved changes. VS Code then keeps its own copy and does not load
  the changed file from disk.

**To apply it:**

1. Check that `cell-07` contains both lines above, then save with Ctrl+S.
2. Click **Restart**.
3. Run `cell-07` again before any other cell.

**Proof:** with `cell-07`, `cell-14` and `cell-15` run in order in the notebook's own kernel, `cell-15` printed
`Reading web page: https://maze.edwarddonner.com` and then the maze text "The Maze. This page is for an AI that
can read web pages…".

**Note:** `truststore` is not listed in `pyproject.toml`. It is installed only because another package
depends on it. If that package stops depending on it, `cell-07` fails with `ModuleNotFoundError`. Then run
`uv add truststore`.

## 2. `NameError: name 'openrouter' is not defined`

**File:** `setup/setup.ipynb`

**Cell where it shows:** `99dbd12f`, under "Using the tool once", which starts
`messages = [{"role": "user", "content": "Please read https://maze.edwarddonner.com ...`

**Error:**

```
NameError                                 Traceback (most recent call last)
----> 3 response = openrouter.chat.completions.create(model=MODEL, messages=messages, tools=tools)
NameError: name 'openrouter' is not defined
```

**Cause:** after a kernel restart, two cells were not run again:

- `cell-09`, "Check your key", which reads `OPENROUTER_API_KEY` from `.env`.
- `cell-11`, "Connect to OpenRouter", which creates the `openrouter` client and sets `MODEL`.

A restart clears every variable. A cell that uses one fails until the cell that creates it runs again.

**Fix applied:** we ran these cells again in order in the same kernel:

1. `cell-07`, the imports.
2. `cell-09`, the key check.
3. `cell-11`, Connect to OpenRouter.
4. `cell-14`, `read_web_page`.
5. `cell-17`, the tool description.
6. `cell-19`, `handle_tool_call`.

Then we ran `99dbd12f` again.

**Proof:** `99dbd12f` printed:

```
Answered by nvidia/nemotron-3-super-120b-a12b:free
Finish reason: tool_calls
[ChatCompletionMessageFunctionToolCall(... arguments='{"url":"https://maze.edwarddonner.com"}', name='read_web_page' ...)]
```

**To avoid it:** after every kernel restart, click **Run All**, or run the cells in order from the top.
Do not start halfway down the notebook.

## Quick check after a restart

| Cell | What you should see |
| --- | --- |
| `cell-09` | `OpenRouter API key exists and begins sk-or-v1-` |
| `cell-12` | `Answered by <model name>` and a reply |
| `cell-15` | `Reading web page: https://maze.edwarddonner.com` and the maze text |
| `99dbd12f` | `Finish reason: tool_calls` |
