import requests
from time import time

def profile(f):
    t = time()
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        print time() - t
        return res
    return wrapper

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
    assert res.status_code == 201
    assert res.json()['owner_id'] == user['id']
    print "create playlist: [OK]"
    return res.json()

def create_track(user, playlist):
    """
    Creates a track in a user playlist
    """
    url = "/playlists/%s/tracks/" % (playlist['id'])
    res = request(user, url, "post", {"source_url": "https://www.youtube.com/watch?v=hgu28Hqg8Vc"})
    assert res.status_code == 201
    # FIXME : assert owner_id and playlist_id
    print "create track: [OK]"
    return res.json()

def list_tracks(user, playlist, track):
    """
    """
    url = "/playlists/%s/tracks/" % (playlist['id'])
    res = request(user, url, "get")
    assert res.status_code == 200
#    print res.json()['results']

    print "list_tracks from playlists: [OK]"

    # FIXME : assert that source_url is in the result
    #         assert that url_checksum is not exposed
#    assert track in res.json['results']

def follow(user, follower):
    """
    """
    url = "/follows/"
    res = request(follower, url, "post", {"followed": user['id']})
    assert res.status_code == 201

    # FIXME : assert owner_id and followed

    print "follow a user : [OK]"

    return res.json()


def like(user, track):
    """
    """
    url = "/likes/"
    res = request(user, url, "post", {"track_id": track['id']})
    assert res.status_code == 201
    
    # FIXME : assert owner_id and track_id

    print "like a track : [OK]"

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
        for ressource in result['results']:
            remove(user, "/%s/%s/" % (ressource_name, ressource['id']))

    print "cleaning %s: [OK]" % ressource_name

def tests():
    """
    """

    # FIXME : redo things without auth to check some publicly accessible
    # endpoints

    user = get_or_create_user("auto_test", "test@test.com", "test")
    follower = get_or_create_user("second_auto_test", "test2@test.com", "test")

    cleaning(user, "playlists")
    cleaning(user, "tracks")
    cleaning(follower, "follows")

    playlist = create_playlist(user)

    track = create_track(user, playlist)

    list_tracks(user, playlist, track)

    like(user, track)

    follow(user, follower)

    # FIXME : create other tracks for better checks
    get_stream(follower, [track])

    print "All normal tests pass !!!"

    results = {
        "playlist": playlist,
        "track": track,
    }

    return results
