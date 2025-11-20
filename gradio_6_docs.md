# Gradio 6 Comprehensive Documentation

## Table of Contents
1. [Getting Started](#getting-started)
2. [Mobile-Friendly UI Patterns](#mobile-friendly-ui-patterns)
3. [Event Handling and State Management](#event-handling-and-state-management)
4. [Component Library Overview](#component-library-overview)
5. [Layout Options for Mobile-First Design](#layout-options-for-mobile-first-design)
6. [Advanced Features](#advanced-features)

---

## Getting Started

### Installation

Gradio requires **Python 3.10 or higher**. Install Gradio using pip:

```bash
pip install --upgrade gradio
```

**Best Practice:** Install Gradio in a virtual environment.

### Your First Gradio App

Create a simple greeting application in just a few lines:

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

**Running the App:**
- If saved as `app.py`, run: `python app.py`
- The demo opens at `http://localhost:7860`

### Hot Reload Mode

For faster development with automatic reloading:

```bash
gradio app.py
```

Enable **vibe mode** for in-browser chat to write or edit your Gradio app using natural language:

```bash
gradio --vibe app.py
```

### Understanding the Interface Class

The `gr.Interface` class is designed for quick demos with three core arguments:

- **`fn`**: The Python function to wrap with a UI
- **`inputs`**: Gradio component(s) for input. Must match function arguments
- **`outputs`**: Gradio component(s) for output. Must match return values

**Example with Multiple Inputs:**

```python
import gradio as gr

def greet(name, intensity):
    return f"Hello, {name}!" * int(intensity)

demo = gr.Interface(
    fn=greet,
    inputs=[
        gr.Textbox(label="Name"),
        gr.Slider(minimum=1, maximum=10, label="Intensity")
    ],
    outputs=gr.Textbox(label="Greeting")
)

demo.launch()
```

### Sharing Your Demo

Generate a public URL instantly by setting `share=True`:

```python
demo.launch(share=True)
```

This creates a public link like `https://a23dsf231adb.gradio.live` that anyone can access.

### Gradio's Core Classes

#### 1. **gr.Interface**
High-level class for quick demos. Automatically creates UI layout.

**When to Use:**
- Single-function applications
- Quick prototypes
- Simple input-output workflows

#### 2. **gr.Blocks**
Low-level class for customizable layouts and complex data flows.

**When to Use:**
- Multi-component applications
- Custom layouts and positioning
- Complex interactions (outputs as inputs to other functions)
- Updating component properties/visibility based on user interaction

**Example with Blocks:**

```python
import gradio as gr

def greet(name):
    return f"Hello, {name}!"

with gr.Blocks() as demo:
    name_input = gr.Textbox(label="Enter your name")
    greet_button = gr.Button("Greet")
    greeting_output = gr.Textbox(label="Greeting")

    greet_button.click(greet, inputs=name_input, outputs=greeting_output)

demo.launch()
```

#### 3. **gr.ChatInterface**
Specialized class for building chatbot UIs.

**Example:**

```python
import gradio as gr

def chat_function(message, history):
    return f"You said: {message}"

demo = gr.ChatInterface(fn=chat_function)
demo.launch()
```

---

## Mobile-Friendly UI Patterns

### Responsive Design Principles

Gradio 6 automatically adapts to mobile screens, but you can optimize further:

#### 1. **Fill Width for Mobile**

```python
demo = gr.Interface(
    fn=your_function,
    inputs="text",
    outputs="text",
    fill_width=True  # Horizontally expand to fill container
)
```

#### 2. **Progressive Web App (PWA)**

Enable PWA for installable mobile apps:

```python
demo.launch(pwa=True)
```

**Note:** PWA is automatically enabled on Hugging Face Spaces.

#### 3. **Mobile-Optimized Components**

Use components that work well on touch devices:

```python
with gr.Blocks() as demo:
    # Radio buttons instead of dropdowns for better mobile UX
    choice = gr.Radio(["Option 1", "Option 2", "Option 3"], label="Select")

    # Sliders with appropriate min/max for easy touch interaction
    value = gr.Slider(minimum=0, maximum=100, step=1, label="Value")

    # Large touch-friendly buttons
    submit_btn = gr.Button("Submit", variant="primary")
```

#### 4. **Responsive Layouts with Blocks**

```python
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1, min_width=200):
            input1 = gr.Textbox(label="Input 1")
        with gr.Column(scale=2):
            input2 = gr.Textbox(label="Input 2")
```

### Best Practices for Mobile

1. **Minimize Vertical Scrolling:** Use Accordions and Tabs
2. **Touch-Friendly Elements:** Ensure buttons and interactive elements are at least 44x44 pixels
3. **Readable Text:** Use appropriate font sizes (handled automatically by Gradio)
4. **Optimize Images:** Set reasonable dimensions for mobile displays

```python
gr.Image(height=300, width=300)  # Fixed, mobile-friendly dimensions
```

---

## Event Handling and State Management

### Event Types

Gradio supports multiple event types:

#### 1. **Click Events**

```python
with gr.Blocks() as demo:
    text = gr.Textbox()
    button = gr.Button("Submit")
    output = gr.Textbox()

    button.click(fn=process_function, inputs=text, outputs=output)
```

#### 2. **Change Events**

Triggered when component value changes:

```python
with gr.Blocks() as demo:
    slider = gr.Slider(0, 100)
    output = gr.Number()

    slider.change(fn=update_value, inputs=slider, outputs=output)
```

#### 3. **Submit Events**

For Enter key in textboxes:

```python
textbox.submit(fn=process_text, inputs=textbox, outputs=output)
```

#### 4. **Input Events**

Real-time updates as user types:

```python
textbox.input(fn=live_update, inputs=textbox, outputs=output)
```

### State Management

Use `gr.State()` to persist data across interactions:

```python
import gradio as gr

def add_to_history(message, history):
    history = history or []
    history.append(message)
    return history, "\n".join(history)

with gr.Blocks() as demo:
    history_state = gr.State([])
    message_input = gr.Textbox(label="Message")
    history_display = gr.Textbox(label="History", interactive=False)
    submit_btn = gr.Button("Add")

    submit_btn.click(
        fn=add_to_history,
        inputs=[message_input, history_state],
        outputs=[history_state, history_display]
    )

demo.launch()
```

### Trigger Modes

Control how events are processed:

```python
button.click(
    fn=process,
    inputs=input_component,
    outputs=output_component,
    trigger_mode="once"  # Options: "once", "multiple", "always_last"
)
```

- **`once`**: No new submissions while event is pending (default for most events)
- **`multiple`**: Unlimited submissions while pending
- **`always_last`**: Allow second submission after pending event (default for `.change()` and `.key_up()`)

### Chaining Events

Execute multiple functions in sequence:

```python
with gr.Blocks() as demo:
    input_text = gr.Textbox()
    intermediate = gr.Textbox()
    final_output = gr.Textbox()

    input_text.submit(
        fn=first_function,
        inputs=input_text,
        outputs=intermediate
    ).then(
        fn=second_function,
        inputs=intermediate,
        outputs=final_output
    )
```

### Conditional Visibility

Update component properties based on user interaction:

```python
def toggle_visibility(choice):
    if choice == "Advanced":
        return gr.update(visible=True)
    return gr.update(visible=False)

with gr.Blocks() as demo:
    mode = gr.Radio(["Simple", "Advanced"], label="Mode")
    advanced_options = gr.Textbox(label="Advanced Options", visible=False)

    mode.change(
        fn=toggle_visibility,
        inputs=mode,
        outputs=advanced_options
    )
```

---

## Component Library Overview

Gradio offers **30+ built-in components** for various input and output types.

### Text Components

#### Textbox

```python
# Basic textbox
gr.Textbox(label="Name", placeholder="Enter name here")

# Multi-line textbox
gr.Textbox(lines=5, label="Description")

# Password field
gr.Textbox(type="password", label="Password")

# With copy button
gr.Textbox(show_copy_button=True, label="Output")
```

#### Markdown

```python
gr.Markdown("# Hello World\nThis is **bold** text")
```

#### HTML

```python
gr.HTML("<h1>Custom HTML</h1>")
```

### Input Components

#### Button

```python
# Primary button
gr.Button("Submit", variant="primary")

# Stop button
gr.Button("Stop", variant="stop")

# Secondary button
gr.Button("Reset", variant="secondary")
```

#### Slider

```python
gr.Slider(
    minimum=0,
    maximum=100,
    value=50,
    step=1,
    label="Intensity"
)
```

#### Radio

```python
gr.Radio(
    choices=["Option 1", "Option 2", "Option 3"],
    label="Select One",
    value="Option 1"  # Default selection
)
```

#### Dropdown

```python
gr.Dropdown(
    choices=["Python", "JavaScript", "Java"],
    label="Programming Language",
    multiselect=False  # Set True for multiple selections
)
```

#### Checkbox

```python
gr.Checkbox(label="I agree to terms", value=False)
```

#### CheckboxGroup

```python
gr.CheckboxGroup(
    choices=["Feature 1", "Feature 2", "Feature 3"],
    label="Select Features"
)
```

### Media Components

#### Image

```python
# For input
gr.Image(
    height=300,
    width=300,
    type="numpy",  # Options: "numpy", "pil", "filepath"
    label="Upload Image"
)

# For output
gr.Image(label="Result")
```

#### Audio

```python
# For recording or upload
gr.Audio(
    sources=["microphone", "upload"],
    type="filepath",
    label="Audio Input"
)

# For playback
gr.Audio(autoplay=True, show_download_button=True)
```

#### Video

```python
gr.Video(
    height=400,
    label="Upload Video"
)
```

#### File

```python
gr.File(
    file_count="multiple",
    file_types=[".pdf", ".csv"],
    label="Upload Files"
)
```

### Data Components

#### Dataframe

```python
import pandas as pd

gr.Dataframe(
    value=pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}),
    headers=["Column 1", "Column 2"],
    interactive=True
)
```

#### Number

```python
gr.Number(
    value=0,
    minimum=0,
    maximum=100,
    label="Count"
)
```

#### JSON

```python
gr.JSON(value={"key": "value"})
```

### Visualization Components

#### Plot

For matplotlib, plotly, bokeh, and altair charts:

```python
import matplotlib.pyplot as plt

def create_plot():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    return fig

gr.Plot()
```

#### Gallery

```python
gr.Gallery(
    value=["image1.jpg", "image2.jpg"],
    label="Image Gallery",
    columns=3,
    height="auto"
)
```

#### Model3D

```python
gr.Model3D(
    clear_color=[0, 0, 0, 0],
    label="3D Model Viewer",
    camera_position=[None, None, None]
)
```

### Special Components

#### Examples

```python
gr.Examples(
    examples=[
        ["Example 1", 10],
        ["Example 2", 20]
    ],
    inputs=[text_input, slider_input]
)
```

#### AnnotatedImage

```python
gr.AnnotatedImage(
    value=(image, annotations),
    label="Annotated Result"
)
```

#### HighlightedText

```python
gr.HighlightedText(
    value=[("This is", None), ("highlighted", "positive"), ("text", None)],
    color_map={"positive": "green"}
)
```

### Component Customization

All components support:
- **`label`**: Display label
- **`show_label`**: Show/hide label
- **`interactive`**: Enable/disable user interaction
- **`visible`**: Show/hide component
- **`elem_id`**: Custom HTML element ID
- **`elem_classes`**: Custom CSS classes

---

## Layout Options for Mobile-First Design

### Row and Column Layouts

```python
with gr.Blocks() as demo:
    with gr.Row():
        col1 = gr.Textbox(label="Column 1")
        col2 = gr.Textbox(label="Column 2")
        col3 = gr.Textbox(label="Column 3")
```

**Responsive Columns with Scale:**

```python
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            input1 = gr.Textbox()
        with gr.Column(scale=2):  # Takes 2x space
            input2 = gr.Textbox()
```

**Minimum Width for Mobile:**

```python
with gr.Row():
    with gr.Column(min_width=200):  # Prevents shrinking below 200px
        gr.Textbox()
```

### Tabs

Perfect for organizing complex interfaces on mobile:

```python
with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("Input"):
            input_text = gr.Textbox()
        with gr.Tab("Results"):
            output_text = gr.Textbox()
        with gr.Tab("Settings"):
            settings = gr.Slider()
```

### Accordion

Collapse sections to save screen space:

```python
with gr.Blocks() as demo:
    with gr.Accordion("Advanced Options", open=False):
        option1 = gr.Slider(0, 100, label="Option 1")
        option2 = gr.Textbox(label="Option 2")
```

### Group

Visually group related components:

```python
with gr.Blocks() as demo:
    with gr.Group():
        name = gr.Textbox(label="Name")
        email = gr.Textbox(label="Email")
```

### Complete Mobile-First Layout Example

```python
import gradio as gr

def process_data(name, age, choice):
    return f"Hello {name}, age {age}, you chose {choice}"

with gr.Blocks(fill_width=True) as demo:
    gr.Markdown("# Mobile-Friendly App")

    with gr.Row():
        with gr.Column(scale=1, min_width=200):
            name = gr.Textbox(label="Name", placeholder="Your name")
            age = gr.Slider(0, 100, label="Age", value=25)

        with gr.Column(scale=2):
            with gr.Tabs():
                with gr.Tab("Options"):
                    choice = gr.Radio(
                        ["Option A", "Option B", "Option C"],
                        label="Choose"
                    )
                with gr.Tab("Advanced"):
                    with gr.Accordion("More Settings", open=False):
                        advanced = gr.Slider(0, 10, label="Advanced")

    submit = gr.Button("Submit", variant="primary")
    output = gr.Textbox(label="Result", show_copy_button=True)

    submit.click(
        fn=process_data,
        inputs=[name, age, choice],
        outputs=output
    )

demo.launch(share=True, pwa=True)
```

---

## Advanced Features

### Streaming

For real-time updates (chatbots, video processing):

```python
def generate_stream(prompt):
    for word in prompt.split():
        yield word + " "

with gr.Blocks() as demo:
    input_text = gr.Textbox()
    output_text = gr.Textbox()

    input_text.submit(
        fn=generate_stream,
        inputs=input_text,
        outputs=output_text
    )
```

### Queueing

Enable for better handling of concurrent users:

```python
demo = gr.Interface(fn=slow_function, inputs="text", outputs="text")
demo.queue(max_size=20)  # Max 20 users in queue
demo.launch()
```

### Progress Indicators

Show progress for long-running tasks:

```python
import time

def long_task(progress=gr.Progress()):
    progress(0, desc="Starting...")
    for i in range(100):
        time.sleep(0.1)
        progress((i + 1) / 100, desc=f"Processing {i+1}/100")
    return "Complete!"

demo = gr.Interface(fn=long_task, inputs=None, outputs="text")
demo.launch()
```

### Flagging

Allow users to flag problematic outputs:

```python
demo = gr.Interface(
    fn=your_function,
    inputs="text",
    outputs="text",
    flagging_mode="manual"  # Options: "never", "auto", "manual"
)
```

### Theming

Customize appearance with built-in themes:

```python
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    # Your components here
    pass

# Other themes: gr.themes.Default(), gr.themes.Glass(), etc.
```

**Custom Theme:**

```python
theme = gr.themes.Base(
    primary_hue="blue",
    secondary_hue="orange",
    neutral_hue="slate"
)

with gr.Blocks(theme=theme) as demo:
    pass
```

### API Access

Query Gradio apps programmatically:

```python
from gradio_client import Client

client = Client("https://your-gradio-app.hf.space")
result = client.predict("input text", fn_index=0)
print(result)
```

### Custom Components

Create your own components:

```bash
gradio cc create MyComponent --template SimpleTextbox --install
gradio cc dev  # Development server
gradio cc build  # Build package
```

### Deployment Options

1. **Local Sharing:**
   ```python
   demo.launch(share=True)  # 72-hour temporary link
   ```

2. **Hugging Face Spaces:**
   ```bash
   gradio deploy
   ```

3. **Cloud Platforms:** Deploy on AWS, Google Cloud, or Azure

4. **Docker:**
   ```dockerfile
   FROM python:3.10
   COPY . /app
   WORKDIR /app
   RUN pip install gradio
   CMD ["python", "app.py"]
   ```

### Examples with Caching

Speed up loading with cached examples:

```python
demo = gr.Interface(
    fn=your_function,
    inputs=["text", "slider"],
    outputs="image",
    examples=[
        ["Example 1", 10],
        ["Example 2", 20]
    ],
    cache_examples=True
)
```

---

## Additional Resources

- **Official Documentation:** https://www.gradio.app/docs
- **Guides:** https://www.gradio.app/guides
- **Custom Component Gallery:** https://www.gradio.app/custom-components
- **Hugging Face Spaces:** https://huggingface.co/spaces
- **GitHub Repository:** https://github.com/gradio-app/gradio
- **Discord Community:** Join for support and discussions

---

## Quick Reference: Common Patterns

### Simple Text Processor
```python
import gradio as gr

demo = gr.Interface(
    fn=lambda x: x.upper(),
    inputs=gr.Textbox(placeholder="Enter text"),
    outputs=gr.Textbox()
)
demo.launch()
```

### Image Processor
```python
import numpy as np
import gradio as gr

def sepia(image):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    sepia_img = image.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img

demo = gr.Interface(
    fn=sepia,
    inputs=gr.Image(height=200, width=200),
    outputs="image"
)
demo.launch()
```

### Multi-Modal App
```python
with gr.Blocks() as demo:
    with gr.Row():
        text_input = gr.Textbox()
        image_input = gr.Image()

    with gr.Row():
        text_output = gr.Textbox()
        image_output = gr.Image()

    btn = gr.Button("Process")
    btn.click(
        fn=process_multimodal,
        inputs=[text_input, image_input],
        outputs=[text_output, image_output]
    )

demo.launch()
```

---

**Version:** Gradio 6.x (Latest as of 2025)
**Last Updated:** November 2025
