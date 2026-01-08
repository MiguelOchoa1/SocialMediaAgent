# Hard-coded Video Configuration
# Each video has multiple captions that will rotate daily

VIDEO_CONFIG = {
    "Addio.MOV": {
        "captions": [
            "Who broke this guy's heart bruh🥀\n\n\n\n\n#sad #breakup #piano #classical #original",
            "After the video I caught this fool crying \n\n\n\n\n#piano #breakup #piano #orginal",
            "This is an original I wrote when I went through a break up\n\n\n\n\n#breakup #classical #pianist #sad"
        ]
    },
    
    "Charlie Brown.mov": {
        "captions": [
            "Good old Charlie Brown never gets old\n\n\n\n\n#charliebrown #themesong #pianocover #vinceguaraldi #linusandlucy",
            "Peanuts theme never gets old \n\n\n\n\n#charliebrown #themesong #pianocover #vinceguaraldi #linusandlucy",
            "Bro is dancing like he's a turkey\n\n\n\n\n#charliebrown #themesong #pianocover #vinceguaraldi #linusandlucy"
        ]
    },
    
    "Chihiro.mov": {
        "captions": [
            "Bro is being way to dramatic I feel like \n\n\n\n\n#chihiro #billieeilish #fiu #pianocover",
            "Why is he playing at an empty auditorium tho?? \n\n\n\n\n#chihiro #billieeilish #fiu #pianocover",
            "Should I report this guy?\n\n\n\n\n#chihiro #billieeilish #fiu #pianocover"
        ]
    },
    
    "Clair De Lune.MP4": {
        "captions": [
            "Debussy after dark \n\n\n\n\n#clairdelune #debussy #pianocover #classical",
            "Bruh who was that guy laying on the floor\n\n\n\n\n#clairdelune #debussy #pianocover #classical",
            "POV: it's 2am and you can't sleep \n\n\n\n\n#clairdelune #debussy #pianocover #classical"
        ]
    },
    
    "Fantasy.MP4": {
        "captions": [
            "Why is bro blinded folded\n\n\n\n\n#fantaisieimpromptu #pianocover #chopin #fiu #blindfolded",
            "This guy seems possesed bruh  \n\n\n\n\n#fantaisieimpromptu #pianocover #chopin #fiu #blindfolded",
            "Why is he here at this time \n\n\n\n\n#fantaisieimpromptu #pianocover #chopin #fiu #blindfolded"
        ]
    },
    
    "Howls Moving Castle.MP4": {
        "captions": [
            "I was asleep and this guy wakes me up\n\n\n\n\n#howlsmovingcastle #anime #fiu #themesong #pianocover",
            "Whos mans this ???\n\n\n\n\n#howlsmovingcastle #anime #fiu #themesong #pianocover",
            "Why is this guy everywhere I go\n\n\n\n\n#howlsmovingcastle #anime #fiu #themesong #pianocover"
        ]
    },
    
    "Organ 1.mov": {
        "captions": [
            "I was doing my nighly checks and this guy is here\n\n\n\n\n#organ #everythinginitsrightplace #radiohead #wokeupsuckingalemon #fiu",
            "This guy scared the s- out of me \n\n\n\n\n#organist #organ #everythinginitsrightplace #radiohead #wokeupsuckingalemon #fiu",
            "how did he get in here?? this is closed \n\n\n\n\n#organ #everythinginitsrightplace #radiohead #wokeupsuckingalemon #fiu"
        ]
    },
    
    "Pixies.MOV": {
        "captions": [
            "Where is my mind? \n\n\n\n\n#pixies #whereismymind #piano #cover #fiu",
            "Bruh who was that guy standing on the chair\n\n\n\n\n#pixies #piano #alternative #cover #fiu",
            "got kicked out once and now he's playing again\n\n\n\n\n#whereismymind #pixies #pianocover #fiu"
        ]
    },
    
    "Succession.mov": {
        "captions": [
            "caught bro playing succession\n\n\n\n\n#succession #painocover #fiu #themesong",
            "I just saw this place was empty and now he's back\n\n\n\n\n#succession #pianocover #themesong #fiu",
            "Who's mans is this and why is he playing here\n\n\n\n\n#succession #themesong #pianocover #fiu"
        ]
    }
}


# Daily upload schedule - 4 uploads per day
# Organ 1.mov is uploaded every day at one of the time slots
# Format: {day_of_week: [list of 4 videos for 9am, 12pm, 6pm, 11pm]}
DAILY_SCHEDULE = {
    0: ["Organ 1.mov", "Addio.MOV", "Charlie Brown.mov", "Chihiro.mov"],            # Monday
    1: ["Organ 1.mov", "Clair De Lune.MP4", "Fantasy.MP4", "Howls Moving Castle.MP4"],  # Tuesday
    2: ["Organ 1.mov", "Pixies.MOV", "Succession.mov", "Addio.MOV"],               # Wednesday
    3: ["Organ 1.mov", "Charlie Brown.mov", "Chihiro.mov", "Clair De Lune.MP4"],  # Thursday
    4: ["Organ 1.mov", "Fantasy.MP4", "Howls Moving Castle.MP4", "Pixies.MOV"],   # Friday
    5: ["Organ 1.mov", "Succession.mov", "Addio.MOV", "Charlie Brown.mov"],       # Saturday
    6: ["Organ 1.mov", "Chihiro.mov", "Clair De Lune.MP4", "Fantasy.MP4"],       # Sunday
}

# Upload times (24-hour format) - 4 times per day
UPLOAD_TIMES = ["09:00", "12:00", "18:00", "23:00"]  # 9am, 12pm, 6pm, 11pm

# Platform settings - upload to multiple platforms
PLATFORMS = ["instagram"]  # Instagram only for now (YouTube coming soon)
