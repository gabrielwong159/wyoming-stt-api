import asyncio
import logging

from wyoming_stt_api.dependencies import create_handler, server

logger = logging.getLogger(__name__)


async def main():
    logger.info(f"Starting Wyoming server with {server.host=} {server.port=}")
    await server.run(create_handler)


if __name__ == "__main__":
    asyncio.run(main())
