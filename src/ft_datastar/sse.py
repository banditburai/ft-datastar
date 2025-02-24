"""Server-Sent Events integration for DataStar."""

from fasthtml.starlette import StreamingResponse
from fasthtml.common import to_xml
from datastar_py.sse import SSE_HEADERS, ServerSentEventGenerator
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Tuple, Union
from functools import wraps

class DatastarFastHTMLResponse(StreamingResponse):
    def __init__(self, generator, *args, **kwargs):
        kwargs["headers"] = SSE_HEADERS
        
        class XMLSSEGenerator(ServerSentEventGenerator):
            @classmethod
            def merge_fragments(cls, fragments, *args, **kwargs):
                # Handle both single components and lists
                if not isinstance(fragments, list):
                    fragments = [fragments]
                
                xml_fragments = [
                    f if isinstance(f, str) else to_xml(f)  
                    for f in fragments
                ]
                return super().merge_fragments(xml_fragments, *args, **kwargs)
        
        super().__init__(generator(XMLSSEGenerator), *args, **kwargs)

def srt(handler: Callable) -> Callable:
    """Decorator that handles sequential signal/fragment updates with dynamic targeting"""
    @wraps(handler)
    def wrapped(*args, **kwargs):
        def sse_generator(sse):
            async def proxy():
                gen = handler(*args, **kwargs)
                async for item_type, payload in gen:
                    if item_type == "signals":
                        yield sse.merge_signals(payload)
                    elif item_type == "fragments":
                        # Allow flexible fragment definitions
                        fragment, *options = payload if isinstance(payload, tuple) else (payload,)
                        selector = options[0] if len(options) > 0 else None
                        merge_mode = options[1] if len(options) > 1 else "morph"
                        
                        yield sse.merge_fragments(
                            fragment,
                            selector=selector,
                            merge_mode=merge_mode
                        )
                    else:
                        raise ValueError(f"Invalid item type: {item_type}")
            
            return proxy()
        
        return DatastarFastHTMLResponse(sse_generator)
    return wrapped

def signal_update(**signals: str) -> Tuple[str, Dict[str, str]]:
    return "signals", signals

def fragment_update(fragment: Any, selector: Optional[str] = None, merge_mode: str = "morph") -> Tuple[str, Tuple[Any, Optional[str], str]]:
    return "fragments", (fragment, selector, merge_mode)