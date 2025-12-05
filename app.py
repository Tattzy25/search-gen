import gradio as gr
import time

# Generate searchbar widget HTML based on description
def generate_searchbar(description):
    time.sleep(2)  # Simulate generation time
    
    # Parse description for colors and style
    description_lower = description.lower()
    
    # Default styles
    bg_color = "#ffffff"
    text_color = "#333333"
    border_color = "#cccccc"
    button_color = "#007bff"
    border_radius = "8px"
    
    # Parse colors from description
    if "blue" in description_lower:
        button_color = "#007bff"
    if "red" in description_lower:
        button_color = "#dc3545"
    if "green" in description_lower:
        button_color = "#28a745"
    if "purple" in description_lower:
        button_color = "#6f42c1"
    if "dark" in description_lower:
        bg_color = "#1a1a1a"
        text_color = "#ffffff"
        border_color = "#444444"
    
    # Parse style
    if "rounded" in description_lower or "bubble" in description_lower:
        border_radius = "25px"
    if "sharp" in description_lower or "square" in description_lower:
        border_radius = "0px"
    
    # Generate HTML
    html = f"""
    <div style="width: 100%; max-width: 600px; margin: 0 auto;">
        <div style="display: flex; gap: 8px; padding: 12px; background: {bg_color}; border: 2px solid {border_color}; border-radius: {border_radius}; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <input type="text" placeholder="Search..." style="flex: 1; padding: 12px 16px; border: none; background: transparent; color: {text_color}; font-size: 16px; outline: none;" />
            <button style="padding: 12px 24px; background: {button_color}; color: white; border: none; border-radius: {border_radius}; cursor: pointer; font-size: 16px; font-weight: 600; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">Search</button>
        </div>
    </div>
    """
    
    return html, bg_color, text_color, border_color, button_color, border_radius

# Update specific properties
def update_searchbar(html, bg_color, text_color, border_color, button_color, border_radius):
    html = f"""
    <div style="width: 100%; max-width: 600px; margin: 0 auto;">
        <div style="display: flex; gap: 8px; padding: 12px; background: {bg_color}; border: 2px solid {border_color}; border-radius: {border_radius}; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <input type="text" placeholder="Search..." style="flex: 1; padding: 12px 16px; border: none; background: transparent; color: {text_color}; font-size: 16px; outline: none;" />
            <button style="padding: 12px 24px; background: {button_color}; color: white; border: none; border-radius: {border_radius}; cursor: pointer; font-size: 16px; font-weight: 600; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">Search</button>
        </div>
    </div>
    """
    return html

# Generate embed code with URL
def create_embed_code(url, html):
    if not url:
        return "Please enter a URL first"
    
    # Clean HTML for embed
    clean_html = html.replace('\n', '').replace('    ', '')
    
    embed_code = f'''<div data-search-widget data-url="{url}">
{clean_html}
<script>
document.querySelector('[data-search-widget] button').addEventListener('click', function() {{
  const query = this.previousElementSibling.value;
  window.open('{url}?q=' + encodeURIComponent(query), '_blank');
}});
</script>
</div>'''
    
    return embed_code

# Custom CSS for full screen layout
css = """
#container {
    height: 100vh !important;
    max-height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
}
.gradio-container {
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}
#left-panel, #right-panel {
    height: 100vh !important;
    padding: 40px !important;
    overflow-y: auto !important;
}
#left-panel {
    background: #f8f9fa !important;
}
#right-panel {
    background: #ffffff !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
}
footer {
    display: none !important;
}
.contain {
    padding: 0 !important;
}
"""

with gr.Blocks(css=css, title="Searchbar Widget Generator") as demo:
    # State variables
    current_html = gr.State("")
    bg_color_state = gr.State("#ffffff")
    text_color_state = gr.State("#333333")
    border_color_state = gr.State("#cccccc")
    button_color_state = gr.State("#007bff")
    border_radius_state = gr.State("8px")
    
    with gr.Row(elem_id="container"):
        # Left Panel
        with gr.Column(scale=1, elem_id="left-panel"):
            url_input = gr.Textbox(
                label="",
                placeholder="Enter your website URL (e.g., https://example.com)",
                visible=False,
                container=False
            )
            create_btn = gr.Button("Create Embed Code", visible=False, size="lg", variant="primary")
            
            description_input = gr.Textbox(
                label="",
                placeholder="Describe your searchbar design (e.g., 'blue rounded searchbar with dark background')",
                lines=5,
                container=False
            )
            generate_btn = gr.Button("Generate Searchbar", size="lg", variant="primary")
            
            # Color customization (hidden until generated)
            with gr.Group(visible=False) as customize_group:
                bg_color_picker = gr.ColorPicker(label="Background Color", value="#ffffff")
                text_color_picker = gr.ColorPicker(label="Text Color", value="#333333")
                border_color_picker = gr.ColorPicker(label="Border Color", value="#cccccc")
                button_color_picker = gr.ColorPicker(label="Button Color", value="#007bff")
                update_btn = gr.Button("Update Colors", size="sm")
                regenerate_btn = gr.Button("Regenerate", size="sm", variant="secondary")
        
        # Right Panel
        with gr.Column(scale=1, elem_id="right-panel"):
            loading_message = gr.Markdown("### Preview will appear here", visible=True)
            preview_html = gr.HTML(visible=False)
            embed_output = gr.Code(
                label="",
                language="html",
                visible=False,
                lines=10
            )
    
    # Generate searchbar
    def on_generate(description):
        html, bg, txt, border, btn, radius = generate_searchbar(description)
        return (
            html,  # current_html
            bg,    # bg_color_state
            txt,   # text_color_state
            border, # border_color_state
            btn,   # button_color_state
            radius, # border_radius_state
            gr.update(visible=False),  # loading_message
            gr.update(value=html, visible=True),  # preview_html
            gr.update(visible=True),  # customize_group
            gr.update(visible=True),  # url_input
            gr.update(visible=True),  # create_btn
            bg, txt, border, btn  # Update color pickers
        )
    
    generate_btn.click(
        on_generate,
        inputs=[description_input],
        outputs=[
            current_html, bg_color_state, text_color_state, border_color_state,
            button_color_state, border_radius_state, loading_message, preview_html,
            customize_group, url_input, create_btn,
            bg_color_picker, text_color_picker, border_color_picker, button_color_picker
        ]
    )
    
    # Update colors
    def on_update(html, bg, txt, border, btn, radius):
        new_html = update_searchbar(html, bg, txt, border, btn, radius)
        return new_html, new_html
    
    update_btn.click(
        on_update,
        inputs=[current_html, bg_color_picker, text_color_picker, border_color_picker, 
                button_color_picker, border_radius_state],
        outputs=[preview_html, current_html]
    )
    
    # Regenerate
    regenerate_btn.click(
        on_generate,
        inputs=[description_input],
        outputs=[
            current_html, bg_color_state, text_color_state, border_color_state,
            button_color_state, border_radius_state, loading_message, preview_html,
            customize_group, url_input, create_btn,
            bg_color_picker, text_color_picker, border_color_picker, button_color_picker
        ]
    )
    
    # Create embed code
    def on_create(url, html):
        code = create_embed_code(url, html)
        return gr.update(value=code, visible=True)
    
    create_btn.click(
        on_create,
        inputs=[url_input, current_html],
        outputs=[embed_output]
    )

demo.launch()