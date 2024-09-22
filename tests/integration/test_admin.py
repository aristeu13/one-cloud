import pytest


@pytest.mark.asyncio
async def test_get_admin_success(setup_database, client_test):
    response = await client_test.get(
        "/admin", headers={"Authorization": "Bearer valid_admin_token"}
    )

    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, admin!",
        "data": {
            "name": "Admin Master",
            "email": "admin@example.com",
            "reports": [
                {"id": 1, "title": "Monthly Sales", "status": "Completed"},
                {"id": 2, "title": "User Activity", "status": "Pending"},
            ],
        },
    }
