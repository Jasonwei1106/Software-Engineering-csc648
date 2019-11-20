from . import *

## TO GET RID OF IN DEPLOYMENT ##
#################
### HOME PAGE ###
#################

@app.route('/api')
@app.route('/api/home')
def home():
    return jsonify({'message': 'Hello World!'}), 200
