# python_as_service

# Steps To Setup
0. Created "static", which is a sort of stand-alone UI bundled for this API
1. 
```
py -m venv serv
```
2. 
```
./serv/Scripts/Activate.ps1
```
3. 
```
pip install fastapi
```
4. 
```
pip install uvicorn[standard]
```
5. Created main.py
6. Created app.py
7. 
```
pip install asyncua
```
8. Split routers into "routers" folder
9. Split Pydantic models into "pydantic models" folder
10. Separated OPC code into "opcua" folder
11. Created settings.json
12. Created global_variables.py
13. 
```
pip install psutil
```
14. 
```
pip freeze
```
15. Placed output of above command into "requirements.txt"
