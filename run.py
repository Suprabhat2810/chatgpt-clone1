import logging
from server.app import app
from server.website import Website
from server.backend import Backend_Api
from flask import render_template, request
from json import load

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

@app.route('/home')
def home():
    return ('<h1>Welcome To VerCHell<h1>')

if __name__ == '__main__':
    config = load(open('config.json', 'r'))
    site_config = config['site_config']

    site = Website(app)
    for route in site.routes:
        app.add_url_rule(
            route,
            view_func=site.routes[route]['function'],
            methods=site.routes[route]['methods'],
        )

    backend_api = Backend_Api(app, config)
    for route in backend_api.routes:
        app.add_url_rule(
            route,
            view_func=backend_api.routes[route]['function'],
            methods=backend_api.routes[route]['methods'],
        )


    print(f"Running on port {site_config['port']}")
    app.run(**site_config)
    print(f"Closing port {site_config['port']}")