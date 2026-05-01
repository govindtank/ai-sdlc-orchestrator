"""
SQLAlchemy models for AI SDLC Orchestrator
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    projects = relationship("Project", back_populates="owner")
    requirements = relationship("Requirement", back_populates="owner")
    user_stories = relationship("UserStory", back_populates="owner")
    design_suggestions = relationship("DesignSuggestion", back_populates="owner")
    code_reviews = relationship("CodeReview", back_populates="owner")
    resource_gaps = relationship("ResourceGap", back_populates="owner")
    estimates = relationship("Estimate", back_populates="owner")
    test_cases = relationship("TestCase", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    owner = relationship("User", back_populates="projects")
    requirements = relationship("Requirement", back_populates="project")
    user_stories = relationship("UserStory", back_populates="project")
    design_suggestions = relationship("DesignSuggestion", back_populates="project")
    code_reviews = relationship("CodeReview", back_populates="project")
    resource_gaps = relationship("ResourceGap", back_populates="project")

class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    raw_text = Column(Text)
    refined_text = Column(Text, nullable=True)
    clarification_questions = Column(Text, nullable=True)  # Stored as JSON string
    status = Column(String, default="raw")  # raw, refined, clarified
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="requirements")
    owner = relationship("User", back_populates="requirements")
    user_stories = relationship("UserStory", back_populates="requirement")

class UserStory(Base):
    __tablename__ = "user_stories"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    requirement_id = Column(Integer, ForeignKey("requirements.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text)
    acceptance_criteria = Column(Text, nullable=True)  # Stored as JSON string
    story_points = Column(Integer, nullable=True)
    status = Column(String, default="draft")  # draft, refined, estimated, approved
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="user_stories")
    requirement = relationship("Requirement", back_populates="user_stories")
    owner = relationship("User", back_populates="user_stories")
    test_cases = relationship("TestCase", back_populates="user_story")
    design_suggestions = relationship("DesignSuggestion", back_populates="user_story")
    code_reviews = relationship("CodeReview", back_populates="user_story")

class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    user_story_id = Column(Integer, ForeignKey("user_stories.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text)
    test_type = Column(String)  # functional, edge_case, performance, security
    steps = Column(Text)  # Stored as JSON string
    expected_result = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_story = relationship("UserStory", back_populates="test_cases")
    owner = relationship("User", back_populates="test_cases")

class DesignSuggestion(Base):
    __tablename__ = "design_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    user_story_id = Column(Integer, ForeignKey("user_stories.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    wireframe_description = Column(Text)
    ui_component_suggestions = Column(Text)  # Stored as JSON string
    design_notes = Column(Text)
    status = Column(String, default="generated")  # generated, reviewed, approved
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user_story = relationship("UserStory", back_populates="design_suggestions")
    project = relationship("Project", back_populates="design_suggestions")
    owner = relationship("User", back_populates="design_suggestions")

class CodeReview(Base):
    __tablename__ = "code_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_story_id = Column(Integer, ForeignKey("user_stories.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    commit_hash = Column(String)
    file_path = Column(String)
    review_comments = Column(Text)  # Stored as JSON string
    suggestions = Column(Text)  # Stored as JSON string
    status = Column(String, default="pending")  # pending, reviewed, resolved
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_story = relationship("UserStory", back_populates="code_reviews")
    project = relationship("Project", back_populates="code_reviews")
    owner = relationship("User", back_populates="code_reviews")

class ResourceGap(Base):
    __tablename__ = "resource_gaps"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    gap_type = Column(String)  # requirement, design, data, api, asset
    description = Column(Text)
    suggested_solution = Column(Text)
    severity = Column(String)  # low, medium, high
    status = Column(String, default="open")  # open, in_progress, resolved
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project")
    owner = relationship("User")

class Estimate(Base):
    __tablename__ = "estimates"

    id = Column(Integer, primary_key=True, index=True)
    user_story_id = Column(Integer, ForeignKey("user_stories.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    story_points = Column(Integer)
    confidence = Column(String)  # high, medium, low
    method = Column(String)  # llm, heuristic
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user_story = relationship("UserStory", back_populates="estimates")
    owner = relationship("User", back_populates="estimates")