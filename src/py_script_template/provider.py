from py_script_template.config import ConfigHandler, load_config_from_toml


class BaseProvider:
    def __init__(self, config_path: str):
        self._config_handler: ConfigHandler = load_config_from_toml(
            config_path=config_path
        )

    @property
    def config_handler(self) -> ConfigHandler:
        return self._config_handler

    @config_handler.setter
    def config_handler(self, v: ConfigHandler) -> None:
        self._config_handler = v


# class AppProvider(BaseProvider):
#     pass

global_provider = BaseProvider("config.toml")
