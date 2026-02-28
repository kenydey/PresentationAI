import base64
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from openai import OpenAI

from ppt_generator.models.query_and_prompt_models import (
    ImagePromptWithThemeAndAspectRatio,
)


async def generate_image(
    input: ImagePromptWithThemeAndAspectRatio, output_path: str
) -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    image_prompt = f"{input.image_prompt}, {input.theme_prompt}"
    print(f"Request - Generating Image for {image_prompt}")

    try:
        image_gen_func = (
            generate_image_openai
            if os.getenv("LLM") == "openai"
            else generate_image_google
        )
        await image_gen_func(image_prompt, output_path)
    except Exception as e:
        print(f"Error generating image: {e}")
        with open("assets/images/placeholder.jpg", "rb") as f_a:
            with open(output_path, "wb") as f_b:
                f_b.write(f_a.read())


async def generate_image_openai(prompt: str, output_path: str):
    client = OpenAI()
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        n=1,
        quality="low",
        size="1024x1024",
    )
    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    with open(output_path, "wb") as f:
        f.write(image_bytes)


async def generate_image_google(prompt: str, output_path: str):
    response = await ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-preview-image-generation"
    ).ainvoke([prompt], generation_config={"response_modalities": ["TEXT", "IMAGE"]})

    image_block = next(
        block
        for block in response.content
        if isinstance(block, dict) and block.get("image_url")
    )

    base64_image = image_block["image_url"].get("url").split(",")[-1]
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(base64_image))
