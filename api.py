from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import mysql.connector
from mysql.connector import Error

app = FastAPI()

class Car(BaseModel):
    id: int
    license_plate: str
    distance: float

database=[]

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='carlot',
            user='root',
            password=''  # ตรวจสอบรหัสผ่านของ MySQL ที่ใช้
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def insert_data(connection, distance):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO distance_data (distance) VALUES (%s)"
        cursor.execute(query, (distance,))
        connection.commit()
    except Error as e:
        print(f"Error while inserting data into MySQL: {e}")

@app.post("/data")
async def receive_data(data: Car):
    connection = create_connection()
    if connection:
        insert_data(connection, data.distance)
        connection.close()
    print(f"Car Height: {data.distance}")
    return {"status": "success"}

@app.post("/cars/", response_model=Car)
async def create_car(car: Car):
    database.append(car)
    return car

@app.get("/cars/", response_model=List[Car])
async def get_cars():
    return database

@app.get("/cars/{car_id}", response_model=Car)
async def get_car(car_id: int):
    for car in database:
        if car.id == car_id:
            return car
    return {"error": "Car not found"}

@app.put("/cars/{car_id}", response_model=Car)
async def update_car(car_id: int, car: Car):
    for idx, existing_car in enumerate(database):
        if existing_car.id == car_id:
            database[idx] = car
            return car
    return {"error": "Car not found"}

@app.delete("/cars/{car_id}", response_model=Car)
async def delete_car(car_id: int):
    for idx, existing_car in enumerate(database):
        if existing_car.id == car_id:
            deleted_car = database.pop(idx)
            return deleted_car
    return {"error": "Car not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.31.206", port=8000)
