from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select

engine = create_engine("sqlite:///data/geneva.db", echo=False)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    api_key: str


def create_tables():
    SQLModel.metadata.create_all(engine)


def create_user(username: str, api_key: str) -> User:
    with Session(engine) as session:
        user = User(username=username, api_key=api_key)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user_by_name(username: str) -> Optional[User]:
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()


def user_exists(username: str) -> bool:
    return get_user_by_name(username) is not None
