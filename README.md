# Datastar FastHTML

Datastar integration for FastHTML.

## Installation

```bash
pip install git+https://github.com/banditburai/ft-datastar.git
```

## Usage example in FastHTML
```python
from fasthtml.common import *
from ft_datastar import *
from json import dumps as json_dumps

datastar_script = Script(src="https://cdn.jsdelivr.net/gh/starfederation/datastar@v1.0.0-beta.8/bundles/datastar.js", type="module")

app, rt = fast_app(
    pico=False,
    surreal=False,
    htmx=False,
    live=False,    
    hdrs=(datastar_script,),
)

@rt("/")
def index():
    return Div(
        H2("Datastar + FastHTML Example", cls="text-xl font-bold mb-4"),
        Div(
            "Using signals we default the starting count to 5",
            ds_signals(count="5")
        ),
        Button(
            "Increment",
            ds_on(click="$count++"),
            cls="btn btn-primary mr-2"
        ),
        Button(
            "Reset",
            ds_on(click="$count = 0"),
            cls="btn btn-warning"
        ),
        Div(
            "Count: ",
            Span(ds_text("$count"), cls="font-mono"),
            cls="mt-2"
        ),
        cls="p-4 space-y-2"
    )

if __name__ == "__main__":
    serve()    
```

## Features

`ft-datastar` provides a set of helper functions that make it easy to use [Datastar](https://data-star.dev/) with [FastHTML](https://github.com/answerDotAI/fasthtml/). These helpers map directly to Datastar attributes and functionality.

### Helper Functions

| Function | Description | DataStar Equivalent |
|----------|-------------|---------------------|
| `ds_attrs(**exprs)` | Bind attributes dynamically | `data-attr-*` attributes |
| `ds_bind(name)` | Two-way binding for form elements | `data-bind` attribute |
| `ds_classes(exprs, **kwargs)` | Conditionally apply CSS classes | `data-class` attribute |
| `ds_computed(**computed)` | Define computed properties | `data-computed` attribute |
| `ds_indicator(signal_name)` | Show loading indicator | `data-indicator` attribute |
| `ds_on(**events)` | Attach event handlers | `data-on-*` attributes |
| `ds_show(*args, **conditions)` | Conditionally show elements | `data-show` attribute |
| `ds_signals(exprs, **kwargs)` | Define reactive signals | `data-signals` attribute |
| `ds_text(expr)` | Bind text content | `data-text` attribute |

### Server-Sent Events (SSE)

`ft-datastar` includes support for Server-Sent Events (SSE) to enable real-time updates:

| Function | Description |
|----------|-------------|
| `sse(handler)` | Decorator for SSE endpoint handlers |
| `update_siganls(**signals)` | Update signal values |
| `update_fragments(fragment, selector, merge_mode)` | Update DOM fragments |
| `FastHTMLDatastarSSEResponse` | Response class for SSE streams |

### Components

| Component | Description |
|-----------|-------------|
| `IconifyIcon` | Wrapper for the Iconify web component |


## Examples

Check out the [examples directory](./examples) for sample applications and usage patterns.
