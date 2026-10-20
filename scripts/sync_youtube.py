#!/usr/bin/env python3
"""Zavrseni javni nedeljni livestreamovi, bez automatskog mesanja konferencija."""
import json, os, re, sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen, Request

API='https://www.googleapis.com/youtube/v3/'
KEY=os.environ.get('YOUTUBE_API_KEY','')
HANDLE=os.environ.get('YOUTUBE_CHANNEL_HANDLE','@EvandjeoskaCrkvaJagodina')
OUT=Path(__file__).resolve().parent.parent/'content/youtube-services.json'

def request(endpoint,**params):
 params['key']=KEY
 url=API+endpoint+'?'+urlencode(params)
 with urlopen(Request(url,headers={'User-Agent':'ECJagodinaBot/1.0'}),timeout=25) as r:
  return json.load(r)

def batches(seq,size):
 for i in range(0,len(seq),size):yield seq[i:i+size]

def is_weekly(title):
 normalized=title.casefold()
 if any(x in normalized for x in ('konferenc','seminar','predavanj','omladinsk','dečij','decij','gornja soba')):return False
 return bool(re.search(r'nedelj|bogosluženj|bogosluzenj|sunday service',normalized))

def main():
 if not KEY: sys.exit('YOUTUBE_API_KEY nije postavljen.')
 channel=request('channels',part='contentDetails',forHandle=HANDLE)
 items=channel.get('items',[])
 if not items:sys.exit('YouTube kanal nije pronadjen; proverite HANDLE.')
 playlist=items[0]['contentDetails']['relatedPlaylists']['uploads']
 ids=[]; token=None
 # 500 najnovijih uploadova; stariji postojeći zapisi u arhivi ostaju sačuvani.
 for _ in range(10):
  params={'part':'contentDetails','playlistId':playlist,'maxResults':50}
  if token:params['pageToken']=token
  data=request('playlistItems',**params)
  ids += [x['contentDetails']['videoId'] for x in data.get('items',[])]
  token=data.get('nextPageToken')
  if not token:break
 old=json.loads(OUT.read_text(encoding='utf8')) if OUT.exists() else []
 archive={v['id']:v for v in old if isinstance(v,dict) and re.fullmatch(r'[A-Za-z0-9_-]{11}',v.get('id',''))}
 for group in batches(ids,50):
  result=request('videos',part='snippet,liveStreamingDetails,status',id=','.join(group),maxResults=50)
  for video in result.get('items',[]):
   detail=video.get('liveStreamingDetails',{})
   status=video.get('status',{})
   title=video['snippet']['title']
   if not detail.get('actualEndTime') or status.get('privacyStatus')!='public' or not is_weekly(title):continue
   date=(detail.get('actualStartTime') or video['snippet'].get('publishedAt',''))[:10]
   archive[video['id']]={'id':video['id'],'title':title,'date':date}
 videos=sorted(archive.values(),key=lambda v:(v['date'],v['id']),reverse=True)
 OUT.write_text(json.dumps(videos,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(f'Arhiva: {len(videos)} zavrsenih nedeljnih prenosa.')

if __name__=='__main__':main()
