"""Unit tests for comment_service.py"""
import pytest
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from app.database.models.comment import Comment, CommentCreate
from app.services.comment_service import create_comment, get_comments_tree, get_comment
from app.database.models.user import User

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Comment.metadata.create_all(engine)
    User.metadata.create_all(engine)
    with Session(engine) as session:
        # Create test user
        user = User(username="testuser", email="test@example.com", hashed_password="fake")
        session.add(user)
        session.commit()
        yield session

def test_create_comment(session: Session):
    """Test creating a root-level comment"""
    comment_data = CommentCreate(content="Test comment")
    comment = create_comment(session, comment_data, user_id=1)
    
    assert comment.id is not None
    assert comment.content == "Test comment"
    assert comment.user_id == 1
    assert comment.parent_id == 0

def test_create_reply(session: Session):
    """Test creating a reply to another comment"""
    # First create parent comment
    parent = create_comment(session, CommentCreate(content="Parent"), user_id=1)
    
    # Create reply
    reply_data = CommentCreate(content="Reply", parent_id=parent.id)
    reply = create_comment(session, reply_data, user_id=2)
    
    assert reply.parent_id == parent.id
    assert reply.user_id == 2

def test_get_comments_tree(session: Session):
    """Test building comment tree structure"""
    # Create test comments
    root1 = create_comment(session, CommentCreate(content="Root Comment 1"), user_id=1)
    root2 = create_comment(session, CommentCreate(content="Root Comment 2"), user_id=1)
    reply1 = create_comment(session, CommentCreate(content="Reply 1", parent_id=root1.id), user_id=1)
    reply2 = create_comment(session, CommentCreate(content="Reply 2", parent_id=root1.id), user_id=1)
    
    # Refresh objects to ensure relationships are loaded
    session.refresh(root1)
    session.refresh(root2)
    session.refresh(reply1)
    session.refresh(reply2)
    
    # Get tree
    tree = get_comments_tree(session)
    print(f"Tree: {tree}") 
    
    assert len(tree) == 2  # Two roots
    # # Check children are properly attached
    root1 = next(c for c in tree if c.id == root1.id)
    print(f"root1.children: {root1.children}")
    assert len(root1.children) == 2  # Should have 2 child replies
    # Replies should be ordered newest first
    assert root1.children[0].content == "Reply 2"
    assert root1.children[1].content == "Reply 1"

def test_get_comment(session: Session):
    """Test retrieving a single comment"""
    comment = create_comment(session, CommentCreate(content="Test"), user_id=1)
    found = get_comment(session, comment.id)
    
    assert found.id == comment.id
    assert found.content == "Test"

