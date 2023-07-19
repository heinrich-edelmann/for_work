import uvicorn
from multiprocessing import cpu_count, freeze_support

def start_server(host = "127.0.0.1",
                port = 5000,
                num_workers=4,
                loop="asyncio",
                reload=False):
                uvicorn.run("fastapi_aufgabe:app",
                host=host,
                port=port,
                workers=num_workers,
                loop=loop,
                reload=reload)

if __name__ == "__main__":
    freeze_support()
    num_workers = int(cpu_count() * 0.75)
    start_server(num_workers=num_workers)




