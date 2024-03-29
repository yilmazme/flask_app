from website import create_app
import os

app = create_app()
port = int(os.environ.get('PORT', 33507))

if __name__ == "__main__":
    app.run(port=port)