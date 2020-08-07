from pushbullet.pushbullet import PushBullet

api_key = ''

pb = PushBullet(api_key)


# Get a list of devices
devices = pb.getDevices()
print(devices)

# test values
albumURI = "1231232141sdasd"
deviceID = "123214123212"

# Send a note
note_title = 'Played ' + albumURI
note_body = 'Song played on ' + deviceID
pb.pushNote(devices[1]["iden"], note_title, note_body)
