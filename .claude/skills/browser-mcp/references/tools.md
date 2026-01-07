---
covers: Browser MCP tools reference
type: reference
---

# Browser MCP Tools Reference

Comprehensive reference for all Browser MCP tools. These tools connect to the user's actual Chrome browser, not a separate automation instance.

## Navigation Tools

### browser_navigate

Navigate to a URL. Use for explicit page loads and refreshing to clear console state.

```
browser_navigate(url: "https://example.com")
```

**When to use:**
- Initial page load
- Refreshing to get clean console logs (navigate to same URL)
- Switching between pages during debugging

**Note:** For refresh during debugging, navigate to the current URL to clear console logs and get a fresh page state.

---

### browser_go_back

Navigate back in browser history.

```
browser_go_back()
```

**When to use:**
- Returning to previous page after testing
- Navigating multi-step flows in reverse

---

### browser_go_forward

Navigate forward in browser history.

```
browser_go_forward()
```

**When to use:**
- Moving forward after going back
- Testing navigation flow in either direction

---

## State Capture Tools

### browser_snapshot

Get a text representation of the current page DOM/state. Returns structured content showing page elements, text, and interactive elements.

```
browser_snapshot()
```

**When to use:**
- Understanding current page structure
- Confirming URL and page content with user
- Getting element references for interactions
- Initial observation during debugging setup

**Returns:** Text representation of the visible page including element references for clicking/typing.

---

### browser_screenshot

Capture a visual screenshot of the current page.

```
browser_screenshot()
```

**When to use:**
- Design critique — capturing visual state
- Debugging — seeing actual rendered output
- Comparing before/after states
- Documenting current UI for reports

**Key for debugging:** Captures exactly what the user sees, including visual bugs not apparent from DOM alone.

---

### browser_get_console_logs

Get console output (logs, warnings, errors) from the browser.

```
browser_get_console_logs()
```

**When to use:**
- Debugging — primary tool for seeing console.log output
- Checking for JavaScript errors
- Viewing network errors or warnings
- Reading [DEBUG-AGENT] instrumentation output

**Key for debugging:** Direct access to console without user copy/pasting. Captures:
- `console.log()` output including agent-added instrumentation
- JavaScript errors and stack traces
- Network errors
- Warning messages

---

## Interaction Tools

### browser_click

Click on an element by reference (from browser_snapshot) or selector.

```
browser_click(element: "Submit button")
browser_click(ref: "element-ref-123")
```

**When to use:**
- Triggering button clicks to observe behavior
- Testing interactive elements
- Navigating through multi-step flows

---

### browser_hover

Hover over an element to trigger hover states.

```
browser_hover(element: "Menu item")
browser_hover(ref: "element-ref-456")
```

**When to use:**
- Testing dropdown menus
- Revealing tooltip content
- Triggering hover-based CSS transitions
- Design critique of hover states

---

### browser_type

Type text into an input field.

```
browser_type(element: "Email input", text: "user@example.com")
browser_type(ref: "input-ref-789", text: "search query")
```

**When to use:**
- Filling form fields for testing
- Testing input validation
- Simulating user text entry

**Note:** May need to click the element first to focus it.

---

### browser_select_option

Select an option from a dropdown/select element.

```
browser_select_option(element: "Country dropdown", value: "United States")
```

**When to use:**
- Selecting dropdown values
- Testing form selection behavior

---

### browser_press_key

Send keyboard input (Enter, Escape, Tab, etc).

```
browser_press_key(key: "Enter")
browser_press_key(key: "Escape")
browser_press_key(key: "Tab")
```

**When to use:**
- Submitting forms with Enter
- Closing modals with Escape
- Navigating between form fields
- Testing keyboard shortcuts

---

## Utility Tools

### browser_wait

Wait for a condition or fixed time.

```
browser_wait(seconds: 2)
browser_wait(condition: "element visible", selector: ".loading-complete")
```

**When to use:**
- Waiting for async operations to complete
- Giving time for animations to finish
- Waiting for elements to appear after user action
- Allowing state changes to propagate

**Note:** Use sparingly — prefer explicit conditions when possible.

---

## Tool Combinations by Workflow

### Debugging Pattern

```
1. browser_snapshot()           → Confirm URL/page with user
2. browser_screenshot()         → See current visual state
3. browser_get_console_logs()   → Check for existing errors
4. [Add instrumentation to code]
5. browser_navigate(current_url) → Refresh for clean logs
6. browser_get_console_logs()   → Read new [DEBUG-AGENT] output
7. browser_screenshot()         → Observe result
```

### Design Critique Pattern

```
1. browser_snapshot()           → Understand page structure
2. browser_screenshot()         → Capture desktop view
3. [Adjust viewport if needed]
4. browser_screenshot()         → Capture mobile view
5. [Interact with elements]
6. browser_screenshot()         → Capture interaction states
```
