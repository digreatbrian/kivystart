"""
A lightweight template renderer for Kivy projects.

This class allows for basic template rendering with dynamic content. It supports:
- Variable interpolation using `[[ variable_name ]]`.
- Simple conditional statements (`if`/`else`) to control content flow.

Unlike full-fledged templating engines such as Jinja2, this renderer is designed for simplicity and is not intended for complex use cases. It does **not support** nested conditionals or advanced logic. It is ideal for basic templating needs in Kivy-based applications.

Features:
- Basic variable interpolation: Replace placeholders with values from the provided context.
- Simple conditionals: Supports `[[ if condition ]]` and `[[ else ]]` for basic flow control.
- Lightweight and easy to integrate into Kivy projects.

Example Usage:
    renderer = KivyTemplateRenderer()  # Initialize the renderer
    renderer.set_context({'appname': 'KivyStarter'})  # Set the context with dynamic data

    template = '''
    Welcome to the Kivy app!

    [[ if appname ]]
    App name: [[ appname ]]
    [[ else ]]
    App name not provided.
    [[ endif ]]
    '''

    # Render the template with the given context
    rendered_content = renderer.render(template)

    print(rendered_content)
    
    # Output:
    # Welcome to the Kivy app!
    # App name: KivyStarter

Limitations:
- Does not support nested `if/else` statements.
- Only basic conditional logic and variable replacement are supported.

Notes:
- This renderer replaces the positions for expressions eg. ([[ if ]], [[ else ]], [[ endif ]]) with empty string and this means
   the placeholder for the expression will not be a newline but rather nothing (empty string).

This renderer is ideal for lightweight template processing in Kivy-based projects, where simplicity and minimalism are preferred.
"""
import re
import ast

from typing import Dict, Any


class KivyTemplateRenderer:
    """
    A simple template rendering engine that supports:
    - Variable placeholders
    - Conditional statements (if/else) at any location
    - Python expressions
    
    The syntax is cleaner and more intuitive, using:
    - [[ variable_name ]] for placeholders
    - [[ if condition ]]...[[ else ]]...[[ endif ]] for conditionals
    - [[ some_python_expression ]] for inline Python expressions
    """

    def __init__(self):
        """Initializes the renderer with an empty context."""
        self.context = {}

    def set_context(self, context: dict):
        """Sets the context for rendering templates."""
        self.context = context

    def render(self, template_content: str) -> str:
        """
        Renders the template content by replacing placeholders, evaluating expressions, 
        and handling conditionals.
        """
        template_content = self._render_conditionals(template_content)
        template_content = self._evaluate_python_expressions(template_content)
        template_content = self._render_placeholders(template_content)
        template_content = self._replace_unknown_variables(template_content)
        return template_content

    def _render_placeholders(self, content: str) -> str:
        """Replaces placeholders like [[ variable ]] with context values."""
        pattern = r"\[\[\s*(\w+)\s*\]\]"
        matches = re.findall(pattern, content)

        for match in matches:
            if match in self.context:
                content = content.replace(f"[[ {match} ]]", str(self.context[match]))
            else:
                content = content.replace(f"[[ {match} ]]", f"[[ {match} ]]")
        return content

    def _evaluate_python_expressions(self, content: str) -> str:
        """Evaluates inline Python expressions inside [[ expression ]]."""
        pattern = r"\[\[\s*([^]]+)\s*\]\]"
        matches = re.findall(pattern, content)

        for match in matches:
            try:
                result = self._safe_eval(match)
                content = content.replace(f"[[ {match} ]]", str(result))
            except Exception as e:
                content = content.replace(f"[[ {match} ]]", f"[[ {match} ]]")
        return content

    def _safe_eval(self, expression: str):
        """Safely evaluates a Python expression using a restricted environment."""
        def is_assignment(expression):
            """
            Checks whether the expression is not an assignment.
            """
            if expression.count('=') % 2 != 0:
                return True
            return False
            
        if is_assignment(expression):
            # expression is an assignment
            return False
            
        try:
            tree = ast.parse(expression, mode='eval')
            compiled = compile(tree, filename="<string>", mode="eval")
            return eval(compiled, {"__builtins__": None}, self.context)
        except TypeError as e:
            if "'NoneType' object is not subscriptable" in str(e):
                # used unknown variable in expression
                return None
            raise 
            
        except Exception:
            raise ValueError(f"Error evaluating expression: {expression}")

    def _render_conditionals(self, content: str) -> str:
        """Processes [[ if condition ]]...[[ else ]]...[[ endif ]] blocks."""
        pattern = r"([^\S\n]*\n)?([^\S\n]*)\[\[\s*if\s+(.+?)\s*\]\]([\s\S]*?)(?:\[\[\s*else\s*\]\]([\s\S]*?))?\[\[\s*endif\s*\]\]([^\S\n]*\n)?"
    
        def process_match(match):
            leading_newline, leading_whitespace, condition, true_block, false_block, trailing_whitespace = match.groups()
            leading_newline = leading_newline or ""
            trailing_whitespace = trailing_whitespace or ""
            leading_whitespace = leading_whitespace or ""
            
            try:
                condition_result = self._safe_eval(condition)
                true_block = true_block.strip()
                false_block = false_block.strip() if false_block else ""
                if condition_result:
                    return leading_newline + leading_whitespace + true_block + trailing_whitespace if true_block else ""
                else:
                    return leading_newline + leading_whitespace + false_block + trailing_whitespace if false_block else ""
            except Exception as e:
                raise ValueError(f"Error evaluating if condition '{condition}': {e}")
    
        content = re.sub(pattern, lambda m: process_match(m), content, flags=re.DOTALL)
        return content
        
    def _replace_unknown_variables(self, content: str) -> str:
        """Replaces unknown variables with an empty string."""
        pattern = r"\[\[\s*(\w+)\s*\]\]"
        return re.sub(pattern, "", content)
