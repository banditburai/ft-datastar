# ============================================================================
#  FastHTML + TailwindCSS + DaisyUI Simple Template
# ============================================================================
from fasthtml.common import *
from ft_datastar import *
from dataclasses import dataclass, field
from typing import Any, List, Callable
import random
import asyncio
from json import dumps as json_dumps
from functools import wraps
from version import __version__

# ============================================================================

head_el = (
    Link(rel="icon", href="/static/favicon.ico", sizes="any"), 
    Link(rel="icon", href="/static/icon.svg", type="image/svg+xml"),
    Link(rel="apple-touch-icon", href="/static/apple-touch-icon.png"),
)

socials = Head(
    Meta(charset="utf-8"),
    Meta(name="viewport", content="width=device-width, initial-scale=1"),
    Title("FastHTML + Datastar"),    
    # Open Graph Tags
    Meta(property="og:image", content="https://datastar.daisyft.com/static/og-default.png"),
    Meta(property="og:image:type", content="image/png"),
    Meta(property="og:image:width", content="1200"),
    Meta(property="og:image:height", content="630"),
    Meta(property="og:type", content="website"),
    Meta(property="og:url", content="https://datastar.daisyft.com/"),
    Meta(property="og:title", content="FastHTML + Datastar"),
    Meta(property="og:description", content="FastHTML + Datastar"),
    # Twitter Cards
    Meta(name="twitter:card", content="summary_large_image"),
    Meta(name="twitter:title", content="FastHTML + Datastar"),
    Meta(name="twitter:description", content="FastHTML + Datastar"),
    Meta(name="twitter:image", content="https://datastar.daisyft.com/static/og-default.png"),
    Meta(name="twitter:creator", content="@promptsiren"),
    Meta(name="twitter:site", content="@promptsiren"),        
)

styles = Link(rel="stylesheet", href="/static/styles.css", type="text/css")
iconify_script = Script(src="https://cdn.jsdelivr.net/npm/iconify-icon@2.3.0/dist/iconify-icon.min.js", type="module")
datastar_script = Script(src="https://cdn.jsdelivr.net/gh/starfederation/datastar@v1.0.0-beta.7/bundles/datastar.js", type="module")

highlight_js = Script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js")
highlight_python = Script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js")
highlight_dark_css = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/tokyo-night-dark.min.css", id="highlight-dark-theme")
highlight_light_css = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/panda-syntax-light.min.css", id="highlight-light-theme")

highlight_init_script = Script("""
document.addEventListener('DOMContentLoaded', function() {
    // Configure highlight.js
    hljs.configure({
        cssSelector: 'pre code:not([data-highlighted="yes"])'
    });
    
    // Initial highlighting
    hljs.highlightAll();
    
    // Theme handling for highlight.js
    const darkTheme = document.getElementById('highlight-dark-theme');
    const lightTheme = document.getElementById('highlight-light-theme');
    
    // Set initial theme state
    function updateHighlightTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        darkTheme.disabled = currentTheme !== 'dark';
        lightTheme.disabled = currentTheme !== 'light';
    }
    
    // Update theme on load
    updateHighlightTheme();
    
    // Watch for theme changes - simplified callback since we only care about data-theme
    const observer = new MutationObserver(updateHighlightTheme);
    
    observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['data-theme']
    });
});
""")

highlight_scripts = [
    highlight_js,
    highlight_python,
    highlight_dark_css,
    highlight_light_css,
    highlight_init_script,
]

app, rt = fast_app(
    pico=False,
    surreal=False,
    htmx=False,
    live=False,    
    hdrs=(styles, head_el, socials, iconify_script, datastar_script, *highlight_scripts),
    htmlkw=dict(lang="en", dir="ltr", data_theme="dark"),
    bodykw=dict(cls="min-h-screen bg-base-100")
)

app.title = "FastHTML + Datastar"
# ============================================================================
#  Home Component Functions
# ============================================================================

def _theme_toggle() -> Div:
        theme_checkbox = Input(
            type='checkbox',
            value="dark",
            cls='theme-controller',
            id='theme-toggle'
        )
        github_link = A(
            IconifyIcon(
                icon="fa:github-alt",
                cls="text-2xl"
            ),
            href="https://github.com/banditburai/ft-datastar", 
            target="_blank",
            rel="noopener noreferrer",
            cls="mr-4 text-base-content flex items-center"
        )
        return Div(
                Div(
                github_link,
                Label(
                    theme_checkbox,
                    IconifyIcon(
                        icon="material-symbols:wb-sunny-rounded", 
                        cls="swap-on text-2xl"
                        ),
                    IconifyIcon(
                        icon="material-symbols:dark-mode-rounded", 
                        cls="swap-off text-2xl"
                        ),            
                    cls='swap swap-rotate text-base-content'
                    ),
                cls="flex items-center"
                ),
            _theme_toggle_script(),
            cls="fixed top-4 right-4 z-50",
            )
            
def _theme_toggle_script() -> Script:
    return Script(f"""
    document.addEventListener('DOMContentLoaded', function() {{
        const themeToggle = document.getElementById('theme-toggle');
        const html = document.documentElement;
        
        // Get themes from config
        const defaultTheme = "dark";
        const altTheme = "light";
        
        // Theme initialization
        const savedTheme = localStorage.getItem('theme');
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const initialTheme = savedTheme || (systemDark ? defaultTheme : altTheme);
        
        // Apply theme
        html.setAttribute('data-theme', initialTheme);
        themeToggle.checked = initialTheme === defaultTheme;

        // Toggle handler
        themeToggle.addEventListener('change', function() {{
            const newTheme = this.checked ? defaultTheme : altTheme;
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        }});
    }});
    """)

def hero_section():
    """Hero section for the homepage."""
    return Div(
        Div(
            _theme_toggle(),
            H1("FastHTML + Datastar", cls="text-4xl md:text-5xl font-black mb-2"),
            P("Interactive examples of Datastar's reactive superpowers", 
              cls="text-xl opacity-80"),
            cls="max-w-3xl"
        ),
        cls="py-16 px-6 md:px-8 border-b border-base-300 bg-base-200"
    )

def intro_section():
    """Introduction section explaining what Datastar is."""
    return Div(
        Div(
            H2("What is Datastar?", cls="text-3xl font-bold mb-6"),
            
            P("""
            A lightweight (14.3 KiB) JavaScript library that adds reactivity to HTML using data-* attributes.
            Use with any backend language and Server-Sent Events for real-time UI updates.
            """, cls="mb-6"),
            

            Div(
                Div(
                    H4("Declarative", cls="font-bold mb-2"),
                    P("""
                    Add reactivity directly to HTML with data-* attributes.
                    """),
                    cls="bg-base-200 p-4 rounded-lg"
                ),
                Div(
                    H4("Signals-Based", cls="font-bold mb-2"),
                    P("""
                    State is managed through reactive signals that automatically
                    track and propagate changes throughout your UI.
                    """),
                    cls="bg-base-200 p-4 rounded-lg"
                ),
                Div(
                    H4("Hypermedia-First", cls="font-bold mb-2"),
                    P("""
                    Embrace the web's natural architecture. Keep logic on the server
                    and your frontend lightweight and focused.
                    """),
                    cls="bg-base-200 p-4 rounded-lg"
                ),
                cls="grid grid-cols-1 md:grid-cols-3 gap-4 my-6"
            ),
            
            Div(
                IconifyIcon(icon="material-symbols:south", cls="text-3xl animate-bounce"),
                cls="flex justify-center mt-6"
            ),
            
            cls="prose max-w-4xl mx-auto"
        ),
        cls="py-12 px-6 md:px-8 border-b border-base-300"
    )

@dataclass
class CodeToggleButton:
    """Toggle button for code visibility with rotation animation."""
    icon: str = field(default="material-symbols:expand-more")
    
    def __ft__(self) -> Any:
        return Span(
            IconifyIcon(
                icon=self.icon, 
                cls="mr-1 details-icon transition-transform duration-200"
            ),
            "VIEW CODE", 
            cls="font-mono text-primary text-xs cursor-pointer flex items-center"
        )

@dataclass
class CodeCopyButton:
    """Button to copy code to clipboard with built-in feedback."""
    code_snippet: str
    
    def __ft__(self) -> Any:
        return Div(
            # Initialize a local signal for copy feedback
            ds_signals(_copied="false"),
            
            Button(
                # Text changes based on copy state
                ds_text("$_copied === 'true' ? 'COPIED!' : 'COPY'"),
                # Use Datastar's clipboard action
                ds_on(click="@clipboard(`" + self.code_snippet + "`); $_copied = 'true'; setTimeout(() => $_copied = 'false', 2000)"),
                cls="btn btn-xs btn-ghost font-mono text-xs text-primary ml-auto"
            ),
            cls="inline"
        )

@dataclass
class CodeHeader:
    """Header for code viewer with toggle and copy buttons."""
    code_snippet: str    
    
    def __ft__(self) -> Any:
        return Summary(
            CodeToggleButton(),
            CodeCopyButton(self.code_snippet),
            cls="flex justify-between items-center p-2 bg-base-100 border-b border-base-content/10"
        )

@dataclass
class CodeContent:
    """Code content area with syntax highlighting."""
    code_snippet: str
    
    def __ft__(self) -> Any:
        # Clean up code snippet by removing leading/trailing blank lines and spaces
        cleaned_code = "\n".join(line for line in self.code_snippet.strip().split("\n"))
        
        return Pre(
            Code(cleaned_code, cls="language-python hljs whitespace-pre-wrap break-words"),
            cls="bg-base-300 p-2 sm:p-4 text-xs sm:text-sm overflow-x-auto rounded-none m-0"
        )

@dataclass
class CodeViewer:
    """Collapsible code sample viewer with brutalist aesthetic."""
    code_snippet: str    
    
    def __ft__(self) -> Any:
        # Clean up code snippet by removing leading/trailing blank lines and spaces
        cleaned_code = "\n".join(line for line in self.code_snippet.strip().split("\n"))
        
        return Div(            
            Details(
                CodeHeader(cleaned_code),
                CodeContent(cleaned_code),
                cls="w-full [&[open]_.details-icon]:rotate-180"
            ),
            cls="border border-base-content/10 mt-2"
        )

@dataclass
class ExampleTitle:
    """Title component for example sections with anchor link."""
    title: str
    id_slug: str
    
    def __ft__(self) -> Any:
        return H2(
            A(self.title, href=f"#{self.id_slug}", cls="no-underline hover:underline"),
            id=self.id_slug, 
            cls="text-3xl font-bold mb-6"
        )

@dataclass
class ExampleHeader:
    """Header section for an example, including title and standalone link."""
    title: str
    id_slug: str
    example_url: str
    
    def __ft__(self) -> Any:
        return Div(
            # Standalone link
            Div(
                A(
                    "View standalone example", 
                    href=self.example_url,
                    target="_blank", 
                    cls="font-mono text-primary text-xs cursor-pointer flex items-center hover:underline gap-1"
                ),
                cls="mb-4 flex justify-end"
            ),            
            ExampleTitle(self.title, self.id_slug),
            cls="mb-4"
        )

@dataclass
class FeatureList:
    """Simple component to render a list of bullet points with properly formatted code blocks."""
    items: List[str]
    title: str = None
    
    def __ft__(self) -> Any:
        # Create the list container
        list_items = [
            Li(
                # Create a bullet point with proper styling
                Div(
                    # The bullet point itself
                    Span("•", cls="text-primary font-bold mr-2 flex-shrink-0"),
                    # Process the item text to handle code blocks
                    Div(
                        *self._process_item_text(item),
                        cls="flex-1"
                    ),
                    cls="flex items-start"
                ),
                cls="mb-3"
            ) for item in self.items
        ]
        
        list_content = Ul(
            *list_items,
            cls="list-none pl-0 mt-2"
        )
        
        # If there's a title, include it before the list
        if self.title:
            return Div(
                Div(self.title, cls="font-bold mb-2"),
                list_content,
                cls="mb-4"
            )
        
        return list_content
    
    def _process_item_text(self, text):
        """Split text by code blocks and return appropriate components."""
        parts = []
        # Split by backticks
        segments = text.split('`')
        
        # Odd indices are code blocks, even indices are regular text
        for i, segment in enumerate(segments):
            if not segment:  # Skip empty segments
                continue
                
            if i % 2 == 1:  # This is a code block
                parts.append(Code(segment, cls="bg-base-300 px-2 py-0.5 mx-1 rounded text-xs font-mono inline-block break-all"))
            else:  # This is regular text
                parts.append(segment)
                
        return parts

@dataclass
class ExampleDescription:
    """Simplified description component that handles paragraphs and lists with titles."""
    description: str
    function_name: str
    function_example: str
    
    def __ft__(self) -> Any:
        # Parse the description to identify paragraphs and lists
        content = []
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in self.description.split('\n\n') if p.strip()]
        
        for paragraph in paragraphs:
            lines = paragraph.strip().split('\n')
            
            # Check if this paragraph is a list with a title
            if len(lines) > 0 and lines[0].strip() and not lines[0].strip().startswith('•') and any(line.strip().startswith('•') for line in lines[1:]):
                # First line is a title, rest are list items
                title = lines[0].strip()
                # Extract the items, removing the bullet point marker
                items = [line.strip()[1:].strip() for line in lines[1:] if line.strip().startswith('•')]
                content.append(FeatureList(items, title=title))
            # Check if this is just a bullet list without a title
            elif any(line.strip().startswith('•') for line in lines):
                # Extract the items, removing the bullet point marker
                items = [line.strip()[1:].strip() for line in lines if line.strip().startswith('•')]
                content.append(FeatureList(items))
            else:
                # Handle regular paragraph with code blocks
                content.append(P(
                    *self._process_paragraph_text(paragraph),
                    cls="mb-4"
                ))
        
        return Div(
            # Function reference with compact layout
            Div(
                Span("Function: ", cls="text-xs uppercase tracking-wide text-base-content/70 block mb-2"),
                Code(
                    self.function_name, 
                    cls="bg-primary/10 px-3 py-2 font-bold inline-block break-all"
                ),
                cls="bg-base-200 px-2 sm:px-4 py-3 sm:py-4 rounded-sm border border-base-300 mb-4 overflow-x-auto"
            ),
            
            # Description content with all paragraphs and lists
            Div(
                *content,
                cls="mb-4 pl-2 sm:pl-4"
            ),
            
            # Usage example
            Div(
                Span("Usage: ", cls="text-xs uppercase tracking-wide text-base-content/70 block mb-2"),
                Code(
                    self.function_example, 
                    cls="bg-primary/10 px-3 py-2 inline-block break-all"
                ),
                cls="bg-base-200 px-2 sm:px-4 py-3 sm:py-4 rounded-sm border border-base-300 overflow-x-auto"
            ),
            cls="mb-6 prose max-w-full"
        )
    
    def _process_paragraph_text(self, text):
        """Process a paragraph to handle code blocks within it."""
        parts = []
        # Split by backticks
        segments = text.split('`')
        
        # Odd indices are code blocks, even indices are regular text
        for i, segment in enumerate(segments):
            if not segment:  # Skip empty segments
                continue
                
            if i % 2 == 1:  # This is a code block
                parts.append(Code(segment, cls="bg-base-300 px-2 py-0.5 rounded text-xs font-mono break-all"))
            else:  # This is regular text
                parts.append(segment)
                
        return parts
    
    
@dataclass
class ExampleDemo:
    """Container for the interactive demo component."""
    example_func: Callable
    
    def __ft__(self) -> Any:
        return Div(
            self.example_func(),
            cls="mb-4 p-4 border border-base-300 bg-base-100"
        )

@dataclass
class ExampleSection:
    """Complete example section component with consistent width and styling."""
    title: str
    id_slug: str
    description: str
    function_name: str
    function_example: str
    code_snippet: str
    example_func: Callable
    example_url: str
    bg_gradient: bool = field(default=False)
    max_width: str = field(default="4xl")
    
    def __ft__(self) -> Any:
        # Background class based on gradient preference
        bg_class = "bg-gradient-to-br from-base-100 to-base-200" if self.bg_gradient else ""
        
        return Div(
            Div(                
                Div(                    
                    ExampleHeader(self.title, self.id_slug, self.example_url),                                        
                    ExampleDescription(
                        self.description, 
                        self.function_name, 
                        self.function_example
                    ),                                        
                    ExampleDemo(self.example_func),                                        
                    CodeViewer(self.code_snippet),                    
                    cls="p-2 sm:p-4 space-y-2 border-2 border-base-300 mb-2 overflow-hidden"
                ),
                cls=f"max-w-{self.max_width} mx-auto w-full"
            ),
            cls=f"py-8 sm:py-16 px-3 sm:px-6 md:px-8 border-b border-base-300 {bg_class} overflow-hidden"
        )

# Basic data-bind example
@rt("/examples/bind")
def bind_example():
    return Div(
        H2("Data Binding Example", cls="text-xl font-bold mb-4"),
        Input(
            ds_bind("input1"),
            cls="input w-full max-w-xs",
            placeholder="Type something..."
        ),
        Div(
            "Current value: ",
            Span(ds_text("$input1")),
            cls="mt-2 p-2 bg-base-200 rounded"
        ),
        cls="p-4 space-y-2"
    )

def data_binding_section():
    """Data binding example section."""
    description = """
Creates a two-way connection between form elements and signals. When users interact with the element, the signal updates automatically.

Works with:
• text inputs
• textarea elements
• select dropdowns
• checkboxes
• radio buttons
• custom web components
"""
    
    code_snippet = """
Input(
    ds_bind("input1"),
    cls="input w-full max-w-xs",
    placeholder="Type something..."
)
Div(
    "Current value: ",
    Span(ds_text("$input1")),
    cls="mt-2 p-2 bg-base-200 rounded"
)
"""    
    return ExampleSection(
        title="Data Binding",
        id_slug="data-binding",
        description=description,
        function_name="ds_bind(signal_name)",
        function_example="Input(ds_bind('input1'), ...)",
        code_snippet=code_snippet,
        example_func = bind_example,
        example_url="/examples/bind",
        bg_gradient=True
    )

# Reactive text example
@rt("/examples/text")
def text_example():
    return Div(
        H2("Reactive Text Example", cls="text-xl font-bold mb-4"),
        Input(
            ds_bind("input2"),
            cls="input w-full max-w-xs",
            placeholder="Type something..."
        ),
        Div(
            "Uppercase: ",
            Span(ds_text("$input2.toUpperCase()")),
            cls="mt-2 p-2 bg-base-200 rounded"
        ),
        cls="p-4 space-y-2"
    )

def data_text_section():
    """Reactive text example section."""
    description = """
Sets an element's text content based on signal values using JavaScript expressions. Great for displaying dynamic output that updates automatically when signals change.

Examples:
• Basic: `$input`
• Transformed: `$input.toUpperCase()`
• Conditional: `$input ? $input : 'Nothing entered'`
• Calculations: `'Length: ' + $input.length`
"""
    
    code_snippet = """
Input(
    ds_bind("input2"),
    cls="input w-full max-w-xs",
    placeholder="Type something..."
),
Div(
    "Uppercase: ",
    Span(ds_text("$input2.toUpperCase()")),
    cls="mt-2 p-2 bg-base-200 rounded"
)
"""    
    return ExampleSection(
        title="Reactive Text",
        id_slug="reactive-text",
        description=description,
        function_name="ds_text(expr)",
        function_example="Span(ds_text('$input.toUpperCase()'))",
        code_snippet=code_snippet,
        example_func=text_example,
        example_url="/examples/text",
        bg_gradient=False
    )


@rt("/examples/computed")
def computed_example():
    return Div(
        H2("Computed Example", cls="text-xl font-bold mb-4"),
        Input(
            ds_bind("input3"),
            cls="input w-full max-w-xs",
            placeholder="Type something..."
        ),
        Div(
            ds_computed(
                doubled="$input3.repeat(2)",
                length="$input3.length"
            )
        ),
        Div(
            "Doubled: ",
            Span(ds_text("$doubled")),
            cls="mb-2"
        ),
        Div(
            "Length of input: ",
            Span(ds_text("$length"))
        ),
        cls="p-4 space-y-2"
    )

def data_computed_section():
    """Computed example section."""
    description = """
Creates new read-only signals derived from reactive expressions. These computed values update automatically when their dependencies change.

Examples:
• Basic calculations: `$input.length`
• Text transformations: `$input.repeat(2)` 
• Complex logic: `$input ? $input.toUpperCase() : 'Nothing entered'`
"""
    
    code_snippet = """
Input(
    ds_bind("input3"),
    cls="input w-full max-w-xs",
    placeholder="Type something..."
),
Div(
    ds_computed(
        doubled="$input3.repeat(2)",
        length="$input3.length"
    )
),
Div(
    "Doubled: ",
    Span(ds_text("$doubled")),
    cls="mb-2"
),
Div(
    "Length of input: ",
    Span(ds_text("$length"))
)
"""    
    return ExampleSection(
        title="Computed Values",
        id_slug="computed-values",
        description=description,
        function_name="ds_computed(name=expr, ...)",
        function_example="Div(ds_computed(doubled='$input.repeat(2)'))",
        code_snippet=code_snippet,
        example_func=computed_example,
        example_url="/examples/computed",
        bg_gradient=True
    )

@rt("/examples/show")
def show_example():
    return Div(
        H2("Show/Hide Example", cls="text-xl font-bold mb-4"),
        Input(
            ds_bind("input4"),
            cls="input w-full max-w-xs",
            placeholder="Type something..."
        ),
        Div(
            "Only shown when input not empty",
            ds_show(when="$input4 != ''"),
            cls="p-2 bg-success text-success-content rounded"
        ),
        cls="p-4 space-y-2"
    )

def data_show_section():
    """Show/hide example section."""
    description = """
Conditionally shows or hides elements based on reactive expressions. Elements are only visible when the expression evaluates to true.

Examples:
• Basic visibility: `$input != ''`
• Inverse condition: `!$input`
• Complex logic: `$count > 10 && $isAdmin`

Syntax:
• Explicit: `ds_show(when="$input != ''")`
• Concise: `ds_show("$input != ''")`
"""
    
    code_snippet = """
Input(
    ds_bind("input4"),
    cls="input w-full max-w-xs",
    placeholder="Type something..."
),
Div(
    "Only shown when input not empty",
    ds_show(when="$input4 != ''"),
    cls="p-2 bg-success text-success-content rounded"
)
"""    
    return ExampleSection(
        title="Conditional Display",
        id_slug="conditional-display",
        description=description,
        function_name="ds_show(when=expr)",
        function_example="Button(ds_show(when='$input != \"\"'), 'Save')",
        code_snippet=code_snippet,
        example_func=show_example,
        example_url="/examples/show",
        bg_gradient=False
    )

@rt("/examples/classes")
def classes_example():
    return Div(
        H2("Dynamic Classes Example", cls="text-xl font-bold mb-4"),
        Input(
            ds_bind("input5"),
            cls="input w-full max-w-xs",
            placeholder="Type something..."
        ),
        Div(
            "This text changes style as you type more",
            ds_classes(
                text_primary="$input5.length > 0",
                font_bold="$input5.length > 3",
                text_2xl="$input5.length > 5"
            ),
            cls="p-2"
        ),
        cls="p-4 space-y-2"
    )

def data_classes_section():
    """Dynamic classes example section."""
    description = """
Conditionally applies CSS classes based on reactive expressions. Classes are added when the expression evaluates to true and removed when false.

Examples:
• Single class: `ds_classes(hidden="$input == ''")`
• Multiple classes (object syntax): `ds_classes(text_primary="$input.length > 0", font_bold="$input.length > 3")`
• Use with TailwindCSS: `ds_classes(bg_error="$isInvalid", text_success="$isValid")`
"""
    
    code_snippet = """
Input(
    ds_bind("input5"),
    cls="input w-full max-w-xs",
    placeholder="Type something..."
),
Div(
    "This text changes style as you type more",
    ds_classes(
        text_primary="$input5.length > 0",
        font_bold="$input5.length > 3",
        text_2xl="$input5.length > 5"
    ),
    cls="p-2"
)
"""    
    return ExampleSection(
        title="Dynamic Classes",
        id_slug="dynamic-classes",
        description=description,
        function_name="ds_classes(**expressions)",
        function_example='Div(ds_classes(text_primary="$input.length > 0"))',
        code_snippet=code_snippet,
        example_func=classes_example,
        example_url="/examples/classes",
        bg_gradient=True
    )

@rt("/examples/attrs")
def attrs_example():
    return Div(
        H2("Dynamic Attributes Example", cls="text-xl font-bold mb-4"),
        Input(
            ds_bind("input6"),
            cls="input w-full max-w-xs",
            placeholder="Type 'red' or 'blue'",
        ),
        Span(
            "Hover over the non-disabled button to see the title in a tooltip",            
            cls="text-sm"
        ),
        Button(
            "Submit",
            ds_attrs(
                disabled="!['red', 'blue'].includes($input6)",                
                title="$input6 ? 'Submit ' + $input6 : 'Enter a valid color'"
            ),
            ds_classes(                
                btn_error="$input6 === 'red'",  # btn-error only applies when red                
                btn_info="$input6 === 'blue'",  # btn-info only applies when blue
                ),            
            cls="btn "
        ),
        cls="p-4 flex flex-col max-w-md space-y-2"
    )

def data_attrs_section() :
    """Dynamic attributes example section."""
    description = """
Reactively sets HTML attributes based on signal values. Attributes are updated automatically when the expressions evaluate to new values.

Examples:
• Single attribute: `ds_attrs(disabled="$input == ''")`
• Multiple attributes: `ds_attrs(disabled="!['red', 'blue'].includes($input)", title="$input ? 'Submit ' + $input : 'Enter a valid color'")`
• Style attribute: `ds_attrs(style="'color: ' + ($isError ? 'red' : 'green')")`
• ARIA attributes: `ds_attrs(aria_expanded="$isOpen", aria_label="$buttonLabel")`
"""
    
    code_snippet = """
Input(
    ds_bind("input6"),
    cls="input w-full max-w-xs",
    placeholder="Type 'red' or 'blue'",
),
Span(
    "Hover over the non-disabled button to see the title in a tooltip",            
    cls="text-sm"
),
Button(
    "Submit",
    ds_attrs(
        disabled="!['red', 'blue'].includes($input6)",                
        title="$input6 ? 'Submit ' + $input6 : 'Enter a valid color'"
    ),
    ds_classes(                
        btn_error="$input6 === 'red'",  # btn-error only applies when red                
        btn_info="$input6 === 'blue'",  # btn-info only applies when blue
        ),            
    cls="btn"
)
"""    
    return ExampleSection(
        title="Dynamic Attributes",
        id_slug="dynamic-attributes",
        description=description,
        function_name="ds_attrs(**expressions)",
        function_example='Button(ds_attrs(disabled="$isEmpty"), "Save")',
        code_snippet=code_snippet,
        example_func=attrs_example,
        example_url="/examples/attrs",
        bg_gradient=False
    )

@rt("/examples/signals")
def signals_example():
    return Div(
        H2("Signals Example", cls="text-xl font-bold mb-6"),
        Div(
            ds_signals(count="75")
            ),
        # Basic Signal Section
        Div(
            H3("Basic Signal", cls="text-lg font-semibold mb-2"),                       
            
            Div(
                "Current value: ",
                Span(ds_text("$count"), cls="font-mono"),
                " / 100",
                cls="mb-2"
            ),
            Progress(
                ds_attrs(value="$count", max="100"),
                cls="progress progress-primary w-full"
            ),
            cls="mb-8 p-4 bg-base-200 rounded-lg"
        ),

        # Namespaced Signal Section
        Div(
            H3("Namespaced Signals", cls="text-lg font-semibold mb-2"),
            Div(
                ds_signals(
                    user__name="''",
                    user__email="''"
                )
            ),
            Div(
                Input(
                    ds_bind("user.name"),
                    placeholder="Enter your name",
                    cls="input w-full mb-2"
                ),
                Input(
                    ds_bind("user.email"),
                    placeholder="Enter your email",
                    cls="input w-full",
                    type="email"
                ),
                cls="space-y-2 mb-4"
            ),
            Div(
                "Name: ",
                Span(ds_text("$user.name || 'Anonymous'"), cls="font-mono"),
                cls="mb-2"
            ),
            Div(
                "Email includes @: ",
                Span(
                    ds_text("$user.email.includes('@') ? '✅' : '❌'"),                    
                ),
                cls="flex items-center gap-2"
            ),
            cls="p-4 bg-base-200 rounded-lg"
        ),
        
        cls="p-6 space-y-6 max-w-2xl mx-auto"
    )


def data_signals_section():
    """Signal initialization example section."""
    description = """
Initializes reactive signals that can be accessed throughout your application. Signals are the foundation of Datastar's reactivity system.

Examples:
• Basic signal: `ds_signals(count="0")` - Numbers don't need quotes in JavaScript
• String signal: `ds_signals(name="'Anonymous'")` - Strings require quotes in JavaScript (inner quotes)
• Boolean signal: `ds_signals(isAdmin="false")` - JavaScript booleans are lowercase
• Multiple signals: `ds_signals(count="0", name="'User'", isAdmin="false")` - Define several at once
• Namespaced signals: `ds_signals(user__name="'Anonymous'")` - Double underscore becomes dot notation
• JSON objects: `ds_signals(user=json_dumps({"name": "", "email": ""}))` - For complex nested data
"""
    
    code_snippet = """
Div(
    ds_signals(
        user__name="''",
        user__email="''"
    )
),
Div(
    Input(
        ds_bind("user.name"),
        placeholder="Enter your name",
        cls="input w-full mb-2"
    ),
    Input(
        ds_bind("user.email"),
        placeholder="Enter your email",
        cls="input w-full",
        type="email"
    ),
    cls="space-y-2 mb-4"
),
Div(
    "Name: ",
    Span(ds_text("$user.name || 'Anonymous'"), cls="font-mono"),
    cls="mb-2"
),
Div(
    "Email includes @: ",
    Span(
        ds_text("$user.email.includes('@') ? '✅' : '❌'"),                    
    ),
    cls="flex items-center gap-2"
),
cls="p-4 bg-base-200 rounded-lg"
)
"""    
    return ExampleSection(
        title="Signal Initialization",
        id_slug="signal-initialization",
        description=description,
        function_name="ds_signals(**signal_values)",
        function_example='Div(ds_signals(count="0", name="\'User\'"))',
        code_snippet=code_snippet,
        example_func=signals_example,
        example_url="/examples/signals",
        bg_gradient=True
    )

@rt("/examples/events")
def events_example():
    return Div(
        H2("Events Example", cls="text-xl font-bold mb-4"),
        Div(
            "Using signals we default the starting count to 5",
            ds_signals(count2="5")
        ),
        Button(
            "Increment",
            ds_on(click="$count2++"),
            cls="btn btn-primary mr-2"
        ),
        Button(
            "Reset",
            ds_on(click="$count2 = 0"),
            cls="btn btn-warning"
        ),
        Div(
            "Count: ",
            Span(ds_text("$count2"), cls="font-mono"),
            cls="mt-2"
        ),
        cls="p-4 space-y-2"
    )

def data_events_section():
    """Event handling example section."""
    description = """
Attaches event listeners to elements that execute JavaScript expressions when triggered. This enables interactive UI without writing custom JavaScript functions.

Examples:
• Simple actions: `ds_on(click="$count++")`
• Multiple statements: `ds_on(click="$count = 0; $message = 'Reset'")`
• DOM access: `ds_on(input="$value = evt.target.value")`
• Conditional logic: `ds_on(keydown="if(evt.key === 'Enter') $submit = true")`
• Server actions: `ds_on(click="@post('/api/data')")`

The special `evt` variable gives access to the browser's native event object, allowing you to access properties like `evt.target`, `evt.key`, etc.
"""
    
    code_snippet = """
Button(
    "Increment",
    ds_on(click="$count2++"),
    cls="btn btn-primary mr-2"
),
Button(
    "Reset",
    ds_on(click="$count2 = 0"),
    cls="btn btn-warning"
),
Div(
    "Count: ",
    Span(ds_text("$count2"), cls="font-mono"),
    cls="mt-2"
)
"""    
    return ExampleSection(
        title="Event Handling",
        id_slug="event-handling",
        description=description,
        function_name="ds_on(**event_handlers)",
        function_example='Button(ds_on(click="$count++"), "Increment")',
        code_snippet=code_snippet,
        example_func=events_example,
        example_url="/examples/events",
        bg_gradient=False
    )

@rt("/client-quiz")
def quiz_example():
    return Div(
        # Define initial signals
        Div(
            ds_signals(
                response="''",
                answer="bread"
                ),        
            ds_computed(
                correct="$response.toLowerCase() == $answer"
                ),
        ),
        
        # Quiz interface
        Div(
            "What do you put in a toaster?",
            id="question",
            cls="text-lg font-bold mb-4"
        ),
        
        # Answer button
        Button(
            "BUZZ",
            ds_on(click="$response = prompt('Answer:') ?? ''"),
            cls="btn btn-primary mb-4"
        ),
        
        # Response display
        Div(
            ds_show(when="$response != ''"), # Only show when response exists
            "You answered ",
            Span(ds_text("$response"), cls="font-mono"),
            " . ",
            
            # Correct answer feedback
            Span(
                ds_show(when="$correct"),
                "That is correct. ✅",                
            ),
            
            # Wrong answer feedback
            Span(
                ds_show(when="!$correct"),
                "The correct answer is ",
                Span(ds_text("$answer"), cls="font-mono"),
                ". 🤷",                
            ),                        
            cls="space-y-2"
        ),
        cls="p-6 max-w-lg mx-auto"
    )


def data_client_quiz_section():
    """Client-side quiz example section."""
    description = """
This example demonstrates a simple interactive quiz using Datastar's client-side reactivity features.

Key concepts:
• Signal initialization with `ds_signals` for state management
• Computed values with `ds_computed` for answer validation
• Event handling with `ds_on` for user interaction
• Conditional rendering with `ds_show` for dynamic feedback
• Text interpolation with `ds_text` for displaying values

While the initial HTML is served from a route, all quiz interactions happen entirely in the browser without additional server requests. This makes it simple to implement but limits it to using hardcoded questions.
"""
    
    code_snippet = """
# Define initial signals
Div(
    ds_signals(
        response="''",
        answer="bread"
        ),        
    ds_computed(
        correct="$response.toLowerCase() == $answer"
        ),
),

# Quiz interface
Div(
    "What do you put in a toaster?",
    id="question",
    cls="text-lg font-bold mb-4"
),

# Answer button
Button(
    "BUZZ",
    ds_on(click="$response = prompt('Answer:') ?? ''"),
    cls="btn btn-primary mb-4"
),

# Response display with conditional feedback
Div(
    ds_show(when="$response != ''"),
    "You answered ",
    Span(ds_text("$response"), cls="font-mono"),
    " . ",
    
    # Correct answer feedback
    Span(
        ds_show(when="$correct"),
        "That is correct. ✅",                
    ),
    
    # Wrong answer feedback
    Span(
        ds_show(when="!$correct"),
        "The correct answer is ",
        Span(ds_text("$answer"), cls="font-mono"),
        ". 🤷",                
    ),
    cls="space-y-2"
)
"""
    
    return ExampleSection(
        title="Client-Side Quiz",
        id_slug="client-quiz",
        description=description,
        function_name="ds_signals, ds_computed, ds_on, ds_show, ds_text",
        function_example='Button(ds_on(click="$response = prompt(\'Answer:\')"), "Answer")',
        code_snippet=code_snippet,
        example_func=quiz_example,
        example_url="/examples/quiz",
        bg_gradient=True
    )


@rt("/backend_quiz")
def backend_quiz_example():
    return Div(
        H2("SSE Merge Signals Example", cls="text-xl font-bold mb-4"),
        # Define initial signals
        Div(
            ds_signals(
                question2=json_dumps(""),
                response2=json_dumps(""),
                answer2=json_dumps("")
                ),        
            ds_computed(
                correct2="$response2.toLowerCase() == $answer2"
                ),
        ),        
                
        Button(
            "Fetch New question",
            ds_on(click="@get('/actions/quiz'); $response2 = ''"),  # ← Add inline reset for dual client + server side clearing
            id="fetch-btn",            
            cls="btn btn-accent gap-2 mb-4"
        ),
        Div(
            ds_text("$question2 ?? 'Click above to get a question'"),
            id="question2",
            cls="text-lg font-bold mb-4"
        ),
        Button(
            ds_show(when="$answer2 != ''"), # only shown when question is fetched
            "BUZZ",
            ds_on(click="$response2 = prompt('Answer:') ?? ''"),
            cls="btn btn-primary mb-4"
        ),
         # Dynamic question display
       
        # Response display
        Div(
            ds_show(when="$response2 != ''"), # Only show when response exists
            "You answered ",
            Span(ds_text("$response2"), cls="font-mono"),
            " . ",
            
            # Correct answer feedback
            Span(
                ds_show(when="$correct2"),
                "That is correct. ✅",                
            ),
            
            # Wrong answer feedback
            Span(
                ds_show(when="!$correct2"),
                "The correct answer is ",
                Span(ds_text("$answer2"), cls="font-mono"),
                ". 🤷",                
            ),                        
            cls="space-y-2"
        ),
        cls="p-6 max-w-lg mx-auto"
    )

@rt("/actions/quiz")
@sse
async def quiz_action():
    QUESTIONS = [
        {"question": "What do you put in a toaster?", "answer": "bread"},
        {"question": "What has keys but can't open locks?", "answer": "piano"},
        {"question": "What gets wetter as it dries?", "answer": "towel"},
        {"question": "What has a head and a tail but no body?", "answer": "coin"},
        {"question": "What can travel around the world while staying in a corner?", "answer": "stamp"},
        {"question": "What has a neck but no head?", "answer": "bottle"},
        {"question": "What is full of holes but still holds water?", "answer": "sponge"},
        {"question": "What has a thumb and four fingers but is not alive?", "answer": "glove"},
        {"question": "What goes up but never comes down?", "answer": "age"},
        {"question": "What belongs to you but others use it more than you?", "answer": "name"}
        ]    
    qna = random.choice(QUESTIONS)
    question_fragment = Div(
        qna["question"],
        id="question2",
        cls="text-lg font-bold mb-4"
    )
    
    # Update the question fragment with proper selector and merge mode
    yield fragment_update(question_fragment, selector="#question2", merge_mode="morph")
    
    # Update the signals
    yield signal_update(
        question2=qna["question"],
        answer2=qna["answer"],
        response2=""
    )

def data_server_quiz_section():
    """Server-side enhanced quiz example section."""
    description = """
Building on the client-side quiz, this example demonstrates how to enhance the experience with server-side functionality using Server-Sent Events (SSE).

Key enhancements:
• Server communication with the `@get` directive for dynamic content
• Questions fetched from the server during user interaction
• Real-time UI updates with SSE without page reloads
• Server-side signal updates with `signal_update`
• HTML fragment updates with `fragment_update`

Unlike the previous example where all interaction happens in the browser, this quiz makes additional server requests during use to fetch new questions and answers, demonstrating how Datastar bridges client and server functionality.
"""
    
    code_snippet = """
# Client-side component
Div(
    # Define initial signals
    Div(
        ds_signals(
            question2=json_dumps(""),
            response2=json_dumps(""),
            answer2=json_dumps("")
            ),        
        ds_computed(
            correct2="$response2.toLowerCase() == $answer2"
            ),
    ),        
            
    Button(
        "Fetch New question",
        ds_on(click="@get('/actions/quiz'); $response2 = ''"),
        cls="btn btn-accent gap-2 mb-4"
    ),
    Div(
        ds_text("$question2 ?? 'Click above to get a question'"),
        id="question2",
        cls="text-lg font-bold mb-4"
    ),
    Button(
        ds_show(when="$answer2 != ''"),
        "BUZZ",
        ds_on(click="$response2 = prompt('Answer:') ?? ''"),
        cls="btn btn-primary mb-4"
    ),
    
    # Response display with conditional feedback
    Div(
        ds_show(when="$response2 != ''"),
        "You answered ",
        Span(ds_text("$response2"), cls="font-mono"),
        Span(ds_show(when="$correct2"), "That is correct. ✅"),
        Span(
            ds_show(when="!$correct2"),
            "The correct answer is ",
            Span(ds_text("$answer2"), cls="font-mono"),
            ". 🤷",                
        ),
        cls="space-y-2"
    )
)

# Server-side handler
@rt("/actions/quiz")
@sse
async def quiz_action():
    # Select random question from database
    qna = random.choice(QUESTIONS)
    
    # Create a fragment to update the question display
    question_fragment = Div(
        qna["question"],
        id="question2",
        cls="text-lg font-bold mb-4"
    )
    
    # Update the question fragment with proper selector and merge mode
    yield fragment_update(question_fragment, selector="#question2", merge_mode="morph")
    
    # Update the signals
    yield signal_update(
        question2=qna["question"],
        answer2=qna["answer"],
        response2=""
    )
"""
    
    return ExampleSection(
        title="Server-Enhanced Quiz",
        id_slug="server-quiz",
        description=description,
        function_name="@get, signal_update, fragment_update",
        function_example='Button(ds_on(click="@get(\'/actions/quiz\')"), "Fetch Question")',
        code_snippet=code_snippet,
        example_func=backend_quiz_example,
        example_url="/examples/quiz",
        bg_gradient=False
    )

@rt("/examples/quiz")
def combined_quiz_section():
    """Dedicated page that showcases both quiz examples with comparison."""
    return Div(
        H2("Interactive Quiz Examples", cls="text-2xl font-bold mb-6"),
        
        P("""
        These examples demonstrate how to build interactive quizzes with Datastar, 
        showing the progression from client-side to server-side functionality.
        """, cls="mb-6"),
        
        # Cards for each example
        Div(
            # Client-side quiz card
            Div(
                H3("Client-Side Quiz", cls="text-xl font-bold mb-2"),
                P("""
                A quiz that handles all user interactions in the browser after initial page load.
                No additional server requests are made during quiz interaction.
                
                Demonstrates basic reactivity, computed values, and conditional rendering.
                """, cls="mb-4"),
                A(
                    "View Example",
                    href="/client-quiz",
                    cls="btn btn-primary"
                ),
                cls="p-6 bg-base-200 rounded-lg"
            ),
            
            # Server-side quiz card
            Div(
                H3("Server-Enhanced Quiz", cls="text-xl font-bold mb-2"),
                P("""
                An enhanced quiz that makes additional server requests during interaction.
                Uses Server-Sent Events (SSE) to fetch questions from the server and update the UI in real-time.
                
                Demonstrates how Datastar bridges client and server functionality.
                """, cls="mb-4"),
                A(
                    "View Example",
                    href="/backend_quiz",
                    cls="btn btn-accent"
                ),
                cls="p-6 bg-base-200 rounded-lg"
            ),
            
            cls="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8"
        ),             
        
        # Link back to homepage
        Div(
            A(
                "← Back to All Examples",
                href="/",
                cls="text-primary hover:underline"
            ),
            cls="mt-8"
        ),
        
        cls="container mx-auto px-4 py-8 max-w-4xl"
    )

@rt("/minimal-test")
def minimal_test_ui():
    return Div(
        # Initialize signals
        ds_signals({
            "minimalSignal": 0,
            "testParam": json_dumps(""),  # camelCase JS signal
            "processedResult": "''"
        }),
        
        # Input with kebab-case binding
        Input(
            ds_bind("testParam"),  # HTML attribute
            placeholder="Enter test value",
            cls="input input-bordered w-full mb-4"
        ),
        
        # Display original signal
        Div(
            "Original value: ",
            Span(ds_text("$testParam"), cls="font-mono"),
            cls="mb-2"
        ),
        
        # Display processed result
        Div(
            "Processed result: ",
            Span(ds_text("$processedResult"), cls="font-mono"),
            cls="mb-4"
        ),
        
        # Button with parameter passing
        Button(
            "Process Value",
            ds_on(click="@post('/api/minimal-post')"),
            ds_indicator("minimal.loading"),
            cls="btn btn-primary gap-2"
        ),
        
        cls="p-6 max-w-md mx-auto"
    )

@rt("/api/minimal-post", methods=["POST"])
@sse
async def minimal_post_example(testParam: str):        
    processed = f"Processed: {testParam.upper()}"
    yield "signals", {
        "processedResult": json_dumps(processed),
        "minimalSignal": "prev => prev + 1"
    }

def data_sse_routes_section():
    """Section that explains how SSE routes are set up and used."""
    description = """
Datastar provides a powerful way to create server routes that can send real-time updates to the client using Server-Sent Events (SSE).

Key concepts:
• The `@sse` decorator marks a route as an SSE endpoint
• SSE routes can yield multiple updates to the client
• `fragment_update` replaces or modifies HTML elements
• `signal_update` changes signal values without reloading the page

Route setup:
• Create a route with `@rt("/your/path")` 
• Add the `@sse` decorator to enable streaming
• Use `yield` to send updates to the client
• Client connects using `@get`, `@post`, etc. directives
"""
    
    code_snippet = """
# Client-side component
@rt("/minimal-test")
def minimal_test_ui():
    return Div(
        # Initialize signals
        ds_signals({
            "minimalSignal": 0,
            "testParam": json_dumps(""),  # camelCase JS signal
            "processedResult": "''"
        }),
        
        # Input with binding
        Input(
            ds_bind("testParam"),  # HTML attribute
            placeholder="Enter test value",
            cls="input input-bordered w-full mb-4"
        ),
        
        # Display original signal
        Div(
            "Original value: ",
            Span(ds_text("$testParam"), cls="font-mono"),
            cls="mb-2"
        ),
        
        # Display processed result
        Div(
            "Processed result: ",
            Span(ds_text("$processedResult"), cls="font-mono"),
            cls="mb-4"
        ),
        
        # Button with parameter passing
        Button(
            "Process Value",
            ds_on(click="@post('/api/minimal-post')"),
            ds_indicator("minimal.loading"),
            cls="btn btn-primary gap-2"
        ),
        
        cls="p-6 max-w-md mx-auto"
    )

# Server-side SSE route
@rt("/api/minimal-post", methods=["POST"])
@sse
async def minimal_post_example(testParam: str):        
    # Process the input and update signals
    processed = f"Processed: {testParam.upper()}"
    
    yield signal_update(
        processedResult=json_dumps(processed),
        minimalSignal="prev => prev + 1"  # Increment using a function
    )
"""
    
    return ExampleSection(
        title="Server-Sent Events Routes",
        id_slug="sse-routes",
        description=description,
        function_name="@sse, signal_update, fragment_update",
        function_example='@rt("/api/data") @sse async def handler(): yield signal_update(...)',
        code_snippet=code_snippet,
        example_func=minimal_test_ui,
        example_url="/minimal-test",
        bg_gradient=True
    )

@rt("/indicator-demo")
def indicator_demo():
    return Div(                       
        # Button with loading states
        Button(
            Span("Load Data", ds_show(when="!$fetching")),
            Span("Loading...", ds_show(when="$fetching")),
            ds_on(click="@get('/actions/load-data')"),
            ds_indicator("fetching"),
            cls="btn btn-primary"
        ),
        
        # Spinner indicator (using DaisyUI classes)
        Div(
            ds_classes(
                loading="$fetching",
                hidden="!$fetching"
            ),
            cls="loading loading-spinner ml-2"
        ),        
        cls="p-4 flex items-center gap-2"
    )

@rt("/actions/load-data")
@sse
async def load_data_action():        
    await asyncio.sleep(2)
    yield signal_update(data=json_dumps("Loaded!"))


def data_indicator_section():
    """Create the indicator example section."""
    description = """
    The `ds_indicator` function sets the value of a signal to `true` while a request is in flight, and `false` otherwise. 
    This is particularly useful for showing loading indicators during slower responses.
    
    • Use `ds_indicator("signal_name")` to create a signal that tracks the loading state
    • The signal will be `true` during the request and `false` when complete
    • Combine with `ds_show` or `ds_classes` to create responsive loading states
    • Works with all HTTP methods: GET, POST, PUT, PATCH, and DELETE
    
    On the server side, you need to use the `@sse` decorator on your route handler and yield updates using `signal_update()`. This allows the server to send real-time updates to the client while maintaining the loading state correctly.
    """
    
    function_name = "ds_indicator(signal_name)"
    function_example = 'Button("Load Data", ds_on(click="@get(\'/api/data\')"), ds_indicator("loading"))'
    
    code_snippet = """
@rt("/indicator-demo")
def indicator_demo():
    return Div(                       
        # Button with loading states
        Button(
            Span("Load Data", ds_show(when="!$fetching")),
            Span("Loading...", ds_show(when="$fetching")),
            ds_on(click="@get('/actions/load-data')"),
            ds_indicator("fetching"),
            cls="btn btn-primary"
        ),
        
        # Spinner indicator (using DaisyUI classes)
        Div(
            ds_classes(
                loading="$fetching",
                hidden="!$fetching"
            ),
            cls="loading loading-spinner ml-2"
        ),        
        cls="p-4 flex items-center gap-2"
    )

@rt("/actions/load-data")
@sse
async def load_data_action():    
    # Simulate a slow operation
    await asyncio.sleep(2)
    
    # Send data back to the client
    # The ds_indicator signal will automatically be set to false when this completes
    yield signal_update(data=json_dumps("Loaded!"))
"""
    
    return ExampleSection(
        title="Loading Indicators with ds_indicator",
        id_slug="indicator",
        description=description,
        function_name=function_name,
        function_example=function_example,
        code_snippet=code_snippet,
        example_func=indicator_demo,
        example_url="/indicator-demo",
        bg_gradient=True
    )


@rt("/examples/setall")
def setall_example():
    OPTIONS = [
    ("option1", "Option 1"),
    ("option2", "Option 2"), 
    ("option3", "Option 3")
    ]
    return Div(
        # Initialize checkbox signals
        Div(
             ds_signals({
            "checkboxes": json_dumps({
                "option1": False,
                "option2": False,
                "option3": False
            })
        }),
        ),
        
        # Checkbox group
        Div(
            # Generate checkboxes dynamically
            *[
                Label(
                    Input(                        
                        ds_bind(f"checkboxes.{opt}"),  # Dot notation for object access
                        type="checkbox",                        
                        id=opt,                        
                        cls="checkbox checkbox-primary"
                    ),
                    text,
                    cls="flex items-center gap-2"
                )
                for opt, text in OPTIONS
            ],
            cls="space-y-2 mb-4"
        ),
        
        # Control buttons
        Div(
            Button(
                "Check All",
                ds_on(click="@setAll('checkboxes.', true)"),
                cls="btn btn-sm btn-success mr-2"
            ),
            Button(
                "Uncheck All", 
                ds_on(click="@setAll('checkboxes.', false)"),
                cls="btn btn-sm btn-error"
            ),
            Button(
                "Toggle All",
                ds_on(click="@toggleAll('checkboxes.')"),
                cls="btn btn-sm btn-warning"
            ),
            cls="flex gap-2"
        ),
        Div(
            "Selected: ",
            Span(
                ds_text(
                    "[" + 
                    ",".join([f"{{name:'{text}',value:$checkboxes.{opt}}}" for opt, text in OPTIONS]) + 
                    "].filter(i=>i.value).map(i=>i.name).join(', ')"
                ),
                cls="font-mono"
            ),            
            cls="mt-4"
        ),
        cls="p-4 bg-base-200 rounded-lg"
    )


def data_setall_section():
    """Create the setAll and toggleAll example section."""
    description = """
    Datastar provides two powerful actions for manipulating multiple signals at once: `@setAll()` and `@toggleAll()`.
    
    • `@setAll(prefix, value)` sets all signals that match the prefix to the specified value
    • `@toggleAll(prefix)` toggles the boolean value of all signals that match the prefix
    • Both actions are perfect for working with form fields, checkboxes, and other grouped elements
    • The prefix is used to match against signal names (e.g., 'checkboxes.' will match 'checkboxes.option1', 'checkboxes.option2', etc.)
    
    These actions are especially useful when working with forms or collections of related inputs, allowing you to manipulate multiple values with a single click.
    """
    
    function_name = "@setAll(prefix, value) / @toggleAll(prefix)"
    function_example = 'Button("Check All", ds_on(click="@setAll(\'checkboxes.\', true)"))'
    
    code_snippet = """
@rt("/examples/setall")
def setall_example():
    OPTIONS = [
    ("option1", "Option 1"),
    ("option2", "Option 2"), 
    ("option3", "Option 3")
    ]
    return Div(
        # Initialize checkbox signals
        Div(
             ds_signals({
            "checkboxes": json_dumps({
                "option1": False,
                "option2": False,
                "option3": False
            })
        }),
        ),
        
        # Checkbox group
        Div(
            # Generate checkboxes dynamically
            *[
                Label(
                    Input(                        
                        ds_bind(f"checkboxes.{opt}"),  # Dot notation for object access
                        type="checkbox",                        
                        id=opt,                        
                        cls="checkbox checkbox-primary"
                    ),
                    text,
                    cls="flex items-center gap-2"
                )
                for opt, text in OPTIONS
            ],
            cls="space-y-2 mb-4"
        ),
        
        # Control buttons
        Div(
            Button(
                "Check All",
                ds_on(click="@setAll('checkboxes.', true)"),
                cls="btn btn-sm btn-success mr-2"
            ),
            Button(
                "Uncheck All", 
                ds_on(click="@setAll('checkboxes.', false)"),
                cls="btn btn-sm btn-error"
            ),
            Button(
                "Toggle All",
                ds_on(click="@toggleAll('checkboxes.')"),
                cls="btn btn-sm btn-warning"
            ),
            cls="flex gap-2"
        ),
        Div(
            "Selected: ",
            Span(
                ds_text(
                    "[" + 
                    ",".join([f"{{name:'{text}',value:$checkboxes.{opt}}}" for opt, text in OPTIONS]) + 
                    "].filter(i=>i.value).map(i=>i.name).join(', ')"
                ),
                cls="font-mono"
            ),            
            cls="mt-4"
        ),
        cls="p-4 bg-base-200 rounded-lg"
    )
"""
    
    return ExampleSection(
        title="Bulk Signal Actions with @setAll and @toggleAll",
        id_slug="setall-toggleall",
        description=description,
        function_name=function_name,
        function_example=function_example,
        code_snippet=code_snippet,
        example_func=setall_example,
        example_url="/examples/setall",
        bg_gradient=True
    )


@rt("/complex-example-ui")
def complex_example_ui():
    return Div(
        # Initialize signals
        ds_signals({
            "complex_loading": "false",
            "complex_request_count": 0,
            "complex_result": "''"
        }),
        
        # Control section
        Div(
            Button(
                "Start Complex Process",
                ds_on(click="@post('/api/complex-example')"),
                ds_indicator("complex_loading"),
                cls="btn btn-primary gap-2",                
            ),
            Div(
                "Requests made: ",
                Span(
                    ds_text("$complex_request_count"),
                    cls="font-mono"
                ),
                cls="text-sm mt-2"
            ),
            cls="p-4 bg-base-200 rounded-lg"
        ),
        
        # Status container
        Div(
            id="complex-status-container",
            cls="space-y-4 mt-4",
            # Dynamic fragments will be inserted here
        ),
        
        # Result display
        Div(
            ds_show("$complex_result !== ''"),
            "Final result: ",
            Span(
                ds_text("$complex_result"),
                cls="font-mono text-success"
            ),
            cls="mt-4 p-2 bg-base-300 rounded"
        ),
        
        cls="mx-auto p-4 max-w-2xl"
    )

@rt("/api/complex-example", methods=["POST"])
@sse
async def complex_handler(testParam: str = ""):
    try:
        # Initial signal update
        yield signal_update(
            complex_loading="true",
            complex_request_count="prev => prev + 1"
        )
        
        await asyncio.sleep(1)

        # Deliberately throw an exception
        # raise ValueError("This is a test error")
        # First fragment update
        status_update = Div(
            Div(
                IconifyIcon(icon="fa6-solid:spinner", cls="animate-spin mr-2"),
                Span("Processing..."),
                cls="flex items-center"
            ),
            cls="alert alert-info"
        )
        
        yield fragment_update(status_update, "#complex-status-container", "inner")
        
        await asyncio.sleep(2)
        
        # Final fragment update
        final_status = Div(
            Span("Process completed successfully!"),
            cls="alert alert-success"
        )
        
        yield fragment_update(final_status, "#complex-status-container", "inner")
        
        # Final signal update
        yield signal_update(
            complex_loading="false",
            complex_result=json_dumps(testParam.upper() or "COMPLETED")
        )
    
    except Exception as e:
        # Handle errors gracefully
        error_message = f"Error: {str(e)}"
        yield fragment_update(
            Div(error_message, cls="alert alert-error"),
            "#complex-status-container", 
            "append"
        )
        yield signal_update(
            complex_loading="false",
            complex_result=json_dumps(error_message)
        )


def data_complex_example_section():
    """Create the complex example section with server-side processing and fragment updates."""
    description = """
    This advanced example demonstrates how to create a more complex interaction between client and server using DataStar's features:
    
    • Multi-step server processing with real-time UI updates
    • Combining signal updates and fragment updates in a single request
    • Error handling with graceful UI feedback
    • Progress indicators with dynamic content insertion
    • Stateful counters that persist between requests
    
    The example shows a pattern for long-running operations where you want to keep the user informed about progress. This approach is ideal for file uploads, data processing, or any task that requires multiple steps with visual feedback.
    """
    
    function_name = "signal_update(), fragment_update()"
    function_example = 'yield fragment_update(status_component, "#container", "inner")'
    
    code_snippet = """
@rt("/complex-example-ui")
def complex_example_ui():
    return Div(
        # Initialize signals
        ds_signals({
            "complex_loading": "false",
            "complex_request_count": 0,
            "complex_result": "''"
        }),
        
        # Control section
        Div(
            Button(
                "Start Complex Process",
                ds_on(click="@post('/api/complex-example')"),
                ds_indicator("complex_loading"),
                cls="btn btn-primary gap-2",                
            ),
            Div(
                "Requests made: ",
                Span(
                    ds_text("$complex_request_count"),
                    cls="font-mono"
                ),
                cls="text-sm mt-2"
            ),
            cls="p-4 bg-base-200 rounded-lg"
        ),
        
        # Status container
        Div(
            id="complex-status-container",
            cls="space-y-4 mt-4",
            # Dynamic fragments will be inserted here
        ),
        
        # Result display
        Div(
            ds_show("$complex_result !== ''"),
            "Final result: ",
            Span(
                ds_text("$complex_result"),
                cls="font-mono text-success"
            ),
            cls="mt-4 p-2 bg-base-300 rounded"
        ),
        
        cls="mx-auto p-4 max-w-2xl"
    )

@rt("/api/complex-example", methods=["POST"])
@sse
async def complex_handler(testParam: str = ""):
    try:
        # Initial signal update
        yield signal_update(
            complex_loading="true",
            complex_request_count="prev => prev + 1"
        )
        
        await asyncio.sleep(1)

        # First fragment update
        status_update = Div(
            Div(
                IconifyIcon(icon="fa6-solid:spinner", cls="animate-spin mr-2"),
                Span("Processing..."),
                cls="flex items-center"
            ),
            cls="alert alert-info"
        )
        
        yield fragment_update(status_update, "#complex-status-container", "inner")
        
        await asyncio.sleep(2)
        
        # Final fragment update
        final_status = Div(
            Span("Process completed successfully!"),
            cls="alert alert-success"
        )
        
        yield fragment_update(final_status, "#complex-status-container", "inner")
        
        # Final signal update
        yield signal_update(
            complex_loading="false",
            complex_result=json_dumps(testParam.upper() or "COMPLETED")
        )
    
    except Exception as e:
        # Handle errors gracefully
        error_message = f"Error: {str(e)}"
        yield fragment_update(
            Div(error_message, cls="alert alert-error"),
            "#complex-status-container", 
            "append"
        )
        yield signal_update(
            complex_loading="false",
            complex_result=json_dumps(error_message)
        )
"""
    
    return ExampleSection(
        title="Advanced Server Processing with Fragment Updates",
        id_slug="complex-example",
        description=description,
        function_name=function_name,
        function_example=function_example,
        code_snippet=code_snippet,
        example_func=complex_example_ui,
        example_url="/complex-example-ui",
        bg_gradient=False
    )


# Main homepage route with modular components
@rt("/")
def homepage():
    """Main homepage with modular sections."""
    return Div(
        # Initialize state for code copy buttons
        Div(ds_signals(copied_states="{}")),
        
        # Hero and intro sections
        hero_section(),        
        Div(
            H2("Interactive Todo App", cls="text-3xl font-bold text-center mb-6"),
            P("See Datastar in action with this reactive todo app. Add tasks, toggle completion, and filter - all with real-time UI updates.", 
            cls="mb-8 max-w-2xl mx-auto"),
            TodoContainer(todos_store.items),            
            cls="py-16 px-6 md:px-8 border-b border-base-300 bg-base-200"
        ),
        intro_section(),
        
        # Example sections
        data_binding_section(),
        data_text_section(),
        data_computed_section(),
        data_show_section(),
        data_classes_section(),
        data_attrs_section(),
        data_signals_section(),
        data_events_section(),
        data_client_quiz_section(),                
        data_server_quiz_section(),
        data_sse_routes_section(),
        data_indicator_section(),
        data_setall_section(),
        data_complex_example_section(),

        # Standalone Todo App link before footer
        Div(
            H2("You've reached the end!", cls="text-3xl font-bold text-center mb-4"),
            P("Get building! Or explore the standalone Todo app some more.", 
              cls="text-center mb-6 max-w-2xl mx-auto"),
            Div(
                A(
                    "I have things to do!",
                    href="/todo",
                    cls="btn btn-lg btn-primary"
                ),
                cls="text-center"
            ),
            cls="py-16 px-6 md:px-8 border-t border-base-300 bg-base-200"
        ),
        Footer(
            P("Built with Datastar and FastHTML", cls="text-center"),
            cls="p-6 bg-base-300 border-t border-base-content/10"
        ),
        
        cls="min-h-screen bg-base-100"
    )

# ============================================================================
#  Todo Example
# ============================================================================

@dataclass
class TodoItem:
    """Individual todo item component."""
    id: int
    text: str
    completed: bool = False
    
    def __ft__(self) -> Any:
        # Define variables for conditional rendering
        checkbox_icon = "material-symbols:check-box-outline" if self.completed else "material-symbols:check-box-outline-blank"
        text_class = f"flex-1 text-lg {'line-through opacity-50' if self.completed else ''}"
        
        return Li(
            # Checkbox for toggling completion status
            Label(
                ds_on(click=f"@post('/api/todos/{self.id}/toggle')"),
                IconifyIcon(icon=checkbox_icon, cls="opacity-60 text-5xl sm:text-4xl"),
                cls="cursor-pointer touch-manipulation min-w-[40px] flex items-center justify-center sm:pt-2",                
            ),
            
            # Text display with contenteditable for inline editing
            Span(
                self.text,
                # Keydown just sets activeEditId and triggers blur
                ds_on(keydown="if (evt.key !== 'Enter' || evt.shiftKey) return; evt.preventDefault(); $activeEditId = evt.target.closest('li').id.split('-')[1]; $edited_text = evt.target.innerText.trim(); evt.target.blur()"),
                # Single POST happens here in the blur handler with improved empty text handling
                ds_on(blur="const editedText = evt.target.innerText.trim(); if (!editedText) { evt.target.innerText = this.text; return; } $edited_text = editedText; @post('/api/todos/' + $activeEditId + '/update'); $activeEditId = -1"),
                # Focus handler to initialize editing and store original text
                # uses a local var for early exit if text is empty and restoring original text
                ds_on(focus="$activeEditId = evt.target.closest('li').id.split('-')[1]; this.originalText = this.text"),
                cls=f"{text_class} input py-3 px-2 sm:p-3 h-auto min-h-12 border-none outline-none font-mono whitespace-pre-wrap break-words overflow-x-auto",
                contenteditable="true",                
                id=f"todo-text-{self.id}",              
            ),
                                   
            # Delete button - always visible on mobile for better UX
            Button(
                ds_on(click=f"@delete('/api/todos/{self.id}')"),   
                IconifyIcon(icon="material-symbols:close", cls="text-base"),
                cls="sm:invisible border-2 border-base-300 bg-transparent hover:bg-error hover:text-error-content hover:border-error min-w-[30px] h-[30px] w-[30px] flex items-center justify-center group-hover:visible rounded-none font-mono text-xs mt-2.5",                                         
            ),
            
            cls="flex items-start gap-2 sm:gap-4 py-4 px-2 sm:p-3 group border-b border-base-300 hover:bg-base-200 transition-colors",
            id=f"todo-{self.id}",            
        )

@dataclass
class TodoList:
    """List of todo items with dynamic rendering."""
    items: List[TodoItem]
    
    def __ft__(self) -> Any:
        if not self.items:
            return Div(
                "No tasks match the current filter",
                cls="py-6 sm:py-8 text-center text-base-content/50 font-mono text-sm sm:text-base",
                id="todos_list"
            )
        
        return Ul(
            *[item for item in self.items],
            cls="divide-y divide-base-300 bg-base-100 border border-base-300 rounded-sm shadow-sm w-full max-w-full overflow-hidden",
            id="todos_list",            
        )

@dataclass
class TodoHeader:
    """Header section with title and input field."""
    def __ft__(self) -> Any:
        return Header(
            # Main title
            H1("TASKS", cls="text-3xl sm:text-5xl font-bold font-mono tracking-tight text-center sm:text-left px-2 sm:px-0"),
            
            # Progress bar
            Div(
                # The wrapper div
                Div(
                    # The actual progress bar with color transitions
                    Div(
                        ds_attrs(
                            style="'width: ' + $completion_percentage + '%; background: hsl(' + (120 * ($completion_percentage/100)) + ', 80%, 50%)'"
                        ),
                        cls="h-3 sm:h-4 transition-all duration-500"
                    ),
                    cls="w-full bg-base-300 h-3 sm:h-4 rounded-none"
                ),
                # Percentage display
                Span(
                    ds_text("$completion_percentage + ' %'"),
                    cls="text-xs font-mono"
                ),
                cls="mt-2 mb-4 sm:mb-6 w-full px-2 sm:px-0"
            ),
            
            # Input field area
            Div(
                Input(                    
                    ds_bind("input_value"),
                    ds_on(keydown="if (evt.key !== 'Enter' || !$input_value.trim().length) return; @post('/api/todos'); $input_value = '';"),                    
                    cls="w-full italic input input-md sm:input-lg border border-base-300 rounded-none placeholder:text-base-content/30 font-mono",
                    placeholder="What needs to be done?",
                    enterkeyhint="enter",
                    id="todo_input",                    
                ),
                cls="w-full mb-4 px-2 sm:px-0"
            ),
            
            cls="w-full mb-4 sm:mb-6"
        )

@dataclass
class TodoFilterBar:
    """Top filter bar with view controls."""
    current_mode: str = "all"
    
    def __ft__(self) -> Any:
        return Div(
            # All controls in a single row that will wrap naturally on smaller screens
            Div(
                # Left side - Filter label and buttons
                Div(
                    # Label
                    Div(
                        IconifyIcon(icon="material-symbols:filter-list", cls="text-xl"),
                        "FILTER:",
                        cls="flex items-center gap-2 font-bold font-mono"
                    ),
                    
                    # Filter buttons
                    Button(
                        ds_on(click="@put('/api/todos/filter/all')"),
                        "ALL", 
                        ds_classes({
                            "bg-primary text-primary-content": "$current_mode === 'all'",
                            "bg-base-200": "$current_mode !== 'all'"
                        }),
                        cls="btn btn-sm font-mono",
                    ),
                    Button(
                        "ACTIVE",
                        ds_on(click="@put('/api/todos/filter/active')"),
                        ds_classes({
                            "bg-primary text-primary-content": "$current_mode === 'active'",
                            "bg-base-200": "$current_mode !== 'active'"
                        }),
                        cls="btn btn-sm font-mono",
                    ),
                    Button(
                        "COMPLETED",
                        ds_on(click="@put('/api/todos/filter/completed')"),
                        ds_classes({
                            "bg-primary text-primary-content": "$current_mode === 'completed'",
                            "bg-base-200": "$current_mode !== 'completed'"
                        }),
                        cls="btn btn-sm font-mono",
                    ),
                    cls="flex flex-wrap items-center gap-2"
                ),
                
                # Spacer that pushes the second group to the right on larger screens
                Div(cls="flex-grow"),
                
                # Right side controls - toggle/clear/reset
                Div(
                    Button(
                        ds_on(click="@post('/api/todos/toggle-all')"),
                        IconifyIcon(icon="material-symbols:select-all"),
                        "TOGGLE ALL",
                        cls="btn btn-sm bg-base-200 font-mono",
                    ),
                    Button(
                        ds_on(click="@delete('/api/todos/completed')"),
                        IconifyIcon(icon="material-symbols:delete-sweep"),
                        "CLEAR COMPLETED",
                        cls="btn btn-sm bg-error text-error-content font-mono",
                    ),
                    Button(
                        ds_on(click="@put('/api/todos/reset')"),
                        IconifyIcon(icon="material-symbols:restart-alt"),
                        "RESET",
                        cls="btn btn-sm bg-warning text-warning-content font-mono",
                    ),
                    cls="flex flex-wrap gap-2"
                ),
                
                cls="flex flex-col sm:flex-row sm:items-center gap-4 flex-wrap"
            ),
            
            cls="p-4 bg-base-200 mb-6 border-y border-base-300",
            id="todo_filter_bar"
        )

@dataclass
class TodoFooter:
    """Footer with counters."""
    active_count: int
    current_mode: str = "all"
    
    def __ft__(self) -> Any:
        return Footer(
            Span(
                ds_text("$active_count + ' ITEMS LEFT'"),
                cls="font-mono font-bold text-xs sm:text-sm"
            ),
            cls="py-3 sm:py-4 px-2 sm:px-0 flex justify-between text-sm text-base-content/70"
        )

@dataclass
class TodoContainer:
    """Main todos container component."""
    items: List[TodoItem]
    mode: str = "all"  # 'all', 'active', 'completed'
    lifetime_completed_count: int = 0  # Track completed tasks even after deletion
    
    def __ft__(self) -> Any:
        # Filter items based on mode
        filtered_items = self.items
        if self.mode == "active":
            filtered_items = [item for item in self.items if not item.completed]
        elif self.mode == "completed":
            filtered_items = [item for item in self.items if item.completed]
        
        stats = calculate_todo_stats(self.items, self.lifetime_completed_count)
        
        # Initialize signals
        signals = {
            "active_count": stats["active_count"],
            "current_mode": self.mode,
            "input_value": "''",
            "edited_text": "''",
            "activeEditId": "-1",  # No todo is being edited initially
            "completion_percentage": stats["completion_percentage"]
        }
        
        return Div(
            # Initialize signals
            Div(ds_signals(signals)),
            Div(                
                TodoHeader(),
                TodoFilterBar(current_mode=self.mode),                                
                Div(
                    TodoList(filtered_items),
                    cls="w-full overflow-hidden" 
                ),                                
                TodoFooter(active_count=int(stats["active_count"]), current_mode=self.mode),                
                cls="w-full max-w-full sm:max-w-xl md:max-w-2xl lg:max-w-3xl mx-auto"
            ),
            
            id="todos_container",
            cls="container mx-auto px-2 sm:px-4 md:px-6 py-4 md:py-10 font-sans"
        )

# Store simulation (replace with real persistence)
todos_store = TodoContainer(
    items=[
        TodoItem(0, "Learn Python", True),
        TodoItem(1, "Learn Datastar"),
        TodoItem(2, "???"),
        TodoItem(3, "Profit")
    ]
)

# ============================================================================
# Helper functions
# ============================================================================

def get_active_count(items):
    """Calculate active count."""
    return sum(1 for item in items if not item.completed)

def get_filtered_items(items, mode):
    """Get filtered items based on mode."""
    if mode == "active":
        return [item for item in items if not item.completed]
    elif mode == "completed":
        return [item for item in items if item.completed]
    return items  # "all" mode or any other value

def find_item(items, todo_id):
    """Find a todo item by ID."""
    return next((i for i in items if i.id == todo_id), None)

def calculate_todo_stats(items, lifetime_completed_count=0):
    """Calculate all todo stats in one place, including lifetime achievements."""
    active_count = get_active_count(items)
    total_count = len(items)
    current_completed_count = sum(1 for item in items if item.completed)
    
    # Total completed includes both current completed and previously cleared ones
    total_completed = current_completed_count + lifetime_completed_count
    # Total items includes active items and all completed items (including cleared ones)
    adjusted_total = active_count + total_completed
    
    # Calculate percentage based on all completed tasks (even deleted ones)
    # divided by the adjusted total number of tasks
    completion_percentage = 0
    if adjusted_total > 0:
        completion_percentage = int((total_completed / adjusted_total) * 100)
    
    return {
        "active_count": str(active_count),
        "total_count": str(total_count),
        "completed_count": str(current_completed_count),
        "completion_percentage": str(completion_percentage)
    }

def handle_errors(func):
    """Decorator to handle errors consistently in SSE endpoints."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            async for update in func(*args, **kwargs):
                yield update
        except Exception as e:
            error_message = f"Error: {str(e)}"
            yield fragment_update(
                Div(error_message, cls="alert alert-error"),
                "#todos_container",
                "append"
            )
    return wrapper

# ============================================================================
# API Routes
# ============================================================================

@rt("/api/todos", methods=["POST"])
@sse
@handle_errors
async def add_todo(input_value: str):
    """Add a new todo item"""    
    new_id = max([item.id for item in todos_store.items], default=-1) + 1
    new_todo = TodoItem(id=new_id, text=input_value or "New Todo")
    todos_store.items.append(new_todo)
    
    # A new todo is always active (not completed), so it's visible 
    # in "all" and "active" modes, but not in "completed" mode
    if todos_store.mode != "completed":
        yield fragment_update(new_todo, "#todos_list", "append")
    
    # Get updated stats
    stats = calculate_todo_stats(todos_store.items, todos_store.lifetime_completed_count)
    yield signal_update(
        active_count=stats["active_count"],
        completion_percentage=stats["completion_percentage"]
    )

@rt("/api/todos/completed", methods=["DELETE"])
@sse
@handle_errors
async def delete_completed():
    """Delete all completed todos"""    
    completed_count = sum(1 for item in todos_store.items if item.completed)
    todos_store.lifetime_completed_count += completed_count
    todos_store.items = [item for item in todos_store.items if not item.completed]
    
    filtered_items = get_filtered_items(todos_store.items, todos_store.mode)
    yield fragment_update(TodoList(filtered_items), "#todos_list", "inner")
    stats = calculate_todo_stats(todos_store.items, todos_store.lifetime_completed_count)
    yield signal_update(
        active_count=stats["active_count"],
        completion_percentage=stats["completion_percentage"]
    )

@rt("/api/todos/{todo_id}", methods=["DELETE"])
@sse
@handle_errors
async def delete_todo(todo_id: str):
    """Delete a todo item by id"""
    todo_id = int(todo_id)
    
    # Check if the item being deleted is completed, to update lifetime counter
    item = find_item(todos_store.items, todo_id)
    if item and item.completed:
        todos_store.lifetime_completed_count += 1        
    todos_store.items = [item for item in todos_store.items if item.id != todo_id]
        
    yield fragment_update("", f"#todo-{todo_id}", "outer")
    stats = calculate_todo_stats(todos_store.items, todos_store.lifetime_completed_count)
    yield signal_update(
        active_count=stats["active_count"],
        completion_percentage=stats["completion_percentage"]
    )

@rt("/api/todos/{todo_id}/toggle", methods=["POST"])
@sse
@handle_errors
async def toggle_todo(todo_id: str):
    """Toggle completion status of a todo"""
    todo_id = int(todo_id)        
    item = find_item(todos_store.items, todo_id)
    if not item:
        raise ValueError(f"Todo with ID {todo_id} not found")
    
    item.completed = not item.completed
    
    yield fragment_update(item, f"#todo-{item.id}", "outer")
    stats = calculate_todo_stats(todos_store.items, todos_store.lifetime_completed_count)
    yield signal_update(
        active_count=stats["active_count"],
        completion_percentage=stats["completion_percentage"]
    )

@rt("/api/todos/toggle-all", methods=["POST"])
@sse
@handle_errors
async def toggle_all_todos():
    """Toggle completion status of all todos"""    
    all_completed = all(item.completed for item in todos_store.items)
    for item in todos_store.items:
        item.completed = not all_completed
    
    filtered_items = get_filtered_items(todos_store.items, todos_store.mode)
    yield fragment_update(TodoList(filtered_items), "#todos_list", "inner")
    
    # Get updated stats
    stats = calculate_todo_stats(todos_store.items, todos_store.lifetime_completed_count)
    
    yield signal_update(
        active_count=stats["active_count"],
        completion_percentage=stats["completion_percentage"]
    )

@rt("/api/todos/{todo_id}/update", methods=["POST"])
@sse
@handle_errors
async def update_todo(todo_id: str, edited_text: str):
    """Update todo text"""
    todo_id = int(todo_id)
    item = find_item(todos_store.items, todo_id)
    if not item:
        raise ValueError(f"Todo with ID {todo_id} not found")
    
        item.text = edited_text
    
    yield fragment_update(item, f"#todo-{item.id}", "outer")
    stats = calculate_todo_stats(todos_store.items, todos_store.lifetime_completed_count)
    yield signal_update(completion_percentage=stats["completion_percentage"])

@rt("/api/todos/filter/{mode}", methods=["PUT"])
@sse
@handle_errors
async def filter_todos(mode: str):
    """Filter todos by mode"""    
    todos_store.mode = mode
    filtered_items = get_filtered_items(todos_store.items, mode)
    yield fragment_update(TodoList(filtered_items), "#todos_list", "inner")
    yield signal_update(current_mode=mode)

@rt("/api/todos/reset", methods=["PUT"])
@sse
@handle_errors
async def reset_todos():
    """Reset todos to default state"""    
    todos_store.items = [
        TodoItem(0, "Learn Python", True),
        TodoItem(1, "Learn Datastar"),
        TodoItem(2, "???"),
        TodoItem(3, "Profit")
    ]
    todos_store.mode = "all"
    todos_store.lifetime_completed_count = 0
    
    yield fragment_update(TodoList(todos_store.items), "#todos_list", "inner")
    stats = calculate_todo_stats(todos_store.items, todos_store.lifetime_completed_count)
    yield signal_update(
        active_count=stats["active_count"],
        current_mode="all",
        completion_percentage=stats["completion_percentage"]
    )

@rt("/todo")
def get():
    """Main todo app route"""
    return Div(
        Div(
            TodoContainer(todos_store.items),
            cls="min-h-screen flex items-start sm:items-center justify-center py-2 sm:py-4 px-0 sm:px-4"
        ),
        cls="min-h-screen bg-base-100"
    )

@rt("/version")
def version_info():
    return {"version": __version__}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5001,
        log_level="info",
        reload=False
    )