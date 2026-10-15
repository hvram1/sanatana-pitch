# The workflow diagram for the Nāma-Kośa loop: swimlanes (who) by stages (when),
# arrows for the real branches. Human decisions are gold; agents are indigo.
from xml.sax.saxutils import escape as x
import textwrap
STAGES0=STAGES=['Request','Check','Prepare','Read','Decide','Publish','Thank']
LANES0=LANES=[('out','Others'),('agent','Agents'),('student','Students'),('junior','Junior vidvāns'),('senior','Senior vidvān')]
LW, CW, NW, NH, GAP = 116, 194, 138, 72, 14
STYLE='''<style>
.fd{font-family:"Source Sans 3","Segoe UI",system-ui,sans-serif}
.fd .bg{fill:var(--surface,#fff)}
.fd .band{fill:var(--band,#eceef2)}
.fd .lane{font-family:"Spectral",Georgia,serif;font-size:15px;font-weight:600;fill:var(--ink,#1b2130)}
.fd .stg{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:10.5px;letter-spacing:.1em;fill:var(--muted,#5b6474)}
.fd .grid{stroke:var(--rule,#d9dde5);stroke-width:1;stroke-dasharray:2 4}
.fd .nb{fill:var(--surface,#fff);stroke:var(--rule,#cfd4dd);stroke-width:1.2}
.fd .L-agent .nb{stroke:var(--accent,#2f3a8f);stroke-width:1.6}
.fd .L-student .nb{stroke:var(--leaf,#2f6f55);stroke-width:1.6}
.fd .L-out .nb{stroke:var(--muted,#5b6474);stroke-dasharray:4 3}
.fd .gate .nb{fill:var(--gold-soft,#fbf1dc);stroke:var(--gold,#a86a00);stroke-width:2}
.fd .num{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:10.5px;font-weight:500;fill:var(--accent,#2f3a8f)}
.fd .L-student .num{fill:var(--leaf,#2f6f55)} .fd .gate .num{fill:var(--gold,#a86a00)} .fd .L-out .num{fill:var(--muted,#5b6474)}
.fd .who{font-size:12px;font-weight:700;fill:var(--ink,#1b2130)}
.fd .tx{font-size:11.5px;fill:var(--muted,#5b6474)}
.fd .ed{stroke:var(--muted,#5b6474);stroke-width:1.5;fill:none;stroke-linejoin:round}
.fd .ed.hum{stroke:var(--gold,#a86a00)}
.fd .ah{fill:var(--muted,#5b6474)} .fd .ah.hum{fill:var(--gold,#a86a00)}
.fd .el{font-size:11px;font-style:italic;fill:var(--ink,#1b2130);paint-order:stroke;stroke:var(--surface,#fff);stroke-width:5px;stroke-linejoin:round}
.fd .gm{fill:var(--gold,#a86a00)}
@media (prefers-color-scheme:dark){svg.fd:root{--surface:#1a1f2b;--band:#202535;--rule:#39405a;--ink:#e6e8ee;--muted:#9aa3b5;--accent:#9aa6ff;--leaf:#7fcca8;--gold:#f0b44a;--gold-soft:#2e2615}}
</style>'''

def build(name, title, nodes, edges, stages=None, lanes=None):
  global STAGES, LANES
  STAGES=stages or STAGES0; LANES=lanes or LANES0
  # nodes: id -> (lane, stage, who, text, gate)
  lanes=[l for l,_ in LANES]
  stack={}
  pos={}
  for nid,(lane,st,who,tx,gate) in nodes.items():
    k=(lane,st); i=stack.get(k,0); stack[k]=i+1; pos[nid]=(lane,st,i)
  rows={l:max([stack.get((l,s),0) for s in range(len(STAGES))]+[0]) for l in lanes}
  used=[l for l in lanes if rows[l]]
  top=58; y=top; ly={}
  for l in used:
    h=rows[l]*(NH+GAP)+GAP; ly[l]=(y,h); y+=h+8
  W=LW+len(STAGES)*CW+16; H=y+8
  o=[f'<svg xmlns="http://www.w3.org/2000/svg" class="fd" viewBox="0 0 {W} {H}" role="img" aria-label="{x(title)}">',f'<title>{x(title)}</title>',STYLE,
     '<defs><marker id="a-'+name+'" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ah" d="M0 0 L10 5 L0 10 z"/></marker>',
     '<marker id="h-'+name+'" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ah hum" d="M0 0 L10 5 L0 10 z"/></marker></defs>',
     f'<rect class="bg" width="{W}" height="{H}" rx="12"/>']
  for i,s in enumerate(STAGES):
    cx=LW+i*CW+CW/2; o.append(f'<text class="stg" x="{cx}" y="36" text-anchor="middle">{s.upper()}</text>')
    if i: o.append(f'<line class="grid" x1="{LW+i*CW}" y1="46" x2="{LW+i*CW}" y2="{H-8}"/>')
  lab=dict(LANES)
  for l in used:
    y0,h=ly[l]; o.append(f'<rect class="band" x="10" y="{y0}" width="{W-20}" height="{h}" rx="8"/>')
    o.append(f'<text class="lane" x="22" y="{y0+h/2+5}">{x(lab[l])}</text>')
  box={}
  for nid,(lane,st,i) in pos.items():
    y0,h=ly[lane]; n=rows[lane]; cnt=stack[(lane,st)]
    # centre a short stack in a taller lane
    off=(n-cnt)*(NH+GAP)/2
    bx=LW+st*CW+(CW-NW)/2; by=y0+GAP+off+i*(NH+GAP)
    box[nid]=(bx,by,NW,NH)
  def anchor(n,side):
    bx,by,w,h=box[n]
    return {'r':(bx+w,by+h/2),'l':(bx,by+h/2),'t':(bx+w/2,by),'b':(bx+w/2,by+h)}[side]
  for e in edges:
    a,b=e[0],e[1]; lbl=e[2] if len(e)>2 else ''; off=e[3] if len(e)>3 else 0; hum=nodes[a][4]
    sa=nodes[a][1]; sb=nodes[b][1]
    cls='ed hum' if hum else 'ed'; mk=('h-' if hum else 'a-')+name
    if sb==sa:
      ax,ay,aw,ah=box[a]; bx_,by_,bw,bh=box[b]
      p1=anchor(a,'b') if by_>ay else anchor(a,'t'); p2=anchor(b,'t') if by_>ay else anchor(b,'b')
      pts=[p1,p2]; lx,ly_=p1[0]+6,(p1[1]+p2[1])/2+4; anc='start'
    else:
      p1=anchor(a,'r'); p2=anchor(b,'l')
      chx=LW+sb*CW+off   # centre of the gutter before the target column   # the gutter just before the target column
      pts=[p1,(chx,p1[1]),(chx,p2[1]),p2] if abs(p1[1]-p2[1])>1 else [p1,p2]
      if abs(p1[1]-p2[1])>24: lx,ly_,anc=chx,(p1[1]+p2[1])/2+4,'middle'
      else: lx,ly_,anc=(p1[0]+chx)/2,p1[1]-6,'middle'
    o.append(f'<path class="{cls}" d="M'+' L'.join(f'{px:.0f} {py:.0f}' for px,py in pts)+f'" marker-end="url(#{mk})"/>')
    if lbl: o.append(f'<text class="el" x="{lx:.0f}" y="{ly_:.0f}" text-anchor="{anc}">{x(lbl)}</text>')
  order=list(nodes)
  for k,nid in enumerate(order):
    lane,st,who,tx,gate=nodes[nid]; bx,by,w,h=box[nid]
    o.append(f'<g class="L-{lane}{" gate" if gate else ""}"><rect class="nb" x="{bx}" y="{by}" width="{w}" height="{h}" rx="9"/>')
    if gate: o.append(f'<path class="gm" d="M{bx+w-12} {by+h-18} l6 6 l-6 6 l-6 -6 z"/>')
    o.append(f'<text class="num" x="{bx+9}" y="{by+16}">{k+1}</text><text class="who" x="{bx+(30 if k>=9 else 22)}" y="{by+16}">{x(who)}</text>')
    for j,line in enumerate(textwrap.wrap(tx,20)[:3]):
      o.append(f'<text class="tx" x="{bx+9}" y="{by+33+j*14}">{x(line)}</text>')
    o.append('</g>')
  o.append('</svg>')
  open(f'flow-{name}.svg','w').write('\n'.join(o))

R=False; G=True
build('request','One request, from a student\u2019s question to their name on the verse',{
 'r1':('out',0,'Student','asks about Yayāti',R),
 'r2':('agent',0,'Agent','opens one job for his family',R),
 'r3':('agent',1,'Agent','checks what the index already has',R),
 'r4':('junior',1,'Junior vidvān','ticks or strikes the 36 known links',G),
 'r5':('agent',2,'Agent','finds 522 Purāṇa verses and sorts them',R),
 'r6':('agent',2,'Agent','makes batches, two readers each',R),
 'r7':('student',3,'Two students','is this our Yayāti? verse by verse',G),
 'r8':('agent',3,'Agent','reminds, then compares the answers',R),
 'r9':('junior',4,'Junior vidvān','confirms where they agree; signs',G),
 'r10':('senior',4,'Senior vidvān','decides the hard ones; signs',G),
 'r11':('agent',5,'Agent','records who read and who signed; rebuilds the site',R),
 'r12':('agent',6,'Agent','tells each student their verses are live',R),
 'r13':('out',6,'Upanyāsakar','invited to tell the story',R)},
 [('r1','r2'),('r2','r3'),('r3','r4','known'),('r3','r5','missing'),('r5','r6'),('r6','r7'),('r7','r8'),('r8','r9','agree'),('r8','r10','differ'),
  ('r4','r9','checked'),('r9','r11'),('r10','r11'),('r11','r12'),('r12','r13')])
