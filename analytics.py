"""Daily normalized post snapshots and honest weekly reporting; no scraped X sessions."""
import json
import os
import statistics
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import automation as a

DATA=a.ROOT/'analytics'

def load(name,default):return a.read_json(DATA/name,default)
def write(name,value):
    DATA.mkdir(exist_ok=True)
    (DATA/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def commit():
    if os.getenv('GITHUB_ACTIONS')!='true':return
    subprocess.run(['git','add','analytics'],cwd=a.ROOT,check=True)
    if subprocess.run(['git','diff','--cached','--quiet'],cwd=a.ROOT).returncode:
        subprocess.run(['git','commit','-m','Update performance snapshots and editorial review'],cwd=a.ROOT,check=True)
        subprocess.run(['git','push','origin','HEAD:main'],cwd=a.ROOT,check=True)

def collect():
    token=os.getenv('BUFFER_INSIGHTS_KEY')
    if not token:raise RuntimeError('BUFFER_INSIGHTS_KEY not configured; analytics collection is not enabled')
    os.environ['BUFFER_API_KEY']=token
    org=a.organization()
    snapshots=load('snapshots.json',[])
    now=datetime.now(a.TZ)
    cursor=None
    for _ in range(20):
        q='{posts(first:100,after:'+a.literal(cursor)+',input:{organizationId:'+a.literal(org)+',filter:{status:[sent],channelIds:['+a.literal(a.CHANNEL)+']}}){pageInfo{endCursor hasNextPage}edges{node{id dueAt text metrics{type name value unit}metricsUpdatedAt metadata{... on TwitterPostMetadata{threadCount}}}}}}'
        result=a.buffer(q)['posts']
        for edge in result['edges']:
            post=edge['node']
            if not post.get('dueAt'):continue
            due=datetime.fromisoformat(post['dueAt'].replace('Z','+00:00'))
            age=(now-due).total_seconds()/3600
            if not 0<=age<=35*24:continue
            metrics={m['type']:m['value'] for m in (post.get('metrics') or [])}
            # Missing metrics stay null, including views. Never turn absent access into zero.
            row={'observed_at':now.isoformat(),'date':now.date().isoformat(),'post_id':post['id'],'due':post['dueAt'],'age_hours':round(age,1),'metrics_updated_at':post.get('metricsUpdatedAt'),'impressions':metrics.get('impressions'),'likes':metrics.get('reactions'),'reposts':metrics.get('reposts'),'replies':metrics.get('comments'),'thread_count':(post.get('metadata') or {}).get('threadCount',1)}
            snapshots=[r for r in snapshots if not(r['post_id']==row['post_id'] and r['date']==row['date'])]
            snapshots.append(row)
        if not result['pageInfo']['hasNextPage']:break
        cursor=result['pageInfo']['endCursor']
    else:raise RuntimeError('Incomplete analytics pagination')
    write('snapshots.json',snapshots)
    print('Post metric snapshots stored:',len(snapshots))
    # Public Buffer API has no follower-count field. UI observations are separately attributed.
    print('Follower count collection: unavailable through the documented public API; not inferred from post metrics.')
    commit()

def recommendation(rows,records):
    groups={}
    for row in rows:
        if row.get('impressions') is None or row['impressions']<=0:continue
        record=records.get(row['post_id'],{})
        angle=record.get('editorial_angle')
        if not angle:continue
        groups.setdefault(angle,[]).append(row)
    scored=[]
    for angle,group in groups.items():
        complete=[r for r in group if all(r.get(k) is not None for k in ('likes','reposts','replies'))]
        if len(complete)<5:continue
        rate=statistics.median((r['likes']+r['reposts']+r['replies'])/r['impressions'] for r in complete)
        reach=statistics.median(r['impressions'] for r in complete)
        scored.append((angle,rate,reach,len(complete)))
    if len(scored)<2:return {'preferred_angle':None,'reason':'En az iki anlatım biçiminde beşer olgun ve eksiksiz ölçüm yok; planı gürültüye göre değiştirmiyoruz.'}
    scored.sort(key=lambda r:(r[1],r[2]),reverse=True)
    best,second=scored[:2]
    if best[1]<max(0.005,second[1]*1.2):return {'preferred_angle':None,'reason':'Karar eşiğini aşan bir fark yok; çeşitlilik korunuyor.'}
    return {'preferred_angle':best[0],'reason':'En az beşer ölçümde medyan görünür etkileşim oranı en az %20 daha yüksek. Bu nedensel kanıt değildir; gelecek hafta günde en fazla bir zincirde denenecek.','sample_size':best[3],'median_rate':best[1]}

def report():
    now=datetime.now(a.TZ)
    snapshots=load('snapshots.json',[])
    # Freeze the first available 24–48h snapshot for age-comparable editorial tests.
    mature={}
    for row in sorted(snapshots,key=lambda r:r['observed_at']):
        due=datetime.fromisoformat(row['due'].replace('Z','+00:00'))
        if now-timedelta(days=8)<=due<now-timedelta(days=1) and 24<=row['age_hours']<=48:
            mature.setdefault(row['post_id'],row)
    rows=list(mature.values())
    records={r.get('post_id'):r for r in a.read_json(a.STATE,{'records':[]})['records'] if r.get('post_id')}
    decision=recommendation(rows,records)
    decision['reviewed_at']=now.isoformat()
    decision['expires_at']=(now+timedelta(days=8)).isoformat()
    write('editorial.json',decision)
    observations=load('follower-observations.json',[{'date':'2026-10-26','followers':683,'source':'Buffer Insights ekranı — elle doğrulanmış başlangıç gözlemi'}])
    write('follower-observations.json',observations)
    observations.sort(key=lambda r:r['date'])
    latest=observations[-1] if observations else None
    lines=['# Haftalık X raporu — '+now.date().isoformat(),'','Hedef: 25 Ekim başlangıcı 683 + 2.000 net takipçi = 24 Kasım sonunda 2.683 toplam takipçi. Hedef garanti değildir.','']
    if latest:
        lines+=['Son doğrulanmış takipçi gözlemi: **'+str(latest['followers'])+'**, tarih '+latest['date']+', kaynak '+latest['source']+'.','Takipçi sayısı otomatik güncellenmiyor; güncel gözlem olmadan net artış veya hedefe varış tahmini hesaplanmaz.','']
    lines+=['24–48 saatlik karşılaştırılabilir ölçümü bulunan gönderi/zincir kökü: '+str(len(rows))+'.','Zincirlerin yalnız kök gönderi metrikleri dönüyorsa bunlar tüm zincirin toplamı diye sunulmaz. Görüntülenme tekil kişi değildir.','', '| Ölçüm | Toplam | Veri bulunan gönderi |','|---|---:|---:|']
    for key,name in [('impressions','Görüntülenme'),('likes','Beğeni'),('reposts','Repost'),('replies','Yanıt')]:
        available=[r[key] for r in rows if r.get(key) is not None]
        lines.append('| '+name+' | '+(str(round(sum(available),2)) if available else 'Erişilemiyor')+' | '+str(len(available))+'/'+str(len(rows))+' |')
    lines+=['','## İçerik kararı',decision['reason'],'Yeni içerikler üç bağlantılı gönderi: araştırmanın sorusu, kanıt ve sayı, sınırı belirtilmiş kişisel editoryal yorum. Kanıt kalitesi büyüme hedefine feda edilmez.','', '## Veri sınırı','Buffer X metrik erişimi hesap/izin/plan koşullarına bağlıdır. API metriği boşsa bunu sıfır saymıyoruz. Follower sayısı için belgelenmiş herkese açık Buffer API alanı bulunmuyor; rapor bunu ayrıca belirtir. Son 24 saatte yayımlanan içerikler olgun karşılaştırmaya alınmaz.']
    content='\n'.join(lines)+'\n'
    DATA.mkdir(exist_ok=True)
    (DATA/('weekly-'+now.date().isoformat()+'.md')).write_text(content)
    (DATA/'latest-weekly.md').write_text(content)
    if os.getenv('GITHUB_STEP_SUMMARY'):Path(os.environ['GITHUB_STEP_SUMMARY']).write_text(content)
    commit()
    print(content)

def run(mode):
    if mode=='analytics':collect()
    else:report()
