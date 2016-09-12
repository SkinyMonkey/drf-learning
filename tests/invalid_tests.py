import requests

def request(user, url, method, body={}):
    url = "http://127.0.0.1:8000" + url
    if (method == "get"):
        return requests.get(url, auth=(user['username'], user['password'])) 
    elif (method == "post"):
        return requests.post(url, auth=(user['username'], user['password']), json=body)
    elif (method == "delete"):
        return requests.delete(url, auth=(user['username'], user['password']), json=body)
    else:
        raise Exception("Not implemented")

def remove(user, url):
    res = request(user, url, "delete")
    assert res.status_code == 204
    return res

def get_user(admin_user, user):
    url = "/users/?username=" + user['username']
    res = request(admin_user, url, "get")
    assert res.status_code == 200
    return res

def get(user, url):
    res = request(user, url, "get")
    assert res.status_code == 200
    return res.json()

def create_user(admin_user, user):
    """
    Create a user
    """
    url = "/users/"
    res = request(admin_user, url, "post", user)
    assert res.status_code == 201
    return res.json()

def create_playlist(user):
    """
    Creates a playlist for the created user
    """
    url = "/playlists/"
    res = request(user, url, "post", {"name": "test_playlist"})
    assert res.status_code == 400
    assert 'PLAYLIST_ALREADY_EXISTS' in res.json()['non_field_errors']
    print "create playlist invalid: [OK]"
    return res.json()

def create_track(user, playlist, error, source_url = None):
    """
    Creates a track in a user playlist
    """
    if source_url == None:
        source_url = "https://www.youtube.com/watch?v=hgu28Hqg8Vc"
    url = "/playlists/%s/tracks/" % (playlist['id'])
    res = request(user, url, "post", {"source_url": source_url})
    assert res.status_code == 400
    assert error in res.json()['non_field_errors']

    print "create track invalid: [OK]"
    return res.json()

def list_tracks(user, playlist, track):
    """
    """
    url = "/playlists/%s/tracks" % (playlist['id'])
    res = request(user, url, "get")
    assert res.status_code == 200
#    print res.json()['results']

    print "list_tracks from playlists: [OK]"

    # FIXME : assert that source_url is in the result
    #         assert that url_checksum is not exposed
#    assert track in res.json['results']

def follow(user, follower, error):
    """
    """
    url = "/follows/"
    res = request(follower, url, "post", {"followed": user['id']})
    assert res.status_code == 400

    result = res.json()

    if ('followed' in result):
        assert error in result['followed']
    else:
        assert error in result['non_field_errors']

    print "follow a user invalid : [OK]"
    return result


def like(user, track):
    """
    """
    url = "/likes/"
    res = request(user, url, "post", {"track_id": track['id']})
    assert res.status_code == 400
    assert "USER_ALREADY_LIKED" in res.json()['non_field_errors']

    print "like a track invalid : [OK]"

    return res.json()

def get_stream(user, tracks):
    """
    """
    url = "/stream/"
    res = request(user, url, "get")
    assert res.status_code == 200

    # FIXME : check that the tracks are in there

    print "get a stream : [OK]"

    return res.json()
    

def get_or_create_user(username, email, password):
    admin_user = {"username": "adrien", "password": "lolilollolilol"}

    user = {"username": username, "email": email, "password": password}

    existing_user = get_user(admin_user, user)

    if len(existing_user.json()['results']) > 0:
        user = existing_user.json()['results'][0]
    else:
        create_user(admin_user, user)

#    print user

    user['password'] = password

    print "Get user: [OK]"

    return user

def cleaning(user, ressource_name):
    result = get(user, "/%s/?owner_id=%s" % (ressource_name, user['id']))

    print "filter on %s: [OK]" % ressource_name

    if len(result['results']) > 0:
        remove(user, "/%s/%s/" % (ressource_name, result['results'][0]['id']))

    print "cleaning %s: [OK]" % ressource_name

def tests(valid_results):
    """
    """

    # TODO
    # forbidden everywhere needed

    user = get_or_create_user("auto_test", "test@test.com", "test")
    follower = get_or_create_user("second_auto_test", "test2@test.com", "test")

    create_playlist(user)

    playlist = valid_results["playlist"]

    # source_url checks
#   create_track(user, playlist, "TRACK_ALREADY_IN_PLAYLIST") # FIXME : replace
    create_track(user, playlist, "TRACK_ALREADY_REGISTERED")
    create_track(user, playlist, "INVALID_PROVIDER", "http://google.fr")
    create_track(user, playlist, "UNEXISTING_VIDEO_SOURCE",
                                 "https://www.youtube.com/watch?v=Sagg08DrO5u")

    follow(user, user, 'CANT_FOLLOW_SELF')
    follow(user, follower, 'USER_ALREADY_FOLLOWING')

    like(user, valid_results['track'])

    print "All invalid tests pass !!!"
