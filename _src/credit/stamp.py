"""Stamp a footer credit pill (name + site) on blog figure images. Usage: stamp.py list.json"""
import sys,json,os,shutil,asyncio,base64
def U(n): return 'data:font/woff2;base64,'+base64.b64encode(open('_src/stability_images/fonts/'+n,'rb').read()).decode()
from PIL import Image
from playwright.async_api import async_playwright
F='_src/stability_images/fonts/'
CSS=f"""@font-face{{font-family:S;src:url('{U('sora-latin-700-normal.woff2')}')}}
@font-face{{font-family:NSB;src:url('{U('noto-serif-bengali-bengali-700-normal.woff2')}')}}
body{{margin:0;background:transparent}}
#p{{display:inline-flex;align-items:center;gap:12px;padding:9px 20px;border-radius:999px;background:rgba(14,28,30,.82);color:#fff;font:700 22px S;white-space:nowrap}}
#p i{{width:8px;height:8px;border-radius:50%;background:#E98250}}
#p .b{{font-family:NSB,S}}#p .u{{color:#9fe0d6}}"""
HT={'en':'<span>Sayedul Abrar</span><i></i><span class=u>sayedulabrar.site</span>',
    'bn':'<span class=b>সাইয়্যেদুল আবরার</span><i></i><span class=u>sayedulabrar.site</span>'}
async def pills():
    out={}
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(device_scale_factor=2)
        for k,h in HT.items():
            await pg.set_content(f'<meta charset=utf-8><style>{CSS}</style><div id=p>{h}</div>')
            await pg.evaluate('document.fonts.ready');await pg.wait_for_timeout(600)
            await pg.locator('#p').screenshot(path=f'/tmp/pill_{k}.png',omit_background=True)
        await b.close()
asyncio.run(pills())
lst=[x if isinstance(x,list) else [x,'br'] for x in json.load(open(sys.argv[1]))];os.makedirs('/tmp/orig',exist_ok=True)
for i,pos in lst:
    path='.'+i;bk='/tmp/orig/'+i.replace('/','_')
    if not os.path.exists(bk): shutil.copy(path,bk)
    im=Image.open(bk).convert('RGBA');W,H=im.size
    pl=Image.open('/tmp/pill_%s.png'%('bn' if 'bn' in os.path.basename(i).lower().replace('benefit','') and i.endswith('-bn.webp') else 'en')).convert('RGBA')
    s=W/1600*0.5;pl=pl.resize((int(pl.width*s),int(pl.height*s)),Image.LANCZOS)
    m=int(W*0.016);x=W-pl.width-m-(int(W*0.17) if pos=='brl' else 0);y=m if pos=='tr' else H-pl.height-m
    im.alpha_composite(pl,(x,y))
    im.convert('RGB').save(path,'WEBP',quality=88,method=6)
print('stamped',len(lst))
