import argparse
import os
import sys
import toml
from typing import Dict, Any, Union

# 映射类型名称到Python类型
TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
}


def safe_type_cast(value: Any, target_type: Union[type, str]) -> Any:
    """
    安全地将值转换为目标类型。避免使用eval, 提高安全性。
    """
    if isinstance(target_type, str):
        target_type = TYPE_MAP.get(target_type, str)

    # 确认target_type是一个可调用对象（如函数或类）
    if not callable(target_type):
        raise ValueError("target_type必须是一个可调用对象(如函数或类)")

    # 现在安全地调用target_type，因为它已验证为可调用
    return target_type(value)


def read_config(config_path: str) -> Dict[str, Any]:
    """
    读取并返回TOML配置文件的内容。
    """
    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            return toml.load(config_file)
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
        sys.exit(1)
    except toml.TomlDecodeError:
        print(f"Error: Unable to decode TOML in '{config_path}'.")
        sys.exit(1)


def parse_arguments(config: Dict[str, Any]) -> argparse.Namespace:
    """
    根据配置解析命令行参数, 并返回解析后的Namespace对象。
    """
    parser = argparse.ArgumentParser(description=config.get("description", "CLI Tool"))
    for arg, details in config.get("arguments", {}).items():
        required = details.get("required", False)
        choices = details.get("choices")
        default = details.get("default")
        help_text = details.get("help")
        arg_type = safe_type_cast(details.get("type", "str"), str)  # 使用安全的类型转换

        # 添加参数到解析器
        parser.add_argument(
            f"--{arg}",
            required=required,
            choices=choices,
            default=default,
            help=help_text,
            type=lambda x: safe_type_cast(x, arg_type),  # 使用lambda进行延迟类型转换
        )
    return parser.parse_args(sys.argv[1:])


def get_cli_argument(config_path: str) -> Dict[str, Any]:
    """
    读取TOML配置文件并解析命令行参数, 返回解析后的参数字典。
    """
    config = read_config(config_path)
    parsed_args = parse_arguments(config)
    return vars(parsed_args)


# 调用示例
if __name__ == "__main__":
    script_path = __file__
    script_dir = os.path.dirname(script_path)
    config_file = os.path.join(script_dir, "..", "..", "cli_config.toml")
    arguments = get_cli_argument(config_file)
    print(arguments)
