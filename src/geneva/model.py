import json
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select

engine = create_engine("sqlite:///data/geneva.db", echo=False)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    api_key: str


class UserQuery(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    gene: str
    disease: str
    service_response: str
    llm_response: Optional[str] = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


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


def save_user_query(
    user_id: int,
    gene: str,
    disease: str,
    service_response: dict,
    llm_response: Optional[dict] = None,
) -> UserQuery:
    with Session(engine) as session:
        query = UserQuery(
            user_id=user_id,
            gene=gene,
            disease=disease,
            service_response=json.dumps(service_response),
            llm_response=json.dumps(llm_response) if llm_response else None,
        )
        session.add(query)
        session.commit()
        session.refresh(query)
        return query


def get_user_queries(user_id: int) -> list[UserQuery]:
    with Session(engine) as session:
        statement = select(UserQuery).where(UserQuery.user_id == user_id)
        return session.exec(statement).all()
