from config import get_db_connection

# Veritabanı bağlantısı
conn = get_db_connection()
cur = conn.cursor()

# Transaction başlat, tutarlılık için olası hata durumunda ihtiyaç.
try:
    #Cascade ile ilişki verilerin silinmesi. ilişki veri tabanında karmaşıklığı önler, bütünlüğü sağlar.
    # Tabloların silinmesi (Var olanları temizle)
    cur.execute('DROP TABLE IF EXISTS Photos CASCADE;')
    cur.execute('DROP TABLE IF EXISTS Comments CASCADE;')
    cur.execute('DROP TABLE IF EXISTS Posts CASCADE;')
    cur.execute('DROP TABLE IF EXISTS Albums CASCADE;')
    cur.execute('DROP TABLE IF EXISTS Todos CASCADE;')
    cur.execute('DROP TABLE IF EXISTS Users CASCADE;')

    # Users tablosu
    cur.execute('''
        CREATE TABLE Users (
            id serial PRIMARY KEY,
            name varchar(150) NOT NULL,
            username varchar(50) NOT NULL,
            email varchar(100) NOT NULL,
            address JSONB NOT NULL,
            geo JSONB NOT NULL,
            phone varchar(20),
            website varchar(100),
            company_name varchar(100),
            company_catchphrase varchar(255),
            company_bs varchar(255)
        );
    ''')

    # Posts tablosu
    cur.execute('''
        CREATE TABLE Posts (
            id serial PRIMARY KEY,
            user_id integer REFERENCES Users(id) ON DELETE CASCADE,
            title varchar(255),
            body text
        );
    ''')

    # Comments tablosu
    cur.execute('''
        CREATE TABLE Comments (
            id serial PRIMARY KEY,
            post_id integer REFERENCES Posts(id) ON DELETE CASCADE,
            name varchar(255),
            email varchar(100),
            body text
        );
    ''')

    # Albums tablosu
    cur.execute('''
        CREATE TABLE Albums (
            id serial PRIMARY KEY,
            user_id integer REFERENCES Users(id) ON DELETE CASCADE,
            title varchar(255)
        );
    ''')

    # Photos tablosu
    cur.execute('''
        CREATE TABLE Photos (
            id serial PRIMARY KEY,
            album_id integer REFERENCES Albums(id) ON DELETE CASCADE,
            title varchar(255),
            url varchar(255),
            thumbnail_url varchar(255)
        );
    ''')

    # Todos tablosu
    cur.execute('''
        CREATE TABLE Todos (
            id serial PRIMARY KEY,
            user_id integer REFERENCES Users(id) ON DELETE CASCADE,
            title varchar(255),
            completed boolean
        );
    ''')

    # Örnek kullanıcı ekleme
    cur.execute('''
        INSERT INTO Users (name, username, email, address, geo, phone, website, company_name, company_catchphrase, company_bs)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    ''', (
        'rumeysa', 'rbk', 'rbk@gmail.com',
        '{"street": "Hello", "suite": "guys 100", "city": "Ankara", "zipcode": "2344-32"}',  
        '{"lat": "-434.54", "lng": "43.54"}',  
        '5056788676', 'rumeysa.org', 'roma home', 'multi layered client server neural net', 'herness real-time e-markets'
    ))

    user_id = cur.fetchone()[0]

    # Örnek post ekleme
    cur.execute('''
        INSERT INTO Posts (user_id, title, body)
        VALUES (%s, %s, %s) RETURNING id;
    ''', (
        user_id, 'Post Title', 'This is the body of the post.'
    ))

    post_id = cur.fetchone()[0]

    # Örnek comment ekleme
    cur.execute('''
        INSERT INTO Comments (post_id, name, email, body)
        VALUES (%s, %s, %s, %s);
    ''', (
        post_id, 'Commenter Name', 'commenter@example.com', 'This is a comment on the post.'
    ))

    # Örnek album ekleme
    cur.execute('''
        INSERT INTO Albums (user_id, title)
        VALUES (%s, %s) RETURNING id;
    ''', (
        user_id, 'Album Title'
    ))

    album_id = cur.fetchone()[0]

    # Örnek photo ekleme
    cur.execute('''
        INSERT INTO Photos (album_id, title, url, thumbnail_url)
        VALUES (%s, %s, %s, %s);
    ''', (
        album_id, 'Photo Title', 'https://via.placeholder.com/435/34f34', 'https://via.placeholder.com/435/34f34'
    ))

    # Örnek todo ekleme
    cur.execute('''
        INSERT INTO Todos (user_id, title, completed)
        VALUES (%s, %s, %s);
    ''', (
        user_id, 'Task Title', False
    ))

    
    conn.commit()

except Exception as e:
    # Hata durumunda işlemi geri al, veri kaybı ya da yanlış veri girişi önler
    conn.rollback()
    print(f"Hata: {e}")

finally:
    # Cursor ve bağlantıyı kapat
    cur.close()
    conn.close()