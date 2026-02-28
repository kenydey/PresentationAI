import os
import unittest

from utils.user_config import get_user_config, update_env_with_user_config


class UserConfigMappingTest(unittest.TestCase):
    def setUp(self) -> None:
        self._orig_env = os.environ.copy()
        # 避免真实 userConfig.json 影响测试
        os.environ.setdefault("USER_CONFIG_PATH", "__nonexistent_user_config__.json")

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self._orig_env)

    def test_default_provider_and_model_from_env(self) -> None:
        os.environ["LLM"] = "openai"
        os.environ["OPENAI_API_KEY"] = "test-key"
        os.environ["OPENAI_MODEL"] = "gpt-test"

        cfg = get_user_config()

        self.assertEqual(cfg.default_llm_provider, "openai")
        self.assertEqual(cfg.LLM, "openai")
        self.assertEqual(cfg.default_llm_model, "gpt-test")
        self.assertEqual(cfg.OPENAI_API_KEY, "test-key")
        self.assertEqual(cfg.OPENAI_MODEL, "gpt-test")

        # 修改环境变量，然后通过 update_env_with_user_config 重新同步
        os.environ["LLM"] = ""
        os.environ["OPENAI_MODEL"] = ""

        update_env_with_user_config()

        self.assertEqual(os.getenv("LLM"), "openai")
        self.assertEqual(os.getenv("OPENAI_MODEL"), "gpt-test")


if __name__ == "__main__":
    unittest.main()

