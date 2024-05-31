import hashlib
import logging
import os
from datetime import datetime


def mkdir_if_not_exist(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def parse_timestamp(timestamp, custom_strfmt="%Y-%m-%d %H:%M:%S"):
    # 将时间戳转换为datetime对象
    dt = datetime.fromtimestamp(timestamp)

    # 格式化日期和时间
    formatted = dt.strftime(custom_strfmt)

    return formatted


def set_logging_default_config() -> None:
    Log_level = 15
    logging.addLevelName(15, "TEMPLATE_DEBUG")

    console_handler = logging.StreamHandler()
    save_dir = "./logs"
    mkdir_if_not_exist(save_dir)

    # file_handler = logging.FileHandler(
    #     f"./{save_dir}/template-{parse_timestamp(float(time.time()),'%Y-%m-%d-%H-%M-%S')}.log",
    #     encoding="utf-8",
    # )
    file_handler = logging.FileHandler(f"./{save_dir}/template.log", encoding="utf-8")
    console_handler.setLevel(Log_level)
    file_handler.setLevel(Log_level)

    console_format = logging.Formatter(
        "[%(asctime)s] %(funcName)s - %(levelname)s | %(message)s"
    )
    file_format = logging.Formatter(
        "[%(asctime)s] %(funcName)s - %(levelname)s | %(message)s"
    )

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    logging.basicConfig(level=Log_level, handlers=[console_handler, file_handler])


def get_sha256_hash_of_file(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # 读取文件直到结束
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


def is_within_days(days: int, new_timestamp: float, old_timestamp: float):
    """
    new_timestamp = 1714722954  # 新时间戳
    old_timestamp = 1714636554  # 旧时间戳

    if is_within_days(2, new_timestamp, old_timestamp):
        print("旧时间戳处于新时间戳的前两天之内")
    else:
        print("旧时间戳不在新时间戳的前两天之内")
    """
    # 将时间戳转换为 datetime 对象
    new_date = datetime.fromtimestamp(new_timestamp)
    old_date = datetime.fromtimestamp(old_timestamp)

    # 计算两个日期之间的差值
    delta = new_date - old_date

    # 判断差值是否在两天之内
    return delta <= datetime.timedelta(days=days)  # type: ignore
