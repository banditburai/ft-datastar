"""Component wrappers for FastHTML integration."""

from fasthtml.common import ft_hx
from typing import Any, Optional, Dict

def IconifyIcon(*children: Any, target_id: Optional[str] = None, **kwargs: Any) -> Any:
    """Iconify web component wrapper."""
    # Convert underscores to hyphens in attributes
    processed_kwargs = {
        key.replace('_', '-'): value
        for key, value in kwargs.items()
    }
    return ft_hx('iconify-icon', *children, target_id=target_id, **processed_kwargs)
