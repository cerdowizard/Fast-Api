from sqlalchemy import Boolean, Column, String, Integer, Enum, DateTime, func, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from api.database.database_connect import Base


class Roles(str, enum.Enum):
    Admin = "admin"
    User = "user"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(101), unique=True, nullable=False)
    email = Column(String(101), nullable=False, unique=True, index=True)
    password = Column(String(101), nullable=False)
    is_active = Column(Boolean(), default=True)
    role = Column(Enum(Roles), default=Roles.User)
    created_at = Column(DateTime(), default=func.now())
    posts = relationship("Post", back_populates="owner", cascade="all,delete")


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(101), nullable=False, unique=True, index=True)
    short_desc = Column(String(101), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(101), nullable=False)
    imageUrl = Column(String(101), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")
    author = Column(String(101))
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), onupdate=datetime.now())


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(101), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), onupdate=datetime.now())


class Token(Base):
    __tablename__ = "rest_code"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(101), nullable=False, unique=True, index=True)
    rest_code = Column(String(101))
    expire_in = Column(DateTime)
    created_at = Column(DateTime(), default=func.now())

# created_by = Column(INTEGER, nullable=True)
# created_at = Column(TIMESTAMP, nullable=False,
#                     server_default=text("CURRENT_TIMESTAMP"))
# updated_by = Column(INTEGER, nullable=True)
# updated_at = Column(TIMESTAMP, nullable=True,
#                     server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

# from sqlalchemy import Table, Column, Float, Enum, Integer, String, Sequence, DateTime, MetaData
#
# metadata = MetaData()
#
# users = Table(
#     "py_user", metadata,
#     Column("id", Integer, Sequence("user_id_seq"), primary_key=True),
#     Column("email", String(101)),
#     Column("password", String(101)),
#     Column("Fullname", String(101)),
#     Column("created_on", DateTime),
#     Column("status", String(1))
#
# )
#
# transaction = Table(
#     "transaction", metadata,
#     Column("id", Integer, primary_key=True),
#     Column("customer_name", String(101)),
#     Column("gas_quantity", Float),
#     Column("gas_price", Float),
#     Column("total_price", Float),
#     Column("created_on", DateTime),
#     Column("status", String(1))
# )
#
