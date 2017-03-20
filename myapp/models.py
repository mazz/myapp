import datetime
from uuid import uuid4

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from websauna.system.model.meta import Base
from websauna.system.model.columns import UTCDateTime
from websauna.utils.time import now


class Question(Base):

    #: The table in the database
    __tablename__ = "question"

    #: Database primary key for the row (running counter)
    id = Column(Integer, autoincrement=True, primary_key=True)

    #: Publicly exposed non-guessable
    uuid = Column(UUID(as_uuid=True), default=uuid4)

    #: Question text
    question_text = Column(String(256), default=None)

    #: When this question was published
    published_at = Column(UTCDateTime, default=None)

    #: Relationship mapping between question and choice.
    #: Each choice can have only question.
    #: Deleting question deletes its choices.
    choices = relationship("Choice",
                           back_populates="question",
                           lazy="dynamic",
                           cascade="all, delete-orphan",
                           single_parent=True)

    def is_recent(self):
        return self.published_at >= now() - datetime.timedelta(days=1)

    def __repr__(self):
        return "#{}: {}".format(self.id, self.question_text)

    def __str__(self):
        """Python default and admin UI string presentation."""
        return self.question_text


class Choice(Base):

    #: The table in the database
    __tablename__ = "choice"

    #: Database primary key for the row (running counter)
    id = Column(Integer, autoincrement=True, primary_key=True)

    #: Publicly exposed non-guessable id
    uuid = Column(UUID(as_uuid=True), default=uuid4)

    #: What the user sees for this choice
    choice_text = Column(String(256), default=None)

    #: How many times this choice has been voted
    votes = Column(Integer, default=0)

    #: Which question this choice is part of
    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship("Question", back_populates="choices")

    def __repr__(self):
        """Shell and debugger presentation."""
        return "#{}: {}".format(self.id, self.choice_text)

    def __str__(self):
        """Python default and admin UI string presentation."""
        return self.choice_text
