from fastapi import FastAPI

app = FastAPI()


@app.get("/query/")
async def query(inches: int):
    return {"message": "AGGGGGHHHHH" + str(inches)}