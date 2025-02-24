"""Helper functions for DataStar integration."""

from typing import Dict, Any, Optional

class _DSHelper(dict):
    """Special dictionary that converts keys to proper data-* attributes"""
    def __init__(self, attrs: dict):
        super().__init__({
            key.replace('_', '-'): value 
            for key, value in attrs.items()
        })

def ds_attrs(**exprs: str) -> _DSHelper:
    """Convert expressions to DataStar data-attr-* attributes."""
    return _DSHelper({
        f"data_attr_{key}": value 
        for key, value in exprs.items()
    })

def ds_classes(exprs: Optional[Dict[str, str]] = None, **kwargs: str) -> _DSHelper:    
    """Convert expressions to DataStar data-class JavaScript object."""
    class_map = {}
    inputs = {**(exprs or {}), **kwargs}
    for key, value in inputs.items():
        for cls_name in key.split():
            normalized = cls_name.replace('_', '-')
            class_map[normalized] = value
    
    js_obj = "{" + ", ".join(
        f"'{k}': {v}" 
        for k, v in class_map.items()
    ) + "}"
    return _DSHelper({"data_class": js_obj})

def ds_signals(exprs: Optional[Dict[str, str]] = None, **kwargs: str) -> _DSHelper:    
    """Support both namespaced signals and camelCase with automatic conversion"""
    def process_key(key: str) -> str:
        # Convert double underscores to dots for namespacing
        return key.replace('__', '.')
    
    def wrap_value(v: str) -> str:
        if not v or v[0] in ('"', "'", '{', '$'):
            return v
        return f"'{v}'"

    inputs = {**(exprs or {}), **kwargs}
    processed = {process_key(k): wrap_value(v) for k, v in inputs.items()}
    
    js_obj = "{" + ", ".join(
        f"'{k}': {v}" for k, v in processed.items()
    ) + "}"
    return _DSHelper({"data_signals": js_obj})

def ds_on(**events: str) -> _DSHelper:
    """Convert event handlers to DataStar data-on-* attributes."""
    return _DSHelper({
        f"data_on_{k}": v 
        for k, v in events.items()
    })

def ds_computed(**computed: str) -> _DSHelper:
    """Convert expressions to DataStar data-computed-* attributes."""
    return _DSHelper({
        f"data_computed_{k}": v 
        for k, v in computed.items()
    })


def ds_show(*args, **conditions: str) -> _DSHelper:
    """Convert expressions to DataStar data-show attributes.
    
    Supports both styles:
    1. Explicit: ds_show(when="$input != ''")
    2. Concise: ds_show("$input != ''")
    """
    # Handle positional argument
    if args:
        if conditions:
            raise ValueError("Cannot mix positional and keyword arguments")
        return _DSHelper({"data_show": args[0]})
    
    # Handle keyword arguments
    if "when" in conditions:
        return _DSHelper({"data_show": conditions["when"]})
    return _DSHelper({"data_show": next(iter(conditions.values()))})

def ds_bind(name: str) -> _DSHelper:
    """Create data-bind attribute helper for direct value syntax.
    
    Example:
        <input data-bind="input1"> → ds_bind("input1")
    """
    return _DSHelper({"data_bind": name})

def ds_text(expr: str) -> _DSHelper:
    """Create data-text attribute helper."""
    return _DSHelper({"data_text": expr})

def ds_indicator(signal_name: str) -> _DSHelper:
    """Track request state with a boolean signal."""
    return _DSHelper({"data_indicator": signal_name})