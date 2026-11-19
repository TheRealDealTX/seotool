#!/usr/bin/env python3
"""Generate logo, favicons and per-post Open Graph images. Run from the site root:
   python3 scripts/make_images.py   (needs Pillow and PHP CLI)"""
import json, subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont

NAVY=(15,42,68); ACCENT=(217,72,43); CREAM=(247,244,238); WHITE=(255,255,255)
CAT={'buying':(47,111,208),'selling':(217,72,43),'investing':(19,128,111),'homeownership':(138,92,199),'insurance-claims':(199,115,29),'houston':(31,143,179)}
SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SANS='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
SANSR='/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'

def mark(size, bg=NAVY, fg=WHITE):
    im=Image.new('RGBA',(size,size),(0,0,0,0)); d=ImageDraw.Draw(im)
    r=int(size*.22); d.rounded_rectangle([0,0,size-1,size-1],r,fill=bg)
    d.rectangle([0,int(size*.86),size,size],fill=ACCENT)
    d.rounded_rectangle([0,0,size-1,size-1],r,outline=None)
    mask=Image.new('L',(size,size),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,size-1,size-1],r,fill=255)
    im.putalpha(mask)
    f=ImageFont.truetype(SANS,int(size*.40)); d=ImageDraw.Draw(im)
    d.text((size/2,size*.46),'540',font=f,fill=fg,anchor='mm')
    return im

mark(512).save('assets/img/logo-512.png')
mark(180).convert('RGB').save('apple-touch-icon.png') if False else None
apple=Image.new('RGB',(180,180),NAVY); apple.paste(mark(180),(0,0),mark(180)); apple.save('apple-touch-icon.png')
mark(64).save('favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
open('favicon.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><clipPath id="c"><rect width="64" height="64" rx="14"/></clipPath></defs><g clip-path="url(#c)"><rect width="64" height="64" fill="#0f2a44"/><rect y="55" width="64" height="9" fill="#d9482b"/></g><text x="32" y="38" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="25" fill="#fff" text-anchor="middle">540</text></svg>')

def og(title, label, color, path):
    W,H=1200,630; im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
    for i,(rr,w) in enumerate([(420,3),(300,3),(180,3)]):
        d.ellipse([W-260-rr,-120-rr+200,W-260+rr,-120+rr+200],outline=tuple(min(255,c+40) for c in NAVY),width=w)
    d.rectangle([0,0,18,H],fill=color)
    im.paste(mark(84),(70,64),mark(84))
    d.text((172,78),'Exit Real Estate 540',font=ImageFont.truetype(SERIF,34),fill=WHITE)
    d.text((172,122),'exitrealestate540.com',font=ImageFont.truetype(SANSR,24),fill=(185,199,214))
    lf=ImageFont.truetype(SANS,26); lw=d.textlength(label.upper(),font=lf)
    d.rounded_rectangle([70,210,70+lw+40,256],23,fill=color); d.text((90,233),label.upper(),font=lf,fill=WHITE,anchor='lm')
    size=62
    while True:
        f=ImageFont.truetype(SERIF,size); lines=textwrap.wrap(title,width=int(1900/size))
        if len(lines)<=4 and all(d.textlength(l,font=f)<=1050 for l in lines): break
        size-=4
    y=290
    for l in lines: d.text((70,y),l,font=f,fill=WHITE); y+=int(size*1.22)
    d.rectangle([0,H-14,W,H],fill=ACCENT)
    im.save(path,optimize=True)

og('Texas real estate guides & free calculators for buyers, sellers, investors and homeowners','Houston & Texas',ACCENT,'assets/img/og-default.png')
data=json.loads(subprocess.check_output(['php','-r',"define('ERE',1);define('ROOT',getcwd());require 'inc/functions.php';echo json_encode(array_map(fn($p)=>[$p['title'],$p['category']],all_posts()));"]))
cats=json.loads(subprocess.check_output(['php','-r',"define('ERE',1);define('ROOT',getcwd());require 'inc/functions.php';echo json_encode(array_map(fn($c)=>$c['name'],cfg('categories')));"]))
for slug,(title,cat) in data.items():
    og(title,cats[cat],CAT[cat],f'assets/img/og/{slug}.png')
print('images:',len(data)+1)
