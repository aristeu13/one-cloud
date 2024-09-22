import pytest


@pytest.mark.asyncio
async def test_get_user_success(setup_database, client_test):
    response = await client_test.get(
        "/user", headers={"Authorization": "Bearer valid_user_token"}
    )

    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, user!",
        "data": {
            "name": "John Doe",
            "email": "john@example.com",
            "purchases": [
                {"id": 1, "item": "Laptop", "price": 2500},
                {"id": 2, "item": "Smartphone", "price": 1200},
            ],
        },
    }
