import waitress
import main

waitress.serve(main.app, host="127.0.0.1", port=6969)