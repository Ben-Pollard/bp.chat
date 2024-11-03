def test_call_test_endpoint(api_client):
    response_gen = api_client.get_test_response()
    response = "".join([r["utterance"] for r in response_gen])
    assert response == "hello there"
