"""DataStar integration for FastHTML."""

from .components import IconifyIcon
from .helpers import (
    ds_attrs, ds_bind, ds_classes, ds_computed, 
    ds_indicator, ds_on, ds_show, ds_signals, ds_text
)
from .sse import (
    DatastarFastHTMLResponse, sse, signal_update, fragment_update
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
    "DatastarFastHTMLResponse",
    "sse",
    "signal_update",
    "fragment_update",
]