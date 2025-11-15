# Gradio 6 Boilerplate & Tutorial Guide

A comprehensive guide to building interactive web UIs with Gradio 6, including forms, radio buttons, and dynamic UI updates.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Basic Examples](#basic-examples)
- [Forms and Radio Buttons](#forms-and-radio-buttons)
- [Dynamic UI Updates](#dynamic-ui-updates)
- [Advanced Patterns](#advanced-patterns)
- [Mobile-Friendly Tips](#mobile-friendly-tips)
- [Deployment](#deployment)

---

## Installation

### Requirements
- Python 3.10 or higher
- pip package manager

### Install Gradio

```bash
# Basic installation
pip install gradio

# Upgrade to latest version
pip install --upgrade gradio
```

### Recommended: Virtual Environment Setup

```bash
# Create virtual environment
python -m venv gradio_env

# Activate (Linux/Mac)
source gradio_env/bin/activate

# Activate (Windows)
gradio_env\Scripts\activate

# Install Gradio
pip install gradio
```

### Verify Installation

```python
import gradio as gr
print(gr.__version__)  # Should show 5.0.0 or higher for Gradio 6
```

---

## Quick Start

### Hello World Example

```python
import gradio as gr

def greet(name):
    return f"Hello {name}!"

demo = gr.Interface(
    fn=greet,
    inputs="text",
    outputs="text"
)

demo.launch()
```

**Running the App:**
- From script: `python app.py` → Opens at http://localhost:7860
- With hot reload: `gradio app.py` → Auto-reloads on file changes

### Simple Interface with Multiple Inputs

```python
import gradio as gr

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
)

demo.launch()
```

---

## Basic Examples

### 1. Text Processing App

```python
import gradio as gr

def upper_case(text):
    return text.upper()

demo = gr.Interface(
    fn=upper_case,
    inputs=gr.Textbox(
        lines=3,
        placeholder="Enter text here...",
        label="Input Text"
    ),
    outputs=gr.Textbox(
        label="Output",
        show_copy_button=True
    ),
    title="Text Transformer",
    description="Convert text to uppercase",
    examples=[
        ["hello world"],
        ["gradio is awesome"],
        ["python programming"]
    ]
)

demo.launch()
```

### 2. Multiple Input Components

```python
import gradio as gr

def process_inputs(text, number, choice):
    return f"Text: {text}\nNumber: {number}\nChoice: {choice}"

demo = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Textbox(label="Enter text"),
        gr.Slider(0, 100, label="Choose a number"),
        gr.Dropdown(["Option A", "Option B", "Option C"], label="Select option")
    ],
    outputs="text",
    title="Multi-Input Demo"
)

demo.launch()
```

### 3. Image Processing Example

```python
import gradio as gr
import numpy as np

def flip_image(img):
    return np.fliplr(img)

demo = gr.Interface(
    fn=flip_image,
    inputs=gr.Image(),
    outputs=gr.Image(),
    title="Image Flipper",
    description="Upload an image to flip it horizontally"
)

demo.launch()
```

---

## Forms and Radio Buttons

### Calculator with Radio Buttons

Complete example showing forms with multiple input types:

```python
import gradio as gr

def calculator(num1, operation, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            return "Error: Division by zero"
        return num1 / num2

with gr.Blocks() as demo:
    gr.Markdown("# Simple Calculator")

    with gr.Row():
        with gr.Column():
            num_1 = gr.Number(value=4, label="First Number")
            operation = gr.Radio(
                ["add", "subtract", "multiply", "divide"],
                label="Operation",
                value="add"
            )
            num_2 = gr.Number(value=0, label="Second Number")
            submit_btn = gr.Button(value="Calculate", variant="primary")

        with gr.Column():
            result = gr.Number(label="Result")

    # Set up examples
    examples = gr.Examples(
        examples=[
            [5, "add", 3],
            [10, "divide", 2],
            [4, "multiply", 2.5],
            [7, "subtract", 1.2]
        ],
        inputs=[num_1, operation, num_2]
    )

    submit_btn.click(
        calculator,
        inputs=[num_1, operation, num_2],
        outputs=[result]
    )

if __name__ == "__main__":
    demo.launch()
```

### Form with Dropdown and Radio

```python
import gradio as gr

def personalized_greeting(name, age, title):
    return f"Hello {title} {name}! You are {age} years old."

with gr.Blocks() as demo:
    gr.Markdown("## User Information Form")

    with gr.Row():
        name = gr.Textbox(label="Name", placeholder="Enter your name")
        age = gr.Number(label="Age", value=25)

    title = gr.Radio(
        ["Mr.", "Ms.", "Dr.", "Prof."],
        label="Title",
        value="Mr."
    )

    submit = gr.Button("Submit")
    output = gr.Textbox(label="Greeting", interactive=False)

    submit.click(
        personalized_greeting,
        inputs=[name, age, title],
        outputs=output
    )

demo.launch()
```

---

## Dynamic UI Updates

### Dynamic Textbox Visibility

```python
import gradio as gr

def change_textbox(choice):
    if choice == "short":
        return gr.Textbox(lines=2, visible=True, placeholder="Write a short essay")
    elif choice == "long":
        return gr.Textbox(
            lines=8,
            visible=True,
            value="Lorem ipsum dolor sit amet...",
            placeholder="Write a long essay"
        )
    else:
        return gr.Textbox(visible=False)

with gr.Blocks() as demo:
    gr.Markdown("# Dynamic Text Input")

    radio = gr.Radio(
        ["short", "long", "none"],
        label="What kind of essay would you like to write?",
        value="short"
    )

    text = gr.Textbox(lines=2, interactive=True, show_copy_button=True)

    radio.change(fn=change_textbox, inputs=radio, outputs=text)

demo.launch()
```

### Conditional UI Updates

```python
import gradio as gr

def update_ui(mode):
    if mode == "Basic":
        return {
            advanced_options: gr.Column(visible=False),
            result: gr.Textbox(value="Basic mode selected")
        }
    else:
        return {
            advanced_options: gr.Column(visible=True),
            result: gr.Textbox(value="Advanced mode selected")
        }

with gr.Blocks() as demo:
    mode = gr.Radio(["Basic", "Advanced"], label="Mode", value="Basic")

    with gr.Column(visible=False) as advanced_options:
        option1 = gr.Checkbox(label="Option 1")
        option2 = gr.Slider(0, 100, label="Option 2")

    result = gr.Textbox(label="Status")

    mode.change(
        update_ui,
        inputs=mode,
        outputs=[advanced_options, result]
    )

demo.launch()
```

### Update Multiple Components

```python
import gradio as gr

def update_examples(country):
    if country == "USA":
        return gr.Dataset(samples=[["Chicago"], ["Little Rock"], ["San Francisco"]])
    else:
        return gr.Dataset(samples=[["Islamabad"], ["Karachi"], ["Lahore"]])

with gr.Blocks() as demo:
    dropdown = gr.Dropdown(
        label="Country",
        choices=["USA", "Pakistan"],
        value="USA"
    )
    textbox = gr.Textbox(label="City")
    examples = gr.Examples([["Chicago"], ["Little Rock"], ["San Francisco"]], textbox)

    dropdown.change(update_examples, dropdown, examples.dataset)

demo.launch()
```

---

## Advanced Patterns

### Tab-Based Interface

```python
import gradio as gr
import numpy as np

def flip_image(img):
    return np.fliplr(img)

def greet_user(name):
    return f"How are you, {name}?"

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Custom UI with Blocks")

    with gr.Tabs():
        with gr.TabItem("Image Flipper"):
            with gr.Row():
                image_input = gr.Image()
                image_output = gr.Image()
            image_button = gr.Button("Flip Image")

        with gr.TabItem("Greeter"):
            name_input = gr.Textbox(label="Name")
            greeting_output = gr.Textbox(label="Greeting")
            greet_button = gr.Button("Greet")

    # Define interactions
    image_button.click(fn=flip_image, inputs=image_input, outputs=image_output)
    greet_button.click(fn=greet_user, inputs=name_input, outputs=greeting_output)

demo.launch()
```

### Accordion and Layout

```python
import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("# Advanced Layout Demo")

    with gr.Accordion("Settings", open=False):
        setting1 = gr.Checkbox(label="Enable feature 1")
        setting2 = gr.Slider(0, 100, label="Threshold")

    with gr.Row():
        with gr.Column(scale=2):
            input_text = gr.Textbox(label="Input", lines=5)
            submit = gr.Button("Process", variant="primary")

        with gr.Column(scale=1):
            output_text = gr.Textbox(label="Output", lines=5)

    def process(text, feat1, threshold):
        result = f"Text: {text}\nFeature 1: {feat1}\nThreshold: {threshold}"
        return result

    submit.click(
        process,
        inputs=[input_text, setting1, setting2],
        outputs=output_text
    )

demo.launch()
```

### ChatBot Interface

```python
import gradio as gr
import random

def random_response(message, history):
    responses = [
        "That's interesting!",
        "Tell me more about that.",
        "I see what you mean.",
        "Could you elaborate?",
        "That's a great point!"
    ]
    return random.choice(responses)

demo = gr.ChatInterface(
    fn=random_response,
    title="Simple Chatbot",
    description="A chatbot that responds randomly",
    examples=["Hello!", "How are you?", "What's new?"]
)

demo.launch()
```

### Real-Time Updates

```python
import gradio as gr
import time

def slow_process(text):
    for i in range(5):
        time.sleep(0.5)
        yield f"Processing step {i+1}/5: {text}"
    yield f"Complete! Final result: {text.upper()}"

with gr.Blocks() as demo:
    input_box = gr.Textbox(label="Input")
    output_box = gr.Textbox(label="Output")
    btn = gr.Button("Process")

    btn.click(slow_process, inputs=input_box, outputs=output_box)

demo.launch()
```

---

## Mobile-Friendly Tips

### Responsive Layout

```python
import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("# Mobile-Friendly Demo")

    # Use columns that stack on mobile
    with gr.Row():
        with gr.Column(min_width=300):  # Minimum width ensures mobile stacking
            input1 = gr.Textbox(label="Input 1")
            input2 = gr.Textbox(label="Input 2")

        with gr.Column(min_width=300):
            output = gr.Textbox(label="Output")

    # Large buttons for mobile
    submit = gr.Button("Submit", size="lg")

demo.launch()
```

### Best Practices for Mobile

1. **Use appropriate component sizes:**
   ```python
   # Good for mobile
   gr.Button("Submit", size="lg")
   gr.Textbox(label="Input", lines=3)  # Not too tall
   ```

2. **Avoid excessive horizontal layouts:**
   ```python
   # Better for mobile - stacks vertically
   with gr.Column():
       input1 = gr.Textbox()
       input2 = gr.Textbox()
   ```

3. **Use responsive themes:**
   ```python
   with gr.Blocks(theme=gr.themes.Soft()) as demo:
       # Soft theme is mobile-friendly
       pass
   ```

4. **Test with mobile viewport:**
   ```python
   # Set custom CSS for mobile optimization
   css = """
   @media (max-width: 768px) {
       .container { padding: 10px; }
   }
   """

   with gr.Blocks(css=css) as demo:
       pass
   ```

---

## Deployment

### Local Development

```bash
# Standard launch
python app.py

# With hot reload
gradio app.py

# With AI assistance
gradio --vibe app.py
```

### Share with Others

```python
import gradio as gr

demo = gr.Interface(fn=my_function, inputs="text", outputs="text")
demo.launch(share=True)  # Generates public URL
```

### Deploy to Hugging Face Spaces

1. **Create account** at huggingface.co
2. **Create new Space** with Gradio SDK
3. **Create files:**

**requirements.txt:**
```
gradio>=4.0.0
numpy
pillow
```

**app.py:**
```python
import gradio as gr

def greet(name):
    return f"Hello {name}!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

if __name__ == "__main__":
    demo.launch()
```

4. **Push to Space** (auto-deploys)

### Environment Variables

```python
import gradio as gr
import os

# Access secrets
API_KEY = os.getenv("API_KEY")

def process(text):
    # Use API_KEY here
    return f"Processed with key: {API_KEY[:4]}..."

demo = gr.Interface(fn=process, inputs="text", outputs="text")
demo.launch()
```

---

## Complete Boilerplate Template

Here's a complete, production-ready template combining all concepts:

```python
import gradio as gr
import numpy as np

# ============================================
# HELPER FUNCTIONS
# ============================================

def process_text(text, mode, intensity):
    """Process text based on selected mode."""
    if mode == "uppercase":
        result = text.upper()
    elif mode == "lowercase":
        result = text.lower()
    elif mode == "title":
        result = text.title()
    else:
        result = text

    # Apply intensity
    return result * int(intensity)

def process_image(image):
    """Process image - example: flip horizontally."""
    if image is None:
        return None
    return np.fliplr(image)

def chatbot_response(message, history):
    """Simple chatbot logic."""
    return f"You said: {message}"

# ============================================
# UI COMPONENTS
# ============================================

def create_text_interface():
    """Create text processing tab."""
    with gr.TabItem("Text Processor"):
        with gr.Row():
            with gr.Column():
                text_input = gr.Textbox(
                    label="Input Text",
                    placeholder="Enter text here...",
                    lines=3
                )
                mode = gr.Radio(
                    ["uppercase", "lowercase", "title", "none"],
                    label="Processing Mode",
                    value="uppercase"
                )
                intensity = gr.Slider(
                    1, 5,
                    value=1,
                    step=1,
                    label="Repeat Intensity"
                )
                process_btn = gr.Button("Process Text", variant="primary")

            with gr.Column():
                text_output = gr.Textbox(
                    label="Output",
                    lines=3,
                    show_copy_button=True
                )

        # Examples
        gr.Examples(
            examples=[
                ["hello world", "uppercase", 2],
                ["GRADIO ROCKS", "lowercase", 1],
                ["python programming", "title", 1]
            ],
            inputs=[text_input, mode, intensity]
        )

        # Connect components
        process_btn.click(
            fn=process_text,
            inputs=[text_input, mode, intensity],
            outputs=text_output
        )

def create_image_interface():
    """Create image processing tab."""
    with gr.TabItem("Image Processor"):
        with gr.Row():
            image_input = gr.Image(label="Upload Image")
            image_output = gr.Image(label="Processed Image")

        image_btn = gr.Button("Flip Image", variant="primary")

        image_btn.click(
            fn=process_image,
            inputs=image_input,
            outputs=image_output
        )

def create_chat_interface():
    """Create chatbot tab."""
    with gr.TabItem("Chatbot"):
        chatbot = gr.ChatInterface(
            fn=chatbot_response,
            title="Simple Chatbot",
            description="Chat with the bot!",
            examples=["Hello!", "How are you?", "Tell me a joke"]
        )

# ============================================
# MAIN APPLICATION
# ============================================

def create_app():
    """Create the main Gradio application."""

    # Custom CSS for styling
    custom_css = """
    .container { max-width: 1200px; margin: auto; }
    @media (max-width: 768px) {
        .container { padding: 10px; }
    }
    """

    with gr.Blocks(
        theme=gr.themes.Soft(),
        css=custom_css,
        title="Gradio 6 Boilerplate"
    ) as demo:

        # Header
        gr.Markdown("""
        # Gradio 6 Complete Boilerplate

        This is a comprehensive example demonstrating:
        - Multiple input types (text, radio, slider)
        - Dynamic UI updates
        - Image processing
        - Chatbot interface
        - Responsive mobile-friendly layout
        """)

        # Settings accordion
        with gr.Accordion("⚙️ Settings", open=False):
            theme_choice = gr.Radio(
                ["Light", "Dark"],
                label="Theme",
                value="Light"
            )
            show_advanced = gr.Checkbox(label="Show Advanced Options")

        # Main content tabs
        with gr.Tabs():
            create_text_interface()
            create_image_interface()
            create_chat_interface()

        # Footer
        gr.Markdown("""
        ---
        Built with [Gradio](https://gradio.app) |
        [Documentation](https://gradio.app/docs) |
        [GitHub](https://github.com)
        """)

    return demo

# ============================================
# LAUNCH APPLICATION
# ============================================

if __name__ == "__main__":
    app = create_app()
    app.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,        # Default port
        share=False,             # Set to True for public URL
        show_error=True,         # Show errors in UI
        debug=False              # Set to True for development
    )
```

---

## Quick Reference

### Common Components

```python
# Text
gr.Textbox(label="", placeholder="", lines=1)
gr.TextArea(label="", lines=3)  # Deprecated in favor of Textbox with lines

# Numbers
gr.Number(label="", value=0)
gr.Slider(minimum=0, maximum=100, value=50, step=1)

# Selection
gr.Radio(choices=[], label="", value="")
gr.Dropdown(choices=[], label="", value="", multiselect=False)
gr.CheckboxGroup(choices=[], label="")
gr.Checkbox(label="", value=False)

# Media
gr.Image(label="", type="pil")  # or "numpy", "filepath"
gr.Audio(label="", type="numpy")
gr.Video(label="")
gr.File(label="", file_count="single")

# Display
gr.Markdown("# Text")
gr.HTML("<div>HTML content</div>")
gr.Label(label="")  # For classification results
gr.JSON(label="")

# Layout
gr.Row()
gr.Column(scale=1, min_width=0)
gr.Tabs()
gr.TabItem("Tab Name")
gr.Accordion("Title", open=False)

# Interactive
gr.Button(value="Click", variant="primary")  # or "secondary", "stop"
gr.Examples(examples=[], inputs=[])
gr.Dataset(samples=[])
```

### Event Handlers

```python
# Click events
button.click(fn=function, inputs=[...], outputs=[...])

# Change events
textbox.change(fn=function, inputs=[...], outputs=[...])
dropdown.change(fn=function, inputs=[...], outputs=[...])

# Submit events (Enter key)
textbox.submit(fn=function, inputs=[...], outputs=[...])

# Upload events
image.upload(fn=function, inputs=[...], outputs=[...])

# Clear events
image.clear(fn=function)

# Chaining events
btn.click(fn1, inputs, outputs).then(fn2, inputs, outputs)
```

### Launch Options

```python
demo.launch(
    server_name="0.0.0.0",      # Bind address
    server_port=7860,            # Port number
    share=False,                 # Create public URL
    debug=False,                 # Debug mode
    show_error=True,             # Show errors in UI
    auth=("user", "pass"),       # Basic authentication
    auth_message="Login required",
    max_threads=40,              # Concurrent requests
    show_api=True,               # Show API docs
    quiet=False,                 # Suppress output
    favicon_path=None,           # Custom favicon
)
```

---

## Resources

- **Official Documentation:** https://gradio.app/docs
- **Quickstart Guide:** https://gradio.app/guides/quickstart
- **GitHub Repository:** https://github.com/gradio-app/gradio
- **Hugging Face Spaces:** https://huggingface.co/spaces
- **Community Gallery:** https://gradio.app/gallery
- **Discord Community:** https://discord.gg/gradio

---

## Tips and Best Practices

1. **Use `gr.Blocks()` for complex layouts** - More control than `gr.Interface()`
2. **Add examples** - Helps users understand your app quickly
3. **Enable share=True for demos** - Easy sharing with public URLs
4. **Use themes** - `gr.themes.Soft()`, `gr.themes.Monochrome()`, etc.
5. **Add error handling** - Wrap functions in try/except
6. **Optimize for mobile** - Use responsive layouts with min_width
7. **Cache expensive operations** - Use `@functools.lru_cache`
8. **Stream long outputs** - Use `yield` for real-time updates
9. **Add loading states** - Use `gr.Progress()` for long operations
10. **Test thoroughly** - Check all input combinations

---

**Last Updated:** November 2025 | **Gradio Version:** 6.x
