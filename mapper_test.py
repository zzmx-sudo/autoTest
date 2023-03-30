from basic.py_mybatis.mapper import PyMapper#, PY_MYBATIS_TYPE_HANDLER, PyMybatisTypeHandler
mapper = PyMapper(xml_path='mapper_test.xml')
import time

# for statement_id in mapper.list_statement():
#     print(statement_id)


params = {
    'type': 'GK',
    'wareCode': 'CK30001'
}
print(mapper.statement('getWareInfoList', params=params))

