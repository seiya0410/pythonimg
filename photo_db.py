import re, photo_file, photo_sqlite
from photo_sqlite import exec, select

#make a new album
def album_new(user_id, args):
    name = args.get('name', '')
    if name == '': return 0
    album_id = exec(
        'INSERT INTO albums (name, user_id) VALUES (?,?)',
        name, user_id)
    return album_id


#get the album of the specific user
def get_albums(user_id):
    return select(
        'SELECT * FROM albums where user_id=?',
        user_id
    )

# get the info of the specigid album
def get_album(album_id):
    a = select(
        'SELECT * FROM albums where album_id=?',  album_id)
    if len(a) == 0: return None
    return a[0]

#Get album name
def get_album_name(album_id):
    a = get_album(album_id)
    if a == None: return 'Not classified'
    return a['name']

#save the uploaded file
def save_file(user_id, upfile, album_id):
    #allow only jpeg
    if not re.search(r'\.(jpg|jpeg)$', upfile.filename):
        print('This is not JPEG:', upfile.filename)
        return 0
    #If an album is not specified, make a new one
    if album_id == 0:
        a = select('SELECT * FROM albums where user_id=? AND name=?', user_id, '未分類')
        print('sql:',a )
        if len(a) == 0:
            album_id = exec('INSERT INTO albums (user_id, name) VALUES (?,?)', user_id, '未分類')
        else:
            album_id = a[0]['album_id']

    #save a file info
    file_id = exec('''INSERT INTO files (user_id, filename, album_id) VALUES (?,?,?)''', user_id, upfile.filename, album_id)

    #save file
    upfile.save(photo_file.get_path(file_id))
    return file_id

#get the info of the file
def get_file(file_id, ptype):
    print('file_id', file_id)
    a = select(
        'SELECT * FROM files where file_id=?',  file_id)
    print('len', len(a))
    if len(a) == 0: return None
    p = a[0]
    p['path'] = photo_file.get_path(file_id)
    #thumb nail
    if ptype == 'thumb':
        p['path'] = photo_file.make_thumbnail(file_id, 300)
    return p

#get all file
def get_files():
    a = select('SELECT * FROM files ORDER BY file_id DESC LIMIT 50')
    print('aaa:',a)
    for i in a:
        print('album_id:', i['album_id'])
        i['name'] = get_album_name(i['album_id'])
    return a

#get all file names in an album
def get_album_files(album_id):
    return select('''SELECT * FROM files WHERE album_id=? ORDER BY file_id DESC''', album_id)

# get all user's file
def get_user_files(user_id):
    a = select('''SELECT * FROM files WHERE user_id=? ORDER BY file_id DESC LIMIT 50''', user_id)
    for i in a:
        i['name'] = get_album_name(i['album_id'])
    return a



