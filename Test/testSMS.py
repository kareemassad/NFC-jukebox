from pushbullet.pushbullet import PushBullet

api_key = ''

pb = PushBullet(api_key)


# Get a list of devices
devices = pb.getDevices()
print(devices)

# Send a note
pb.pushNote(devices[1]["iden"], 'Hello world', 'Test body')

#note_title = "Title"
#note_body = "Body"
#push = pb.push_note(note_title, note_body)
