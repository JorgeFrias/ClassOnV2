from classOn import app, socketio


# # No debug with pycharm
# if __name__ == '__main__':
#     # _assigment = setAssigment()         # Set the assigment
#     app.secret_key = 'secret123'
#     # app.run(threaded=True)              # Allow multiple users
#     app.run()              # Allow one user

# Debug with pycharm
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Development Server Help')
    parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
                        help="run in debug mode (for use with PyCharm)", default=False)
    parser.add_argument("-p", "--port", dest="port",
                        help="port of server (default:%(default)s)", type=int, default=5000)

    cmd_args = parser.parse_args()
    app_options = {"port": cmd_args.port}

    if cmd_args.debug_mode:
        app_options["debug"] = True
        app_options["use_debugger"] = False
        app_options["use_reloader"] = False
        app_options["threaded"] = True

    # app.run(**app_options)                    # Run without socket.io
    socketio.run(app)                           # Run with socket.io