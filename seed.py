'''Seed file to make sample data for blogly db.'''

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add Users
pam      = User( first_name='Phedias'    ,last_name='A.M.'      ,img_url='https://avatars.githubusercontent.com/u/123711623?v=4' )
whiskey  = User( first_name='Whiskey'    ,last_name='Tango'     ,img_url='https://images.unsplash.com/photo-1615887023544-3a566f29d822?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=987&q=80' )
bowser   = User( first_name='Bowser Jr.' ,last_name='Koopa'     ,img_url='https://images.unsplash.com/photo-1585696862208-ca12defa3a78?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=987&q=80' )
spike    = User( first_name='Spike'      ,last_name='Chain'     ,img_url='https://images.unsplash.com/photo-1523626797181-8c5ae80d40c2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1335&q=80' )
river    = User( first_name='River'      ,last_name='Nile'      ,img_url='https://images.unsplash.com/photo-1689799980599-60c7b1846ffa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3346&q=80')
summer   = User( first_name='Summer'     ,last_name='Winter'    ,img_url='https://images.unsplash.com/photo-1542481694-f6539f365918?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=987&q=80')
joaquin  = User( first_name='Joaquin'    ,last_name='Phoenix'   ,img_url='https://images.unsplash.com/photo-1622599511051-16f55a1234d0?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1336&q=80')
octavia  = User( first_name='Octavia'    ,last_name='Spencer'   ,img_url='https://plus.unsplash.com/premium_photo-1682893682272-46534e543c50?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80')
larry    = User( first_name='Larry'      ,last_name='David'     ,img_url='https://plus.unsplash.com/premium_photo-1664456329834-8b832667ffb9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2344&q=80')
kurt     = User( first_name='Kurt'       ,last_name='Cobain'    ,img_url="https://upload.wikimedia.org/wikipedia/commons/3/37/Nirvana_around_1992_%28cropped%29.jpg")
rain     = User( first_name='Rain'       ,last_name='Phoenix'   )

# Add new objects to session, so they'll persist
db.session.add_all([pam,whiskey,bowser,spike,river,summer,joaquin,octavia,larry,kurt,rain])

# Commit--otherwise, this never gets saved!
db.session.commit()

# Add Posts
post_0 = { "title": "Welcome To This App!","content": "Hi, I hope you enjoy this little app. if you find any bugs do let me know!"}
post_1 = { "title": "A Beautiful Day","content": "Today, the weather was perfect."}
post_2 = { "title": "Delicious Recipes", "content": "I tried a new recipe today."}
post_3 = { "title": "Exploring New Places", "content": "Visited an amazing new place today."}
post_4 = { "title": "Whispers of the River: A Fishing Haiku", "content":"Amidst calm waters, Angler casts a hopeful line, Nature\'s dance unfolds." }

# User object
author_user_0 = pam
author_user_1 = whiskey  
author_user_2 = bowser 
author_user_3 = spike
author_user_4 = larry

# Call the create_post function to add the posts to the database we dod this this way because i didnt want to manually put in a datetime yet.
# Been advised to have the sqlalchemy server have call its now() function.
post_0 = Post.create_post(author_user_0, post_0["title"], post_0["content"])
post_1 = Post.create_post(author_user_1, post_1["title"], post_1["content"])
post_2 = Post.create_post(author_user_2, post_2["title"], post_2["content"])
post_3 = Post.create_post(author_user_3, post_3["title"], post_3["content"])
post_4 = Post.create_post(author_user_4, post_4['title'], post_4["content"])

# Add new objects to session, so they'll persist
db.session.add_all([post_1,post_2,post_3, post_4])

# Commit--otherwise, this never gets saved!
db.session.commit()


## Add tags
hw    = Tag(name = "HELLO_WORLD" )
wel   = Tag(name = "Welcome")
app   = Tag(name = "AppIntroduction")
bug   = Tag(name = "BugReport")
wea   = Tag(name = "Weather")
bea   = Tag(name = "BeautifulDay")
sun   = Tag(name = "SunnyWeather")
rec   = Tag(name = "Recipes")
coo   = Tag(name = "Cooking")
YOLO  = Tag(name = "YOLO")
new   = Tag(name = "NewRecipe")
tra   = Tag(name = "Travel")
exp   = Tag(name = "Exploration")
new   = Tag(name = "NewPlaces")
poe   = Tag(name = "Poetry")
hai   = Tag(name = "Haiku")
fis   = Tag(name = "Fishing")
nat   = Tag(name = "Nature")
tec   = Tag(name = "TechTags")
cod   = Tag(name = "CodingLife")
sof   = Tag(name = "SoftwareDev")
pyt   = Tag(name = "Pythonic")
web   = Tag(name = "WebDev")
dat   = Tag(name = "DataScience")
ai    = Tag(name = "AIandML")
cod   = Tag(name = "CodeGeek")
devop = Tag(name = "DevOps")
tecom = Tag(name = "TechCommunity")

# Add new objects to session, so they'll persist
db.session.add_all([hw, wel, app, bug, wea, bea, sun, rec, 
                    coo, YOLO, new, tra, exp, new, poe, hai, fis, nat, 
                    tec, cod, sof, pyt, web, dat, ai, cod, devop, tecom])

# Commit--otherwise, this never gets saved!
db.session.commit()

# Match tags to corresponding posts
post_0.has_tags.append(wel)
post_0.has_tags.append(app)
post_0.has_tags.append(bug)

post_1.has_tags.append(wea)
post_1.has_tags.append(bea)
post_1.has_tags.append(sun)

post_2.has_tags.append(rec)
post_2.has_tags.append(coo)
post_2.has_tags.append(new)

post_3.has_tags.append(tra)
post_3.has_tags.append(exp)
post_3.has_tags.append(new)

post_4.has_tags.append(poe)
post_4.has_tags.append(hai)
post_4.has_tags.append(fis)
post_4.has_tags.append(nat)

# Add new objects to session, so they'll persist
db.session.add_all([post_1,post_2,post_3, post_4])

# Commit--otherwise, this never gets saved!
db.session.commit()