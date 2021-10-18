#pylint: disable=W0612
#pylint: disable=R0801
"""
Fixture test file
testing the fixture
"""

# test fixtures against dummy code
# Do not run this during demo

def test_fixtures(auth_fixture):
    """
    Testing inputs from auth_fixture
    """
    (server_data, auth_fixture) = auth_fixture
    # you can access fixture data directly like this
    assert auth_fixture[0]["email"] == "richard@gmail.com"
    assert auth_fixture[1]["email"] == "kevin@gmail.com"
    assert auth_fixture[2]["email"] == "steven@gmail.com"
    assert auth_fixture[3]["email"] == "jay@gmail.com"
    assert auth_fixture[4]["email"] == "robert@gmail.com"

    assert auth_fixture[0]["password"] == "12345333"
    assert auth_fixture[1]["password"] == "099401010"
    assert auth_fixture[2]["password"] == "312214141"
    assert auth_fixture[3]["password"] == "10003DDfe"
    assert auth_fixture[4]["password"] == "jfkw22131"

def test_channels_fixture_richard(channels_fixture):
    """
    Testing inputs from channel_fixture
    """
    (server_data, channels_fixture) = channels_fixture
    assert channels_fixture[0]["email"] == "richard@gmail.com"
    assert channels_fixture[0]["channels"][0]["name"] == "COMP1531"
    assert channels_fixture[0]["channels"][0]["is_public"]
    assert channels_fixture[0]["channels"][0]["channel_id"] == 0
    assert channels_fixture[0]["channels"][1]["name"] == "COMP2511"
    assert channels_fixture[0]["channels"][1]["is_public"]
    assert channels_fixture[0]["channels"][1]["channel_id"] == 5

def test_channels_fixture_kevin(channels_fixture):
    """
    Testing inputs from channel_fixture
    """
    (server_data, channels_fixture) = channels_fixture
    assert channels_fixture[1]["email"] == "kevin@gmail.com"
    assert channels_fixture[1]["channels"][0]["name"] == "ENG1001"
    assert not channels_fixture[1]["channels"][0]["is_public"]
    assert channels_fixture[1]["channels"][0]["channel_id"] == 1

def test_channels_fixture_steven(channels_fixture):
    """
    Testing inputs from channel_fixture
    """
    (server_data, channels_fixture) = channels_fixture
    assert channels_fixture[2]["email"] == "steven@gmail.com"
    assert channels_fixture[2]["channels"][0]["name"] == "COMP3331"
    assert channels_fixture[2]["channels"][0]["is_public"]
    assert channels_fixture[2]["channels"][0]["channel_id"] == 2

def test_channels_fixture_jay(channels_fixture):
    """
    Testing inputs from channel_fixture
    """
    (server_data, channels_fixture) = channels_fixture
    assert channels_fixture[3]["email"] == "jay@gmail.com"
    assert channels_fixture[3]["channels"][0]["name"] == "COMP3211"
    assert channels_fixture[3]["channels"][0]["is_public"]
    assert channels_fixture[3]["channels"][0]["channel_id"] == 3

def test_channels_fixture_robert(channels_fixture):
    """
    Testing inputs from channel_fixture
    """
    (server_data, channels_fixture) = channels_fixture
    assert channels_fixture[4]["email"] == "robert@gmail.com"
    assert channels_fixture[4]["channels"][0]["name"] == "ADAD1010"
    assert not channels_fixture[4]["channels"][0]["is_public"]
    assert channels_fixture[4]["channels"][0]["channel_id"] == 4
