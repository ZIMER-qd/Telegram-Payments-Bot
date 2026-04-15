from app.database.models import async_session
from app.database.models import User, Subscription, Product, UserProduct

from sqlalchemy import delete, select

from typing import List

import logging