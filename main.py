import streamlit as st
import fal_client
from dotenv import load_dotenv
import os
import sys

def main():
    load_dotenv()

    st.set_page_config(
        page_title="Text to Image Generator",
        page_icon="🎨",
        layout="centered"
    )

    st.title("🎨 Text to Image Generator")
    st.write("Generate amazing images using AI! Enter your prompt below and let the magic happen.")

    FAL_KEY = os.getenv("FAL_KEY")
    if not FAL_KEY:
        st.error("Please set your FAL API key in the .env file as FAL_KEY.")
        st.stop()

    # Function to handle image generation
    def generate_image(prompt):
        try:
            def on_queue_update(update):
                if isinstance(update, fal_client.InProgress):
                    for log in update.logs:
                        st.write(log["message"])

            result = fal_client.subscribe(
                "fal-ai/flux-pro/v1.1-ultra",
                arguments={"prompt": prompt},
                with_logs=True,
                on_queue_update=on_queue_update,
            )
            return result
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None

    # Create a form for the prompt
    with st.form("image_generation_form"):
        prompt = st.text_area(
            "Enter your prompt",
            placeholder="Describe the image you want to generate...",
            height=100
        )
        submitted = st.form_submit_button("Generate Image")

    # Handle form submission
    if submitted and prompt:
        with st.spinner("Generating your image... This may take a few moments."):
            result = generate_image(prompt)
            if result:
                st.image(result["images"][0]["url"], caption="Generated Image", use_column_width=True)
                st.success("Image generated successfully!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--streamlit":
        main()
    else:
        import subprocess
        subprocess.run(["streamlit", "run", __file__, "--", "--streamlit"]) 