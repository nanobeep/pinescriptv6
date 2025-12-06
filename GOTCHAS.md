# Pine Script v6 Gotchas & Lessons Learned

## 1. `syminfo.tickerid` Can Be "Dirty"
**Observation:** In some execution contexts (likely specific to replay modes, pasted code, or certain platform environments), `syminfo.tickerid` may contain unexpected artifacts like extra quotes (`"`) or closing braces (`}`).
**Fix:** Always sanitize symbol strings if relying on exact string matching.
```pine
rootSymbol(s) =>
    // Aggressive cleaning of potential artifacts
    sClean = str.replace_all(str.replace_all(s, "\"", ""), "}", "")
    sTrim = str.trim(sClean)
    // ... rest of parsing logic
```

## 2. Input Data Fragility
**Observation:** Manual text inputs (`input.text_area` or `input.string`) are prone to trailing whitespace or invisible characters, causing `str.tonumber()` to return `na`.
**Fix:** Always wrap parsed string segments in `str.trim()` before conversion.
```pine
// Risky
lvl = str.tonumber(array.get(parts, 2)) 

// Safe
lvlStr = str.trim(array.get(parts, 2))
lvl = str.tonumber(lvlStr)
```

## 3. Empty Array Crashes
**Observation:** Loops that iterate backwards (e.g., `for i = size - 1 to 0`) will crash if the array is empty because `size - 1` becomes `-1`.
**Fix:** Always guard loops with a size check.
```pine
sz = array.size(myArray)
if sz > 0
    for i = sz - 1 to 0
        // ...
```

## 4. `var` Variable Persistence
**Observation:** Using `var` for a local variable inside a user-defined function (`var float out = na`) persists its value across bar executions. If the logic depends on re-evaluating conditions from scratch every bar (like finding a specific level for *this* timestamp), `var` can cause the function to return stale or incorrect "locked-in" values.
**Fix:** Use standard variable declarations (`float out = na`) for values that must be recalculated fresh on every bar.

## 5. Debugging "Invisible" Errors
**Observation:** When lines don't appear, it is often due to data format mismatches (e.g., "AAPL" vs "AAPL"}). Visual inspection of code isn't enough.
**Fix:** Use `log.info` to print the exact strings being compared during the *last* bar to see what the script actually sees.
```pine
if barstate.islast
    log.info("Target: |" + targetSym + "| vs Data: |" + dataSym + "|")
```

## 6. Input Strings & Multiline Data
**Observation:** Pine v6 doesn't support Python-style triple-quoted multiline strings; using raw newlines inside `input.string` can misparse. Complex concatenation is also easy to break.
**Fix:** Keep `input.string` literals on one line with explicit `\n` separators, e.g. `"2025-12-03|AAPL|192.50\n2025-12-03|MSFT|452.10"`. Avoid trailing `+` or unmatched parentheses in inputs.

## 7. Collections Inside Collections
**Observation:** Pine forbids collections as template parameters for other collections (e.g., `map<string, array<int>>` or `array<array<float>>`).
**Fix:** Flatten storage or wrap collections inside a user-defined type and store that type, or use parallel arrays / symbol-index maps instead.

## 8. Missing Record Constructors
**Observation:** User-defined types require `.new(...)` for construction; `HVN(t, lvl)` fails with “Could not find function or function reference”.
**Fix:** Use `HVN.new(t, lvl)`.

## 9. Map Templates Are Required
**Observation:** `map.new()` without templates errors in v6 (“requires a template”).  
**Fix:** Always specify types: `map.new<string, float>()`.

## 10. Symbol Normalization
**Observation:** Data may use bare tickers (“AAPL”) while chart symbols are prefixed (“NASDAQ:AAPL”).  
**Fix:** Normalize by splitting on `":"` via `str.split`, taking the last part, and uppercasing:  
```pine
rootSymbol(s) =>
    parts = str.split(str.trim(s), ":")
    base = array.size(parts) > 1 ? array.get(parts, array.size(parts) - 1) : str.trim(s)
    str.upper(base)
```

## 11. Use `syminfo.tickerid` for Requests, But Compare Roots
**Observation:** Exact `tickerid` string may not match pasted data; comparing raw strings fails silently.  
**Fix:** Compare normalized roots for matching; still use `syminfo.tickerid` for requests when needed.

## 12. Reverse Scans Require Size Guards
**Observation:** Backward loops on empty arrays crash.  
**Fix:** Guard with `if array.size(arr) > 0` before `for i = size - 1 to 0`.

## 13. Persistent Levels on Main Chart
**Observation:** Using `line.new` for price levels can result in "floating" lines that do not scale with the price axis if not anchored correctly or if the script is not an overlay.
**Fix:** To render standard indicator levels that stick to price candles, use `plot()` with `style = plot.style_stepline` (or `plot.style_linebr`) and ensure `force_overlay = true` is set in the `plot()` call or `overlay = true` in the `indicator()` declaration.

## 14. Multiline Data Pasting
**Observation:** `input.string` creates a single-line text field which is unusable for pasting large blocks of multiline data (e.g., CSV).
**Fix:** Use `input.text_area` for any input intended to accept multiline text or pasted data blobs.