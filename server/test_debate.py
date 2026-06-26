from .src.services.debate_service import DebateService
from dotenv import load_dotenv
load_dotenv()
import asyncio
import os



async def main():
    groq_api_key = os.getenv('GROQ_API_KEY')

    service = DebateService()

    result = await service.run("Should AI replace software engineers?", groq_api_key=groq_api_key)

    print(result)

if __name__ == "__main__":
    asyncio.run(main())