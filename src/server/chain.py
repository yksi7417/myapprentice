from src.ai.llm_qa_chain import build_chain
from src.server.llm import LLMBackend, BACKENDS, generate_sse


class ChainBackend(LLMBackend):
    def __init__(self):
        self.chain = build_chain()

    async def invoke(self, prompt: str) -> str:
        result = self.chain.invoke({"query": prompt})
        return result["result"]

    async def stream(self, prompt: str):
        content = await self.invoke(prompt)
        async for chunk in generate_sse(content):
            yield chunk


# register
BACKENDS["chain"] = ChainBackend()
