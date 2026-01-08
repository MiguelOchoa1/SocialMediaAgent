# Hard-coded Video Configuration
# Each video has multiple captions that will rotate daily

VIDEO_CONFIG = {
    "Addio.MOV": {
        "captions": [
            "Bro is not in carnegie hall 🥀\n\n\n\n\n#addio #organ #piano #classical",
            "Just vibing with Einaudi 🎹\n\n\n\n\n#ludovicoeinaudi #addio #piano #organmusic",
            "When the organ hits different 😮‍💨\n\n\n\n\n#addio #classical #pianist #organ"
        ]
    },
    
    "Charlie Brown.mov": {
        "captions": [
            "Childhood hits different on keys 🎹\n\n\n\n\n#charliebrown #peanuts #piano #nostalgia",
            "Peanuts theme never gets old 🥜\n\n\n\n\n#vinceguaraldi #charliebrown #jazzpiano #classic",
            "This song = instant serotonin 💛\n\n\n\n\n#charliebrown #piano #cover #feelgood"
        ]
    },
    
    "Chihiro.mov": {
        "captions": [
            "Spirited Away on the keys 🎵\n\n\n\n\n#chihiro #studioghibli #joehisaishi #piano",
            "Pure ghibli magic right here ✨\n\n\n\n\n#spiritedaway #chihiro #piano #anime",
            "This song lives rent free in my head 🏠\n\n\n\n\n#ghibli #chihiro #pianover #nostalgia"
        ]
    },
    
    "Clair De Lune.MP4": {
        "captions": [
            "Debussy after dark 🌙\n\n\n\n\n#clairdelune #debussy #piano #classical",
            "The most peaceful 5 minutes of your day 🤍\n\n\n\n\n#clairdelune #piano #relaxing #classicalmusic",
            "POV: it's 2am and you can't sleep 🌃\n\n\n\n\n#clairdelune #debussy #latenight #piano"
        ]
    },
    
    "Fantasy.MP4": {
        "captions": [
            "Lost in the fantasy \n\n\n\n\n#fantasy #piano #improv #original",
            "When the improv hits just right \n\n\n\n\n#pianopractice #fantasy #musician #improv",
            "Making up songs at 3am 🌙\n\n\n\n\n#fantasy #piano #original #latenight"
        ]
    },
    
    "Howls Moving Castle.MP4": {
        "captions": [
            "Howl's theme making me emotional again 😭\n\n\n\n\n#howlsmovingcastle #ghibli #joehisaishi #piano",
            "Studio Ghibli supremacy 👑\n\n\n\n\n#howl #ghibli #piano #anime",
            "This is my comfort song fr 🤍\n\n\n\n\n#howlsmovingcastle #piano #ghibli #peaceful"
        ]
    },
    
    "Organ 1.mov": {
        "captions": [
            "Church organ vibes 🎹\n\n\n\n\n#organ #organmusic #church #classical",
            "The organ hits different I promise 😤\n\n\n\n\n#organist #organ #musician #practice",
            "POV: You're in a gothic cathedral 🏰\n\n\n\n\n#organ #classical #church #aesthetic"
        ]
    },
    
    "Pixies.MOV": {
        "captions": [
            "Where is my mind? 🎸\n\n\n\n\n#pixies #whereismymind #piano #cover",
            "Piano version hits different ngl 💭\n\n\n\n\n#pixies #piano #alternative #90s",
            "This song never gets old 🖤\n\n\n\n\n#whereismymind #pixies #pianocover #indie"
        ]
    },
    
    "Succession.mov": {
        "captions": [
            "Succession theme on the keys 👔\n\n\n\n\n#succession #hbo #piano #theme",
            "When the intro is better than the show 💼\n\n\n\n\n#succession #piano #tv #cover",
            "That HBO prestige sound 🎹\n\n\n\n\n#succession #hbo #pianotheme #drama"
        ]
    }
}


# Daily upload schedule - which video to upload on which day
# Format: Day of week (0=Monday, 6=Sunday) -> video filename
DAILY_SCHEDULE = {
    0: "Addio.MOV",                    # Monday
    1: "Charlie Brown.mov",            # Tuesday
    2: "Chihiro.mov",                  # Wednesday
    3: "Clair De Lune.MP4",           # Thursday
    4: "Fantasy.MP4",                  # Friday
    5: "Howls Moving Castle.MP4",     # Saturday
    6: "Organ 1.mov",                  # Sunday
}

# Upload time (24-hour format)
UPLOAD_TIME = "18:00"  # 6:00 PM

# Platform settings
PLATFORM = "instagram"  # instagram, tiktok, youtube
