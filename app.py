from fastapi import FastAPI

app = FastAPI()

def is_prime(num: int) -> bool:
    if num < 2:
        return False
    elif num == 2:
        return True
    elif num % 2 == 0:
        return False
    for i in range(3, int(num**0.5) + 1, 2):
        if num % i == 0:
            return False
    return True

def list_of_primes(st: int, nd: int) -> list:
    return [i for i in range(st, nd+1) if is_prime(i)]

def prime_factors(num: int) -> list:
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return [i] + prime_factors(num // i)
    return [int(num)]

@app.get("/is_prime/{num}", summary="Check if the given number is a prime number",  description="Check if the given number is a prime number")
def check_if_prime(num: int):
    return {"is_prime": is_prime(num)}

@app.get("/list_of_primes/{st}/{nd}")
def get_list_of_primes(st: int, nd: int):
    return {"list_of_primes": list_of_primes(st, nd)}

@app.get("/prime_factors/{num}")
def get_prime_factors(num: int):
    return {"prime_factors": prime_factors(num)}
