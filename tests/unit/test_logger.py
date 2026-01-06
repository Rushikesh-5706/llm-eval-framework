from llm_eval.utils.logger import get_logger

def test_logger():
    logger = get_logger("test")
    logger.info("hello")
    assert logger.name == "test"
