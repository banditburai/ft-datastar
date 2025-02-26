# Datastar FastHTML

Datastar integration for FastHTML.

## Installation

```bash
pip install git+https://github.com/banditburai/ft-datastar.git
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
| `signal_update(**signals)` | Update signal values |
| `fragment_update(fragment, selector, merge_mode)` | Update DOM fragments |
| `FastHTMLDatastarSSEResponse` | Response class for SSE streams |

### Components

| Component | Description |
|-----------|-------------|
| `IconifyIcon` | Wrapper for the Iconify web component |


## Examples

Check out the [examples directory](./examples) for sample applications and usage patterns.
