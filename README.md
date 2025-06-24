# cover-agent
If you start frontend 
```
streamlit run ./front/front.py --server.port=5000
```
If you start backend
```
uvicorn agent:app --reload --host 0.0.0.0 --port 8000
```