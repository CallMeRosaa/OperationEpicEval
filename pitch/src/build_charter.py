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
    c.drawString(M,H-0.30*inch,"PROJECT CHARTER  ·  PROPOSAL TO THE DAF AI FACTORY (AFRL)")
    c.drawRightString(W-M,H-0.30*inch,"DRAFT  ·  PRE-DECISIONAL  ·  SEP 2026")
    c.setFont("Helvetica-Bold",23); c.drawString(M,H-0.64*inch,"Evaluation & Awards Ecosystem")
    c.setFont("Helvetica",9.5)
    c.drawString(M,H-0.86*inch,"Proposed by: [Name, Rank]  ·  96th Maintenance Squadron, 96 MXG  ·  [Email / DSN]")
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
botline_h=0.80*inch
frames=[Frame(M,top-botline_h,W-2*M,botline_h,id="bl",leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),
        Frame(M,0.52*inch,colw,top-botline_h-0.52*inch-0.08*inch,id="L",leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),
        Frame(M+colw+gut,0.52*inch,colw,top-botline_h-0.52*inch-0.08*inch,id="R",leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)]
doc=BaseDocTemplate(out,pagesize=letter,leftMargin=M,rightMargin=M,topMargin=M,bottomMargin=M,
    title="Evaluation & Awards Ecosystem — Project Charter",author="96 MXS",subject="Proposal to the DAF AI Factory (AFRL)")
doc.addPageTemplates([PageTemplate(id="p",frames=frames,onPage=hdr)])

st=[]
t=Table([[Paragraph("<b>Bottom line:</b> Evaluations and awards are valuable. The hours spent writing, emailing, marking up and re-sending them are not. "
  "We propose a secure, AI-assisted ecosystem that <b>gives that administrative time back to the warfighter</b> and produces stronger records, "
  "piloted in the 96 MXS and built to scale across the DAF at IL4/IL5.",bot)]],colWidths=[W-2*M])
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
st+=B(["<b>Humans decide.</b> The AI drafts and advises and never submits.",
 "<b>AI scores the writing, not the person.</b> Boards never see AI scores and score packages with names removed.",
 "<b>Traceable.</b> Every AI output is logged with model and prompt version and traced to the member's own entries.",
 "<b>Private by default.</b> A member's journal is theirs. Supervisors see only submitted packages. Access follows the rating chain."])
st+=[H_("Built for DoD deployment")]
st+=B(["Cloud-agnostic: <b>AWS GovCloud or Azure Government</b>, targeting <b>IL4</b> (CUI/PII) with an IL5 path.",
 "Kubernetes and Platform One compatible; Iron Bank images; FIPS crypto; CAC/PKI login; air-gap ready.",
 "Designed to inherit platform controls; Privacy Impact Assessment planned early.",
 "A prep and coordination tool that feeds official systems of record rather than replacing them."])
st.append(FrameBreak())

# RIGHT
st+=[H_("Roadmap")]
rows=[[Paragraph("<b>When</b>",cellb),Paragraph("<b>Phase</b>",cellb),Paragraph("<b>Exit gate</b>",cellb)],
 ["FY27 Q1","<b>0 · Pitch & prototype.</b> Clickable demo on synthetic 96 MXS data.","Selected; sponsor named"],
 ["FY27 Q2","<b>1 · MVP.</b> Journal, library & import, SEL setup, rules & six-line check, routing, AI coach & editor.","Full cycle on synthetic data"],
 ["FY27 Q3","<b>2 · 96 MXS pilot.</b> IL4 environment, privacy & ATO path, one real quarterly award cycle, AI scorer & copilot.","Pilot metrics met"],
 ["FY27 Q4–FY28 Q1","<b>3 · Group & wing.</b> Nominations advance to 96 MXG and wing; dashboards; evaluation drafts.","New squadron onboarded in < 1 day"],
 ["FY28+","<b>4 · Enterprise.</b> Other wings, both clouds, IL5 option, export to official systems.","Enterprise sponsor & sustainment"]]
rows=[rows[0]]+[[Paragraph(r[0],cellb),Paragraph(r[1],cell),Paragraph(r[2],cell)] for r in rows[1:]]
rt=Table(rows,colWidths=[0.78*inch,colw-0.78*inch-1.02*inch,1.02*inch])
rt.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,0),(-1,0),SUNK),("BACKGROUND",(0,3),(-1,3),YELS),
  ("LINEBELOW",(0,0),(-1,-1),0.4,LINE),("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),
  ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
st+=[rt]
st+=[H_("How we'll measure success")]
st+=B(["<b>Admin hours returned to the mission</b> per package (member + every reviewer), measured against a pre-pilot baseline.",
 "Share of packages ready <b>before the final week</b>, versus today's deadline crunch.",
 "Emails and PDF versions eliminated; review rounds per package.",
 "Packages rule-compliant on first submission; member and supervisor satisfaction."])

askrows=[
 "<b>1. Sponsorship.</b> Accept the project into the AI Factory portfolio and help align 96 TW / 96 MXG leadership for the pilot.",
 "<b>2. Environment.</b> An IL4 development and pilot environment on the AI Factory platform (AWS GovCloud or Azure Government), with a DevSecOps pipeline.",
 "<b>3. AI model access.</b> An approved LLM and embedding endpoint authorized for CUI/PII workloads.",
 "<b>4. Accreditation & privacy.</b> Guidance on control inheritance and the ATO path, Privacy Impact Assessment and SORN determination, and Responsible AI review.",
 "<b>5. Team.</b> Engineering and UX support (proposed: 2–3 developers and 1 designer for two quarters) alongside the unit's domain experts.",
 "<b>6. Resourcing.</b> Pilot funding and compute (ROM to follow after scoping with the AI Factory)."]
askbox=[Paragraph("HOW THE AI FACTORY CAN HELP",S("ah",fontName="Helvetica-Bold",fontSize=9.5,leading=12,textColor=white,spaceAfter=4))]+[Paragraph(a,S("aa",parent=ask,textColor=white)) for a in askrows]
at=Table([[askbox]],colWidths=[colw])
at.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),OLIVE),("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
st+=[Spacer(1,8),at]
st+=[Spacer(1,6),Paragraph("<b>What the 96 MXS brings:</b> a ready pilot unit with defined award programs and routing, SEL and supervisor subject-matter experts, the unit's writing guides and SOPs, and a working architecture and prototype.",S("bring",parent=b,fontSize=8,leading=10.2,textColor=INK))]

import copy
cur="bl";hs={"bl":0,"L":0,"R":0};order=["bl","L","R"];i=0
for f in st:
    if f.__class__.__name__=="FrameBreak" or getattr(f,"action",None): i+=1; continue
    w,hh=f.wrap(W-2*M if order[i]=="bl" else colw, 2000); hs[order[i]]+=hh+f.getSpaceBefore()+f.getSpaceAfter()
print({k:round(v) for k,v in hs.items()}, "avail", round(frames[1]._height))
doc.build(st)
