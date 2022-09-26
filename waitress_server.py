import waitress
import main

waitress.serve(main.app, host="127.0.1.2", port=6969)