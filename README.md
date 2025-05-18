
### 필수 라이브러리 설치
```
pip install -r requirements.txt
```

### 앱 실행
```shell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8900 --log-level debug
```