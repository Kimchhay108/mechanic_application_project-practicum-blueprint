import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_scope_doc(output_path):
    doc = docx.Document()
    
    # Page Setup: Standard Letter, 1-inch margins
    sections = doc.sections
    for section in sections:
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
        r_ft = p_ft.add_run("MotoCare Cambodia — Project Scope Specification | Page ")
        r_ft.font.name = "Calibri"
        r_ft.font.size = Pt(8.5)
        r_ft.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)

    # Styling Palette
    COLOR_PRIMARY = RGBColor(0x1E, 0x3A, 0x8A)      # Deep Navy Blue
    COLOR_SECONDARY = RGBColor(0x25, 0x63, 0xEB)    # Royal Blue
    COLOR_DARK = RGBColor(0x1F, 0x29, 0x37)         # Charcoal Black (Body)
    COLOR_MUTED = RGBColor(0x4B, 0x55, 0x63)        # Muted Gray
    HEX_PRIMARY = "1E3A8A"
    HEX_SECONDARY = "2563EB"
    HEX_LIGHT_BG = "F8FAFC"
    HEX_CALLOUT_BG = "EFF6FF"
    HEX_BORDER = "CBD5E1"
    
    # Helper: Set Cell Margins
    def set_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    # Helper: Cell Background
    def set_bg(cell, hex_color):
        shading_xml = f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'
        cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

    # Helper: Subtle Border
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

    # Helper: Add Styled Heading 1
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

    # Helper: Add Styled Heading 2
    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    # Helper: Add Styled Heading 3
    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = COLOR_DARK
        return p

    # Helper: Add Paragraph
    def add_p(text, bold_prefix=None, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.font.name = "Calibri"
            r_b.font.size = Pt(10)
            r_b.font.bold = True
            r_b.font.color.rgb = COLOR_DARK
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_DARK
        return p

    # Helper: Callout Box
    def add_callout_box(title, text, hex_bg="EFF6FF", hex_border="2563EB"):
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
        r_t = cp.add_run(f"{title}\n")
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(10)
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_PRIMARY
        
        r_b = cp.add_run(text)
        r_b.font.name = "Calibri"
        r_b.font.size = Pt(9.5)
        r_b.font.color.rgb = COLOR_DARK
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
    r_sub = p_sub.add_run("Intelligent Vehicle Maintenance Tracker — Project Scope Specification (Phase 2)")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = COLOR_SECONDARY

    # Metadata Table
    meta_tbl = doc.add_table(rows=5, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_tbl.autofit = False
    meta_tbl.columns[0].width = Inches(1.8)
    meta_tbl.columns[1].width = Inches(4.7)
    
    meta_data = [
        ("Student & Author", "Thoeurn Kimchhay (ធឿន គីមឆាយ) — Bachelor of Computer Science"),
        ("Institution & Course", "Royal University of Phnom Penh (RUPP) — PPS1Y4 Capstone"),
        ("Project Advisor", "Hang Sopheak"),
        ("Deliverable Baseline", "Phase 2 (MoSCoW Matrix, Maintenance Rules Engine & User Journeys)"),
        ("Project Repository", "github.com/Kimchhay108/mechanic_application_project-practicum-blueprint")
    ]
    
    for row_idx, (k, v) in enumerate(meta_data):
        c0 = meta_tbl.cell(row_idx, 0)
        c1 = meta_tbl.cell(row_idx, 1)
        set_bg(c0, "F1F5F9")
        set_bg(c1, "FFFFFF")
        set_margins(c0, top=60, bottom=60, left=100, right=100)
        set_margins(c1, top=60, bottom=60, left=100, right=100)
        set_subtle_borders(c0, "CBD5E1")
        set_subtle_borders(c1, "CBD5E1")
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k)
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_DARK
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 2. EXECUTIVE SUMMARY & PROBLEM OVERVIEW
    # -------------------------------------------------------------
    add_h1("1. Executive Summary & Problem Overview")
    add_p(
        "In Cambodia, motorcycles and scooters represent over 85% of registered private transportation (notably Honda Dream 125, Honda Scoopy, and Honda Click), operating alongside a dense urban fleet of Japanese hybrid cars (such as the Toyota Prius 2nd/3rd generation). Commuters face extreme tropical heat, stop-and-go congestion, and high dust/flood exposure, accelerating wear on engine oil, CVT drive belts, spark plugs, and brake shoes. However, over 90% of routine maintenance is performed at informal roadside mechanic stalls (ជាងម៉ូតូ) that transact exclusively in cash or KHQR transfers without issuing paper receipts, itemized invoices, or digital records. As a consequence, vehicle owners rely on fading paper fork stickers, blurry handwriting, or fallible human memory, resulting in catastrophic engine seizures and steep economic losses."
    )
    
    add_p(
        "\"Cambodian vehicle owners struggle to maintain regular preventive servicing because informal roadside garages issue no paper or digital records and existing apps ignore local two-wheeler needs, which costs owners expensive catastrophic breakdowns (over $80–$250 in engine repairs), lost daily income, and steep resale value depreciation.\"",
        bold_prefix="Core Problem Statement: "
    )

    add_callout_box(
        "SUPERVISOR FEEDBACK INCORPORATION (WEEK 1 REVIEW)",
        "1. Model-Agnostic Setup: Zero hardcoded vehicle rules in application code; dynamic database table (model_component_configs) links any vehicle profile to component intervals.\n"
        "2. \"At Garage\" Dwell Detection: 15-minute background geofencing near Google Places & user-pinned garages dispatches push alert: \"Looks like you're at a garage. Do you want to log a service?\"\n"
        "3. Persona 3 (The \"Neglectful\" Commuter): \"Davy\" (21, RUPP student, Scoopy) requiring a clean Red/Yellow/Green health status and a 1-tap service logger.\n"
        "4. Authentic Khmer Mechanic Slang: Integrated real Cambodian street vocabulary (ប្រេងម៉ាស៊ីន, ខ្សែពាន, ប៊ូស៊ី, ស្បែកហ្វ្រាំង, ច្រវាក់, ទឹកស្អំ, ជាង).\n"
        "5. Scope Protection: Automated weather and traffic wear multiplier engine is deferred to v2 to preserve MVP focus."
    )

    # -------------------------------------------------------------
    # 3. MOSCOW FEATURE SCOPE MATRIX
    # -------------------------------------------------------------
    add_h1("2. MoSCoW Feature Scope Matrix")
    add_p(
        "To ensure a realistic, defensible scope for the Bachelor Capstone, features are strictly partitioned under the MoSCoW framework. Every feature carries an immutable identifier (F-01 to F-11), a single priority tier, and a direct trace to Phase 1 pain points (PP-01, PP-02, PP-03)."
    )

    # Priority Rules
    rules_tbl = doc.add_table(rows=5, cols=2)
    rules_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    rules_tbl.autofit = False
    rules_tbl.columns[0].width = Inches(1.5)
    rules_tbl.columns[1].width = Inches(5.0)
    
    p_rules = [
        ("Must-Have (Core MVP)", "Without it, the core user journey cannot be demonstrated at the capstone defense. Essential for baseline viability."),
        ("Should-Have (High Value)", "Important, but the app remains usable without it. Built only once all Must-Have features pass automated tests."),
        ("Could-Have (Enhancement)", "Nice-to-have visual polish or non-critical extras. Delivered only if surplus implementation time permits."),
        ("Won't-Have (v1 Excluded)", "Explicitly out of scope for the MVP. Documented as future work in the thesis report.")
    ]
    
    hdr_c0 = rules_tbl.cell(0, 0)
    hdr_c1 = rules_tbl.cell(0, 1)
    set_bg(hdr_c0, HEX_PRIMARY)
    set_bg(hdr_c1, HEX_PRIMARY)
    set_margins(hdr_c0, top=80, bottom=80, left=100, right=100)
    set_margins(hdr_c1, top=80, bottom=80, left=100, right=100)
    
    p = hdr_c0.paragraphs[0]
    r = p.add_run("Priority Tier")
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    
    p = hdr_c1.paragraphs[0]
    r = p.add_run("Capstone Evaluation Rule")
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    
    for idx, (tier, rule) in enumerate(p_rules):
        c0 = rules_tbl.cell(idx + 1, 0)
        c1 = rules_tbl.cell(idx + 1, 1)
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        set_bg(c0, bg)
        set_bg(c1, bg)
        set_margins(c0, top=60, bottom=60, left=100, right=100)
        set_margins(c1, top=60, bottom=60, left=100, right=100)
        set_subtle_borders(c0)
        set_subtle_borders(c1)
        
        p = c0.paragraphs[0]
        r = p.add_run(tier)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = COLOR_DARK
        
        p = c1.paragraphs[0]
        r = p.add_run(rule)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Full MoSCoW Matrix Table
    add_h2("2.1 Detailed Feature Matrix")
    moscow_data = [
        ("F-01", "Multi-Vehicle Profile Management", "Must-Have", "PP-03", "Register multiple scooters, motorcycles, or cars with make, model, year, and starting odometer reading. Foundation of all app journeys."),
        ("F-02", "Dynamic Model-Agnostic Rules Engine", "Must-Have", "PP-02, PP-03", "Database-driven component intervals (model_component_configs) allowing any vehicle profile to link dynamically without hardcoded code changes."),
        ("F-03", "Rapid Service Logging with Khmer Slang", "Must-Have", "PP-01, PP-02", "Enables users to log completed maintenance in <10s using authentic garage slang (ប្រេងម៉ាស៊ីន, ខ្សែពាន, ប៊ូស៊ី, ស្បែកហ្វ្រាំង), parts cost, and odometer."),
        ("F-04", "Dual-Condition Reminder Engine & R/Y/G UI", "Must-Have", "PP-02", "Calculates Upcoming (Green), Due Soon (Yellow), and Overdue (Red) states triggered on whichever occurs first: cumulative mileage or elapsed days."),
        ("F-05", "Roadside Mechanic Pinning & Directory", "Must-Have", "PP-01", "Enables users to pin neighborhood roadside mechanics (ឈ្មោះជាង, លេខទូរស័ព្ទ, ទីតាំង) and query pre-seeded Phnom Penh shops via Google Places API."),
        ("F-06", "\"At-Garage\" 15-Minute Dwell Notification", "Should-Have", "PP-01, PP-02", "Background geofence detects 15+ minute dwell near a garage and fires a push prompt: \"Looks like you're at a garage. Do you want to log a service?\""),
        ("F-07", "Service Photo & Receipt Attachment", "Should-Have", "PP-01", "Allows snapping photos of oil bottle labels, odometer clusters, or handwritten mechanic notes to verify maintenance provenance."),
        ("F-08", "Digital Vehicle Passport & PDF Export", "Should-Have", "PP-01", "Generates a clean, bilingual PDF service passport summarizing all verified maintenance logs to preserve vehicle resale provenance."),
        ("F-09", "Automated Rainy Season & Traffic Multiplier", "Won't-Have", "PP-02", "Deferred to v2 per Advisor Feedback #5; automated live weather/traffic API wear calculations add excessive MVP complexity."),
        ("F-10", "Live Background GPS Route Tracking", "Won't-Have", "PP-02", "Continuous GPS route tracking causes battery drain and phone overheating in Cambodia; periodic odometer prompts are used instead."),
        ("F-11", "In-App Garage Booking & Work Order Pay", "Won't-Have", "PP-01", "Roadside mechanics operate informally without digital appointment systems; cash and external ABA KHQR remain standard.")
    ]

    moscow_tbl = doc.add_table(rows=len(moscow_data) + 1, cols=5)
    moscow_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    moscow_tbl.autofit = False
    moscow_tbl.columns[0].width = Inches(0.6)
    moscow_tbl.columns[1].width = Inches(1.8)
    moscow_tbl.columns[2].width = Inches(1.0)
    moscow_tbl.columns[3].width = Inches(0.8)
    moscow_tbl.columns[4].width = Inches(2.3)
    
    headers = ["ID", "Feature Name", "Priority", "Pain Point", "Architectural Justification"]
    for i, h in enumerate(headers):
        c = moscow_tbl.cell(0, i)
        set_bg(c, HEX_PRIMARY)
        set_margins(c, top=80, bottom=80, left=80, right=80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for row_idx, (f_id, f_name, prio, pp, just) in enumerate(moscow_data):
        row_cells = [moscow_tbl.cell(row_idx + 1, i) for i in range(5)]
        bg_col = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        
        # Priority badge highlight
        prio_color = COLOR_DARK
        if prio == "Must-Have":
            prio_color = RGBColor(0x06, 0x5F, 0x46) # Forest Green
        elif prio == "Should-Have":
            prio_color = RGBColor(0x1E, 0x40, 0xAF) # Royal Blue
        elif prio == "Won't-Have":
            prio_color = RGBColor(0x99, 0x1B, 0x1B) # Crimson Red
            
        for cell in row_cells:
            set_bg(cell, bg_col)
            set_margins(cell, top=60, bottom=60, left=80, right=80)
            set_subtle_borders(cell)
            
        # ID
        p0 = row_cells[0].paragraphs[0]
        r0 = p0.add_run(f_id)
        r0.font.name = "Calibri"
        r0.font.size = Pt(8.5)
        r0.font.bold = True
        
        # Name
        p1 = row_cells[1].paragraphs[0]
        r1 = p1.add_run(f_name)
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        
        # Priority
        p2 = row_cells[2].paragraphs[0]
        r2 = p2.add_run(prio)
        r2.font.name = "Calibri"
        r2.font.size = Pt(8.5)
        r2.font.bold = True
        r2.font.color.rgb = prio_color
        
        # Pain Point
        p3 = row_cells[3].paragraphs[0]
        r3 = p3.add_run(pp)
        r3.font.name = "Calibri"
        r3.font.size = Pt(8.5)
        r3.font.color.rgb = COLOR_MUTED
        
        # Justification
        p4 = row_cells[4].paragraphs[0]
        r4 = p4.add_run(just)
        r4.font.name = "Calibri"
        r4.font.size = Pt(8.5)
        r4.font.color.rgb = COLOR_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 4. MODEL-AGNOSTIC MAINTENANCE RULES ENGINE
    # -------------------------------------------------------------
    add_h1("3. Model-Agnostic Maintenance Rules Engine")
    add_p(
        "A critical flaw in legacy maintenance apps is hardcoding vehicle rules in frontend code (e.g., if vehicle == 'Scoopy' -> oil_interval = 1500). In our architecture, maintenance intervals and cycle attributes are completely model-agnostic and stored dynamically in the PostgreSQL database."
    )
    
    add_h2("3.1 Dynamic Entity Relationship")
    add_p(
        "• vehicles (User's registered asset) -> FK to vehicle_models (e.g. Honda Scoopy 2021).\n"
        "• vehicle_models -> FK to model_component_configs (e.g. interval_km: 1500, interval_days: 90, wear_multiplier: 1.0).\n"
        "• components -> Standardized parts catalog with bilingual slang (e.g. ENGINE_OIL, DRIVE_BELT).\n"
        "• reminder_rules -> Per-vehicle active reminder instances tracking last_serviced_odometer, last_serviced_date, and current R/Y/G status."
    )

    add_h2("3.2 Dual-Condition Reminder Formula")
    add_p(
        "Because urban riders accumulate mileage at unpredictable rates (e.g., couriers ride 100 km/day whereas students ride 15 km/day), reminder triggers are governed by a dual-condition wear formula: whichever threshold occurs first triggers maintenance.",
        bold_prefix="Dual Trigger Logic: "
    )
    add_p(
        "Composite Wear Ratio (ρ) = MAX( ΔKm / TargetKm, ΔDays / TargetDays )\n"
        "Where:\n"
        "• ΔKm = Current_Odometer - Last_Serviced_Odometer\n"
        "• ΔDays = Current_Date - Last_Serviced_Date\n"
        "• TargetKm = Base_Interval_Km * Wear_Multiplier\n"
        "• TargetDays = Base_Interval_Days * Wear_Multiplier",
        space_after=4
    )

    add_h2("3.3 Four-State Health Lifecycle Machine")
    add_p(
        "1. Upcoming (Green): ρ < 0.80 (> 20% distance remaining and > 7 days remaining). Component in healthy operating condition.\n"
        "2. Due Soon (Yellow): 0.80 ≤ ρ < 1.0 (≤ 20% distance remaining or ≤ 7 calendar days remaining). High-priority warning badge shown.\n"
        "3. Overdue (Red): ρ ≥ 1.0 (Distance or days exceeded). Immediate action required to prevent mechanical breakdown.\n"
        "4. Serviced (State Reset): When a service log is saved, baseline counters reset: last_serviced_odometer = current_odometer, last_serviced_date = CURRENT_DATE, returning state to Green."
    )

    # -------------------------------------------------------------
    # 5. AUTHENTIC KHMER MECHANIC SLANG DICTIONARY
    # -------------------------------------------------------------
    add_h1("4. Authentic Khmer Mechanic Slang Dictionary")
    add_p(
        "In direct alignment with Advisor Feedback #4, the application avoids rigid literary Khmer translations and incorporates the actual spoken slang used daily at Cambodian roadside garages (*chang*):"
    )

    slang_data = [
        ("ប្រេងម៉ាស៊ីន", "Preng Masin", "Engine Oil (4T / 10W-40)", "Lubricant", "1,500 – 2,500 km or 90 days"),
        ("ខ្សែពាន", "Ksae Pean", "CVT Drive Belt (Scooter)", "Transmission", "12,000 – 15,000 km or 1 year"),
        ("ប៊ូស៊ី", "Bousi / Bougie", "Spark Plug (Ignition)", "Ignition", "8,000 – 10,000 km or 1 year"),
        ("ស្បែកហ្វ្រាំង", "Sbaek Frang", "Brake Pads / Shoes", "Braking", "8,000 – 12,000 km"),
        ("ច្រវាក់", "Chrawak", "Drive Chain & Sprocket", "Transmission", "2,000 km (Lube) / 15,000 km (Swap)"),
        ("ទឹកស្អំ", "Teuk Sa-om", "Radiator Coolant", "Cooling", "10,000 – 15,000 km or 1 year"),
        ("ជាងម៉ូតូ", "Chang Moto", "Roadside Mechanic Stall", "Entity", "Informal local neighborhood garage")
    ]

    slang_tbl = doc.add_table(rows=len(slang_data) + 1, cols=5)
    slang_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    slang_tbl.autofit = False
    slang_tbl.columns[0].width = Inches(1.4)
    slang_tbl.columns[1].width = Inches(1.3)
    slang_tbl.columns[2].width = Inches(1.5)
    slang_tbl.columns[3].width = Inches(1.0)
    slang_tbl.columns[4].width = Inches(1.3)
    
    headers_sl = ["Khmer Slang", "Phonetic", "English Equivalent", "Category", "Baseline Interval"]
    for i, h in enumerate(headers_sl):
        c = slang_tbl.cell(0, i)
        set_bg(c, HEX_PRIMARY)
        set_margins(c, top=80, bottom=80, left=80, right=80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (km, ph, en, cat, inv) in enumerate(slang_data):
        row_cells = [slang_tbl.cell(row_idx + 1, i) for i in range(5)]
        bg_col = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        for cell in row_cells:
            set_bg(cell, bg_col)
            set_margins(cell, top=60, bottom=60, left=80, right=80)
            set_subtle_borders(cell)
            
        p0 = row_cells[0].paragraphs[0]
        r0 = p0.add_run(km)
        r0.font.name = "Khmer OS Battambang" if "Khmer" in km else "Calibri"
        r0.font.size = Pt(9)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_PRIMARY
        
        p1 = row_cells[1].paragraphs[0]
        r1 = p1.add_run(ph)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9)
        
        p2 = row_cells[2].paragraphs[0]
        r2 = p2.add_run(en)
        r2.font.name = "Calibri"
        r2.font.size = Pt(9)
        r2.font.bold = True
        
        p3 = row_cells[3].paragraphs[0]
        r3 = p3.add_run(cat)
        r3.font.name = "Calibri"
        r3.font.size = Pt(8.5)
        r3.font.color.rgb = COLOR_MUTED
        
        p4 = row_cells[4].paragraphs[0]
        r4 = p4.add_run(inv)
        r4.font.name = "Calibri"
        r4.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 6. AT-GARAGE 15-MINUTE DWELL DETECTION ENGINE
    # -------------------------------------------------------------
    add_h1("5. At-Garage 15-Minute Dwell Geofence Engine")
    add_p(
        "A primary human behavioral obstacle is that vehicle owners simply forget to record maintenance when visiting roadside mechanics. To solve this without requiring user active tracking, MotoCare incorporates passive geofence dwell detection:"
    )
    add_p(
        "• Pre-Seeded & User-Pinned Directory (F-05): Major motorcycle and auto repair shops in Phnom Penh are pre-seeded using Google Places API, while users can tap \"រក្សាទុកទីតាំងជាងម៉ូតូ\" to pin their trusted neighborhood mechanic.\n"
        "• Passive 15-Minute Dwell Condition: When device coordinates remain within 50 meters of a known garage for 15 continuous minutes (900 seconds), the operating system triggers a background wake-event. This suppresses transient traffic stops and red lights.\n"
        "• Actionable Push Prompt (F-06): The device dispatches a high-priority local push notification: \"📍 Looks like you're at a garage. Do you want to log a service?\"\n"
        "• 1-Tap Hand-Off: Tapping the push notification opens the app directly to the Log Service screen pre-filled with the garage name, current date, and estimated odometer, requiring only 1 tap to save."
    )

    # -------------------------------------------------------------
    # 7. TARGET USER PERSONAS
    # -------------------------------------------------------------
    add_h1("6. Target User Personas")
    
    add_h2("Persona 1 (Primary): Davy — The Neglectful Commuter (P-01)")
    add_p(
        "• Profile: 21-year-old undergraduate student at RUPP; commutes 14 km daily on Russian Federation Blvd on a 2021 Honda Scoopy.\n"
        "• Tech Literacy: Medium (uses ABA KHQR, TikTok, Telegram daily; abandons complicated apps).\n"
        "• Pain Points Addressed: PP-01 (paperless garage friction) and PP-02 (silent mechanical degradation).\n"
        "• User Psychology: Non-technical, cannot decipher technical jargon, forgets paper oil stickers, delays servicing until unusual rattling occurs.\n"
        "• Design Solution: Ultra-simple Red / Yellow / Green status dashboard. When service is due, the app shows ONE prominent button: [ ប្តូរប្រេងម៉ាស៊ីន (Change Oil) - ចុចទីនេះពេលដូររួច ]. One tap resets status back to Green."
    )

    add_h2("Persona 2 (Secondary): Sokha — The Heavy Delivery Courier (P-02)")
    add_p(
        "• Profile: 28-year-old delivery rider for Foodpanda/Grab; rides 90–120 km daily across Phnom Penh on a 2020 Honda Dream 125.\n"
        "• Tech Literacy: Medium-Low (uses driver apps, Google Maps, ABA KHQR; requires high contrast and minimal typing).\n"
        "• Pain Points Addressed: PP-01, PP-02, and PP-03 (Western car-app bias).\n"
        "• User Psychology: Maintenance uptime directly impacts daily income. If his chain snaps or engine valve burns out, he loses 3 days of wages ($60) and pays $120 for an engine rebuild.\n"
        "• Design Solution: Rapid 1-tap logging presets with dual USD/KHR currency and weekly proactive odometer check-in reminders."
    )

    # -------------------------------------------------------------
    # 8. CORE USER JOURNEYS (PHASE 2.2)
    # -------------------------------------------------------------
    add_h1("7. Core User Journeys (Phase 2.2 Specification)")
    add_p(
        "The system behavior is defined across 6 end-to-end user journeys written in Given / When / Then form, including both happy and boundary failure paths."
    )

    journeys = [
        ("UJ-01: Vehicle Registration & Rules Binding (F-01, F-02)",
         "Happy Path: Davy selects 'Scooter', Make 'Honda', Model 'Scoopy 2021', and enters current odometer 12,450 km. System automatically binds default configs: Engine Oil (1,500 km / 90 days), Drive Belt (12,000 km / 365 days), and Spark Plug (8,000 km / 365 days) and renders Green cards.\n"
         "Failure Path: Davy inputs negative odometer '-50'. System flags validation error: 'Please enter a valid positive odometer reading' and blocks vehicle creation."),

        ("UJ-02: Rapid 1-Tap Service Logging (F-03, F-04)",
         "Happy Path: Davy finishes an oil change at a roadside stall. She taps '+ កត់ត្រាការជួសជុល', selects preset 'ប្រេងម៉ាស៊ីន', confirms odometer 13,500 km and $5.00 cost, and taps Save. System records immutable log, resets oil reminder to 0 km / 0 days elapsed, and sets status to Green (1,500 km remaining).\n"
         "Failure Path: User enters odometer reading 11,000 km (lower than previous 12,450 km). System shows alert modal: 'Odometer cannot be less than previous record (12,450 km)' and blocks submission."),

        ("UJ-03: 'At-Garage' 15-Minute Dwell Notification (F-05, F-06)",
         "Happy Path: Device remains stationary within 50m of a known garage for 15 minutes. Background geofence fires push notification: 'Looks like you're at a garage. Do you want to log a service?' Davy taps alert; app opens pre-populated with shop name and date for 1-tap confirmation.\n"
         "Failure Path: User sits at an adjacent cafe for 20 minutes and dismisses notification. System suppresses garage notifications for 12 hours without creating empty logs."),

        ("UJ-04: Resolving Overdue Alert via Odometer Update (F-02, F-04)",
         "Happy Path: Sokha updates odometer to 19,850 km after 10 days of heavy delivery riding. Rules engine recalculates: Engine Oil exceeds 1,500 km limit (+150 km overdue) and flips to Red Overdue state. Sokha visits mechanic, logs service, and card returns to Green.\n"
         "Failure Path: User accidentally enters extra zero '198500' km (+180,000 km jump). System displays confirmation safety modal: 'This increases mileage by 180,300 km. Please verify odometer photo'."),

        ("UJ-05: Pinning a Roadside Mechanic & Garage Search (F-05)",
         "Happy Path: Davy discovers an honest local mechanic near campus. She taps 'Pin My Mechanic', inputs name 'ជាង រិទ្ធ ជួសជុលម៉ូតូ', phone '012888999', and confirms GPS pin. Mechanic is saved locally and registered for future 15-min dwell geofence prompts.\n"
         "Failure Path: User searches garages while offline. App loads cached SQLite local garages and displays an offline banner: 'Showing offline saved garages. Connect to internet for live Google Places search.'"),

        ("UJ-06: Digital Vehicle Passport & PDF Maintenance Export (F-07, F-08)",
         "Happy Path: Sokha is selling his Honda Dream 125. He navigates to Vehicle Settings, selects 'Export Digital Passport (PDF)', and generates a bilingual PDF report detailing vehicle specs, total expenditure ($86.50), and chronological verified service logs.\n"
         "Failure Path: New user with 0 service logs taps export. System displays an empty state dialog: 'No service logs found. Complete at least one maintenance log before generating a passport.'")
    ]

    for j_title, j_desc in journeys:
        add_h2(j_title)
        add_p(j_desc, space_after=6)

    # -------------------------------------------------------------
    # 9. REQUIREMENT COVERAGE & TRACEABILITY
    # -------------------------------------------------------------
    add_h1("8. Requirement Coverage & Traceability Matrix")
    add_p(
        "This matrix guarantees that every Must-Have feature is covered by at least one core journey, maps to a verified user pain point, and corresponds to backend database entities."
    )

    trace_data = [
        ("F-01", "Multi-Vehicle Profile Management", "Must-Have", "PP-03", "UJ-01", "vehicles, vehicle_models"),
        ("F-02", "Dynamic Maintenance Rules Engine", "Must-Have", "PP-02, PP-03", "UJ-01, UJ-04", "model_component_configs, reminder_rules"),
        ("F-03", "Rapid Service Logging with Slang", "Must-Have", "PP-01, PP-02", "UJ-02, UJ-03", "service_logs, service_log_items"),
        ("F-04", "Dual-Condition Reminder Engine", "Must-Have", "PP-02", "UJ-02, UJ-04", "reminder_rules, odometer_histories"),
        ("F-05", "Roadside Mechanic Pinning", "Must-Have", "PP-01", "UJ-03, UJ-05", "garages")
    ]

    trace_tbl = doc.add_table(rows=len(trace_data) + 1, cols=6)
    trace_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    trace_tbl.autofit = False
    trace_tbl.columns[0].width = Inches(0.6)
    trace_tbl.columns[1].width = Inches(1.8)
    trace_tbl.columns[2].width = Inches(0.9)
    trace_tbl.columns[3].width = Inches(0.8)
    trace_tbl.columns[4].width = Inches(1.0)
    trace_tbl.columns[5].width = Inches(1.4)
    
    headers_tr = ["Feature", "Feature Name", "Priority", "Pain Point", "Covering Journey", "Database Entities"]
    for i, h in enumerate(headers_tr):
        c = trace_tbl.cell(0, i)
        set_bg(c, HEX_PRIMARY)
        set_margins(c, top=80, bottom=80, left=80, right=80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (fid, fname, prio, pp, uj, dbs) in enumerate(trace_data):
        row_cells = [trace_tbl.cell(row_idx + 1, i) for i in range(6)]
        bg_col = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        for cell in row_cells:
            set_bg(cell, bg_col)
            set_margins(cell, top=60, bottom=60, left=80, right=80)
            set_subtle_borders(cell)
            
        p0 = row_cells[0].paragraphs[0]
        r0 = p0.add_run(fid)
        r0.font.name = "Calibri"
        r0.font.size = Pt(8.5)
        r0.font.bold = True
        
        p1 = row_cells[1].paragraphs[0]
        r1 = p1.add_run(fname)
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.5)
        
        p2 = row_cells[2].paragraphs[0]
        r2 = p2.add_run(prio)
        r2.font.name = "Calibri"
        r2.font.size = Pt(8.5)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(0x06, 0x5F, 0x46)
        
        p3 = row_cells[3].paragraphs[0]
        r3 = p3.add_run(pp)
        r3.font.name = "Calibri"
        r3.font.size = Pt(8.5)
        
        p4 = row_cells[4].paragraphs[0]
        r4 = p4.add_run(uj)
        r4.font.name = "Calibri"
        r4.font.size = Pt(8.5)
        r4.font.bold = True
        r4.font.color.rgb = COLOR_SECONDARY
        
        p5 = row_cells[5].paragraphs[0]
        r5 = p5.add_run(dbs)
        r5.font.name = "Consolas"
        r5.font.size = Pt(8)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 10. SCOPE FREEZE & SIGN-OFF
    # -------------------------------------------------------------
    add_h1("9. Scope Freeze & Change Management")
    add_p(
        "Per capstone guidelines, the project scope defined in this document is FROZEN following Week 2–3 completion. Any prospective changes must be formally agreed upon with the advisor and recorded in the change log below before implementation begins in Phase 5."
    )

    change_tbl = doc.add_table(rows=4, cols=3)
    change_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    change_tbl.autofit = False
    change_tbl.columns[0].width = Inches(1.2)
    change_tbl.columns[1].width = Inches(2.3)
    change_tbl.columns[2].width = Inches(3.0)
    
    headers_ch = ["Date", "Scope Change", "Architectural Rationale"]
    for i, h in enumerate(headers_ch):
        c = change_tbl.cell(0, i)
        set_bg(c, HEX_PRIMARY)
        set_margins(c, top=80, bottom=80, left=80, right=80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    changes = [
        ("2026-10-15", "Added F-05 (Roadside Mechanic Pinning) to Must-Have", "Advisor feedback: Cambodian roadside stalls are informal; riders need to save their mechanic contacts and coordinates."),
        ("2026-10-15", "Shifted F-09 (Weather & Traffic Engine) to Won't-Have (v1)", "Advisor feedback: Automated live weather/traffic API integration adds excessive complexity; deferred to v2."),
        ("2026-10-15", "Added F-06 (15-Min Garage Dwell Geofence) as Should-Have", "Advisor feedback: Proactively prompts forgetful commuters (Persona 3 Davy) to log maintenance when waiting at a garage.")
    ]

    for row_idx, (dt, chg, why) in enumerate(changes):
        c0 = change_tbl.cell(row_idx + 1, 0)
        c1 = change_tbl.cell(row_idx + 1, 1)
        c2 = change_tbl.cell(row_idx + 1, 2)
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        for c in (c0, c1, c2):
            set_bg(c, bg)
            set_margins(c, top=60, bottom=60, left=80, right=80)
            set_subtle_borders(c)
            
        p = c0.paragraphs[0]
        r = p.add_run(dt)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        
        p = c1.paragraphs[0]
        r = p.add_run(chg)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        
        p = c2.paragraphs[0]
        r = p.add_run(why)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    
    # Save document
    doc.save(output_path)
    print(f"Document successfully created and saved to: {output_path}")

if __name__ == "__main__":
    out = os.path.abspath("d:/PPS1Y4/MotoCare_Cambodia_Project_Scope_Document.docx")
    build_scope_doc(out)
