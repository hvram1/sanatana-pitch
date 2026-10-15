# Builds Yayāti's family as two standalone SVGs with the same layout:
#   map-today.svg  what the index holds now: links copied from Sørensen, unchecked, some wrong
#   map-after.svg  what the reading should leave: links signed, mistakes fixed, Purāṇa verses attached
# Family-tree layout: marriage is a short horizontal tie, descent drops from it;
# roles sit inside each box so no label ever lies on a line.
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
node('gar',780,480,'Garuḍa','गरुडः',['carries Gālava'],badges=[('gp','GP Ā.2: tells this Purāṇa')])
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

# today: what is wrong or unknown, per person ('x' wrong, 'q' a question)
TODAY = {
  'yay':[('q','0 Purāṇa verses linked')],
  'dev':[('x','✗ wrong father')],
  'mad':[('x','✗ married to a Janamejaya')],
  'shn':[('q','also spelt Śāntanu, षन्तनु')],
  'par':[('x','✗ verses on another Parīkṣit')],
  'jan':[('x','✗ 2 links to namesakes')],
  'kas':[('q','same as the Garuḍa’s Kaśyapa?')],
  'shi':[('q','same Śibi as Virāṭa 56.9?')],
}
# after: what a vidvān's ruling adds on top of the Purāṇa badges
AFTER = {
  'dev':[('ok','✓ father fixed')],
  'par':[('ok','✓ verses moved')],
  'kas':[('ok','✓ ruled')],
  'shi':[('ok','✓ ruled')],
}
def render(state):
  global out, add
  def box(i):
    cx,cy=P[i][0],P[i][1]; h=NH+ (14 if len(P[i][4])>1 else 0); w=WIDE.get(i,NW)
    return cx-w/2, cy-h/2, w, h
  out=[]
  add=out.append
  add(f'<svg xmlns="http://www.w3.org/2000/svg" class="ym {state}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="ymt ymd">')
  add(f'<title id="ymt">{x(TITLE[state])}</title>')
  add(f'<desc id="ymd">{x(DESC[state])}</desc>')
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
  .ym .x rect{fill:var(--clay-soft,#f6e6e2);stroke:var(--clay,#8a3b2e)} .ym .x text{fill:var(--clay,#8a3b2e)}
.ym .ok rect{fill:var(--leaf,#2f6f55);stroke:var(--leaf,#2f6f55)} .ym .ok text{fill:var(--surface,#ffffff)}
.ym.today .k,.ym.today .tie{stroke-dasharray:3 4;opacity:.55}
.ym.today .nb{fill:var(--surface,#ffffff)}
.ym.today .hero .nb{fill:var(--accent-soft,#e6e8f6)} .ym.today .hero .nm{fill:var(--ink,#1b2130)} .ym.today .hero .rl,.ym.today .hero .dv{fill:var(--muted,#5b6474)}
.ym.today .line .nb,.ym.today .meet .nb{fill:var(--surface,#ffffff);stroke:var(--rule,#cfd4dd);stroke-width:1.2}
.ym .tick circle{fill:var(--leaf,#2f6f55)} .ym .tick path{stroke:#fff;stroke-width:2;fill:none}
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
    if state=='today': badges=TODAY.get(i,[])
    else:
      badges=[b for b in badges if b[0]!='q']+AFTER.get(i,[])
      add(f'<g class="tick"><circle cx="{bx+bw-4}" cy="{by+bh-4}" r="8"/><path d="M{bx+bw-8} {by+bh-4} l3 3 l5 -6"/></g>')
    for door,t in badges:
      w=len(t)*6.6+12; badge(xx,by-19,door,t); xx+=w+4
  # zones
  add(f'<text class="ttl" x="40" y="34">{x(TITLE[state])}</text>')
  add('<text class="zone" x="1290" y="330" text-anchor="end">PŪRU’S LINE ↓</text>')
  add('<text class="zone" x="1300" y="1088" text-anchor="end">THE MAHĀBHĀRATA IS TOLD TO JANAMEJAYA</text>')
  # doors
  def door(x0,y0,w,h,cls,title,rows):
    tone,ink,soft={'bh':('leaf','#2f6f55','#e2f0e9'),'gp':('clay','#8a3b2e','#f6e6e2'),'q':('gold','#a86a00','#fbf1dc'),'x':('clay','#8a3b2e','#f6e6e2')}[cls]
    add(f'<g class="door {cls}"><rect class="f" x="{x0}" y="{y0}" width="{w}" height="{h}" rx="12" style="fill:var(--{tone}-soft,{soft});stroke:var(--{tone},{ink})"/>')
    add(f'<text class="dt" x="{x0+16}" y="{y0+28}" style="fill:var(--{tone},{ink})">{x(title)}</text>')
    for k,(ref,txt) in enumerate(rows):
      yy=y0+56+k*24
      add(f'<text class="dr" x="{x0+16}" y="{yy}" style="fill:var(--{tone},{ink})">{x(ref)}</text>')
      add(f'<text class="dl" x="{x0+108}" y="{yy}">{x(txt)}</text>')
    add('</g>')
  if state=='today':
    door(40,700,385,180,'q','What the index holds today',[
      ('36','family links, copied from Sørensen'),
      ('0','of them checked by a scholar'),
      ('220','Mahābhārata verses cited for Yayāti'),
      ('~477','Purāṇa verses with his name'),
      ('0','of those linked to him')])
    door(440,700,385,180,'x','What is wrong or unknown',[
      ('wrong','3 links join the wrong namesake'),
      ('wrong','Devayānī given the wrong father'),
      ('misfiled','his Purāṇa verses filed under a place'),
      ('spelling','Śantanu stored three ways'),
      ('open','2 questions only a vidvān can settle')])
    add('<text class="rl" x="40" y="912">Badges: <tspan style="fill:var(--clay,#8a3b2e)">wrong</tspan> · <tspan style="fill:var(--gold,#a86a00)">unknown, or a question for a vidvān</tspan>. Faint lines: recorded, never checked.</text>')
    add('<text class="rl" x="40" y="930">Counts from the corpus database, 15 October 2026. Purāṇa counts are word matches, not yet people.</text>')
  else:
    door(40,700,385,180,'bh','In the Bhāgavata, via Parīkṣit',[
      ('9.18–19','Yayāti, Devayānī, Śarmiṣṭhā, Pūru'),
      ('9.20, 9.22','Pūru’s line to the Pāṇḍavas'),
      ('1.18–19','the curse; Śuka comes to Parīkṣit'),
      ('12.6.16–28','the sacrifice; Bṛhaspati stops it'),
      ('12.6.11','Takṣaka meets Kāśyapa on the road')])
    door(440,700,385,180,'gp','In the Garuḍa Purāṇa, via Garuḍa',[
      ('Ā. 2','Garuḍa tells this Purāṇa'),
      ('Ā. 3','hearing it, Kaśyapa revives a burnt tree'),
      ('Ā. 139–140','the lunar line, Yayāti to Janamejaya'),
      ('counts','Vinatā 34 verses · Kadrū 1 · Āstīka 0'),
      ('','no wager, no snake sacrifice')])
    add('<text class="rl" x="40" y="912">Both Purāṇas meet at Parīkṣit’s death (gold boxes). Badges: <tspan style="fill:var(--leaf,#2f6f55)">Bhāgavata</tspan> · <tspan style="fill:var(--clay,#8a3b2e)">Garuḍa Purāṇa</tspan> · <tspan style="fill:var(--leaf,#2f6f55)">✓ a vidvān’s ruling</tspan>.</text>')
    add('<text class="rl" x="40" y="930">Every box and family line signed by a vidvān; every verse shows who read it. Expected outcome: the reading decides the details.</text>')
    add('<text class="rl" x="40" y="948">Purāṇa chapters from the Śrī Śāradā Pīṭham text; Mahābhārata relations from Sørensen.</text>')
  add('</svg>')
  open(f'map-{state}.svg','w').write('\n'.join(out))

TITLE = {'today':'Yayāti’s family in the index today','after':'Yayāti’s family after the work (expected)'}
DESC = {'today':'A family tree from the Mahābhārata, Yayāti to Janamejaya, as the index holds it now: every link copied from Sørensen and none checked, three joining the wrong namesake, and none of his Purāṇa verses linked.',
        'after':'The same family tree after the reading: every link signed by a vidvān, the mistakes corrected, and badges for the chapters of the Bhāgavata and the Garuḍa Purāṇa that tell the same people.'}
for st in ('today','after'):
  out=[]; add=out.append
  render(st)
