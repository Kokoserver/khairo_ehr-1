import uvicorn

if __name__ == '__main__':
    uvicorn.run("khairo:app", debug=True, reload=True)

