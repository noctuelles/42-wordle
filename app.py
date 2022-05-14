from flask import (
    Flask, 
    jsonify,
    render_template
)

def create_app(test_config=None ):
    app = Flask(__name__)

    @app.route('/')
    def hello_world(): 
        return render_template('hello.html', name='name')
        # return jsonify({
        #    "status": "success",
        #     "message": "Hello World!"
        # }) 
     
    return app

APP = create_app()

if __name__ == '__main__':
    # APP.run(host='0.0.0.0', port=5000, debug=True)
    APP.run(debug=True)