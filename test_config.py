#!/usr/bin/env python3
"""Configuration test script"""

import os
from video_config import VIDEO_CONFIG, DAILY_SCHEDULE, UPLOAD_TIMES, PLATFORMS
from datetime import datetime

print('='*70)
print('CONFIGURATION TEST')
print('='*70)

# Test 1: Video files exist
print('\n1. VIDEO FILES CHECK:')
videos_folder = 'videos'
missing = []
for video_name in VIDEO_CONFIG.keys():
    path = os.path.join(videos_folder, video_name)
    exists = os.path.exists(path)
    status = '✓' if exists else '✗'
    print(f'  {status} {video_name}')
    if not exists:
        missing.append(video_name)

if missing:
    print(f'\n  WARNING: {len(missing)} videos not found!')
else:
    print(f'\n  ✓ All {len(VIDEO_CONFIG)} videos found!')

# Test 2: Captions configured
print('\n2. CAPTIONS CHECK:')
total_captions = 0
for video_name, config in VIDEO_CONFIG.items():
    num_captions = len(config['captions'])
    total_captions += num_captions
    print(f'  {video_name}: {num_captions} captions')
print(f'\n  ✓ Total captions configured: {total_captions}')

# Test 3: Schedule
print('\n3. SCHEDULE CHECK:')
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
for day_num in range(7):
    videos = DAILY_SCHEDULE[day_num]
    print(f'  {days[day_num]}: {len(videos)} videos')
print(f'\n  ✓ {len(DAILY_SCHEDULE)} days scheduled')

# Test 4: Upload times
print('\n4. UPLOAD TIMES:')
for time in UPLOAD_TIMES:
    print(f'  • {time}')
print(f'\n  ✓ {len(UPLOAD_TIMES)} uploads per day')

# Test 5: Platforms
print('\n5. PLATFORMS:')
for platform in PLATFORMS:
    print(f'  • {platform}')
print(f'\n  ✓ {len(PLATFORMS)} platforms configured')

# Test 6: Total uploads calculation
print('\n6. DAILY UPLOAD CALCULATION:')
uploads_per_day = len(UPLOAD_TIMES) * len(PLATFORMS)
print(f'  {len(UPLOAD_TIMES)} videos × {len(PLATFORMS)} platforms = {uploads_per_day} uploads/day')
uploads_per_week = uploads_per_day * 7
print(f'  Weekly: {uploads_per_week} total uploads')

# Test 7: Organ 1.mov check
print('\n7. ORGAN 1.MOV VERIFICATION:')
organ_count = 0
for day_num in range(7):
    if 'Organ 1.mov' in DAILY_SCHEDULE[day_num]:
        organ_count += 1
print(f'  Appears on {organ_count}/7 days')
if organ_count == 7:
    print('  ✓ Organ 1.mov scheduled every day!')
else:
    print(f'  ✗ WARNING: Organ 1.mov missing on {7-organ_count} days')

# Test 8: Today schedule
print(f'\n8. TODAY SCHEDULE ({days[datetime.now().weekday()]}):')
today_videos = DAILY_SCHEDULE[datetime.now().weekday()]
for i, video in enumerate(today_videos):
    print(f'  {UPLOAD_TIMES[i]} - {video}')
    for platform in PLATFORMS:
        print(f'    → {platform}')

print('\n' + '='*70)
print('✓ CONFIGURATION TEST COMPLETE')
print('='*70)
