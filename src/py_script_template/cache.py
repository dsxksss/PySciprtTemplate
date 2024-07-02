from typing import Any, Dict, List, Optional
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb.table import Table
import os


class CacheHandler:
    def __init__(self, save_path: str, table_name: Optional[str] = None):
        self.save_path = save_path
        self.db = TinyDB(save_path, storage=CachingMiddleware(JSONStorage))
        self.table_name = table_name
        self.table = (
            self.db.table(table_name) if table_name else self.db.table("_default")
        )

    def _get_table(self, table_name: Optional[str]) -> Table:
        return self.db.table(table_name) if table_name else self.db.table("_default")

    # 检查数据是否已存在
    def is_exists(self, name: str, table_name: Optional[str] = None) -> bool:
        table = self._get_table(table_name)
        result = table.search(Query().name == name)
        return len(result) > 0

    # 存储缓存
    def save_cache(
        self, name: str, key: str, value: Any, table_name: Optional[str] = None
    ) -> None:
        table = self._get_table(table_name)
        if not self.is_exists(name, table_name):
            table.insert({"name": name, key: value})

    # 更新缓存
    def update_cache(
        self, name: str, key: str, value: Any, table_name: Optional[str] = None
    ) -> None:
        table = self._get_table(table_name)
        if self.is_exists(name, table_name):
            table.update({key: value}, Query().name == name)

    # 获取缓存
    def get_cache(self, name: str, table_name: Optional[str] = None) -> Dict[str, Any]:
        table = self._get_table(table_name)
        data = table.search(Query().name == name)
        if data:
            return dict(data[0])

        return dict()

    # 获取全部缓存
    def get_cache_list(self, table_name: Optional[str] = None) -> List[Dict[str, Any]]:
        table = self._get_table(table_name)
        return [dict(doc) for doc in table.all()]

    # 根据缓存名删除某个缓存
    def remove_cache(self, name: str, table_name: Optional[str] = None) -> None:
        table = self._get_table(table_name)
        if self.is_exists(name, table_name):
            table.remove(Query().name == name)

    # 清空缓存
    def clear_all_cache(self, table_name: Optional[str] = None) -> None:
        table = self._get_table(table_name)
        table.truncate()
        # FIXME 不知道什么原因导致的删除文件之后依然可以进行读写问题
        if table_name is None:  # 删除数据库文件
            self.db.close()
            os.remove(self.save_path)


# 示例使用方法
if __name__ == "__main__":
    cache_handler = CacheHandler("./cache.json")

    # 保存缓存
    cache_handler.save_cache("example", "key1", "value1")

    # 更新缓存
    cache_handler.update_cache("example", "key1", "new_value")

    # 获取缓存
    data = cache_handler.get_cache("example")
    print(data)

    # 获取所有缓存
    all_data = cache_handler.get_cache_list()
    print(all_data)

    # 删除某个缓存
    cache_handler.remove_cache("example")

    # 清空所有缓存
    cache_handler.clear_all_cache()

    # 使用分表
    cache_handler.save_cache("example", "key1", "value1", table_name="table1")
    cache_handler.update_cache("example", "key1", "new_value", table_name="table1")
    data = cache_handler.get_cache("example", table_name="table1")
    print(data)
    all_data = cache_handler.get_cache_list(table_name="table1")
    print(all_data)
    cache_handler.remove_cache("example", table_name="table1")
    cache_handler.clear_all_cache(table_name="table1")
