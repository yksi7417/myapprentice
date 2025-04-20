import src.server.llm_chain as llm_chain


def test_llm_chain_build_chain():
    """that the llm chain can be loaded without error"""
    llm_chain.build_chain()
    assert True
