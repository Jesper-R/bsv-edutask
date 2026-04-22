import pytest
from src.controllers.usercontroller import UserController
from src.util.dao import DAO
from unittest.mock import MagicMock

@pytest.fixture
def sut():
    mock_dao = MagicMock()
    return UserController(dao=mock_dao)

@pytest.mark.unit
def test_get_user_by_email_invalid_email_raises_value_error(sut):
    # Arrange (Handled by fixture)

    # Act / Assert
    with pytest.raises(ValueError):
        sut.get_user_by_email('invalid-email')

@pytest.mark.unit
def test_get_user_by_email_no_users_returns_none(sut):
    # Arrange
    sut.dao.find.return_value = []

    # Act
    result = sut.get_user_by_email('john@example.com')

    # Assert
    assert result is None

@pytest.mark.unit
def test_get_user_by_email_one_user_returns_user(sut):
    # Arrange
    user = {'email': 'john@example.com', 'firstName': 'John', 'lastName': 'Doe'}
    sut.dao.find.return_value = [user]

    # Act
    result = sut.get_user_by_email('john@example.com')

    # Assert
    assert result == user

@pytest.mark.unit
def test_get_user_by_email_multiple_users_returns_first_and_warns(sut, capsys):
    # Arrange
    user1 = {'email': 'john@example.com', 'firstName': 'John', 'lastName': 'Doe'}
    user2 = {'email': 'john@example.com', 'firstName': 'John2', 'lastName': 'Doe2'}
    sut.dao.find.return_value = [user1, user2]

    # Act
    result = sut.get_user_by_email('john@example.com')
    captured = capsys.readouterr()

    # Assert
    assert result == user1
    assert 'john@example.com' in captured.out

@pytest.mark.unit
def test_get_user_by_email_database_fails_raises_exception(sut):
    # Arrange
    sut.dao.find.side_effect = Exception('Database error')

    # Act / Assert
    with pytest.raises(Exception):
        sut.get_user_by_email('john@example.com')
