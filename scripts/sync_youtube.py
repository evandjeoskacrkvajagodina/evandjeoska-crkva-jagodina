#!/usr/bin/env python3
"""Arhiva svih javnih zavrsenih YouTube prenosa sa kanala.

Obicni unapred snimljeni videi ne ulaze u arhivu.
"""
import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = 'https://www.googleapis.com/youtube/v3/'
KEY = os.environ.get('YOUTUBE_API_KEY', '')
HANDLE = os.environ.get('YOUTUBE_CHANNEL_HANDLE', '@EvandjeoskaCrkvaJagodina')
OUT = Path(__file__).resolve().parent.parent / 'content/youtube-services.json'


def request(endpoint, **params):
    params['key'] = KEY
    url = API + endpoint + '?' + urlencode(params)
    try:
        with urlopen(Request(url, headers={'User-Agent': 'ECJagodinaBot/1.0'}), timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'YouTube API greska ({exc.code}): {detail[:500]}') from exc


def batches(items, size):
    for start in range(0, len(items), size):
        yield items[start:start + size]


def main():
    if not KEY:
        sys.exit('YOUTUBE_API_KEY nije postavljen.')

    channel = request('channels', part='contentDetails', forHandle=HANDLE)
    items = channel.get('items', [])
    if not items:
        sys.exit('YouTube kanal nije pronadjen; proverite YOUTUBE_CHANNEL_HANDLE.')
    playlist_id = items[0]['contentDetails']['relatedPlaylists']['uploads']

    # Proveri SVE stranice YouTube liste, ukljucujuci najstarije prenose.
    ids = []
    next_token = None
    while True:
        params = {'part': 'contentDetails', 'playlistId': playlist_id, 'maxResults': 50}
        if next_token:
            params['pageToken'] = next_token
        page = request('playlistItems', **params)
        ids.extend(item['contentDetails']['videoId'] for item in page.get('items', [])
                   if item.get('contentDetails', {}).get('videoId'))
        next_token = page.get('nextPageToken')
        if not next_token:
            break

    archive = {}
    # Stare zapise ostavljamo (npr. u slucaju privremeno nedostupnog videa).
    if OUT.exists():
        previous = json.loads(OUT.read_text(encoding='utf-8'))
        if isinstance(previous, list):
            archive = {item['id']: item for item in previous
                       if isinstance(item, dict)
                       and re.fullmatch(r'[A-Za-z0-9_-]{11}', str(item.get('id', '')))}

    found = 0
    for group in batches(list(dict.fromkeys(ids)), 50):
        result = request('videos', part='snippet,liveStreamingDetails,status', id=','.join(group))
        for video in result.get('items', []):
            details = video.get('liveStreamingDetails') or {}
            status = video.get('status') or {}
            # actualEndTime postoji samo za zavrsene prenose (ne obicne video-snimke).
            if not details.get('actualEndTime') or status.get('privacyStatus') != 'public':
                continue
            snippet = video.get('snippet') or {}
            start = details.get('actualStartTime') or snippet.get('publishedAt', '')
            archive[video['id']] = {
                'id': video['id'],
                'title': snippet.get('title', 'Prenos uzivo'),
                'date': start[:10],
            }
            found += 1

    videos = sorted(archive.values(), key=lambda item: (item['date'], item['id']), reverse=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(videos, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Provereno YouTube snimaka: {len(ids)}.')
    print(f'Pronadjeno javnih zavrsenih prenosa: {found}.')
    print(f'Ukupno u arhivi: {len(videos)}.')


if __name__ == '__main__':
    main()
