from voluptuous import Schema, PREVENT_EXTRA
from pytest_voluptuous import S
from utils.base_session import reqres_session
from requests import Response

read_user_schema = Schema(
    {
        "data": {
            "id": int,
            "email": str,
            "first_name": str,
            "last_name": str,
            "avatar": str
        },
        "support": {
            "url": str,
            "text": str
        }
    },
    extra=PREVENT_EXTRA,
    required=True,
)

create_user_schema = Schema(
    {
        'name': str,
        'job': str,
        'id': str,
        'createdAt': str,
    },
    required=True,
    extra=PREVENT_EXTRA
)

update_user_schema = Schema(
    {
        'name': str,
        'job': str,
        'updatedAt': str
    },
    required=True,
    extra=PREVENT_EXTRA
)

register_user_schema = Schema(
    {
        'id': int,
        'token': str,
    },
    required=True,
    extra=PREVENT_EXTRA
)

def test_get_users():
    result: Response = reqres_session().get(
        '/api/users',
        params={'page': 2}
    )

    assert result.status_code == 200
    assert result.json()['page'] == 2
    assert len(result.json()['data']) != 0

def test_get_single_user():

    result: Response = reqres_session().get(
        url='/api/users/3',
    )

    assert result.status_code == 200
    assert result.json() == S(read_user_schema)
    assert len(result.json()['data']) != 0
    assert len(result.json()['support']) != 0
    assert result.json()['data']['first_name'] == 'Emma'

def test_create_user():
    name = 'morpheus'
    job = 'leader'

    result: Response = reqres_session().post(
        url='/api/users',
        json={"name": name, "job": job}
    )

    assert result.status_code == 201
    assert result.json()['name'] == name
    assert result.json()['job'] == job
    assert isinstance(result.json()['id'], str)
    assert result.json() == S(create_user_schema)

def test_update_user():
    name = 'morpheus'
    job = 'zion resident'

    result: Response = reqres_session().put(
        url='/api/users/2',
        json={"name": name, "job": job}
    )

    assert result.status_code == 200
    assert result.json()['name'] == name
    assert result.json()['job'] == job
    assert result.json() == S(update_user_schema)

def test_delete_user():
    result: Response = reqres_session().delete(
        url='/api/users/2',
    )

    assert result.status_code == 204

def test_register_user():
    email = "eve.holt@reqres.in"
    password = "pistol"

    result: Response = reqres_session().post(
        url='/api/register',
        json={"email": email, "password": password}
    )

    assert result.status_code == 200
    assert result.json() == S(register_user_schema)
    assert isinstance(result.json()['id'], int)
    assert isinstance(result.json()['token'], str)
    assert result.json()['id'] == 4
    assert result.json()['token'] == 'QpwL5tke4Pnpja7X4'



