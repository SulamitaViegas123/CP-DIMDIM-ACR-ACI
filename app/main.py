from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql

app = FastAPI(title="DimDim API - Demo Funcional")

# -------- MODELS --------
class User(BaseModel):
    name: str
    email: str

class Transaction(BaseModel):
    user_id: int
    amount: float
    type: str

# -------- DATABASE CONNECTION --------
def get_connection():
    try:
        conn = pymysql.connect(
            host="db",           # nome do serviço MySQL no docker-compose
            user="root",
            password="root",
            database="dimdim",
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro de conexão: {e}")

# -------- USERS --------
@app.post("/users")
def create_user(user: User):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (name, email) VALUES (%s,%s)"
            cursor.execute(sql, (user.name, user.email))
            conn.commit()
            user_id = cursor.lastrowid
        conn.close()
        return {"message": "User criado", "user": {"id": user_id, "name": user.name, "email": user.email}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users")
def get_users():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
        conn.close()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "UPDATE users SET name=%s, email=%s WHERE id=%s"
            cursor.execute(sql, (user.name, user.email, user_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User não encontrado")
        conn.close()
        return {"message": "User atualizado", "user": {"id": user_id, "name": user.name, "email": user.email}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User não encontrado")
        conn.close()
        return {"message": "User deletado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------- TRANSACTIONS --------
@app.post("/transactions")
def create_transaction(transaction: Transaction):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            # Verifica se o user_id existe
            cursor.execute("SELECT * FROM users WHERE id=%s", (transaction.user_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="User não encontrado para transação")

            sql = "INSERT INTO transactions (user_id, amount, type) VALUES (%s,%s,%s)"
            cursor.execute(sql, (transaction.user_id, transaction.amount, transaction.type))
            conn.commit()
            tx_id = cursor.lastrowid
        conn.close()
        return {"message": "Transaction criada", "transaction": {"id": tx_id, "user_id": transaction.user_id, "amount": transaction.amount, "type": transaction.type}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transactions")
def get_transactions():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM transactions")
            txs = cursor.fetchall()
        conn.close()
        return {"transactions": txs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, transaction: Transaction):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            # Verifica se o user_id existe
            cursor.execute("SELECT * FROM users WHERE id=%s", (transaction.user_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="User não encontrado para transação")

            sql = "UPDATE transactions SET user_id=%s, amount=%s, type=%s WHERE id=%s"
            cursor.execute(sql, (transaction.user_id, transaction.amount, transaction.type, transaction_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Transaction não encontrada")
        conn.close()
        return {"message": "Transaction atualizada", "transaction": {"id": transaction_id, "user_id": transaction.user_id, "amount": transaction.amount, "type": transaction.type}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM transactions WHERE id=%s", (transaction_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Transaction não encontrada")
        conn.close()
        return {"message": "Transaction deletada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------- HOME --------
@app.get("/")
def home():
    return {"message": "DimDim API DEMO funcionando"}