def test_glm_agent_module_path():
    from zhike_phoneagent.agents.glm.async_agent import AsyncGLMAgent

    assert AsyncGLMAgent is not None


def test_glm_parser_module_path():
    from zhike_phoneagent.agents.glm.parser import GLMParser

    assert GLMParser is not None
