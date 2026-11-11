import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_week3_doc(output_path):
    doc = docx.Document()
    
    # Page Setup: Standard Letter, 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        # Header / Footer
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ft = p_ft.add_run("MotoCare Cambodia — Week 3: Data Modeling & Architecture | Page ")
        r_ft.font.name = "Calibri"
        r_ft.font.size = Pt(8.5)
        r_ft.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)

    # Palette
    COLOR_PRIMARY = RGBColor(0x1E, 0x3A, 0x8A)      # Deep Navy Blue
    COLOR_SECONDARY = RGBColor(0x25, 0x63, 0xEB)    # Royal Blue
    COLOR_DARK = RGBColor(0x1F, 0x29, 0x37)         # Charcoal Dark
    COLOR_MUTED = RGBColor(0x4B, 0x55, 0x63)        # Slate Muted
    HEX_PRIMARY = "1E3A8A"
    HEX_SECONDARY = "2563EB"
    HEX_LIGHT_BG = "F8FAFC"
    HEX_CALLOUT_BG = "EFF6FF"
    HEX_BORDER = "CBD5E1"
    
    # Helpers
    def set_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def set_bg(cell, hex_color):
        shading_xml = f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'
        cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

    def set_subtle_borders(cell, border_color="E2E8F0"):
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        for edge in ('top', 'left', 'bottom', 'right'):
            element = OxmlElement(f'w:{edge}')
            element.set(qn('w:val'), 'single')
            element.set(qn('w:sz'), '4')
            element.set(qn('w:space'), '0')
            element.set(qn('w:color'), border_color)
            tcBorders.append(element)
        tcPr.append(tcBorders)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_DARK
        return p

    def add_p(text, bold_prefix=None, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.font.name = "Calibri"
            r_b.font.size = Pt(9.5)
            r_b.font.bold = True
            r_b.font.color.rgb = COLOR_DARK
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = COLOR_DARK
        return p

    def add_callout(title, text, hex_bg="EFF6FF", hex_border="2563EB"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.columns[0].width = Inches(6.5)
        cell = tbl.cell(0, 0)
        set_bg(cell, hex_bg)
        set_margins(cell, top=120, bottom=120, left=180, right=180)
        
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        left = OxmlElement('w:left')
        left.set(qn('w:val'), 'single')
        left.set(qn('w:sz'), '24')
        left.set(qn('w:space'), '0')
        left.set(qn('w:color'), hex_border)
        tcBorders.append(left)
        for b in ['top', 'bottom', 'right']:
            node = OxmlElement(f'w:{b}')
            node.set(qn('w:val'), 'none')
            tcBorders.append(node)
        tcPr.append(tcBorders)
        
        cp = cell.paragraphs[0]
        cp.paragraph_format.space_before = Pt(0)
        cp.paragraph_format.space_after = Pt(2)
        r_t = cp.add_run(f"📌 {title}\n")
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(10)
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_PRIMARY
        
        r_b = cp.add_run(text)
        r_b.font.name = "Calibri"
        r_b.font.size = Pt(9)
        r_b.font.color.rgb = COLOR_DARK
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.columns[0].width = Inches(6.5)
        c = tbl.cell(0, 0)
        set_bg(c, "F1F5F9")
        set_margins(c, top=80, bottom=80, left=120, right=120)
        set_subtle_borders(c, "CBD5E1")
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(code_text)
        r.font.name = "Consolas"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # 1. TITLE & COVER HEADER BLOCK
    # -------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    r_main = p_title.add_run("MotoCare Cambodia")
    r_main.font.name = "Calibri"
    r_main.font.size = Pt(24)
    r_main.font.bold = True
    r_main.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(10)
    r_sub = p_sub.add_run("Week 3 Deliverable: Data Modeling, Relational ERD & System Architecture")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = COLOR_SECONDARY

    # Metadata Table
    meta_tbl = doc.add_table(rows=6, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_tbl.autofit = False
    meta_tbl.columns[0].width = Inches(1.8)
    meta_tbl.columns[1].width = Inches(4.7)
    
    meta_data = [
        ("Student & Author", "Thoeurn Kimchhay (ធឿន គីមឆាយ) — Bachelor of Computer Science"),
        ("Institution & Course", "Royal University of Phnom Penh (RUPP) — PPS1Y4 Capstone"),
        ("Project Advisor", "Hang Sopheak"),
        ("Academic Term", "Year 4, Semester 1 (2026)"),
        ("Deliverable Milestones", "Database ERD, State Transition Flowchart, System Architecture & API Contracts"),
        ("Project Status", "Week 3 Complete (Ready for Week 4 UI/UX & Figma Design)")
    ]
    
    for row_idx, (k, v) in enumerate(meta_data):
        c0 = meta_tbl.cell(row_idx, 0)
        c1 = meta_tbl.cell(row_idx, 1)
        set_bg(c0, "F1F5F9")
        set_bg(c1, "FFFFFF")
        set_margins(c0, top=50, bottom=50, left=100, right=100)
        set_margins(c1, top=50, bottom=50, left=100, right=100)
        set_subtle_borders(c0, "CBD5E1")
        set_subtle_borders(c1, "CBD5E1")
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k)
        r0.font.name = "Calibri"
        r0.font.size = Pt(9)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_DARK
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # 2. EXECUTIVE SUMMARY & WEEK 1-2 SYNTHESIS
    # -------------------------------------------------------------
    add_h1("1. Executive Summary & Architecture Strategy")
    add_p(
        "This document details the complete technical architecture and data modeling for MotoCare Cambodia—an intelligent maintenance companion engineered for Cambodia's high-density motorcycle landscape (Honda Dream 125, Scoopy, Click) and Japanese hybrid passenger cars (Toyota Prius 2nd/3rd Gen). Built to bridge the communication gap between riders and informal roadside mechanics (ជាងម៉ូតូ), the system pairs an offline-first mobile client with a cloud PostgreSQL database to track preventive maintenance intervals without requiring paper invoices."
    )
    
    add_callout(
        "CORE ARCHITECTURAL HIGHLIGHTS (WEEK 1 & 2 FEEDBACK ALIGNED)",
        "1. Dynamic Model-Agnostic Schema: Replaces hardcoded intervals with relational database configurations (model_component_configs). Supporting a new vehicle model requires only SQL inserts—zero client code modifications.\n"
        "2. Deterministic 4-State Reminder Engine: Dual-trigger logic (mileage vs. calendar days) transitions components deterministically: Upcoming (Green) -> Due Soon (Yellow) -> Overdue (Red) -> Serviced (Reset).\n"
        "3. Offline-First Resilience: Mobile persistence uses Drift (SQLite v3) for zero-latency local caching, while server transactions run on PostgreSQL 16 via Docker.\n"
        "4. At-Garage Dwell Geofencing: Background geofencing monitors 15-minute continuous dwell time within 50m of Google Places or user-pinned garages, firing proactive service logging notifications.\n"
        "5. Authentic Khmer Slang: Database fields and UI tags feature authentic garage slang (ប្រេងម៉ាស៊ីន, ខ្សែពាន, ប៊ូស៊ី, ស្បែកហ្វ្រាំង) alongside English terminology."
    )

    # -------------------------------------------------------------
    # 3. END-TO-END SYSTEM ARCHITECTURE MAP
    # -------------------------------------------------------------
    add_h1("2. End-to-End System Architecture Topology")
    add_p(
        "The system architecture follows a clean multi-tier topology separating mobile presentation, local persistence, network gateways, domain rules evaluation, relational storage, and third-party integrations."
    )
    
    add_h2("2.1 High-Level Component Topology")
    arch_ascii = (
        "+---------------------------------------------------------------------------------------+\n"
        "|                    FLUTTER MOBILE CLIENT (iOS & Android - Dart 3.5)                   |\n"
        "|                                                                                       |\n"
        "|  +------------------------+  +-------------------------+  +------------------------+  |\n"
        "|  |   Presentation (UI)    |  | State Management        |  | Local Offline Cache    |  |\n"
        "|  |   - R/Y/G Health Cards |  | - Riverpod Providers    |  | - Drift (SQLite v3)    |  |\n"
        "|  |   - Khmer Slang Tags   |  | - Offline Sync Queue    |  | - Instant reads/writes |  |\n"
        "|  +-----------+------------+  +------------+------------+  +-----------+------------+  |\n"
        "|              |                            |                           |               |\n"
        "|  +-----------v------------+               |                           |               |\n"
        "|  | Background Services    |               |                           |               |\n"
        "|  | - 15-Min Dwell Geofence|               |                           |               |\n"
        "|  | - Local Notifications  |               |                           |               |\n"
        "|  +------------------------+               |                           |               |\n"
        "+-------------------------------------------|---------------------------|---------------+\n"
        "                                            | REST API (HTTP / JSON)    |\n"
        "                                            | Port 8000 (/api/v1)       |\n"
        "                                            v                           v\n"
        "+---------------------------------------------------------------------------------------+\n"
        "|                      BACKEND API LAYER (Node.js & Express - TypeScript)               |\n"
        "|                                                                                       |\n"
        "|  +-------------------------------------+     +-------------------------------------+  |\n"
        "|  | Auth & Validation Middleware        |     | Domain Controllers                  |  |\n"
        "|  | - JWT Bearer Token Verification     |---->| - Vehicles & Models Controller      |  |\n"
        "|  | - Zod Payload Schema Sanitization   |     | - Service Logs & Garages Controller |  |\n"
        "|  +-------------------------------------+     +------------------+------------------+  |\n"
        "|                                                                 |                     |\n"
        "|                                              +------------------v------------------+  |\n"
        "|                                              | Maintenance Rules Engine            |  |\n"
        "|                                              | - Dual-Condition Trigger Evaluator  |  |\n"
        "|                                              | - Composite Wear Ratio Calculator   |  |\n"
        "|                                              +------------------+------------------+  |\n"
        "+-----------------------------------------------------------------|---------------------+\n"
        "                                                                  | PostgreSQL Protocol \n"
        "                                            +---------------------+---------------------+\n"
        "                                            |                                           |\n"
        "                                            v                                           v\n"
        "+-------------------------------------------------------+   +---------------------------+\n"
        "|           DATA TIER (PostgreSQL 16 in Docker)         |   | THIRD-PARTY CLOUD SERVICES|\n"
        "|                                                       |   |                           |\n"
        "| - users, vehicles, vehicle_models                     |   | - Google Places API       |\n"
        "| - components, model_component_configs                 |   |   (Nearby garage search)  |\n"
        "| - reminder_rules, service_logs, service_log_items     |   | - Supabase / Local Storage|\n"
        "| - garages, odometer_histories                         |   |   (Receipt & oil photos)  |\n"
        "+-------------------------------------------------------+   +---------------------------+\n"
    )
    add_code_block(arch_ascii)

    add_h2("2.2 Architecture Component Specifications")
    comp_data = [
        ("Mobile UI Layer", "Renders high-contrast Red / Yellow / Green maintenance cards, Khmer slang tags, and odometer inputs.", "Flutter (Dart 3.5)", "Continuously in foreground", "State Management (Riverpod)"),
        ("Local Persistence", "Stores offline vehicle records, queued logs, and pinned garages with <5ms read latency.", "Drift / SQLite v3", "On every read/write event", "Mobile UI, Backend API"),
        ("Geofence Service", "Monitors device proximity to known garages; triggers after 15+ minutes dwell within 50m.", "Android WorkManager / iOS CoreLocation", "Background event trigger", "Local Notification Tray"),
        ("Notification Tray", "Dispatches overdue maintenance alerts and 'At-Garage' service prompt notifications.", "flutter_local_notifications", "Scheduled / Geofence wake", "Mobile UI"),
        ("Backend REST API", "Validates payloads, enforces JWT auth, manages vehicle profiles, and exposes routes on port 8000.", "Node.js (v20) + Express (v4.19)", "Always-on HTTP daemon", "Mobile Client, PostgreSQL"),
        ("Rules Engine", "Calculates composite wear ratios and evaluates dual-condition triggers (km vs. days).", "TypeScript Domain Service", "On odometer update or service log", "PostgreSQL Database"),
        ("PostgreSQL Database", "Persistent relational store for 10 entities, relational cascades, and integer currency.", "PostgreSQL v16 (Docker)", "Always-on database service", "Backend REST API"),
        ("Google Places API", "Pre-seeds verified Phnom Penh motorcycle garages and auto shops with GPS coordinates.", "Google Cloud Platform", "On-demand garage search", "Backend Garage Controller")
    ]
    
    comp_tbl = doc.add_table(rows=len(comp_data) + 1, cols=5)
    comp_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_tbl.autofit = False
    comp_tbl.columns[0].width = Inches(1.3)
    comp_tbl.columns[1].width = Inches(2.0)
    comp_tbl.columns[2].width = Inches(1.1)
    comp_tbl.columns[3].width = Inches(1.0)
    comp_tbl.columns[4].width = Inches(1.1)
    
    headers_cp = ["Component", "Responsibility", "Technology", "Runs When", "Talks To"]
    for i, h in enumerate(headers_cp):
        c = comp_tbl.cell(0, i)
        set_bg(c, HEX_PRIMARY)
        set_margins(c, top=60, bottom=60, left=70, right=70)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (name, resp, tech, when, talks) in enumerate(comp_data):
        row_cells = [comp_tbl.cell(row_idx + 1, i) for i in range(5)]
        bg_col = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        for cell in row_cells:
            set_bg(cell, bg_col)
            set_margins(cell, top=50, bottom=50, left=70, right=70)
            set_subtle_borders(cell)
            
        p0 = row_cells[0].paragraphs[0]
        r0 = p0.add_run(name)
        r0.font.name = "Calibri"
        r0.font.size = Pt(8)
        r0.font.bold = True
        
        p1 = row_cells[1].paragraphs[0]
        r1 = p1.add_run(resp)
        r1.font.name = "Calibri"
        r1.font.size = Pt(8)
        
        p2 = row_cells[2].paragraphs[0]
        r2 = p2.add_run(tech)
        r2.font.name = "Calibri"
        r2.font.size = Pt(8)
        
        p3 = row_cells[3].paragraphs[0]
        r3 = p3.add_run(when)
        r3.font.name = "Calibri"
        r3.font.size = Pt(8)
        
        p4 = row_cells[4].paragraphs[0]
        r4 = p4.add_run(talks)
        r4.font.name = "Calibri"
        r4.font.size = Pt(8)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # 4. MAINTENANCE REMINDER FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------
    add_h1("3. Maintenance Reminder Finite State Machine (FSM)")
    add_p(
        "Preventive vehicle upkeep in Cambodia must balance unpredictable daily mileage (couriers riding 100 km/day vs. students riding 15 km/day). The Maintenance Rules Engine governs component lifecycle through a deterministic 4-state Finite State Machine governed by dual-condition triggers."
    )
    
    add_h2("3.1 Dual-Condition Trigger Formula")
    add_p(
        "Service due dates are evaluated on whichever occurs first between cumulative distance and calendar duration:",
        bold_prefix="Core Formula: "
    )
    add_p(
        "Composite Wear Ratio (ρ) = MAX( ΔKm / TargetKm, ΔDays / TargetDays )\n\n"
        "Where:\n"
        "• ΔKm = Current_Odometer - Last_Serviced_Odometer\n"
        "• ΔDays = Current_Date - Last_Serviced_Date\n"
        "• TargetKm = Base_Interval_Km * Wear_Multiplier\n"
        "• TargetDays = Base_Interval_Days * Wear_Multiplier",
        space_after=4
    )

    add_h2("3.2 State Transition Flowchart")
    fsm_ascii = (
        "       +--------------------------------------------------------------+\n"
        "       |                     [*] VEHICLE CREATED                      |\n"
        "       +------------------------------+-------------------------------+\n"
        "                                      | Default configs bound\n"
        "                                      v\n"
        "       +--------------------------------------------------------------+\n"
        "       |                      UPCOMING (🟢 Green)                     |\n"
        "       |  - Healthy operating condition (ρ < 0.80)                    |\n"
        "       |  - Over 20% distance remaining AND over 7 days remaining      |\n"
        "       +------------------------------+-------------------------------+\n"
        "                                      |\n"
        "                  Remaining distance <= 20% OR remaining days <= 7 days\n"
        "                                      v\n"
        "       +--------------------------------------------------------------+\n"
        "       |                      DUE SOON (🟡 Yellow)                    |\n"
        "       |  - Warning threshold reached (0.80 <= ρ < 1.00)              |\n"
        "       |  - Scheduled push alert dispatches to notification tray      |\n"
        "       +------------------------------+-------------------------------+\n"
        "                                      |\n"
        "                    Current Km >= Next Due Km OR Date >= Next Due Date\n"
        "                                      v\n"
        "       +--------------------------------------------------------------+\n"
        "       |                      OVERDUE (🔴 Red)                        |\n"
        "       |  - Target interval exceeded (ρ >= 1.00)                      |\n"
        "       |  - High-contrast alert badge; immediate action required      |\n"
        "       +------------------------------+-------------------------------+\n"
        "                                      |\n"
        "                User completes maintenance at roadside stall\n"
        "                and taps '+ កត់ត្រាការជួសជុល (Log Service)'\n"
        "                                      v\n"
        "       +--------------------------------------------------------------+\n"
        "       |                     SERVICED (🔵 Reset)                      |\n"
        "       |  - Immutable service log recorded in PostgreSQL & SQLite     |\n"
        "       |  - Last serviced baseline resets: km = current, date = today  |\n"
        "       +------------------------------+-------------------------------+\n"
        "                                      |\n"
        "                                      +----> Returns to UPCOMING (🟢)\n"
    )
    add_code_block(fsm_ascii)

    # State Table
    state_tbl_data = [
        ("UPCOMING", "🟢 Green", "ρ < 0.80", "Component operating normally. Mileage burn rate tracked quietly in background."),
        ("DUE SOON", "🟡 Amber/Yellow", "0.80 ≤ ρ < 1.00", "Within 20% of limit or ≤ 7 calendar days remaining. First push alert triggered."),
        ("OVERDUE", "🔴 Red", "ρ ≥ 1.00", "Target mileage or calendar duration exceeded. Critical dashboard warning shown."),
        ("SERVICED", "🔵 Blue / Reset", "Service Log Saved", "Resets baseline counters (last_serviced_km & date). Transitions immediately to Green.")
    ]
    
    st_tbl = doc.add_table(rows=len(state_tbl_data) + 1, cols=4)
    st_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    st_tbl.autofit = False
    st_tbl.columns[0].width = Inches(1.2)
    st_tbl.columns[1].width = Inches(1.2)
    st_tbl.columns[2].width = Inches(1.5)
    st_tbl.columns[3].width = Inches(2.6)
    
    headers_st = ["State", "UI Indicator", "Trigger Threshold", "System Action & Behavior"]
    for i, h in enumerate(headers_st):
        c = st_tbl.cell(0, i)
        set_bg(c, HEX_PRIMARY)
        set_margins(c, top=60, bottom=60, left=70, right=70)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (st, ui, tr, act) in enumerate(state_tbl_data):
        row_cells = [st_tbl.cell(row_idx + 1, i) for i in range(4)]
        bg_col = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        for cell in row_cells:
            set_bg(cell, bg_col)
            set_margins(cell, top=50, bottom=50, left=70, right=70)
            set_subtle_borders(cell)
            
        p0 = row_cells[0].paragraphs[0]
        r0 = p0.add_run(st)
        r0.font.name = "Calibri"
        r0.font.size = Pt(8.5)
        r0.font.bold = True
        
        p1 = row_cells[1].paragraphs[0]
        r1 = p1.add_run(ui)
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.5)
        
        p2 = row_cells[2].paragraphs[0]
        r2 = p2.add_run(tr)
        r2.font.name = "Calibri"
        r2.font.size = Pt(8.5)
        
        p3 = row_cells[3].paragraphs[0]
        r3 = p3.add_run(act)
        r3.font.name = "Calibri"
        r3.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # 5. RELATIONAL ENTITY-RELATIONSHIP DIAGRAM (ERD)
    # -------------------------------------------------------------
    add_h1("4. Relational Entity-Relationship Diagram (ERD)")
    add_p(
        "The relational database schema is structured across 10 specialized tables in PostgreSQL 16. The design guarantees full third normal form (3NF) compliance, strict foreign key referential integrity with cascading rules, and integer storage for currency values to prevent floating-point rounding errors."
    )
    
    add_h2("4.1 Visual Entity-Relationship Map")
    erd_ascii = (
        "  +-----------------+           +--------------------+           +-----------------+\n"
        "  |      USERS      | 1       N |      VEHICLES      | N       1 | VEHICLE_MODELS  |\n"
        "  |-----------------|-----------|--------------------|-----------|-----------------|\n"
        "  | id (PK)         |           | id (PK)            |           | id (PK)         |\n"
        "  | phone (UK)      |           | user_id (FK)       |           | vehicle_type    |\n"
        "  | full_name       |           | vehicle_model_id(FK|           | make, model     |\n"
        "  | language_pref   |           | license_plate      |           | year_start, end |\n"
        "  +--------+--------+           | current_odometer   |           +--------+--------+\n"
        "           |                    +--------+-----------+                    | 1\n"
        "           | 1                           | 1                              |\n"
        "           |                             |                                | N\n"
        "           | N                           | N                     +--------v--------+\n"
        "  +--------v--------+           +--------v-----------+           | MODEL_COMPONENT |\n"
        "  |     GARAGES     | 1       N |   REMINDER_RULES   | N       1 |     CONFIGS     |\n"
        "  |-----------------|-----------|--------------------|-----------|-----------------|\n"
        "  | id (PK)         |           | id (PK)            |           | id (PK)         |\n"
        "  | user_id (FK)    |           | vehicle_id (FK)    |           | vehicle_model(FK|\n"
        "  | name, phone     |           | component_id (FK)  |           | component_id(FK)|\n"
        "  | lat, lng        |           | interval_km, days  |           | default_int_km  |\n"
        "  | is_verified     |           | last_serviced_date |           | default_int_days|\n"
        "  +--------+--------+           | next_due_km, date  |           | wear_multiplier |\n"
        "           | 1                  | status (R/Y/G)     |           +--------+--------+\n"
        "           |                    +--------------------+                    | N\n"
        "           | N                                                            | 1\n"
        "  +--------v--------+ 1       N +--------------------+ N       1 +--------v--------+\n"
        "  |  SERVICE_LOGS   |-----------| SERVICE_LOG_ITEMS  |-----------|   COMPONENTS    |\n"
        "  |-----------------|           |--------------------|           |-----------------|\n"
        "  | id (PK)         |           | id (PK)            |           | id (PK)         |\n"
        "  | vehicle_id (FK) |           | service_log_id (FK)|           | code (UK)       |\n"
        "  | garage_id (FK)  |           | component_id (FK)  |           | name_en         |\n"
        "  | odometer_km     |           | cost_cents (int)   |           | name_km (slang) |\n"
        "  | total_cost_cents|           | notes              |           | category        |\n"
        "  | invoice_photo   |           +--------------------+           +-----------------+\n"
        "  +-----------------+\n"
    )
    add_code_block(erd_ascii)

    add_h2("4.2 The 10 Core Entities Overview")
    entities_summary = [
        ("users", "User accounts, authentication identity, and language preferences ('km' or 'en').", "1:N with vehicles, 1:N with user-pinned garages."),
        ("vehicle_models", "Model-agnostic vehicle definitions (e.g. Honda Scoopy, Honda Dream 125, Toyota Prius).", "1:N with vehicles, 1:N with model_component_configs."),
        ("components", "Standard maintenance parts catalog featuring authentic Khmer mechanic slang names.", "1:N with model_component_configs, 1:N with reminder_rules."),
        ("model_component_configs", "Dynamic interval configurations (km, days, wear multipliers) per model without code changes.", "Links vehicle_models to components (N:M bridge)."),
        ("vehicles", "Physical assets registered by users, tracking active license plates and current odometers.", "Belongs to user and vehicle_model; has many service logs."),
        ("reminder_rules", "Per-vehicle active reminder instances tracking last serviced metrics and R/Y/G status.", "Governed by vehicle and component; evaluated by rules engine."),
        ("garages", "Pre-seeded Google Places garages and user-pinned neighborhood roadside mechanic stalls.", "1:N with service_logs (tracks where service took place)."),
        ("service_logs", "Immutable historical maintenance events containing odometer, date, total cost, and photos.", "Parent header for service visits; contains itemized lines."),
        ("service_log_items", "Itemized line items detailing specific parts replaced, individual costs, and fluid grades.", "Child lines of service_logs; references components."),
        ("odometer_histories", "Time-series log of verified odometer updates from manual inputs and service visits.", "Child audit log of vehicles for mileage burn-rate modeling.")
    ]

    ent_tbl = doc.add_table(rows=len(entities_summary) + 1, cols=3)
    ent_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    ent_tbl.autofit = False
    ent_tbl.columns[0].width = Inches(1.8)
    ent_tbl.columns[1].width = Inches(2.7)
    ent_tbl.columns[2].width = Inches(2.0)
    
    headers_en = ["Entity Name", "Role & Domain Purpose", "Key Cardinality Relationships"]
    for i, h in enumerate(headers_en):
        c = ent_tbl.cell(0, i)
        set_bg(c, HEX_PRIMARY)
        set_margins(c, top=60, bottom=60, left=70, right=70)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (en, purp, rel) in enumerate(entities_summary):
        row_cells = [ent_tbl.cell(row_idx + 1, i) for i in range(3)]
        bg_col = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        for cell in row_cells:
            set_bg(cell, bg_col)
            set_margins(cell, top=50, bottom=50, left=70, right=70)
            set_subtle_borders(cell)
            
        p0 = row_cells[0].paragraphs[0]
        r0 = p0.add_run(en)
        r0.font.name = "Consolas"
        r0.font.size = Pt(8.5)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_PRIMARY
        
        p1 = row_cells[1].paragraphs[0]
        r1 = p1.add_run(purp)
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.5)
        
        p2 = row_cells[2].paragraphs[0]
        r2 = p2.add_run(rel)
        r2.font.name = "Calibri"
        r2.font.size = Pt(8)
        r2.font.color.rgb = COLOR_MUTED

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # 6. COMPLETE PRODUCTION DATA DICTIONARY
    # -------------------------------------------------------------
    add_h1("5. Comprehensive Production Data Dictionary")
    add_p(
        "Below is the exact schema specification for all 10 tables implemented in PostgreSQL 16, detailing column names, data types, constraints, nullability, and foreign key ON DELETE rules."
    )

    dict_tables = [
        ("Table 1: users (User Accounts & Authentication)", [
            ("id", "uuid", "PRIMARY KEY, DEFAULT gen_random_uuid()", "No", "Unique user identifier"),
            ("phone", "varchar(20)", "UNIQUE", "No", "Cambodian phone number (+855...)"),
            ("full_name", "varchar(100)", "None", "No", "User full name"),
            ("language_preference", "varchar(10)", "DEFAULT 'km', CHECK in ('km', 'en')", "No", "App language preference"),
            ("created_at", "timestamptz", "DEFAULT now()", "No", "Record creation timestamp"),
            ("updated_at", "timestamptz", "DEFAULT now()", "No", "Last update timestamp")
        ]),
        ("Table 2: vehicle_models (Model Catalog & Classifications)", [
            ("id", "uuid", "PRIMARY KEY, DEFAULT gen_random_uuid()", "No", "Unique model identifier"),
            ("vehicle_type", "varchar(20)", "CHECK in ('scooter', 'motorcycle', 'car')", "No", "Vehicle category"),
            ("make", "varchar(50)", "None", "No", "Manufacturer (e.g. Honda, Toyota)"),
            ("model", "varchar(50)", "None", "No", "Model name (e.g. Scoopy, Prius)"),
            ("year_start", "integer", "CHECK (year_start >= 1990)", "No", "Production start year"),
            ("year_end", "integer", "None", "Yes", "Production end year (null if active)"),
            ("created_at", "timestamptz", "DEFAULT now()", "No", "Creation timestamp"),
            ("updated_at", "timestamptz", "DEFAULT now()", "No", "Last update timestamp")
        ]),
        ("Table 3: components (Standard Parts with Authentic Khmer Slang)", [
            ("id", "uuid", "PRIMARY KEY, DEFAULT gen_random_uuid()", "No", "Unique component identifier"),
            ("code", "varchar(50)", "UNIQUE", "No", "System code (e.g. ENGINE_OIL)"),
            ("name_en", "varchar(100)", "None", "No", "English technical name"),
            ("name_km", "varchar(100)", "None", "No", "Authentic Khmer slang (ប្រេងម៉ាស៊ីន)"),
            ("category", "varchar(50)", "CHECK in ('lubricant','transmission','ignition','braking','cooling')", "No", "Domain category"),
            ("created_at", "timestamptz", "DEFAULT now()", "No", "Creation timestamp"),
            ("updated_at", "timestamptz", "DEFAULT now()", "No", "Last update timestamp")
        ]),
        ("Table 4: model_component_configs (Dynamic Interval Configuration Matrix)", [
            ("id", "uuid", "PRIMARY KEY, DEFAULT gen_random_uuid()", "No", "Unique config identifier"),
            ("vehicle_model_id", "uuid", "FK -> vehicle_models.id ON DELETE CASCADE", "No", "Target model"),
            ("component_id", "uuid", "FK -> components.id ON DELETE CASCADE", "No", "Configured component"),
            ("default_interval_km", "integer", "CHECK (default_interval_km > 0)", "No", "Base interval in km"),
            ("default_interval_days", "integer", "CHECK (default_interval_days > 0)", "No", "Base interval in calendar days"),
            ("wear_multiplier", "numeric(3,2)", "DEFAULT 1.00, CHECK (wear_multiplier > 0)", "No", "Wear factor multiplier"),
            ("is_active", "boolean", "DEFAULT true", "No", "Active configuration flag"),
            ("created_at", "timestamptz", "DEFAULT now()", "No", "Creation timestamp"),
            ("updated_at", "timestamptz", "DEFAULT now()", "No", "Last update timestamp")
        ]),
        ("Table 5: vehicles (Registered Assets & Odometer Readings)", [
            ("id", "uuid", "PRIMARY KEY, DEFAULT gen_random_uuid()", "No", "Unique vehicle identifier"),
            ("user_id", "uuid", "FK -> users.id ON DELETE CASCADE", "No", "Owner user account"),
            ("vehicle_model_id", "uuid", "FK -> vehicle_models.id ON DELETE RESTRICT", "No", "Associated model profile"),
            ("license_plate", "varchar(20)", "None", "Yes", "Cambodian plate (e.g. 1JJ-8888)"),
            ("current_odometer", "integer", "DEFAULT 0, CHECK (current_odometer >= 0)", "No", "Latest verified odometer (km)"),
            ("created_at", "timestamptz", "DEFAULT now()", "No", "Creation timestamp"),
            ("updated_at", "timestamptz", "DEFAULT now()", "No", "Last update timestamp")
        ]),
        ("Table 6: reminder_rules (Active Reminders & Health State)", [
            ("id", "uuid", "PRIMARY KEY, DEFAULT gen_random_uuid()", "No", "Unique reminder rule ID"),
            ("vehicle_id", "uuid", "FK -> vehicles.id ON DELETE CASCADE", "No", "Target vehicle"),
            ("component_id", "uuid", "FK -> components.id ON DELETE RESTRICT", "No", "Monitored component"),
            ("interval_km", "integer", "CHECK (interval_km > 0)", "No", "Effective distance trigger"),
            ("interval_days", "integer", "CHECK (interval_days > 0)", "No", "Effective time trigger"),
            ("last_serviced_odometer", "integer", "DEFAULT 0", "No", "Odometer at last service"),
            ("last_serviced_date", "date", "DEFAULT CURRENT_DATE", "No", "Date of last service"),
            ("next_due_odometer", "integer", "CHECK (next_due_odometer >= last_serviced_odometer)", "No", "Target due km"),
            ("next_due_date", "date", "None", "No", "Target due date"),
            ("status", "varchar(20)", "CHECK in ('upcoming', 'due_soon', 'overdue', 'serviced')", "No", "Current health state"),
            ("is_active", "boolean", "DEFAULT true", "No", "Active monitoring flag"),
            ("created_at", "timestamptz", "DEFAULT now()", "No", "Creation timestamp"),
            ("updated_at", "timestamptz", "DEFAULT now()", "No", "Last update timestamp")
        ]),
        ("Table 7: garages (Pre-Seeded & Pinned Roadside Garages)", [
            ("id", "uuid", "PRIMARY KEY, DEFAULT gen_random_uuid()", "No", "Unique garage identifier"),
            ("user_id", "uuid", "FK -> users.id ON DELETE SET NULL", "Yes", "Pinning user (null if pre-seeded)"),
            ("name", "varchar(150)", "None", "No", "Shop name (e.g. ជាង រិទ្ធ ម៉ូតូ)"),
            ("phone", "varchar(20)", "None", "Yes", "Mechanic phone number"),
            ("address", "varchar(255)", "None", "Yes", "Street address or landmark"),
            ("latitude", "numeric(10,7)", "CHECK (latitude BETWEEN -90 AND 90)", "No", "WGS84 GPS latitude"),
            ("longitude", "numeric(10,7)", "CHECK (longitude BETWEEN -180 AND 180)", "No", "WGS84 GPS longitude"),
            ("is_verified", "boolean", "DEFAULT false", "No", "Google Places verified flag"),
            ("created_at", "timestamptz", "DEFAULT now()", "No", "Creation timestamp"),
            ("updated_at", "timestamptz", "DEFAULT now()", "No", "Last update timestamp")
        ]),
        ("Table 8: service_logs (Completed Maintenance Event Headers)", [
            ("id", "uuid", "PRIMARY KEY, DEFAULT gen_random_uuid()", "No", "Unique log identifier"),
            ("vehicle_id", "uuid", "FK -> vehicles.id ON DELETE CASCADE", "No", "Serviced vehicle"),
            ("garage_id", "uuid", "FK -> garages.id ON DELETE SET NULL", "Yes", "Garage location"),
            ("service_date", "date", "DEFAULT CURRENT_DATE", "No", "Service execution date"),
            ("odometer_km", "integer", "CHECK (odometer_km >= 0)", "No", "Odometer during service"),
            ("total_cost_cents", "integer", "DEFAULT 0, CHECK (total_cost_cents >= 0)", "No", "Total cost in cents ($5.00 = 500)"),
            ("currency", "varchar(3)", "DEFAULT 'USD', CHECK in ('USD', 'KHR')", "No", "Payment currency"),
            ("notes", "text", "None", "Yes", "Mechanic remarks or oil brand"),
            ("invoice_photo_url", "varchar(500)", "None", "Yes", "URL of receipt or oil label photo"),
            ("created_at", "timestamptz", "DEFAULT now()", "No", "Creation timestamp"),
            ("updated_at", "timestamptz", "DEFAULT now()", "No", "Last update timestamp")
        ]),
        ("Table 9: service_log_items (Itemized Service Lines)", [
            ("id", "uuid", "PRIMARY KEY, DEFAULT gen_random_uuid()", "No", "Unique line item identifier"),
            ("service_log_id", "uuid", "FK -> service_logs.id ON DELETE CASCADE", "No", "Parent service log"),
            ("component_id", "uuid", "FK -> components.id ON DELETE RESTRICT", "No", "Replaced component"),
            ("cost_cents", "integer", "DEFAULT 0, CHECK (cost_cents >= 0)", "No", "Item parts cost in cents"),
            ("notes", "text", "None", "Yes", "Item notes (e.g. 10W-40 Motul)"),
            ("created_at", "timestamptz", "DEFAULT now()", "No", "Creation timestamp"),
            ("updated_at", "timestamptz", "DEFAULT now()", "No", "Last update timestamp")
        ]),
        ("Table 10: odometer_histories (Time-Series Mileage Audit Trail)", [
            ("id", "uuid", "PRIMARY KEY, DEFAULT gen_random_uuid()", "No", "Unique entry identifier"),
            ("vehicle_id", "uuid", "FK -> vehicles.id ON DELETE CASCADE", "No", "Target vehicle"),
            ("odometer_km", "integer", "CHECK (odometer_km >= 0)", "No", "Recorded mileage"),
            ("recorded_at", "timestamptz", "DEFAULT now()", "No", "Timestamp of observation"),
            ("source", "varchar(20)", "CHECK in ('manual', 'service_log', 'garage_dwell')", "No", "Data capture source"),
            ("created_at", "timestamptz", "DEFAULT now()", "No", "Creation timestamp"),
            ("updated_at", "timestamptz", "DEFAULT now()", "No", "Last update timestamp")
        ])
    ]

    for tbl_title, cols in dict_tables:
        add_h2(tbl_title)
        d_tbl = doc.add_table(rows=len(cols) + 1, cols=5)
        d_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        d_tbl.autofit = False
        d_tbl.columns[0].width = Inches(1.4)
        d_tbl.columns[1].width = Inches(1.1)
        d_tbl.columns[2].width = Inches(1.8)
        d_tbl.columns[3].width = Inches(0.6)
        d_tbl.columns[4].width = Inches(1.6)
        
        headers_dt = ["Column", "Data Type", "Constraints", "Nullable", "Description"]
        for i, h in enumerate(headers_dt):
            c = d_tbl.cell(0, i)
            set_bg(c, HEX_PRIMARY)
            set_margins(c, top=50, bottom=50, left=60, right=60)
            p = c.paragraphs[0]
            r = p.add_run(h)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        for row_idx, (col, dtype, constr, nullb, desc) in enumerate(cols):
            row_cells = [d_tbl.cell(row_idx + 1, i) for i in range(5)]
            bg_col = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
            for cell in row_cells:
                set_bg(cell, bg_col)
                set_margins(cell, top=40, bottom=40, left=60, right=60)
                set_subtle_borders(cell)
                
            p0 = row_cells[0].paragraphs[0]
            r0 = p0.add_run(col)
            r0.font.name = "Consolas"
            r0.font.size = Pt(8)
            r0.font.bold = True
            
            p1 = row_cells[1].paragraphs[0]
            r1 = p1.add_run(dtype)
            r1.font.name = "Consolas"
            r1.font.size = Pt(8)
            
            p2 = row_cells[2].paragraphs[0]
            r2 = p2.add_run(constr)
            r2.font.name = "Calibri"
            r2.font.size = Pt(8)
            
            p3 = row_cells[3].paragraphs[0]
            r3 = p3.add_run(nullb)
            r3.font.name = "Calibri"
            r3.font.size = Pt(8)
            
            p4 = row_cells[4].paragraphs[0]
            r4 = p4.add_run(desc)
            r4.font.name = "Calibri"
            r4.font.size = Pt(8)

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # 7. END-TO-END SYSTEM FLOW TRACE (UJ-02)
    # -------------------------------------------------------------
    add_h1("6. End-to-End System Flow Trace")
    add_p(
        "To verify interaction across client, offline database, network gateway, domain logic, and persistent storage, the flow below traces UJ-02 (Rapid 1-Tap Service Logging) from physical tap to UI Green state confirmation."
    )

    trace_steps = [
        ("1. User Tap & Input", "Client App (UI)", "Davy taps '+ កត់ត្រាការជួសជុល', selects preset 'ប្រេងម៉ាស៊ីន (Engine Oil)', confirms current odometer 13,500 km, cost $5.00, and taps 'រក្សាទុក'."),
        ("2. Request Dispatch", "Client Network Layer", "Flutter app compiles JSON payload and dispatches POST /api/v1/vehicles/:vehicleId/services with header Authorization: Bearer <jwt_token>."),
        ("3. Auth & Sanitization", "Backend Middleware", "JWT middleware authenticates user; Zod schema verifies odometer > previous (12,450 km) and cost >= 0. (Blocks with 400 or 403 on failure)."),
        ("4. Database Transaction", "Backend Controller", "Executes SQL transaction: inserts into service_logs (total_cost_cents=500, odometer_km=13500) and links service_log_items for Engine Oil."),
        ("5. Rules Re-Evaluation", "Rules Engine", "Locates reminder_rules for Engine Oil; updates last_serviced_odometer=13500, last_serviced_date=NOW, and recalculates status='upcoming'. Commits transaction."),
        ("6. Client Confirmation", "Client App & SQLite", "API responds 201 Created with updated health summary. Client updates local Drift SQLite cache, turns status card Green (1,500 km remaining), and displays success snackbar.")
    ]

    tr_tbl = doc.add_table(rows=len(trace_steps) + 1, cols=3)
    tr_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tr_tbl.autofit = False
    tr_tbl.columns[0].width = Inches(1.5)
    tr_tbl.columns[1].width = Inches(1.6)
    tr_tbl.columns[2].width = Inches(3.4)
    
    headers_tr = ["Execution Step", "System Layer", "Architectural Action & State Mutation"]
    for i, h in enumerate(headers_tr):
        c = tr_tbl.cell(0, i)
        set_bg(c, HEX_PRIMARY)
        set_margins(c, top=60, bottom=60, left=70, right=70)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (stp, lyr, actn) in enumerate(trace_steps):
        row_cells = [tr_tbl.cell(row_idx + 1, i) for i in range(3)]
        bg_col = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        for cell in row_cells:
            set_bg(cell, bg_col)
            set_margins(cell, top=50, bottom=50, left=70, right=70)
            set_subtle_borders(cell)
            
        p0 = row_cells[0].paragraphs[0]
        r0 = p0.add_run(stp)
        r0.font.name = "Calibri"
        r0.font.size = Pt(8.5)
        r0.font.bold = True
        
        p1 = row_cells[1].paragraphs[0]
        r1 = p1.add_run(lyr)
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.5)
        
        p2 = row_cells[2].paragraphs[0]
        r2 = p2.add_run(actn)
        r2.font.name = "Calibri"
        r2.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # 8. REST API CONTRACT SPECIFICATIONS (EP-01 TO EP-08)
    # -------------------------------------------------------------
    add_h1("7. REST API Contracts & Test Collection")
    add_p(
        "The backend REST API adheres strictly to capstone blueprint conventions: local base URL http://localhost:8000, routes prefixed with /api/v1, JSON request/response payloads, and standard Bearer token authorization."
    )

    api_endpoints = [
        ("EP-01", "GET", "/api/v1/health", "System health check and uptime probe", "No", "status 200; status equals 'ok'"),
        ("EP-02", "POST", "/api/v1/vehicles", "Create vehicle profile and bind default configs", "Yes", "status 201; bound_reminders_count >= 1"),
        ("EP-03", "GET", "/api/v1/vehicles", "List user vehicles with health status summaries", "Yes", "status 200; health_summary.status exists"),
        ("EP-04", "PATCH", "/api/v1/vehicles/:id/odometer", "Update vehicle odometer & re-evaluate rules", "Yes", "status 200; current_odometer updated"),
        ("EP-05", "GET", "/api/v1/vehicles/:id/reminders", "Get active component reminders & R/Y/G status", "Yes", "status 200; contains name_km & status"),
        ("EP-06", "POST", "/api/v1/vehicles/:id/services", "Log service event & reset reminder counters", "Yes", "status 201; reset_reminders array returned"),
        ("EP-07", "GET", "/api/v1/vehicles/:id/services", "Retrieve paginated historical service logs", "Yes", "status 200; total_cost_cents is integer"),
        ("EP-08", "POST", "/api/v1/garages", "Pin & register neighborhood roadside mechanic", "Yes", "status 201; garage created with valid UUID")
    ]

    api_tbl = doc.add_table(rows=len(api_endpoints) + 1, cols=6)
    api_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    api_tbl.autofit = False
    api_tbl.columns[0].width = Inches(0.6)
    api_tbl.columns[1].width = Inches(0.7)
    api_tbl.columns[2].width = Inches(1.9)
    api_tbl.columns[3].width = Inches(1.7)
    api_tbl.columns[4].width = Inches(0.6)
    api_tbl.columns[5].width = Inches(1.0)
    
    headers_api = ["ID", "Method", "Endpoint Route", "Description", "Auth", "Test Assertion"]
    for i, h in enumerate(headers_api):
        c = api_tbl.cell(0, i)
        set_bg(c, HEX_PRIMARY)
        set_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(8)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (epid, meth, route, desc, auth, tst) in enumerate(api_endpoints):
        row_cells = [api_tbl.cell(row_idx + 1, i) for i in range(6)]
        bg_col = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        for cell in row_cells:
            set_bg(cell, bg_col)
            set_margins(cell, top=50, bottom=50, left=60, right=60)
            set_subtle_borders(cell)
            
        p0 = row_cells[0].paragraphs[0]
        r0 = p0.add_run(epid)
        r0.font.name = "Calibri"
        r0.font.size = Pt(8)
        r0.font.bold = True
        
        p1 = row_cells[1].paragraphs[0]
        r1 = p1.add_run(meth)
        r1.font.name = "Consolas"
        r1.font.size = Pt(8)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(0x06, 0x5F, 0x46) if meth == "GET" else RGBColor(0x1E, 0x40, 0xAF)
        
        p2 = row_cells[2].paragraphs[0]
        r2 = p2.add_run(route)
        r2.font.name = "Consolas"
        r2.font.size = Pt(7.5)
        
        p3 = row_cells[3].paragraphs[0]
        r3 = p3.add_run(desc)
        r3.font.name = "Calibri"
        r3.font.size = Pt(8)
        
        p4 = row_cells[4].paragraphs[0]
        r4 = p4.add_run(auth)
        r4.font.name = "Calibri"
        r4.font.size = Pt(8)
        
        p5 = row_cells[5].paragraphs[0]
        r5 = p5.add_run(tst)
        r5.font.name = "Calibri"
        r5.font.size = Pt(7.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 9. CONCLUSION & TRANSITION TO PHASE 4
    # -------------------------------------------------------------
    add_h1("8. Sign-Off & Transition to Phase 4 (Figma Design)")
    add_p(
        "With the completion and advisor approval of Phase 3 (Data Modeling & System Architecture), the core schema, state machine, and API contracts are formally frozen. The project is completely unblocked to begin Phase 4 (UI/UX & Figma Design), where screens, navigation flows, and interactive prototypes will be crafted strictly against these verified architectural entities."
    )

    doc.save(output_path)
    print(f"Week 3 Word Document successfully generated: {output_path}")

if __name__ == "__main__":
    out_file = os.path.abspath("d:/PPS1Y4/MotoCare_Cambodia_Week_3_Data_Modeling_System_Architecture.docx")
    build_week3_doc(out_file)
