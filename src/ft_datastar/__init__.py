"""DataStar integration for FastHTML."""

from .components import IconifyIcon
from .helpers import (
    ds_attrs, ds_bind, ds_classes, ds_computed, 
    ds_indicator, ds_on, ds_show, ds_signals, ds_text
)
from .sse import (
    FastHTMLDatastarSSEResponse, 
    sse, update_signals, update_fragments
)

__all__ = [
    # Components
    "IconifyIcon",
    
    # Helpers
    "ds_attrs",
    "ds_bind",
    "ds_classes",
    "ds_computed",
    "ds_indicator",
    "ds_on",
    "ds_show",
    "ds_signals",
    "ds_text",
    
    # SSE
    "FastHTMLDatastarSSEResponse",    
    "sse",
    "update_signals",
    "update_fragments",
]