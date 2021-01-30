from khairo import app, template


@app.get("/")
def Home():
    return "Home"