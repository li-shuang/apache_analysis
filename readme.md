# 程序

## 程序功能
```
实现apache的日志解析，得到用户想要的报表
```

## 程序运行
### 生成所有报表
```
python main 200.200.1.35 log.txt all
```
### 生成IP表报
```
python main 200.200.1.35 log.txt ip
```
### 生成文章报表
```
python main 200.200.1.35 log.txt title
```
### 生成完整报表
```
python main 200.200.1.35 log.txt full
```

## 生成覆盖率
```
1. coverage run --source=common apache_analysis_unit.py
2. coverage report
3. coverage html
```

## 覆盖率结果
```

Name                      Stmts   Miss  Cover
---------------------------------------------
common/__init__.py            0      0   100%
common/data_analysis.py     122     11    91%
common/data_load.py          12      3    75%
---------------------------------------------
TOTAL                       134     14    90%

```