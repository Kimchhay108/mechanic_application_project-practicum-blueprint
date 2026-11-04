"""
MotoCare Cambodia - Phase 3 Diagram Generator
Generates high-resolution vector SVG diagrams for:
1. Database Entity-Relationship Diagram (ERD) - 10 tables with PK/FK and cardinality
2. System Architecture Topology Diagram - Flutter, Express, PostgreSQL, Google Places
3. Reminder Lifecycle Finite State Machine (FSM) Diagram
"""

import os

def create_erd_svg():
    width = 1750
    height = 1180

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3A8A" />
      <stop offset="100%" stop-color="#2563EB" />
    </linearGradient>
    <linearGradient id="headerGradModel" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F766E" />
      <stop offset="100%" stop-color="#0D9488" />
    </linearGradient>
    <linearGradient id="headerGradLog" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#7C2D12" />
      <stop offset="100%" stop-color="#C2410C" />
    </linearGradient>
    <linearGradient id="headerGradRule" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4C1D95" />
      <stop offset="100%" stop-color="#7C3AED" />
    </linearGradient>

    <!-- Drop Shadows -->
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.08" />
    </filter>

    <!-- Connector Markers -->
    <marker id="crow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M0,2 L10,6 L0,10 M10,0 L10,12" fill="none" stroke="#64748B" stroke-width="1.8" />
    </marker>
    <marker id="one" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M5,0 L5,10 M8,0 L8,10" fill="none" stroke="#64748B" stroke-width="1.8" />
    </marker>

    <style>
      .title {{ font-size: 24px; font-weight: 700; fill: #0F172A; }}
      .subtitle {{ font-size: 14px; fill: #64748B; }}
      .tbl-title {{ font-size: 14px; font-weight: 700; fill: #FFFFFF; letter-spacing: 0.5px; }}
      .col-name {{ font-size: 12px; font-weight: 500; fill: #1E293B; }}
      .col-name-pk {{ font-size: 12px; font-weight: 700; fill: #0F172A; }}
      .col-type {{ font-size: 11px; fill: #64748B; font-family: 'Consolas', 'Fira Code', monospace; }}
      .badge-pk {{ fill: #FEF3C7; stroke: #D97706; }}
      .badge-pk-txt {{ font-size: 9px; font-weight: 700; fill: #92400E; }}
      .badge-fk {{ fill: #DBEAFE; stroke: #2563EB; }}
      .badge-fk-txt {{ font-size: 9px; font-weight: 700; fill: #1E40AF; }}
      .badge-uk {{ fill: #D1FAE5; stroke: #059669; }}
      .badge-uk-txt {{ font-size: 9px; font-weight: 700; fill: #065F46; }}
      .wire {{ fill: none; stroke: #64748B; stroke-width: 1.8; stroke-dasharray: none; }}
      .wire-subtle {{ fill: none; stroke: #94A3B8; stroke-width: 1.5; stroke-dasharray: 4 3; }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="#F8FAFC" />
  
  <!-- Subtle Grid Pattern -->
  <g opacity="0.4">
    {''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="#E2E8F0" stroke-width="1" />' for x in range(0, width, 50))}
    {''.join(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#E2E8F0" stroke-width="1" />' for y in range(0, height, 50))}
  </g>

  <!-- Title Block -->
  <g transform="translate(50, 45)">
    <rect x="-10" y="-20" width="600" height="65" rx="8" fill="#FFFFFF" stroke="#E2E8F0" opacity="0.9" />
    <text class="title" x="10" y="12">MotoCare Cambodia — Database ERD</text>
    <text class="subtitle" x="10" y="34">Relational PostgreSQL 16 Data Model | 10 Entities | Dynamic Model-Agnostic Engine</text>
  </g>

  <!-- Legend Block -->
  <g transform="translate(1360, 30)">
    <rect width="340" height="65" rx="8" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#shadow)" />
    <text x="15" y="22" font-size="12" font-weight="700" fill="#1E293B">LEGEND &amp; CARDINALITY</text>
    
    <rect x="15" y="34" width="28" height="16" rx="3" class="badge-pk" />
    <text x="21" y="46" class="badge-pk-txt">PK</text>
    <text x="48" y="46" font-size="11" fill="#475569">Primary Key</text>

    <rect x="125" y="34" width="28" height="16" rx="3" class="badge-fk" />
    <text x="131" y="46" class="badge-fk-txt">FK</text>
    <text x="158" y="46" font-size="11" fill="#475569">Foreign Key</text>

    <rect x="235" y="34" width="28" height="16" rx="3" class="badge-uk" />
    <text x="241" y="46" class="badge-uk-txt">UK</text>
    <text x="268" y="46" font-size="11" fill="#475569">Unique</text>
  </g>
"""

    def render_table(x, y, w, title, cols, header_grad="headerGrad"):
        header_h = 36
        row_h = 24
        total_h = header_h + (len(cols) * row_h) + 10
        
        box_svg = f"""
  <g transform="translate({x}, {y})" filter="url(#shadow)">
    <!-- Table Shell -->
    <rect width="{w}" height="{total_h}" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
    <!-- Table Header -->
    <path d="M0,8 Q0,0 8,0 L{w-8},0 Q{w},0 {w},8 L{w},{header_h} L0,{header_h} Z" fill="url(#{header_grad})" />
    <text class="tbl-title" x="14" y="23">{title}</text>
"""
        for idx, (name, col_type, badge) in enumerate(cols):
            row_y = header_h + 18 + (idx * row_h)
            badge_svg = ""
            if badge == "PK":
                badge_svg = f'<rect x="{w-78}" y="{row_y-12}" width="24" height="15" rx="3" class="badge-pk"/><text x="{w-74}" y="{row_y-1}" class="badge-pk-txt">PK</text>'
            elif badge == "FK":
                badge_svg = f'<rect x="{w-78}" y="{row_y-12}" width="24" height="15" rx="3" class="badge-fk"/><text x="{w-74}" y="{row_y-1}" class="badge-fk-txt">FK</text>'
            elif badge == "UK":
                badge_svg = f'<rect x="{w-78}" y="{row_y-12}" width="24" height="15" rx="3" class="badge-uk"/><text x="{w-74}" y="{row_y-1}" class="badge-uk-txt">UK</text>'
            elif badge == "PK, FK":
                badge_svg = f'<rect x="{w-88}" y="{row_y-12}" width="36" height="15" rx="3" class="badge-pk"/><text x="{w-85}" y="{row_y-1}" class="badge-pk-txt">PK,FK</text>'

            is_pk = "PK" in badge or "FK" in badge
            name_class = "col-name-pk" if is_pk else "col-name"

            box_svg += f"""
    <line x1="0" y1="{row_y+6}" x2="{w}" y2="{row_y+6}" stroke="#F1F5F9" stroke-width="1" />
    <text class="{name_class}" x="14" y="{row_y}">{name}</text>
    {badge_svg}
    <text class="col-type" x="{w-14}" y="{row_y}" text-anchor="end">{col_type}</text>
"""
        box_svg += "  </g>\n"
        return box_svg, total_h

    # Table Definitions
    # 1. users (x=50, y=140)
    users_cols = [
        ("id", "uuid", "PK"),
        ("phone", "varchar(20)", "UK"),
        ("full_name", "varchar(100)", ""),
        ("language_preference", "varchar(10)", ""),
        ("created_at", "timestamptz", ""),
        ("updated_at", "timestamptz", "")
    ]

    # 2. vehicles (x=380, y=140)
    vehicles_cols = [
        ("id", "uuid", "PK"),
        ("user_id", "uuid", "FK"),
        ("vehicle_model_id", "uuid", "FK"),
        ("license_plate", "varchar(20)", ""),
        ("current_odometer", "integer", ""),
        ("created_at", "timestamptz", ""),
        ("updated_at", "timestamptz", "")
    ]

    # 3. vehicle_models (x=730, y=140)
    models_cols = [
        ("id", "uuid", "PK"),
        ("vehicle_type", "varchar(20)", ""),
        ("make", "varchar(50)", ""),
        ("model", "varchar(50)", ""),
        ("year_start", "integer", ""),
        ("year_end", "integer", ""),
        ("created_at", "timestamptz", "")
    ]

    # 4. model_component_configs (x=1080, y=140)
    configs_cols = [
        ("id", "uuid", "PK"),
        ("vehicle_model_id", "uuid", "FK"),
        ("component_id", "uuid", "FK"),
        ("default_interval_km", "integer", ""),
        ("default_interval_days", "integer", ""),
        ("wear_multiplier", "numeric(3,2)", ""),
        ("is_active", "boolean", ""),
        ("created_at", "timestamptz", "")
    ]

    # 5. components (x=1430, y=140)
    components_cols = [
        ("id", "uuid", "PK"),
        ("code", "varchar(50)", "UK"),
        ("name_en", "varchar(100)", ""),
        ("name_km (slang)", "varchar(100)", ""),
        ("category", "varchar(50)", ""),
        ("created_at", "timestamptz", "")
    ]

    # Row 2 Tables:
    # 6. reminder_rules (x=380, y=420)
    reminder_cols = [
        ("id", "uuid", "PK"),
        ("vehicle_id", "uuid", "FK"),
        ("component_id", "uuid", "FK"),
        ("interval_km", "integer", ""),
        ("interval_days", "integer", ""),
        ("last_serviced_odometer", "integer", ""),
        ("last_serviced_date", "date", ""),
        ("next_due_odometer", "integer", ""),
        ("next_due_date", "date", ""),
        ("status (upcoming/due/over)", "varchar(20)", ""),
        ("is_active", "boolean", "")
    ]

    # 7. garages (x=50, y=440)
    garages_cols = [
        ("id", "uuid", "PK"),
        ("user_id (nullable)", "uuid", "FK"),
        ("name (ឈ្មោះជាង)", "varchar(150)", ""),
        ("phone", "varchar(20)", ""),
        ("address", "varchar(255)", ""),
        ("latitude", "numeric(10,7)", ""),
        ("longitude", "numeric(10,7)", ""),
        ("is_verified", "boolean", "")
    ]

    # 8. service_logs (x=730, y=480)
    servicelog_cols = [
        ("id", "uuid", "PK"),
        ("vehicle_id", "uuid", "FK"),
        ("garage_id (nullable)", "uuid", "FK"),
        ("service_date", "date", ""),
        ("odometer_km", "integer", ""),
        ("total_cost_cents", "integer", ""),
        ("currency (USD/KHR)", "varchar(3)", ""),
        ("notes", "text", ""),
        ("invoice_photo_url", "varchar(500)", "")
    ]

    # 9. service_log_items (x=1080, y=480)
    logitems_cols = [
        ("id", "uuid", "PK"),
        ("service_log_id", "uuid", "FK"),
        ("component_id", "uuid", "FK"),
        ("cost_cents", "integer", ""),
        ("notes", "text", "")
    ]

    # 10. odometer_histories (x=380, y=780)
    odometer_cols = [
        ("id", "uuid", "PK"),
        ("vehicle_id", "uuid", "FK"),
        ("odometer_km", "integer", ""),
        ("recorded_at", "timestamptz", ""),
        ("source (manual/log/dwell)", "varchar(20)", "")
    ]

    # Render All Tables
    t1, h1 = render_table(50, 140, 270, "users", users_cols, "headerGrad")
    t2, h2 = render_table(380, 140, 290, "vehicles", vehicles_cols, "headerGrad")
    t3, h3 = render_table(730, 140, 290, "vehicle_models", models_cols, "headerGradModel")
    t4, h4 = render_table(1080, 140, 290, "model_component_configs", configs_cols, "headerGradModel")
    t5, h5 = render_table(1430, 140, 270, "components", components_cols, "headerGradModel")
    
    t6, h6 = render_table(380, 420, 290, "reminder_rules", reminder_cols, "headerGradRule")
    t7, h7 = render_table(50, 440, 270, "garages", garages_cols, "headerGradLog")
    t8, h8 = render_table(730, 480, 290, "service_logs", servicelog_cols, "headerGradLog")
    t9, h9 = render_table(1080, 480, 290, "service_log_items", logitems_cols, "headerGradLog")
    t10, h10 = render_table(380, 800, 290, "odometer_histories", odometer_cols, "headerGrad")

    svg += t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9 + t10

    # Connector Lines
    connectors = """
  <!-- Relational Connectors -->
  <g class="wire">
    <!-- users (1) to vehicles (N) -->
    <path d="M320,180 L380,180" marker-start="url(#one)" marker-end="url(#crow)" />

    <!-- vehicle_models (1) to vehicles (N) -->
    <path d="M730,180 L670,180" marker-start="url(#one)" marker-end="url(#crow)" />

    <!-- vehicle_models (1) to model_component_configs (N) -->
    <path d="M1020,180 L1080,180" marker-start="url(#one)" marker-end="url(#crow)" />

    <!-- components (1) to model_component_configs (N) -->
    <path d="M1430,180 L1370,180" marker-start="url(#one)" marker-end="url(#crow)" />

    <!-- users (1) to garages (N) -->
    <path d="M180,330 L180,440" marker-start="url(#one)" marker-end="url(#crow)" />

    <!-- vehicles (1) to reminder_rules (N) -->
    <path d="M520,350 L520,420" marker-start="url(#one)" marker-end="url(#crow)" />

    <!-- vehicles (1) to service_logs (N) -->
    <path d="M670,250 L700,250 L700,530 L730,530" marker-start="url(#one)" marker-end="url(#crow)" />

    <!-- garages (1) to service_logs (N) -->
    <path d="M320,530 L730,530" marker-start="url(#one)" marker-end="url(#crow)" />

    <!-- service_logs (1) to service_log_items (N) -->
    <path d="M1020,530 L1080,530" marker-start="url(#one)" marker-end="url(#crow)" />

    <!-- components (1) to service_log_items (N) -->
    <path d="M1520,330 L1520,530 L1370,530" marker-start="url(#one)" marker-end="url(#crow)" />

    <!-- components (1) to reminder_rules (N) -->
    <path d="M1430,220 L1400,220 L1400,380 L670,380 L670,450" marker-start="url(#one)" marker-end="url(#crow)" />

    <!-- vehicles (1) to odometer_histories (N) -->
    <path d="M430,730 L430,800" marker-start="url(#one)" marker-end="url(#crow)" />
  </g>
"""

    svg += connectors + "</svg>"
    return svg


def create_architecture_svg():
    width = 1350
    height = 720

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif">
  <defs>
    <linearGradient id="clientGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EFF6FF" />
      <stop offset="100%" stop-color="#DBEAFE" />
    </linearGradient>
    <linearGradient id="serverGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EEF2FF" />
      <stop offset="100%" stop-color="#E0E7FF" />
    </linearGradient>
    <linearGradient id="dataGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FEF3C7" />
      <stop offset="100%" stop-color="#FDE68A" />
    </linearGradient>
    
    <filter id="boxShadow" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#0F172A" flood-opacity="0.07" />
    </filter>

    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#3B82F6"/>
    </marker>
    <marker id="arr-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#64748B"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="#FFFFFF" />

  <!-- Header -->
  <text x="40" y="45" font-size="22" font-weight="700" fill="#0F172A">MotoCare Cambodia — System Architecture Map</text>
  <text x="40" y="70" font-size="13" fill="#64748B">Multi-Tier Offline-First Architecture (Flutter + Express + PostgreSQL 16 Docker)</text>

  <!-- TIER 1: CLIENT APPLICATION (FLUTTER) -->
  <rect x="40" y="100" width="560" height="580" rx="14" fill="#F8FAFC" stroke="#93C5FD" stroke-width="2" filter="url(#boxShadow)"/>
  <rect x="40" y="100" width="560" height="42" rx="14" fill="#3B82F6"/>
  <text x="60" y="128" font-size="15" font-weight="700" fill="#FFFFFF">CLIENT LAYER: FLUTTER MOBILE APP (iOS &amp; Android)</text>

  <!-- Client Sub-components -->
  <!-- UI -->
  <rect x="70" y="165" width="230" height="110" rx="8" fill="#FFFFFF" stroke="#BFDBFE" stroke-width="1.5" />
  <text x="85" y="195" font-size="14" font-weight="700" fill="#1E3A8A">Mobile UI Layer</text>
  <text x="85" y="218" font-size="11" fill="#475569">• R/Y/G Vehicle Health Cards</text>
  <text x="85" y="236" font-size="11" fill="#475569">• Authentic Khmer Slang Tags</text>
  <text x="85" y="254" font-size="11" fill="#475569">• 1-Tap Quick Action Logger</text>

  <!-- State -->
  <rect x="330" y="165" width="240" height="110" rx="8" fill="#FFFFFF" stroke="#BFDBFE" stroke-width="1.5" />
  <text x="345" y="195" font-size="14" font-weight="700" fill="#1E3A8A">State Management</text>
  <text x="345" y="218" font-size="11" fill="#475569">• Riverpod StateNotifiers</text>
  <text x="345" y="236" font-size="11" fill="#475569">• Vehicle &amp; Reminder Providers</text>
  <text x="345" y="254" font-size="11" fill="#475569">• Optimistic Offline Dispatcher</text>

  <!-- Local Cache (Drift) -->
  <rect x="70" y="315" width="500" height="120" rx="8" fill="url(#clientGrad)" stroke="#2563EB" stroke-width="1.5" />
  <text x="90" y="345" font-size="15" font-weight="700" fill="#1E3A8A">Local Persistence: Drift (SQLite v3)</text>
  <text x="90" y="370" font-size="12" fill="#334155">• 100% Offline read/write capability (&lt; 5ms latency at roadside stalls)</text>
  <text x="90" y="392" font-size="12" fill="#334155">• Local tables: vehicles, cached reminders, pending service queue, pinned garages</text>
  <text x="90" y="414" font-size="12" fill="#334155">• Automatic sync engine flushes queue when mobile data/Wi-Fi is reconnected</text>

  <!-- Background Services -->
  <rect x="70" y="465" width="500" height="185" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" />
  <text x="90" y="495" font-size="14" font-weight="700" fill="#0F172A">Native Background OS Services</text>
  
  <rect x="90" y="515" width="220" height="115" rx="6" fill="#F1F5F9" stroke="#E2E8F0" />
  <text x="105" y="540" font-size="12" font-weight="700" fill="#1E293B">At-Garage Dwell Engine</text>
  <text x="105" y="562" font-size="11" fill="#475569">• 50m circular geofences</text>
  <text x="105" y="580" font-size="11" fill="#475569">• 15-min dwell continuous filter</text>
  <text x="105" y="598" font-size="11" fill="#475569">• Zero CPU wake outside zones</text>

  <rect x="330" y="515" width="220" height="115" rx="6" fill="#F1F5F9" stroke="#E2E8F0" />
  <text x="345" y="540" font-size="12" font-weight="700" fill="#1E293B">Local Notification Tray</text>
  <text x="345" y="562" font-size="11" fill="#475569">• flutter_local_notifications</text>
  <text x="345" y="580" font-size="11" fill="#475569">• Proactive overdue alerts</text>
  <text x="345" y="598" font-size="11" fill="#475569">• "Looks like you're at garage"</text>

  <!-- ARROWS BETWEEN CLIENT & BACKEND -->
  <!-- Wire from client to backend -->
  <path d="M600,220 L730,220" fill="none" stroke="#2563EB" stroke-width="2.2" marker-end="url(#arr)" />
  <text x="665" y="210" font-size="11" font-weight="700" fill="#1E40AF" text-anchor="middle">HTTP REST (JSON)</text>
  <text x="665" y="238" font-size="10" fill="#64748B" text-anchor="middle">Port 8000 /api/v1</text>
  <text x="665" y="254" font-size="10" fill="#64748B" text-anchor="middle">Bearer &lt;JWT&gt;</text>

  <!-- TIER 2: BACKEND API LAYER (EXPRESS + TYPESCRIPT) -->
  <rect x="730" y="100" width="300" height="580" rx="14" fill="#F8FAFC" stroke="#818CF8" stroke-width="2" filter="url(#boxShadow)"/>
  <rect x="730" y="100" width="300" height="42" rx="14" fill="#4F46E5"/>
  <text x="750" y="128" font-size="15" font-weight="700" fill="#FFFFFF">BACKEND API (PORT 8000)</text>

  <rect x="750" y="165" width="260" height="95" rx="8" fill="#FFFFFF" stroke="#C7D2FE" stroke-width="1.5" />
  <text x="765" y="193" font-size="13" font-weight="700" fill="#312E81">Auth &amp; Validation Gate</text>
  <text x="765" y="216" font-size="11" fill="#475569">• JWT Bearer Token Verification</text>
  <text x="765" y="234" font-size="11" fill="#475569">• Zod Payload Schema Sanitization</text>

  <rect x="750" y="280" width="260" height="120" rx="8" fill="#FFFFFF" stroke="#C7D2FE" stroke-width="1.5" />
  <text x="765" y="308" font-size="13" font-weight="700" fill="#312E81">Controllers &amp; Services</text>
  <text x="765" y="331" font-size="11" fill="#475569">• Vehicles &amp; Models Controller</text>
  <text x="765" y="349" font-size="11" fill="#475569">• Service Logs Controller</text>
  <text x="765" y="367" font-size="11" fill="#475569">• Roadside Garages Controller</text>

  <rect x="750" y="420" width="260" height="150" rx="8" fill="url(#serverGrad)" stroke="#4F46E5" stroke-width="1.5" />
  <text x="765" y="448" font-size="14" font-weight="700" fill="#312E81">Maintenance Rules Engine</text>
  <text x="765" y="471" font-size="11" fill="#3730A3">• Dual-Condition Evaluator (km vs days)</text>
  <text x="765" y="489" font-size="11" fill="#3730A3">• Dynamic model_component_configs</text>
  <text x="765" y="507" font-size="11" fill="#3730A3">• Composite wear ratio calculation:</text>
  <text x="765" y="525" font-size="11" font-weight="600" fill="#3730A3">  ρ = MAX(ΔKm/TargetKm, ΔDays/TargetDays)</text>
  <text x="765" y="545" font-size="11" fill="#3730A3">• Deterministic R/Y/G status resets</text>

  <!-- TIER 3: DATA TIER & EXTERNAL SERVICES -->
  <!-- Wire backend to Postgres -->
  <path d="M1030,300 L1100,300" fill="none" stroke="#4F46E5" stroke-width="2" marker-end="url(#arr)" />
  
  <!-- PostgreSQL -->
  <rect x="1100" y="100" width="210" height="340" rx="14" fill="#FFFBEB" stroke="#F59E0B" stroke-width="2" filter="url(#boxShadow)"/>
  <rect x="1100" y="100" width="210" height="42" rx="14" fill="#D97706"/>
  <text x="1120" y="128" font-size="14" font-weight="700" fill="#FFFFFF">DATA TIER (PostgreSQL 16)</text>
  
  <text x="1120" y="170" font-size="12" font-weight="700" fill="#92400E">Docker Container</text>
  <text x="1120" y="195" font-size="11" fill="#78350F">• users</text>
  <text x="1120" y="215" font-size="11" fill="#78350F">• vehicle_models</text>
  <text x="1120" y="235" font-size="11" fill="#78350F">• components</text>
  <text x="1120" y="255" font-size="11" fill="#78350F">• model_component_configs</text>
  <text x="1120" y="275" font-size="11" fill="#78350F">• vehicles</text>
  <text x="1120" y="295" font-size="11" fill="#78350F">• reminder_rules</text>
  <text x="1120" y="315" font-size="11" fill="#78350F">• garages</text>
  <text x="1120" y="335" font-size="11" fill="#78350F">• service_logs</text>
  <text x="1120" y="355" font-size="11" fill="#78350F">• service_log_items</text>
  <text x="1120" y="375" font-size="11" fill="#78350F">• odometer_histories</text>
  <text x="1120" y="405" font-size="10" font-style="italic" fill="#B45309">Integer currency (cents)</text>

  <!-- External Services -->
  <rect x="1100" y="465" width="210" height="215" rx="14" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="6 4"/>
  <text x="1120" y="495" font-size="13" font-weight="700" fill="#475569">EXTERNAL SERVICES</text>

  <rect x="1115" y="515" width="180" height="65" rx="6" fill="#F8FAFC" stroke="#E2E8F0" />
  <text x="1125" y="538" font-size="11" font-weight="700" fill="#1E293B">Google Places API</text>
  <text x="1125" y="556" font-size="10" fill="#64748B">Phnom Penh garage lookup</text>
  <text x="1125" y="570" font-size="10" fill="#64748B">Fallback: Local DB seed</text>

  <rect x="1115" y="595" width="180" height="65" rx="6" fill="#F8FAFC" stroke="#E2E8F0" />
  <text x="1125" y="618" font-size="11" font-weight="700" fill="#1E293B">Receipt &amp; Photo Storage</text>
  <text x="1125" y="636" font-size="10" fill="#64748B">Supabase / Local cache</text>
  <text x="1125" y="650" font-size="10" fill="#64748B">Oil bottle &amp; odometer snaps</text>

  <path d="M1010,350 L1115,545" fill="none" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arr-gray)" />
</svg>"""
    return svg


def create_state_machine_svg():
    width = 1100
    height = 680

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif">
  <defs>
    <filter id="shadowFSM" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.08" />
    </filter>
    <marker id="arrowFSM" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#475569"/>
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#059669"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="#F8FAFC" />

  <!-- Title -->
  <text x="50" y="50" font-size="22" font-weight="700" fill="#0F172A">MotoCare Cambodia — Reminder State Machine</text>
  <text x="50" y="75" font-size="13" fill="#64748B">Deterministic 4-State Lifecycle for Vehicle Component Maintenance</text>

  <!-- Start Node -->
  <circle cx="550" cy="115" r="16" fill="#0F172A" />
  <text x="550" y="85" font-size="12" font-weight="700" fill="#334155" text-anchor="middle">Vehicle Created &amp; Rules Bound</text>
  <line x1="550" y1="131" x2="550" y2="165" stroke="#475569" stroke-width="2" marker-end="url(#arrowFSM)" />

  <!-- STATE 1: UPCOMING (GREEN) -->
  <g transform="translate(410, 170)" filter="url(#shadowFSM)">
    <rect width="280" height="90" rx="12" fill="#ECFDF5" stroke="#059669" stroke-width="2" />
    <circle cx="30" cy="30" r="10" fill="#10B981" />
    <text x="52" y="35" font-size="16" font-weight="700" fill="#065F46">UPCOMING (🟢 Green)</text>
    <text x="24" y="58" font-size="11" fill="#047857">• Healthy operating condition: ρ &lt; 0.80</text>
    <text x="24" y="74" font-size="11" fill="#047857">• &gt; 20% distance remaining AND &gt; 7 days</text>
  </g>

  <!-- Arrow Upcoming -> Due Soon -->
  <line x1="550" y1="260" x2="550" y2="310" stroke="#475569" stroke-width="2" marker-end="url(#arrowFSM)" />
  <rect x="555" y="272" width="250" height="22" rx="4" fill="#FFFFFF" stroke="#E2E8F0" />
  <text x="562" y="287" font-size="10.5" font-weight="600" fill="#475569">Remaining km ≤ 20% OR Days ≤ 7 days</text>

  <!-- STATE 2: DUE SOON (YELLOW) -->
  <g transform="translate(410, 315)" filter="url(#shadowFSM)">
    <rect width="280" height="90" rx="12" fill="#FFFBEB" stroke="#D97706" stroke-width="2" />
    <circle cx="30" cy="30" r="10" fill="#F59E0B" />
    <text x="52" y="35" font-size="16" font-weight="700" fill="#92400E">DUE SOON (🟡 Yellow)</text>
    <text x="24" y="58" font-size="11" fill="#B45309">• Warning threshold: 0.80 ≤ ρ &lt; 1.00</text>
    <text x="24" y="74" font-size="11" fill="#B45309">• Scheduled local push alert fired</text>
  </g>

  <!-- Arrow Due Soon -> Overdue -->
  <line x1="550" y1="405" x2="550" y2="455" stroke="#475569" stroke-width="2" marker-end="url(#arrowFSM)" />
  <rect x="555" y="418" width="250" height="22" rx="4" fill="#FFFFFF" stroke="#E2E8F0" />
  <text x="562" y="433" font-size="10.5" font-weight="600" fill="#DC2626">Current Km ≥ Next Due Km OR Date reached</text>

  <!-- STATE 3: OVERDUE (RED) -->
  <g transform="translate(410, 460)" filter="url(#shadowFSM)">
    <rect width="280" height="90" rx="12" fill="#FEF2F2" stroke="#DC2626" stroke-width="2" />
    <circle cx="30" cy="30" r="10" fill="#EF4444" />
    <text x="52" y="35" font-size="16" font-weight="700" fill="#991B1B">OVERDUE (🔴 Red)</text>
    <text x="24" y="58" font-size="11" fill="#B91C1C">• Interval exceeded: ρ ≥ 1.00</text>
    <text x="24" y="74" font-size="11" fill="#B91C1C">• Critical card shown; immediate service needed</text>
  </g>

  <!-- Sudden large mileage jump shortcut: Upcoming -> Overdue -->
  <path d="M690,215 L880,215 L880,505 L690,505" fill="none" stroke="#DC2626" stroke-width="1.8" stroke-dasharray="4 3" marker-end="url(#arrowFSM)" />
  <rect x="885" y="345" width="180" height="34" rx="4" fill="#FFFFFF" stroke="#FCA5A5" />
  <text x="892" y="360" font-size="10" font-weight="600" fill="#991B1B">Sudden mileage jump</text>
  <text x="892" y="373" font-size="9" fill="#991B1B">exceeds target interval</text>

  <!-- STATE 4: SERVICED (RESET) -->
  <g transform="translate(60, 315)" filter="url(#shadowFSM)">
    <rect width="270" height="90" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="2" />
    <circle cx="30" cy="30" r="10" fill="#3B82F6" />
    <text x="52" y="35" font-size="16" font-weight="700" fill="#1E40AF">SERVICED (🔵 Reset)</text>
    <text x="20" y="58" font-size="11" fill="#1E3A8A">• 1-Tap service log recorded</text>
    <text x="20" y="74" font-size="11" fill="#1E3A8A">• Baseline odometer &amp; date reset</text>
  </g>

  <!-- Arrows from Upcoming, Due Soon, Overdue -> Serviced -->
  <!-- From Overdue to Serviced -->
  <path d="M410,505 L195,505 L195,405" fill="none" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowFSM)" />
  <text x="270" y="495" font-size="10.5" font-weight="600" fill="#1E40AF">Corrective Service Log</text>

  <!-- From Due Soon to Serviced -->
  <line x1="410" y1="360" x2="330" y2="360" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowFSM)" />
  <text x="340" y="350" font-size="10" font-weight="600" fill="#1E40AF">Scheduled</text>

  <!-- From Upcoming to Serviced -->
  <path d="M410,215 L195,215 L195,315" fill="none" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowFSM)" />
  <text x="270" y="210" font-size="10.5" font-weight="600" fill="#1E40AF">Early Service Log</text>

  <!-- Arrow from Serviced back to Upcoming -->
  <path d="M195,315 L195,140 L410,185" fill="none" stroke="#059669" stroke-width="2.5" marker-end="url(#arrowGreen)" />
  <rect x="205" y="145" width="220" height="24" rx="4" fill="#FFFFFF" stroke="#A7F3D0" />
  <text x="215" y="161" font-size="11" font-weight="700" fill="#047857">Reset status back to UPCOMING (🟢)</text>

  <!-- Bottom Formula Box -->
  <rect x="50" y="590" width="1000" height="60" rx="8" fill="#FFFFFF" stroke="#CBD5E1" />
  <text x="70" y="615" font-size="12" font-weight="700" fill="#1E293B">DUAL-CONDITION TRIGGER FORMULA:</text>
  <text x="70" y="635" font-size="12" font-family="'Consolas', monospace" fill="#2563EB">Composite Wear Ratio (ρ) = MAX( ΔKm / TargetKm, ΔDays / TargetDays )</text>
  <text x="620" y="635" font-size="11" fill="#475569">TargetKm = BaseInterval * WearMultiplier</text>
</svg>"""
    return svg


def main():
    target_dir = os.path.abspath("d:/PPS1Y4/context/assets")
    os.makedirs(target_dir, exist_ok=True)

    erd_path = os.path.join(target_dir, "database_erd.svg")
    with open(erd_path, "w", encoding="utf-8") as f:
        f.write(create_erd_svg())
    print(f"Created: {erd_path}")

    arch_path = os.path.join(target_dir, "system_architecture.svg")
    with open(arch_path, "w", encoding="utf-8") as f:
        f.write(create_architecture_svg())
    print(f"Created: {arch_path}")

    fsm_path = os.path.join(target_dir, "state_machine.svg")
    with open(fsm_path, "w", encoding="utf-8") as f:
        f.write(create_state_machine_svg())
    print(f"Created: {fsm_path}")

    # Also create an interactive viewer HTML in context/assets/preview_diagrams.html
    html_path = os.path.join(target_dir, "preview_diagrams.html")
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MotoCare Cambodia — Phase 3 Technical Diagrams</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    body { background: #0F172A; color: #F8FAFC; padding: 24px; }
    header { max-width: 1400px; margin: 0 auto 24px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 16px; }
    h1 { font-size: 22px; color: #38BDF8; }
    p { font-size: 13px; color: #94A3B8; margin-top: 4px; }
    .tabs { display: flex; gap: 10px; }
    .tab-btn { background: #1E293B; color: #E2E8F0; border: 1px solid #475569; padding: 8px 18px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600; transition: all 0.2s; }
    .tab-btn:hover { background: #334155; }
    .tab-btn.active { background: #2563EB; border-color: #3B82F6; color: #FFFFFF; }
    .container { max-width: 1400px; margin: 0 auto; background: #FFFFFF; border-radius: 12px; padding: 20px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3); overflow: auto; min-height: 700px; }
    .diagram-panel { display: none; text-align: center; }
    .diagram-panel.active { display: block; }
    img, svg { max-width: 100%; height: auto; border-radius: 8px; }
    .caption { margin-top: 12px; font-size: 12px; color: #64748B; text-align: left; }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>MotoCare Cambodia — Phase 3 Architectural & Data Diagrams</h1>
      <p>Student: Thoeurn Kimchhay (ធឿន គីមឆាយ) | Advisor: Hang Sopheak | Royal University of Phnom Penh (RUPP)</p>
    </div>
    <div class="tabs">
      <button class="tab-btn active" onclick="showTab('erd')">1. Database ERD</button>
      <button class="tab-btn" onclick="showTab('arch')">2. System Architecture</button>
      <button class="tab-btn" onclick="showTab('fsm')">3. Reminder State Machine</button>
    </div>
  </header>

  <div class="container">
    <div id="erd" class="diagram-panel active">
      <img src="database_erd.svg" alt="Database Entity-Relationship Diagram" />
      <div class="caption">Figure 3.3: Relational 10-Entity PostgreSQL Database ERD with dynamic model_component_configs table.</div>
    </div>

    <div id="arch" class="diagram-panel">
      <img src="system_architecture.svg" alt="System Architecture Map" />
      <div class="caption">Figure 3.2: High-Level System Architecture Topology showing Flutter Client, Drift SQLite, Express API, and PostgreSQL.</div>
    </div>

    <div id="fsm" class="diagram-panel">
      <img src="state_machine.svg" alt="Reminder Lifecycle State Machine" />
      <div class="caption">Figure 3.2b: Deterministic 4-State Reminder Lifecycle State Machine with dual-condition trigger evaluations.</div>
    </div>
  </div>

  <script>
    function showTab(id) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.diagram-panel').forEach(p => p.classList.remove('active'));
      event.target.classList.add('active');
      document.getElementById(id).classList.add('active');
    }
  </script>
</body>
</html>"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Created: {html_path}")

if __name__ == "__main__":
    main()
