<h1 align="center">SE2022 Backend</h1>

<div align="center">waiting badge</div>

## Usage

建议使用 `python3.7`

### Local

```
// install dependencies
$ pip install -r requirements.txt

// run server 
$ python manage.py runserver 8000
```

- 运行于
  - [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/)

### Server

```
// install dependencies
$ pip install -r requirements.txt

// run server
$ python manage.py runserver 0.0.0.0:8000
```

- 运行于 
  - [`http://0.0.0.0:8000/`](http://0.0.0.0:8000/)
  - [`http://47.94.7.26:8000/`](http://47.94.7.26:8000/)

### 报错

若报错
```
File "/home/admin/.local/lib/python3.7/site-packages/django/db/backends/mysql/operations.py", line 146, in last_executed_query
    query = query.decode(errors='replace')
AttributeError: 'str' object has no attribute 'decode'
```
则注释掉该文件的`145-146`行
```
145         # if query is not None:
146         # query = query.decode(errors='replace')
147         return query
```



## 账户

目前设置已有的管理员账户为：

```
'USER': admin
'PASSWORD': se-mcdb-o2e
```

也可以自行创建管理员账户：

```
python manage.py createsuperuser
```



