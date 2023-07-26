# FastAPI

# Install dependencies
```python
pip install -r requirements.tx
```

# Run the server
```console
uvicorn main:app --reload
```

# Check api

http://127.0.0.1:8000/items/5?q=pablo%20emilio%20escobar

response {"item_id":5,"q":"pablo emilio escobar"}
