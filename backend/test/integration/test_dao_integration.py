import pytest
import pymongo

from src.util.dao import DAO
from pymongo.errors import WriteError
from unittest.mock import patch

@pytest.fixture
def sut():
    # Setup
    test_client = pymongo.MongoClient()
    test_db = test_client['edutask_test']

    with patch('src.util.dao.pymongo.MongoClient') as MockMongoClient:
        MockMongoClient.return_value.edutask = test_db
        user_dao = DAO('user')
        todo_dao = DAO('todo')
        yield {'user_dao': user_dao, 'todo_dao': todo_dao}

        # Teardown
        user_dao.drop()
        todo_dao.drop()

    test_client.close()


@pytest.mark.integration
def test_create_all_conditions_met_returns_object(sut):
    # Arrange
    valid_user = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john@example.com'
    }

    # Act
    result = sut['user_dao'].create(valid_user)
    #print(result)

    # Assert
    assert result is not None
    assert '_id' in result
    assert result['firstName'] == valid_user['firstName']
    assert result['lastName'] == valid_user['lastName']
    assert result['email'] == valid_user['email']

@pytest.mark.integration
def test_create_missing_required_property_raises_write_error(sut):
    # Arrange
    invalid_user = {
        'firstName': 'John',
        'lastName': 'Doe'
    }

    # Act / Assert
    with pytest.raises(WriteError):
        sut['user_dao'].create(invalid_user)

@pytest.mark.integration
@pytest.mark.parametrize(
    'dao_name, invalid_data',
    [
        ('user_dao', {'firstName': 123, 'lastName': 'Doe', 'email': 'john@example.com'}),
        ('todo_dao', {'description': 'This is a todo item', 'done': 'string'})
    ]
)
def test_create_bson_type_violation_raises_write_error(sut, dao_name, invalid_data):

    # Act / Assert
    with pytest.raises(WriteError):
        sut[dao_name].create(invalid_data)

@pytest.mark.integration
def test_create_unique_violation_raises_write_error(sut):
    # Arrange
    user_one = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john@example.com'
    }
    sut['user_dao'].create(user_one)

    duplicate_user_one = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john@example.com'
    }

    # Act / Assert
    with pytest.raises(WriteError):
        sut['user_dao'].create(duplicate_user_one)

@pytest.mark.integration
def test_create_database_failing_raises_exception(sut):
    # Arrange
    valid_user = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john@example.com'
    }

    with patch.object(sut['user_dao'].collection, 'insert_one', side_effect=Exception('Database error')):
        # Act / Assert
        with pytest.raises(Exception):
            sut['user_dao'].create(valid_user)
