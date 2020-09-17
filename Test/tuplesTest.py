def tester():
    yes = True
    if not(yes):
        uri = "123124341"
        artist = "Blue"
        album = "Machine"
        return uri, artist, album
    else:
        # Base Case
        return False


albumInfo = tester()

print(albumInfo)
