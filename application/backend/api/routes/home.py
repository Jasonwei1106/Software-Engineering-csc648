""" Home Route

This file contains the home route mainly used for testing.

"""

from . import *

@app.route('/api/home')
def home():
    """
    Home route to test frontend is connected to backend code.

    Parameters
    ----------

    Returns
    -------
    "Hello World!"

    """
    return jsonify({'message': 'Hello World!'}), 200
