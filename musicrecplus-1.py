
def opendb():
  '''Opens the database file and returns a cursor object'''
  # reads file and creates dictionary db of format:
  #  db[UserName] = [Artist1, Artist2, Artist3, ...]
  global db
  global db_with_priv
  try:
    content = read_file("musicrecplus.txt")
    db = {}
    db_with_priv = {}
  except:
    content = ""
    db = {}
    db_with_priv = {}
  if content == "":
    return ({}, {})
  lines = content.split("\n")
  for l in lines:
    split = l.split(":")
    if split != ['']:
      username = split[0]
      artistlist = split[1].split(",")
    if username[-1] != "$":
      db[username] = artistlist
    db_with_priv[username] = artistlist
  return (db, db_with_priv)


def read_file(filename):
  '''Reads a file and returns its contents as a string.'''
  myfile = open(filename, "r")
  contents = myfile.read()
  myfile.close()
  return contents


def NameAndArtist(dbALL, db):
  '''Prompts the user for a username and an artist name.'''
  global name
  name = input("Enter your name (put a $ symbol after your name if you wish your preferences to remain private):\n")
  if name not in dbALL.keys():
    dbALL[name] = []
    if name[-1] != "$":
      db[name] = []
    enterPreferences(name, db, dbALL)
  return name


def enterPreferences(name, db, dbALL):
  '''Prompts the user for preferences and adds them to the database.''' ''
  artists = []  
  while True:
    nextArtist = input("Enter an artist that you like (Enter to finish):\n")
    nextArtist.title()
    if nextArtist != '':
      artists.append(nextArtist)
    else:
      break
    if name[-1] != "$":
        db[name] = artists
        db[name] = sorted(db[name])
    dbALL[name] = artists
    dbALL[name] = sorted(dbALL[name])
  return artists

def compareUsers(user, user2):
    # returns an int of how many artists are shared between two users
    # helper function for getRecommendations
    count = 0
    for i in user[1]:
        for j in user2[1]:  
            if i == j:
                count += 1
    return count
def deepcopy(list):
    #deep copies an array
    # helper function for getRecommendations
    new = []
    for i in list:
        new.append(i)
    return new
def deleteRepeats(list1, list):
    # deletes repeated elements in list, returns new array
    # helper function for getRecommendations
    rec = []
    for n in list:
        if n not in list1:
            rec.append(n)
    return rec

def getRecommendations(name, db):
    '''returns array of recommended artists based on other users'''
    user = (name, db[name])
    highest = [[],0]
    for i in db.keys():
        if i != user[0]:
            user2 = (i, db[i])
            a = compareUsers(user, user2)
            if a >= highest[1] and deleteRepeats(user[1], user2[1]) != []:
                if a == highest[1] and len(highest[0]) > len(user2[1]):
                    highest = [highest[0], a]
                else:
                    highest = [user2[1], a]
                    #print(highest)
    sort = deleteRepeats(user[1], highest[0])
    return sorted(sort)

def showMostPopularArtists(db):
  '''Shows the most popular artists.''' 
  artistPopularity = {}
  max = []
  str = ""
  for artistlist in db.values():
    for artist in artistlist:
      if artist in artistPopularity:
        artistPopularity[artist] += 1
      else:
        artistPopularity[artist] = 1
  for i in range(3):
    m = ""
    for n in artistPopularity.keys():
      if m == "":
        m = n
      elif artistPopularity[n] > artistPopularity[m]:
        m = n
    if m != "" and m in artistPopularity.keys():
      max.append(m)
      del artistPopularity[max[i]]
  if len(max) > 0:
    for artist in max:
      str += artist +"\n"
  elif max.len == 0:
    str = "Sorry, no artists found."
  return (str[:-1], artistPopularity)
  
def mostPopularLikes(db):
  '''Calculates the number of likes the most popular artist received'''
  artistPopularity = {}
  max = []
  str = ""
  for artistlist in db.values():
    for artist in artistlist:
      if artist in artistPopularity:
        artistPopularity[artist] += 1
      else:
        artistPopularity[artist] = 1
        
  if artistPopularity == {}:
    return 0
  else:
    max = 0
    for artist, likes in artistPopularity.items():
      if likes > max:
        max = likes
    return max
    
def mostLikedUsers(db):
  '''Returns a list of users who like the most artists.'''
  userLikes = {}

  for username, artistlist in db.items():
      if username[-1] != "$":  # Exclude users in private mode
          userLikes[username] = len(artistlist)

  max_likes = max(userLikes.values(), default=0)

  if max_likes == 0:
      print("Sorry, no user found.")
      return []

  most_liked_users = [username for username, likes in userLikes.items() if likes == max_likes]

  return sorted(most_liked_users)

def save(dbALL):
  '''Saves the database to a file.''' ''
  string = ""
  for username, artistlist in dbALL.items():
    if artistlist != []:
      string += username + ":"
      for artist in artistlist[:-1]:
        string += artist + ","
      string += artistlist[-1]
      string += "\n"
  myfile = open("musicrecplus.txt", "w")
  myfile.write(string)
  myfile.close()

def start():
  db = opendb()[0]
  dbALL = opendb()[1]  # including private users
  name = NameAndArtist(dbALL, db)

  menu = '''Enter a letter to choose an option:
  e - Enter preferences
  r - Get recommendations
  p - Show most popular artists
  h - How popular is the most popular
  m - Which user has the most likes
  q - Save and quit'''

  while True:
    print(menu)
    userChoice = input()

    if userChoice == 'e':
      enterPreferences(name, db, dbALL)

    elif userChoice == 'r':
      a = getRecommendations(name, db)
      try:
        if a == []:
            print("No recommendations available at this time.")
        else:
            for i in a:   
                print(i)
      except:
        print("No recommendations available at this time.")
    elif userChoice == 'p':
      #users = []
      print(showMostPopularArtists(db)[0])

    elif userChoice == 'h':
      likes = mostPopularLikes(db)
      if likes != 0:
        print(likes)
      elif likes == 0:
        print("Sorry, no artists found")

    elif userChoice == 'm':
      for i in mostLikedUsers(db):
        print(i)

    elif userChoice == 'q':
      save(dbALL)
      break

    else:
      print("Invalid choice. Please enter a valid option.")

#end of start function

start()