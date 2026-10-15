# Builds the Yayāti map as a standalone SVG. Family-tree layout: marriage is a
# short horizontal tie, descent drops from it; roles sit inside each box so no
# label ever lies on a line. Purāṇa doors are colour-coded badges on the boxes.
from xml.sax.saxutils import escape as x
W,H = 1400, 1110
NW, NH = 150, 62
P = {}   # id -> (cx, cy, name, deva, [role lines], kind, [badges])
WIDE = {'yay':196,'vai':184,'kas':168,'par':160}
def node(i,cx,cy,name,deva,roles,kind='',badges=()): P[i]=(cx,cy,name,deva,roles,kind,list(badges))
# badges: (door, text) door in {'bh','gp','q'}
node('brh',110,100,'Bṛhaspati','बृहस्पतिः',['guru of the devas'],badges=[('bh','Bh 12.6: stops the sacrifice')])
node('shu',420,100,'Śukra','शुक्रः',['guru of the asuras','curses Yayāti: old age'])
node('nah',640,100,'Nahuṣa','नहुषः',['Yayāti\'s father'])
node('vrs',860,100,'Vṛṣaparvan','वृषपर्वा',['king of the asuras'])
node('kac',110,215,'Kaca','कचः',['learns the sañjīvanī','refuses Devayānī'])
node('dev',420,215,'Devayānī','देवयानी',['Śukra\'s daughter'],badges=[('bh','Bh 9.18')])
node('yay',640,215,'Yayāti','ययातिः',['“desire is never','quenched by indulgence”'],'hero',badges=[('bh','Bh 9.18–19'),('gp','GP Ā.139')])
node('sha',860,215,'Śarmiṣṭhā','शर्मिष्ठा',['Vṛṣaparvan\'s daughter'],badges=[('bh','Bh 9.18')])
node('yad',380,355,'Yadu','यदुः',['refuses the old age','his line: the Yādavas'])
node('tur',540,355,'Turvasu','तुर्वसुः',['refuses'])
node('dru',720,355,'Druhyu','द्रुह्युः',['refuses'])
node('anu',880,355,'Anu','अनुः',['refuses'])
node('pur',1050,355,'Pūru','पूरुः',['takes the old age','receives the kingdom'],'line',badges=[('bh','Bh 9.20')])
node('mad',300,480,'Mādhavī','माधवी',['Yayāti\'s daughter'])
node('gal',560,480,'Gālava','गालवः',['owes 800 horses','to Viśvāmitra'])
node('gar',780,480,'Garuḍa','गरुडः',['carries Gālava','hero of Arc 1'],badges=[('gp','GP Ā.2: tells this Purāṇa')])
node('vas',110,625,'Vasumanas','वसुमनाः',['gives Yayāti his merit'])
node('pra',270,625,'Pratardana','प्रतर्दनः',['gives Yayāti his merit'])
node('shi',430,625,'Śibi','शिबिः',['gives Yayāti his merit'],badges=[('q','Virāṭa 56.9: same Śibi?')])
node('ash',590,625,'Aṣṭaka','अष्टकः',['dialogue after','Yayāti\'s fall'])
node('bha',1050,460,'Bharata','भरतः',['through Duṣyanta','and Śakuntalā'],'line')
node('kur',1050,570,'Kuru','कुरुः',['the Kurus\' name'],'line')
node('shn',1050,680,'Śantanu','शन्तनुः',['Bhīṣma\'s father'],'line')
node('kau',930,800,'Kauravas','कौरवाः',['Dhṛtarāṣṭra\'s sons'],'line')
node('pan',1170,800,'Pāṇḍavas','पाण्डवाः',['Pāṇḍu\'s sons'],'line',badges=[('bh','Bh 9.22')])
node('par',1170,915,'Parīkṣit','परीक्षित्',['dies by Takṣaka','hears the Bhāgavata'],'meet',badges=[('bh','Bh 1.18–19, 12.6'),('q','scan: wrong Parīkṣit')])
node('kas',925,915,'Kāśyapa','काश्यपः',['the healer, turned back','revives the burnt tree'],'meet',badges=[('gp','GP Ā.3'),('q','same Kaśyapa?')])
node('jan',1170,1035,'Janamejaya','जनमेजयः',['holds the snake sacrifice'],'line',badges=[('bh','Bh 12.6'),('gp','GP Ā.140')])
node('vai',925,1035,'Vaiśampāyana','वैशम्पायनः',['tells him the epic'])

def box(i):
  cx,cy=P[i][0],P[i][1]; h=NH+ (14 if len(P[i][4])>1 else 0); w=WIDE.get(i,NW)
  return cx-w/2, cy-h/2, w, h
out=[]
add=out.append
add(f'<svg xmlns="http://www.w3.org/2000/svg" class="ym" viewBox="0 0 {W} {H}" role="img" aria-labelledby="ymt ymd">')
add('<title id="ymt">Yayāti\'s world, and two doors into the Purāṇas</title>')
add('<desc id="ymd">A family tree from the Mahābhārata: Yayāti with his gurus, queens, sons and daughter Mādhavī, and Pūru\'s line down to Parīkṣit and Janamejaya. Badges mark the chapters of the Bhāgavata and the Garuḍa Purāṇa that tell the same people. Both doors meet at Parīkṣit\'s death.</desc>')
add('''<style>
.ym{font-family:"Source Sans 3","Segoe UI",system-ui,sans-serif}
.ym .bg{fill:var(--surface,#ffffff)}
.ym .nb{fill:var(--band,#eceef2);stroke:var(--rule,#cfd4dd);stroke-width:1.2}
.ym .hero .nb{fill:var(--accent,#2f3a8f);stroke:var(--accent,#2f3a8f)}
.ym .hero .nm,.ym .hero .rl,.ym .hero .dv{fill:var(--surface,#ffffff)}
.ym .line .nb{fill:var(--accent-soft,#e6e8f6);stroke:var(--accent,#2f3a8f)}
.ym .meet .nb{fill:var(--gold-soft,#fbf1dc);stroke:var(--gold,#a86a00);stroke-width:2}
.ym .nm{font-family:"Spectral",Georgia,serif;font-size:16px;font-weight:600;fill:var(--ink,#1b2130)}
.ym .dv{font-family:"Tiro Devanagari Sanskrit","Noto Serif Devanagari","Nirmala UI",serif;font-size:12.5px;fill:var(--muted,#5b6474)}
.ym .rl{font-size:11.5px;fill:var(--muted,#5b6474)}
.ym .k{stroke:var(--muted,#5b6474);stroke-width:1.4;fill:none}
.ym .tie{stroke:var(--ink,#1b2130);stroke-width:2.2}
.ym .st{stroke:var(--accent,#2f3a8f);stroke-width:1.6;stroke-dasharray:5 4;fill:none}
.ym .sl{font-size:11.5px;fill:var(--accent,#2f3a8f);font-style:italic}
.ym .bh rect{fill:var(--leaf-soft,#e2f0e9);stroke:var(--leaf,#2f6f55)} .ym .bh text{fill:var(--leaf,#2f6f55)}
.ym .gp rect{fill:var(--clay-soft,#f6e6e2);stroke:var(--clay,#8a3b2e)} .ym .gp text{fill:var(--clay,#8a3b2e)}
.ym .q rect{fill:var(--gold-soft,#fbf1dc);stroke:var(--gold,#a86a00)} .ym .q text{fill:var(--gold,#a86a00)}
.ym .bdg text{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:10.5px}
.ym .zone{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px;letter-spacing:.12em;fill:var(--muted,#5b6474)}
.ym .door rect.f{stroke-width:1.5}
.ym .dt{font-family:"Spectral",Georgia,serif;font-size:17px;font-weight:600}
.ym .dl{font-size:12.5px;fill:var(--ink,#1b2130)}
.ym .dr{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px}
.ym .ttl{font-family:"Spectral",Georgia,serif;font-size:22px;font-weight:700;fill:var(--ink,#1b2130)}
@media (prefers-color-scheme:dark){svg.ym:root{--surface:#1a1f2b;--band:#232838;--rule:#39405a;--ink:#e6e8ee;--muted:#9aa3b5;--accent:#9aa6ff;--accent-soft:#232a45;--gold:#f0b44a;--gold-soft:#2e2615;--leaf:#7fcca8;--leaf-soft:#18302a;--clay:#f0a090;--clay-soft:#35201c}}
</style>''')
add(f'<rect class="bg" width="{W}" height="{H}" rx="14"/>')
def ln(x1,y1,x2,y2,c='k'): add(f'<path class="{c}" d="M{x1} {y1} L{x2} {y2}"/>')
def poly(pts,c='k'): add(f'<path class="{c}" d="M'+' L'.join(f'{a} {b}' for a,b in pts)+'"/>')
def bottom(i): bx,by,bw,bh=box(i); return P[i][0], by+bh
def top(i): bx,by,bw,bh=box(i); return P[i][0], by
def left(i): bx,by,bw,bh=box(i); return bx, P[i][1]
def right(i): bx,by,bw,bh=box(i); return bx+bw, P[i][1]
# parent -> child verticals
for a,b in [('brh','kac'),('shu','dev'),('nah','yay'),('vrs','sha'),('pur','bha'),('bha','kur'),('kur','shn'),('par','jan')]:
  ln(*bottom(a),*top(b))
# marriages: ties in the gaps
for a,b in [('dev','yay'),('yay','sha')]:
  (x1,y),(x2,_) = right(a), left(b); ln(x1,y-4,x2,y-4,'tie'); ln(x1,y+4,x2,y+4,'tie')
# children of Devayānī = Yayāti
m1 = (right('dev')[0]+left('yay')[0])/2; y0=P['dev'][1]+4
poly([(m1,y0),(m1,280)]); poly([(380,280),(540,280)])
for c in ('yad','tur'): ln(P[c][0],280,*top(c))
m2 = (right('yay')[0]+left('sha')[0])/2
poly([(m2,y0),(m2,292)]); poly([(720,292),(1050,292)])
for c in ('dru','anu','pur'): ln(P[c][0],292,*top(c))
# Yayāti -> Mādhavī (down the gap between Turvasu and Druhyu)
gx=630; poly([(gx,bottom('yay')[1]),(gx,428),(300,428),top('mad')])
# Mādhavī -> her four sons
yb=548; poly([(300,bottom('mad')[1]),(300,yb)]); poly([(110,yb),(590,yb)])
for c in ('vas','pra','shi','ash'): ln(P[c][0],yb,*top(c))
# Śantanu -> Kauravas / Pāṇḍavas; Pāṇḍavas -> Parīkṣit
yb=745; poly([(1050,bottom('shn')[1]),(1050,yb)]); poly([(930,yb),(1170,yb)])
for c in ('kau','pan'): ln(P[c][0],yb,*top(c))
ln(*bottom('pan'),*top('par'))
# story links, labelled only where the gap is clear
def story(p1,p2,lab=None,lx=None,ly=None,anchor='middle'):
  add(f'<path class="st" d="M{p1[0]} {p1[1]} L{p2[0]} {p2[1]}"/>')
  if lab: add(f'<text class="sl" x="{lx}" y="{ly}" text-anchor="{anchor}">{x(lab)}</text>')
story(right('brh'),left('shu'),'rival gurus',265,92)
story(right('kac'),left('dev'),'mutual curses',265,207)
story((185,190),(345,128),'his student',252,150,'start')
story(right('mad'),left('gal'),'given to him',430,472)
story(right('gal'),left('gar'),'carries',670,472)
story(left('kas'),right('vai'))  # placeholder removed below
out.pop()
story(right('kas'),left('par'),'turned back',1050,907)
story(right('vai'),left('jan'),'tells',1060,1027)
story((1245,915),(1245,915))
out.pop()
# nodes
def badge(bx,by,door,text):
  w=len(text)*6.6+12
  add(f'<g class="bdg {door}"><rect x="{bx}" y="{by}" width="{w:.0f}" height="17" rx="8.5"/><text x="{bx+6}" y="{by+12.5}">{x(text)}</text></g>')
  return w
for i,(cx,cy,name,deva,roles,kind,badges) in P.items():
  bx,by,bw,bh = box(i)
  add(f'<g class="n {kind}"><rect class="nb" x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10"/>')
  add(f'<text class="nm" x="{cx}" y="{by+22}" text-anchor="middle">{x(name)} <tspan class="dv">{x(deva)}</tspan></text>')
  for k,r in enumerate(roles): add(f'<text class="rl" x="{cx}" y="{by+40+k*14}" text-anchor="middle">{x(r)}</text>')
  add('</g>')
# badges sit just above each box, left-aligned, so they never cover lines below
for i,(cx,cy,name,deva,roles,kind,badges) in P.items():
  bx,by,bw,bh = box(i); xx=bx
  for door,t in badges:
    w=len(t)*6.6+12; badge(xx,by-19,door,t); xx+=w+4
# zones
add(f'<text class="ttl" x="40" y="34">Yayāti’s world, and two doors into the Purāṇas</text>')
add('<text class="zone" x="1290" y="330" text-anchor="end">PŪRU’S LINE ↓</text>')
add('<text class="zone" x="1300" y="1088" text-anchor="end">ARC 1 · TOLD TO HIS OWN DESCENDANT</text>')
# doors
def door(x0,y0,w,h,cls,title,rows):
  add(f'<g class="door {cls}"><rect class="f" x="{x0}" y="{y0}" width="{w}" height="{h}" rx="12" style="fill:var(--{"leaf" if cls=="bh" else "clay"}-soft,{"#e2f0e9" if cls=="bh" else "#f6e6e2"});stroke:var(--{"leaf" if cls=="bh" else "clay"},{"#2f6f55" if cls=="bh" else "#8a3b2e"})"/>')
  add(f'<text class="dt" x="{x0+16}" y="{y0+28}" style="fill:var(--{"leaf" if cls=="bh" else "clay"},{"#2f6f55" if cls=="bh" else "#8a3b2e"})">{x(title)}</text>')
  for k,(ref,txt) in enumerate(rows):
    yy=y0+56+k*24
    add(f'<text class="dr" x="{x0+16}" y="{yy}" style="fill:var(--{"leaf" if cls=="bh" else "clay"},{"#2f6f55" if cls=="bh" else "#8a3b2e"})">{x(ref)}</text>')
    add(f'<text class="dl" x="{x0+108}" y="{yy}">{x(txt)}</text>')
  add('</g>')
door(40,700,385,180,'bh','Door 1 · Bhāgavata, through Parīkṣit',[
  ('9.18–19','Yayāti, Devayānī, Śarmiṣṭhā, Pūru'),
  ('9.20, 9.22','Pūru’s line to the Pāṇḍavas'),
  ('1.18–19','the curse; Śuka comes to Parīkṣit'),
  ('12.6.16–28','the sacrifice; Bṛhaspati stops it'),
  ('12.6.11','Takṣaka meets Kāśyapa on the road')])
door(440,700,385,180,'gp','Door 2 · Garuḍa Purāṇa, through Garuḍa',[
  ('Ā. 2','Garuḍa tells this Purāṇa'),
  ('Ā. 3','hearing it, Kaśyapa revives a burnt tree'),
  ('Ā. 139–140','the lunar line, Yayāti to Janamejaya'),
  ('counts','Vinatā 34 verses · Kadrū 1 · Āstīka 0'),
  ('','no wager, no snake sacrifice')])
add('<text class="rl" x="40" y="912">Both doors meet at Parīkṣit’s death (gold boxes). Badges: <tspan style="fill:var(--leaf,#2f6f55)">Bhāgavata</tspan> · <tspan style="fill:var(--clay,#8a3b2e)">Garuḍa Purāṇa</tspan> · <tspan style="fill:var(--gold,#a86a00)">a question for the vidvān</tspan>.</text>')
add('<text class="rl" x="40" y="930">Family ties: = marriage, lines drop to children. Dashed: links in the story.</text>')
add('<text class="rl" x="40" y="948">Purāṇa chapters from the Śrī Śāradā Pīṭham text; Mahābhārata relations from Sørensen. All to be confirmed by a vidvān.</text>')
add('</svg>')
open('yayati-map.svg','w').write('\n'.join(out))
