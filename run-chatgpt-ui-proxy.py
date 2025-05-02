import logging
import uvicorn
from src.server.config import CHATGPT_PROXY_PORT


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    uvicorn.run("src.server.proxy:app", host="localhost",
                port=CHATGPT_PROXY_PORT, reload=False)
