# cover-agent tools

tool :
- CV writing : tools_/CV_writing : re-writing a CV (x)
- make docs : tools_/make_docx : make a cover letter with a docx file. (x)
- portfolio_analysis : tools_/portfolio_analysis : analyze the portfolio. (x)
- recommendation : tools_/recommendation : recommend the Job based on the matching rate. 


# cover-agent
If you start frontend 
```
streamlit run ./front/front.py --server.port=5000
```
If you start backend
```
uvicorn agent:app --reload --host 0.0.0.0 --port 8000
```

# Sequence
First make a frontend with a react or next.js

Second, connect backend and frontend 

Third, make Job RAG system with Milvus.