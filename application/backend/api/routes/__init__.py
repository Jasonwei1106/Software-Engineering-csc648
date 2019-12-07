""" Init File for Routes

This file is to connect all the routes. The init file imports the methods
token_required decorator, average_rating_type_for_tutorial helper function,
and all imports needed for the route files.

"""

from .config import *

from .comments_routes import *
from .home import *
from .item_routes import *
from .rating_routes import *
from .steps_routes import *
from .tutorial_routes import *
from .user_routes import *
