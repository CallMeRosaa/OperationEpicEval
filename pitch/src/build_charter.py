import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, FrameBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

OLIVE=HexColor("#4B5320"); INK=HexColor("#1B1E15"); INK2=HexColor("#454A3A"); INK3=HexColor("#737866")
YEL=HexColor("#E3B505"); YELS=HexColor("#F7EDC2"); SUNK=HexColor("#ECEEE6"); BLUE=HexColor("#2F6690"); LINE=HexColor("#B9BDA8")
W,H=letter; M=0.45*inch; HEAD=1.02*inch

out=sys.argv[1]
def hdr(c,doc):
    c.saveState()
    c.setFillColor(OLIVE); c.rect(0,H-HEAD,W,HEAD,fill=1,stroke=0)
    c.setFillColor(YEL); c.rect(0,H-HEAD-4,W,4,fill=1,stroke=0)
    c.setFillColor(white); c.setFont("Helvetica",7.5)
    c.drawString(M,H-0.30*inch,"PROJECT CHARTER  ·  PATHFINDER PROPOSAL TO THE DAF AI FACTORY (AFRL)")
    c.drawRightString(W-M,H-0.30*inch,"DRAFT  ·  PRE-DECISIONAL  ·  SEP 2026")
    c.setFont("Helvetica-Bold",23); c.drawString(M,H-0.64*inch,"Evaluation & Awards Ecosystem")
    c.setFont("Helvetica",9.5)
    c.drawString(M,H-0.86*inch,"Proposed by: Michael Rosa  ·  96th Maintenance Squadron, 96 MXG  ·  Michael.Rosa@us.af.mil")
    # footer
    c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(M,0.42*inch,W-M,0.42*inch)
    c.setFillColor(INK3); c.setFont("Helvetica",6.8)
    c.drawString(M,0.28*inch,"Unclassified. Contains no CUI or personnel data. Timeline and figures are targets for discussion.")
    c.drawRightString(W-M,0.28*inch,"Reference unit: 96 MXS (Munitions & PMEL Flights)")
    c.restoreState()

S=lambda n,**k: ParagraphStyle(n,**k)
h=S("h",fontName="Helvetica-Bold",fontSize=9,leading=11,textColor=OLIVE,spaceBefore=8,spaceAfter=3)
b=S("b",fontName="Helvetica",fontSize=8.3,leading=10.6,textColor=INK2)
bl=S("bl",parent=b,leftIndent=9,bulletIndent=0,spaceAfter=1.2)
bot=S("bot",fontName="Helvetica",fontSize=9.6,leading=12.6,textColor=INK)
cell=S("cell",fontName="Helvetica",fontSize=7.6,leading=9.4,textColor=INK2)
cellb=S("cellb",parent=cell,fontName="Helvetica-Bold",textColor=INK)
ask=S("ask",parent=b,fontSize=8.3,leading=10.6,textColor=INK,leftIndent=11,bulletIndent=0,spaceAfter=2.5)

def H_(t): return Paragraph(t.upper(),h)
def P(t): return Paragraph(t,b)
def B(items): return [Paragraph(i,bl,bulletText="•") for i in items]

top=H-HEAD-4-0.14*inch
gut=0.26*inch; colw=(W-2*M-gut)/2
botline_h=1.12*inch
frames=[Frame(M,top-botline_h,W-2*M,botline_h,id="bl",leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),
        Frame(M,0.52*inch,colw,top-botline_h-0.52*inch-0.08*inch,id="L",leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),
        Frame(M+colw+gut,0.52*inch,colw,top-botline_h-0.52*inch-0.08*inch,id="R",leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)]
doc=BaseDocTemplate(out,pagesize=letter,leftMargin=M,rightMargin=M,topMargin=M,bottomMargin=M,
    title="Evaluation & Awards Ecosystem — Project Charter",author="Michael Rosa, 96 MXS",subject="Proposal to the DAF AI Factory (AFRL)")
doc.addPageTemplates([PageTemplate(id="p",frames=frames,onPage=hdr)])

st=[]
t=Table([[Paragraph("<b>Bottom line:</b> Evaluations and awards are valuable. The hours spent writing, emailing, marking up and re-sending them are not. "
  "We propose a secure, AI-assisted ecosystem that <b>gives that administrative time back to the warfighter</b> and produces stronger records, "
  "piloted in the 96 MXS and built to scale across the DAF at IL4/IL5. It is also a deliberate <b>pathfinder</b>: a benchmark of how fast the DAF "
  "can take an identified gap to an MVP and IOC in an IL4/IL5 environment under today's processes, technology and regulations.",bot)]],colWidths=[W-2*M])
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),YELS),("LINEBEFORE",(0,0),(0,-1),4,YEL),
  ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
st+= [t, FrameBreak()]

# LEFT
st+=[H_("The problem"),
 P("Every quarter and every year, Airmen and Guardians rebuild their accomplishments from memory. Packages then move as PDFs by email: opened, marked up, saved and sent back at every layer. An estimated <b>60–80% of this work happens right at the deadline</b>. The know-how for a strong, promotable record lives in scattered PDFs and in a few experienced supervisors' heads. The result is lost detail, uneven quality, version confusion, and hours pulled away from the mission.")]
st+=[H_("The solution: three layers, one AI assistant")]
st+=B(["<b>Capture.</b> A year-round journal. Members log jobs, efforts, dates, impact and metrics in about 30 seconds, as work happens.",
 "<b>Context.</b> Each unit's rules are codified: who can apply for which award, format (e.g., 5 statements, 6 lines max), routing and suspense dates. The SEL sets it up in a <b>5–10 minute guided interview</b>, inheriting from group and wing. A <b>document library</b> of writing guides, award SOPs and sanitized past winners teaches the AI the unit's playbook.",
 "<b>Coordination.</b> One live package routes member > supervisor > section > flight > SEL > board, with inline comments, tracked edits, returns and full history. No email or PDF loop.",
 "<b>AI assistant.</b> Coaches members (\"how many aircraft? what did it save?\"), drafts from journal entries, checks format live, scores the <i>writing</i> against the award rubric, suggests edits, and speeds supervisor review. Every suggestion cites its source."])
st+=[H_("Responsible AI by design")]
st+=B(["<b>Humans decide.</b> The AI drafts and advises and never submits. It <b>scores the writing, not the person</b>, and boards never see AI scores.",
 "<b>Traceable.</b> Every AI output is logged with model and prompt version and cited to its source.",
 "<b>Private by default.</b> A member's journal is theirs. Supervisors see only submitted packages."])
st+=[H_("A pathfinder for DAF speed to capability")]
st+=[P("We will move as fast as current policy allows and <b>instrument every step</b>, so the DAF gets a measured, repeatable path from pain point to fielded capability.")]
st+=B(["<b>Benchmark the pipeline:</b> days from approval to IL4/IL5 environment, DevSecOps pipeline, ATO / cATO, MVP in a testable environment, and IOC.",
 "<b>Log every blocker:</b> each approval, handoff and wait, with owner and duration. The output is a playbook and a list of policy and process gaps.",
 "<b>Exercise the whole enterprise:</b> cyber and comm/IT, software factories, the AI Factory, privacy and legal, CFMs, MAJCOM and HQ, and DAF/A1 policy owners."])
st.append(FrameBreak())

# RIGHT
st+=[H_("Roadmap")]
rows=[[Paragraph("<b>When</b>",cellb),Paragraph("<b>Phase</b>",cellb),Paragraph("<b>Exit gate</b>",cellb)],
 ["FY27 Q1","<b>0 · Pitch & prototype.</b> Clickable demo on synthetic 96 MXS data.","Selected; sponsor named"],
 ["FY27 Q2","<b>1 · MVP.</b> Journal, library, SEL setup, rules check, routing, AI coach & editor in a testable IL4 environment.","MVP live in IL4 test env"],
 ["FY27 Q3","<b>2 · IOC: 96 MXS pilot.</b> ATO and privacy complete, one real quarterly award cycle, AI scorer & copilot.","IOC declared; benchmark report"],
 ["FY27 Q4–FY28 Q1","<b>3 · Group & wing.</b> Nominations advance to 96 MXG and wing; dashboards; evaluation drafts.","New squadron onboarded in < 1 day"],
 ["FY28+","<b>4 · Enterprise.</b> Other wings, both clouds, IL5 option, export to official systems.","Enterprise sponsor & sustainment"]]
rows=[rows[0]]+[[Paragraph(r[0],cellb),Paragraph(r[1],cell),Paragraph(r[2],cell)] for r in rows[1:]]
rt=Table(rows,colWidths=[0.78*inch,colw-0.78*inch-1.02*inch,1.02*inch])
rt.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,0),(-1,0),SUNK),("BACKGROUND",(0,3),(-1,3),YELS),
  ("LINEBELOW",(0,0),(-1,-1),0.4,LINE),("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),
  ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
st+=[rt]
st+=[H_("How we'll measure success")]
st+=B(["<b>Mission:</b> admin hours returned per package (member + every reviewer) against a pre-pilot baseline; share of packages ready before the final week; emails and PDF versions eliminated.",
 "<b>DAF throughput:</b> days from idea to IL4/IL5 environment, to ATO, to MVP and to IOC; number of blockers and the time each one cost."])

st+=[H_("Built for DoD deployment")]
st+=B(["<b>AWS GovCloud or Azure Government</b>, IL4 (CUI/PII) with an IL5 path. Kubernetes, Platform One compatible, Iron Bank, FIPS, CAC/PKI. Feeds official systems of record."])

askrows=[
 "<b>1. Sponsorship.</b> Accept this as an AI Factory pathfinder and help convene cyber, comm/IT, software factory, CFM, HQ and DAF stakeholders.",
 "<b>2. Environment.</b> An IL4 development and pilot environment on the AI Factory platform (AWS GovCloud or Azure Government), with a DevSecOps pipeline.",
 "<b>3. AI model access.</b> An approved LLM and embedding endpoint authorized for CUI/PII workloads.",
 "<b>4. Accreditation & privacy.</b> The fastest available ATO / cATO path with control inheritance, PIA and SORN guidance, and Responsible AI review.",
 "<b>5. Team.</b> Engineering and UX support (proposed: 2–3 developers, 1 designer, two quarters) alongside unit experts.",
 "<b>6. Resourcing.</b> Pilot funding and compute (ROM to follow scoping)."]
askbox=[Paragraph("HOW THE AI FACTORY CAN HELP",S("ah",fontName="Helvetica-Bold",fontSize=9.5,leading=12,textColor=white,spaceAfter=4))]+[Paragraph(a,S("aa",parent=ask,textColor=white)) for a in askrows]
at=Table([[askbox]],colWidths=[colw])
at.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),OLIVE),("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
st+=[Spacer(1,7),at]
st+=[Spacer(1,6),Paragraph("<b>What the 96 MXS brings:</b> a ready pilot unit, SEL and supervisor experts, the unit's guides and SOPs, a working architecture, and a commitment to document the journey for the DAF.",S("bring",parent=b,fontSize=8,leading=10.2,textColor=INK))]

import copy
cur="bl";hs={"bl":0,"L":0,"R":0};order=["bl","L","R"];i=0
for f in st:
    if f.__class__.__name__=="FrameBreak" or getattr(f,"action",None): i+=1; continue
    w,hh=f.wrap(W-2*M if order[i]=="bl" else colw, 2000); hs[order[i]]+=hh+f.getSpaceBefore()+f.getSpaceAfter()
print({k:round(v) for k,v in hs.items()}, "avail", round(frames[1]._height))
doc.build(st)
