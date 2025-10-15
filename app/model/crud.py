import os
import sys
import base64

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from app.log import setup_logging, handle_exception
from dotenv import load_dotenv
load_dotenv()

logger = setup_logging()
sys.excepthook = handle_exception

async def analyze_image_with_gpt(image_base64: str) -> str:
    llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

    system_message = SystemMessage(content="You are an image analysis expert who helps people find information about images. Please also analyze the images and provide detailed explanations in Korean.")
    human_message = HumanMessage(
        content=[
            {"type": "text", "text": "Analyze the following image and provide a detailed description:"},
            {
                "type": "image_url", 
                "image_url": {
                    "url": f"data:image/png;base64,{image_base64}"
                },
            }
        ]
    )

    response = await llm.ainvoke([system_message, human_message])

    if isinstance(response, AIMessage):
        return response.content
    else:
        return "Error: Unexpected response type from LLM."