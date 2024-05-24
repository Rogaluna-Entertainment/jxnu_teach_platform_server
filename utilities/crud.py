from configs import database
from typing import List, Optional, Dict
from fastapi import  HTTPException

# 增
#   在指定的表中插入新的条目，使用提供的数据。
#
# 参数:
#   table_name (str): 数据将被插入的表名。
#   data (dict): 包含列名和对应值的字典，用于插入数据。
#
# 返回值:
#   lst_record_id: 插入的序号id
#
# 示例:
#   data = {"name": "John", "age": 30}
#   id = await create_entry("users", data)
async def create_entry(table_name: str, data: dict):
    keys = ", ".join(data.keys())
    values = ":" + ", :".join(data.keys())
    query = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"
    try:
        result = await database.execute(query=query, values=data)
        last_record_id = result
        return last_record_id
    except Exception as e:
        print(f"Error executing query: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# 查
#   查询数据表中的条目，支持过滤、排序和分页。
#
# 参数:
#   table_name (str): 表名。
#   filters (dict): 过滤条件，键为列名，值为期望值。
#   order_by (str): 排序条件。
#   limit (int): 返回记录的最大数量。
#   offset (int): 返回记录的起始偏移量。
#
# 示例:
#   accounts_data = await read_entries('users', filters={'age': 25}, order_by='name ASC', limit=10, offset=0)
# 或者filters使用List:
#   filters = {}
#   filters['age'] = [20, 25]
async def read_entries(
        table_name: str, 
        filters: Optional[dict] = None, 
        fields: Optional[List[str]] = None,
        order_by: Optional[str] = None, 
        limit: Optional[int] = None, 
        offset: Optional[int] = None):
    
    # 如果未指定字段，默认选择所有字段
    if fields is None:
        fields_query = '*'
    else:
        fields_query = ', '.join(fields)

    where_clauses = []
    values = {}
    if filters:
        for key, value in filters.items():
            # where_clauses.append(f"{key} = :{key}")
            # values[key] = value
            if isinstance(value, list):
                where_clauses.append(f"{key} IN ({','.join(':{}{}'.format(key, i) for i in range(len(value)))})")
                for i, v in enumerate(value):
                    values[f'{key}{i}'] = v
            else:
                where_clauses.append(f"{key} = :{key}")
                values[key] = value

    where_statement = " AND ".join(where_clauses) if where_clauses else "1=1"
    order_by_statement = f" ORDER BY {order_by}" if order_by else ""
    limit_statement = f" LIMIT {limit}" if limit is not None else ""
    offset_statement = f" OFFSET {offset}" if offset is not None else ""

    query = f"SELECT {fields_query} FROM {table_name} WHERE {where_statement}{order_by_statement}{limit_statement}{offset_statement}"
    return await database.fetch_all(query=query, values=values)


# 改
#   更新指定表中的特定条目。
#
# 参数:
#   table_name (str): 表名。
#   data (dict): 包含更新数据的键值对字典。
#   conditions (dict): 更新条件，格式为列名和期望值的映射。
#
# 示例:
# await update_entry('users', {'age': 26}, {'name': 'Alice'})
async def update_entry(table_name: str, data: dict, conditions: dict):
    set_clause = ", ".join([f"{key}=:{key}" for key in data.keys()])
    condition_clause = " AND ".join([f"{key}=:{key}_cond" for key in conditions.keys()])
    values = {**data, **{f"{k}_cond": v for k, v in conditions.items()}}
    query = f"UPDATE {table_name} SET {set_clause} WHERE {condition_clause}"
    await database.execute(query=query, values=values)


# 删
#   从指定表中删除特定条目。
#
# 参数:
#   table_name (str): 表名。
#   conditions (dict): 删除条件，格式为列名和期望值的映射。
#
# 示例:
#   await delete_entry('users', {'name': 'Bob'})
async def delete_entry(table_name: str, conditions: dict):
    condition_clause = " AND ".join([f"{key}=:{key}" for key in conditions.keys()])
    query = f"DELETE FROM {table_name} WHERE {condition_clause}"
    await database.execute(query=query, values=conditions)


# 计数
#   统计指定表中满足特定条件的条目数。只返回计数结果，不返回具体数据。
#
# 参数:
#   table_name (str): 需要查询的表名。
#   filters (Optional[Dict[str, any]]): 过滤条件，字典格式，键为数据库字段名，值为匹配值。
#
# 返回值:
#   int: 符合条件的记录总数。
#
#  示例:
#    计算用户表中年龄为25岁的用户数量
#    count = await count_entries('users', {'age': 25})
async def count_entries(table_name: str, filters: Optional[Dict[str, any]] = None) -> int:
    where_clauses = []
    values = {}
    if filters:
        for key, value in filters.items():
            where_clauses.append(f"{key} = :{key}")
            values[key] = value

    where_statement = " AND ".join(where_clauses) if where_clauses else "1=1"
    query = f"SELECT COUNT(*) FROM {table_name} WHERE {where_statement}"
    result = await database.fetch_one(query=query, values=values)
    return result[0]  # Assuming the COUNT(*) is the first column in the result