#!/usr/bin/env python3
"""
Autonomous Google SEO Question Researcher & Multi-Module Topic Generator
Targets high-intent Google search queries and 'People Also Ask' questions across:
- SAP MM (Materials Management / Sourcing & Procurement)
- SAP EWM (Extended Warehouse Management)
- SAP SD (Sales & Distribution / Order-to-Cash)
- SAP FICO (Financial Accounting & Controlling / S/4HANA Finance)
- SAP Joule AI (Agentic AI, Copilot & Autonomous Logistics in S/4HANA 2026)

Adheres strictly to AGENTS.md Universal Blog Publisher Standards
"""

import os
import sys
import json
import time
import random
import urllib.request
import urllib.parse
from typing import List, Dict, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(BASE_DIR, "blog")

MODULES = ["mm", "ewm", "sd", "fico", "joule"]

MODULE_META = {
    "mm": {
        "name": "SAP MM / Sourcing & Procurement",
        "badge": "SAP MM MASTERCLASS",
        "category": "Tutorial",
        "default_tags": ["SAP MM", "S/4HANA 2026", "Procurement", "P2P", "SPRO"],
        "default_role": "SAP MM Functional Consultant / Inventory Lead"
    },
    "ewm": {
        "name": "SAP EWM / Warehouse Logistics",
        "badge": "SAP EWM BLUEPRINT",
        "category": "Tutorial",
        "default_tags": ["SAP EWM", "S/4HANA 2026", "Warehouse Management", "Logistics Execution"],
        "default_role": "SAP EWM Solution Architect / Logistics Lead"
    },
    "sd": {
        "name": "SAP SD / Order-to-Cash",
        "badge": "SAP SD MASTERCLASS",
        "category": "Tutorial",
        "default_tags": ["SAP SD", "S/4HANA 2026", "Order-to-Cash", "Pricing Procedure", "O2C"],
        "default_role": "SAP SD Functional Consultant / Order-to-Cash Architect"
    },
    "fico": {
        "name": "SAP FICO / S/4HANA Finance",
        "badge": "SAP FICO BLUEPRINT",
        "category": "Tutorial",
        "default_tags": ["SAP FICO", "S/4HANA Finance", "Universal Journal", "ACDOCA", "Controlling"],
        "default_role": "SAP FICO Lead Consultant / Financial Architect"
    },
    "joule": {
        "name": "SAP Joule AI / Autonomous ERP",
        "badge": "SAP JOULE AI 2026",
        "category": "Technology",
        "default_tags": ["SAP Joule", "Agentic AI", "S/4HANA 2026", "Clean Core", "AI Automation"],
        "default_role": "SAP AI Transformation Lead / Enterprise Architect"
    }
}

# Live Google Suggest Scraper
def fetch_google_suggestions(query: str, limit: int = 6) -> List[str]:
    """Queries Google Suggest endpoint to discover actual phrases real users type."""
    encoded_q = urllib.parse.quote(query)
    url = f"https://suggestqueries.google.com/complete/search?client=chrome&hl=en&q={encoded_q}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    })
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            if len(data) > 1 and isinstance(data[1], list):
                return data[1][:limit]
    except Exception as e:
        # Fallback gracefully if network timeout
        pass
    return []

# Curated High-Intent Knowledge Base Across All 5 Modules
# Grounded in official SPRO configuration, S/4HANA 2026 architecture, and real interview scenarios
TOPIC_DATABASE: Dict[str, List[Dict]] = {
    "mm": [
        {
            "title": "SAP MM Pricing Procedure (Calculation Schema) Configuration Step-by-Step",
            "slug": "sap-mm-pricing-procedure-calculation-schema-guide",
            "badge": "SAP MM BLUEPRINT",
            "category": "Tutorial",
            "read_time": "14 min read",
            "keyword": "sap mm pricing procedure configuration calculation schema m/08",
            "meta_desc": "Master SAP MM Pricing Procedure: Condition Tables (M/03), Access Sequences (M/07), Condition Types (M/06), Calculation Schema (M/08), and Schema Determination (OMF2).",
            "role": "SAP MM Functional Consultant & Pricing Specialist",
            "process_title": "Condition Technique Determination Flow",
            "process_steps": [
                ("1. Condition Table", "Define key fields for price lookup (e.g. Vendor + Material) via M/03"),
                ("2. Access Sequence", "Create search hierarchy from specific to generic combinations via M/07"),
                ("3. Condition Types", "Configure base gross price (PB00), discounts (RA01), and freight (FRB1) via M/06"),
                ("4. Schema Determination", "Link Schema Group Pur Org + Schema Group Vendor to Calculation Schema via OMF2")
            ],
            "table_headers": ["Pricing Component", "Customizing T-Code / SPRO Node", "Configuration Function"],
            "table_rows": [
                ("Condition Tables", "M/03, M/04, M/05", "Defines database table structure storing condition records (e.g., Table 017)."),
                ("Access Sequence", "M/07", "Directs SAP system search order from narrowest to broadest key combinations."),
                ("Calculation Schema", "M/08", "Defines mathematical hierarchy of gross price, surcharges, discounts, and net effective price."),
                ("Schema Determination", "OMF2 (Purchasing Customizing)", "Maps Purchasing Organization schema group + Vendor schema group to calculation schema.")
            ],
            "sections": [
                ("Architecture of the Condition Technique", "Understanding the four-tier hierarchy: Condition Table, Access Sequence, Condition Type, and Calculation Schema."),
                ("Step-by-Step SPRO Customizing", "Configuring gross price PB00/PBXX, cash discounts, non-deductible taxes, and freight accruals in M/08."),
                ("Schema Determination & Vendor Groups", "Assigning schema groups in Vendor Business Partner (BP) Purchasing view and Purchasing Organization."),
                ("Troubleshooting Pricing Errors in POs", "Analyzing condition determination logs in ME21N/ME22N and fixing unpicked price records.")
            ],
            "faqs": [
                ("What is the difference between condition type PB00 and PBXX?", "PB00 is an automatic condition type connected to an access sequence that searches condition records from Purchase Info Records or Contracts. PBXX is a manual condition type without an access sequence, used when no master condition record exists."),
                ("How does SAP determine the calculation schema for a Purchase Order?", "SAP determines the schema using the Schema Group assigned to the Purchasing Organization and the Schema Group assigned to the Supplier (Vendor BP) under Purchasing Data, mapped in transaction OMF2."),
                ("Why does a freight condition require an accrual key?", "Delivery freight conditions (e.g. FRB1, FRA1) are paid to a separate forwarding agent rather than the main material vendor. The accrual key routes this cost into a freight clearing balance sheet account upon Goods Receipt (MIGO).")
            ]
        },
        {
            "title": "SAP MM Subcontracting Cycle with S/4HANA Special Stock 'O' Guide",
            "slug": "sap-mm-subcontracting-cycle-special-stock-o-guide",
            "badge": "SAP MM MASTERCLASS",
            "category": "Tutorial",
            "read_time": "13 min read",
            "keyword": "sap mm subcontracting process step by step movement type 541 101",
            "meta_desc": "Complete guide to SAP MM Subcontracting: Item Category L, Bill of Materials (BOM), Transfer Posting 541 to Special Stock 'O', Goods Receipt 101, and 543 consumption.",
            "role": "SAP MM / Sourcing Functional Consultant",
            "process_title": "End-to-End Subcontracting Lifecycle",
            "process_steps": [
                ("1. Subcontract PO", "Create Purchase Order with Item Category L and exploding component BOM (ME21N)"),
                ("2. Issue Components", "Transfer stock to subcontractor via Transfer Posting 541 (Special Stock 'O') in MIGO"),
                ("3. Monitor Vendor Stock", "Track inventory at subcontractor location via ME2O / MBLB"),
                ("4. Goods Receipt", "Post GR 101 for finished product; system auto-consumes raw materials with movement 543")
            ],
            "table_headers": ["Subcontracting Step", "Movement Type", "Inventory & Accounting Impact"],
            "table_rows": [
                ("Component Issue to Vendor", "541 (Non-valuated)", "Moves stock from Unrestricted to Vendor Special Stock 'O' (no FI document generated)."),
                ("Finished Product Receipt", "101 (Valuated)", "Debit: Finished Inventory (BSX), Credit: Subcontracting Service Clearing (WRX)."),
                ("Component Auto-Consumption", "543 (Valuated)", "Debit: Raw Material Consumption (GBB/VBO), Credit: Raw Material Inventory (BSX)."),
                ("Subsequent Adjustment", "544 / 543 (Credit/Debit)", "Adjusts component variance when actual consumed quantity differs from planned BOM quantity.")
            ],
            "sections": [
                ("Subcontracting Business Architecture", "How manufacturing companies outsource specialized processing while maintaining inventory visibility."),
                ("Master Data & BOM Configuration", "Setting up Subcontracting Info Record (PIR Category Subcontracting) and CS01 BOM Explosion."),
                ("Execution & Stock Transfer Mechanics", "Issuing components via ME2O/MIGO 541, tracking via MBLB, and handling scrap or by-products (movement 545)."),
                ("Financial Accounting & Subcontracting Settlement", "Understanding OBYC transaction keys BSX, WRX, GBB-VBO, and FRL (subcontracting services).")
            ],
            "faqs": [
                ("Does movement type 541 generate an accounting document?", "No. Movement 541 is a non-valuated transfer posting within the same plant. The stock still belongs to the enterprise, only the location changes to vendor custody (Special Stock 'O')."),
                ("How do you handle scrap or excess material consumed by the subcontractor?", "Use transaction MIGO with 'Subsequent Adjustment' (Movement 543 for excess consumption or 544 for component return) referencing the original Purchase Order."),
                ("What is the difference between item category L and subcontracting info record?", "Item category L in the PO line instructs SAP that the item is a subcontracted service and triggers BOM explosion. The subcontracting info record provides the specific service fee agreed upon with that vendor.")
            ]
        },
        {
            "title": "SAP MM OBYC Automatic Account Determination: S/4HANA Integration Blueprint",
            "slug": "sap-mm-obyc-account-determination-s4hana-guide",
            "badge": "SAP MM ADVANCED",
            "category": "Tutorial",
            "read_time": "15 min read",
            "keyword": "sap mm obyc automatic account determination s4hana bsx wrx gbb",
            "meta_desc": "Master SAP MM-FI integration via OBYC: Chart of Accounts, Valuation Class, Valuation Grouping Code (OMWD), Account Modification keys, and BSX, WRX, GBB, PRD keys.",
            "role": "SAP MM / FI Integration Specialist",
            "process_title": "OBYC Determination Sequence Flow",
            "process_steps": [
                ("1. Movement & Value String", "Goods movement triggers predefined value string (e.g., WA01 for GI 201)"),
                ("2. Valuation Grouping", "Plant maps to Valuation Grouping Code via OMWD (Chart of Accounts linkage)"),
                ("3. Valuation Class", "Material Master Accounting 1 view provides material Valuation Class"),
                ("4. OBYC Account Match", "System resolves exact G/L account from Transaction Key + Valuation Class + Modification Key")
            ],
            "table_headers": ["Transaction Key", "Posting Description", "Debited / Credited During"],
            "table_rows": [
                ("BSX (Inventory Posting)", "Balance sheet inventory account for valuated materials", "Debited on Goods Receipt (101); Credited on Goods Issue (201/261)."),
                ("WRX (GR/IR Clearing)", "Intermediary clearing account bridging logistics and finance", "Credited on Goods Receipt (101); Debited on Invoice Receipt (MIRO)."),
                ("GBB (Offsetting Entry)", "P&L consumption or inventory adjustment account", "Account modifications: VBR (cost centers), VBO (subcontracting), BSA (initial stock)."),
                ("PRD (Price Differences)", "Expense/revenue account capturing purchase price variance", "Debited/Credited when PO price differs from Standard Price (S) during GR/IR.")
            ],
            "sections": [
                ("The Architecture of MM-FI Integration", "How SAP links physical warehouse movements seamlessly to financial ledgers without manual journal vouchers."),
                ("Valuation Class & Account Category Reference", "Configuring OMSK: grouping material types and enforcing valid valuation classes."),
                ("Valuation Grouping Code & OMWD Customizing", "Enabling multi-plant valuation grouping under shared enterprise charts of accounts."),
                ("Troubleshooting M8147 & Posting Errors", "Resolving 'Account determination for entry XXXX not possible' error with structured debugging.")
            ],
            "faqs": [
                ("What does the error 'Account determination for entry INT BSX 0001 ____ 3000 not possible' mean?", "It means transaction key BSX in chart of accounts INT, valuation grouping 0001, and valuation class 3000 has no G/L account assigned in transaction OBYC."),
                ("What is the role of Account Modification keys in transaction key GBB?", "GBB is used for diverse offsetting entries. Account Modification keys (e.g. VBR for cost centers, VNG for scrap, VBO for subcontracting) allow assigning separate G/L accounts for different business events sharing the same movement group."),
                ("What happens to WRX balance at month-end?", "Any open balance in the WRX (GR/IR clearing) account represents goods received but not invoiced (or vice versa). It is analyzed via MR11 and reconciled using period-end clearing programs.")
            ]
        }
    ],
    "ewm": [
        {
            "title": "Difference Between POSC and LOSC in SAP EWM: Real-World Inbound vs Outbound Guide",
            "slug": "difference-between-posc-and-losc-sap-ewm-guide",
            "badge": "SAP EWM BLUEPRINT",
            "category": "Tutorial",
            "read_time": "14 min read",
            "keyword": "difference between posc and losc sap ewm inbound outbound storage control",
            "meta_desc": "In-depth architectural comparison between Process-Oriented (POSC) and Layout-Oriented (LOSC) Storage Control in SAP EWM with step-by-step customizing rules.",
            "role": "SAP EWM Solution Architect & Warehouse Designer",
            "process_title": "Combined POSC + LOSC Multi-Step Execution Flow",
            "process_steps": [
                ("1. External Step (POSC)", "Pallet unloaded from truck to receiving staging bay (IB01)"),
                ("2. Intermediate Transit (LOSC)", "Pallet routed through conveyor pickup/drop point (P&D) before decon center"),
                ("3. Work Center (POSC)", "Deconsolidation and sample quality inspection executed (IB02/IB03)"),
                ("4. Final Putaway (POSC)", "System determines final high-bay rack bin; creates final putaway task (IB04)")
            ],
            "table_headers": ["Comparison Criteria", "Process-Oriented Storage Control (POSC)", "Layout-Oriented Storage Control (LOSC)"],
            "table_rows": [
                ("Core Driving Factor", "Business Process Requirements (Unload, Decon, Quality, Pack).", "Physical Layout Constraints (Conveyors, P&D points, Elevators, Height restrictions)."),
                ("Object Level", "Executed at Handling Unit (HU) level across warehouse.", "Executed between Source and Destination Storage Bins/Types."),
                ("Step Nature", "Sequential business activities (Step 1 > Step 2 > Step 3).", "Physical routing detour bypassing architectural obstructions."),
                ("Customizing Location", "SPRO > EWM > Cross-Process Settings > Storage Control > POSC.", "SPRO > EWM > Cross-Process Settings > Storage Control > LOSC.")
            ],
            "sections": [
                ("Why Modern Warehouses Need Dual Storage Control", "Understanding business process steps vs physical layout detours in high-automation facilities."),
                ("Configuring POSC: Storage Processes & External Steps", "Defining Storage Process Definitions, External Steps (IB01-IB04), and assigning to warehouse process types."),
                ("Configuring LOSC: Intermediate Bins & Routing Detours", "Mapping source storage type, destination storage type, and intermediate conveyor P&D drop points."),
                ("Real-World Scenario: Can POSC and LOSC Work Together?", "Walkthrough of an automated distribution center where POSC deconsolidation requires an LOSC conveyor transfer.")
            ],
            "faqs": [
                ("Can a warehouse task have both POSC and LOSC active at the same time?", "Yes! POSC defines the logical business sequence (e.g. Unload -> Decon -> Putaway). When the HU moves from the receiving door to the decon station, LOSC can intercept that task to route it via an automated conveyor system."),
                ("Why does POSC require Handling Units (HUs)?", "POSC tracks status and routing history at the container level across multiple work centers. Because loose unpacked stock cannot hold routing status attributes, POSC strictly mandates Handling Units."),
                ("Which transaction is used to monitor POSC and LOSC tasks?", "The EWM Warehouse Management Monitor (/SCWM/MON) under Documents > Warehouse Task or Inbound > Handling Unit provides full real-time visibility into open and confirmed storage control steps.")
            ]
        },
        {
            "title": "SAP EWM Wave Management & Warehouse Order Creation Rules (WOCR) Blueprint",
            "slug": "sap-ewm-wave-management-wocr-blueprint-guide",
            "badge": "SAP EWM MASTERCLASS",
            "category": "Tutorial",
            "read_time": "15 min read",
            "keyword": "sap ewm wave management wocr configuration /scwm/wavet",
            "meta_desc": "Configure SAP EWM Wave Templates, capacity thresholds, release profiles, and Warehouse Order Creation Rules (WOCR) to bundle picking tasks for optimal warehouse throughput.",
            "role": "SAP EWM Functional Consultant & Fulfillment Architect",
            "process_title": "Outbound Wave Planning & WOCR Execution Lifecycle",
            "process_steps": [
                ("1. ODO Allocation", "Outbound Delivery Orders automatically assigned to Wave Templates via Condition Technique"),
                ("2. Wave Release", "Wave released automatically on schedule or manually in /SCWM/WAVE"),
                ("3. WT Generation", "Warehouse Tasks generated based on removal strategies and stock determination"),
                ("4. WOCR Bundling", "WOCR filters and groups tasks into ergonomically sized Warehouse Orders for pickers")
            ],
            "table_headers": ["WOCR Configuration Element", "Customizing Activity in SPRO", "Operational Impact on Pickers"],
            "table_rows": [
                ("Activity Area Filtering", "Assign Activity Areas to WOCR", "Restricts tasks in one WO to a specific aisle or zone, preventing cross-warehouse walking."),
                ("Limit Values Profile", "Define Limit Values for WO", "Caps WO size by maximum weight (e.g. 500 kg), volume (e.g. 2 m3), or pick item count."),
                ("Consolidation Group Profile", "Define Consolidation Profile", "Ensures items shipping to the same customer, route, or loading dock door stay grouped together."),
                ("Packaging Specification", "Assign Pack Spec to WOCR", "Instructs picker which pick-handling unit (pallet/tote) to construct during pick-pack operations.")
            ],
            "sections": [
                ("Wave Planning Architecture", "Understanding cutoff times, release methods, and wave templates (/SCWM/WAVET) in fulfillment centers."),
                ("Wave Determination Condition Technique", "Configuring table condition records based on shipping route, priority, and freight carrier in /SCWM/WDGCM."),
                ("WOCR Engineering & Filter Rules", "Constructing Item Filters, Limit Rules, Consolidation Profiles, and Pick-Pack-Pass logic."),
                ("Warehouse Monitor Operations & Triage", "Supervising wave progress, unreleased items, and labor assignment using /SCWM/MON.")
            ],
            "faqs": [
                ("What is the difference between a Warehouse Task (WT) and a Warehouse Order (WO)?", "A Warehouse Task is a line-item instruction to move a specific quantity of a product from a source bin to a destination bin. A Warehouse Order is an executable bundle of multiple Warehouse Tasks assigned to a single warehouse worker."),
                ("Why does a wave fail to release with an error 'No stock found'?", "Common causes include insufficient stock in the source storage type, stock locked by an open physical inventory document, stock reserved by another wave, or an incorrect stock removal search sequence."),
                ("How does Pick-Pack-Pass work in SAP EWM?", "Pick-Pack-Pass divides picking across consecutive activity areas. Worker 1 picks items in Zone A into a tote, passes it to Worker 2 in Zone B who adds more items, until the order is completely fulfilled and handed over to packing.")
            ]
        }
    ],
    "sd": [
        {
            "title": "SAP SD Pricing Procedure & Condition Technique: Complete Step-by-Step Guide",
            "slug": "sap-sd-pricing-procedure-condition-technique-guide",
            "badge": "SAP SD MASTERCLASS",
            "category": "Tutorial",
            "read_time": "15 min read",
            "keyword": "sap sd pricing procedure configuration step by step condition technique v/08 ovkk",
            "meta_desc": "Step-by-step configuration of SAP SD Pricing Procedure: Condition Tables (V/03), Access Sequences (V/07), Condition Types (V/06), Pricing Schema (V/08), and Determination (OVKK).",
            "role": "SAP SD Functional Consultant & Pricing Lead",
            "process_title": "SD Pricing Procedure Determination Flow",
            "process_steps": [
                ("1. Condition Tables", "Define key combinations (e.g. Customer + Material) via V/03"),
                ("2. Access Sequences", "Set search priority order from most specific to general via V/07"),
                ("3. Pricing Procedure", "Build mathematical schema with Base Price PR00, Discounts K004/K007, and MWST via V/08"),
                ("4. Determination (OVKK)", "Map Sales Org + Dist Channel + Division + Doc Pricing + Cust Pricing to Schema")
            ],
            "table_headers": ["Pricing Component", "Transaction Code / SPRO Path", "Customizing Significance"],
            "table_rows": [
                ("Condition Tables", "V/03, V/04, V/05", "Defines relational keys for pricing master data records (stored in tables A001-A999)."),
                ("Condition Types", "V/06", "Configures calculation type (percentage, fixed, quantity), plus/minus sign, and manual changes."),
                ("Calculation Schema", "V/08", "Defines step numbers, from-to reference ranges, subtotal keys, and requirement routines."),
                ("Pricing Determination", "OVKK", "Determines the active pricing procedure during sales order creation based on organizational and master data keys.")
            ],
            "sections": [
                ("The Architecture of SD Pricing", "How the SAP Condition Technique calculates dynamic prices, freight, discounts, and statutory taxes in milliseconds."),
                ("Step-by-Step Customizing in SPRO", "Configuring condition types (PR00, K004, RA00, KF00, MWST), access sequences, and calculation schema rules."),
                ("Pricing Determination Parameters (OVKK)", "Aligning Sales Area, Document Pricing Procedure (from Order Type), and Customer Pricing Procedure (from BP)."),
                ("VKOA Revenue Account Determination", "Connecting SD billing condition types to FI revenue accounts (KOFI/KOFN) in the General Ledger.")
            ],
            "faqs": [
                ("How does SAP determine which pricing procedure to trigger in a Sales Order?", "Via transaction OVKK, using 5 key parameters: Sales Organization + Distribution Channel + Division + Document Pricing Procedure (assigned to the Sales Document Type) + Customer Pricing Procedure (assigned to the Customer Master BP)."),
                ("What is the purpose of the 'Requirement' column in transaction V/08?", "A Requirement is an ABAP routine that checks whether a condition type should be executed. For example, Requirement 002 ensures that discount conditions are only calculated if a net value already exists."),
                ("What is the difference between Condition Exclusion and Condition Update?", "Condition Exclusion determines which discount wins when multiple conflicting discounts apply (e.g. Best Price vs Lowest Price). Condition Update limits a condition record to a maximum cumulative value or quantity across multiple orders.")
            ]
        },
        {
            "title": "SAP S/4HANA Order-to-Cash (O2C) Process Flow with FI Integration Guide",
            "slug": "sap-s4hana-order-to-cash-o2c-process-guide",
            "badge": "SAP SD BLUEPRINT",
            "category": "Tutorial",
            "read_time": "14 min read",
            "keyword": "sap s4hana order to cash o2c process flow fi integration vkoa",
            "meta_desc": "Comprehensive walkthrough of the end-to-end SAP S/4HANA Order-to-Cash (O2C) cycle: Inquiries, Sales Orders (VA01), Outbound Deliveries (VL01N), PGI, Billing (VF01), and AR Clearing.",
            "role": "SAP SD / O2C Solution Architect",
            "process_title": "End-to-End Order-to-Cash (O2C) Process Flow",
            "process_steps": [
                ("1. Sales Order Creation", "Order booked in VA01 or Fiori Create Sales Orders; triggers ATP check & pricing"),
                ("2. Outbound Delivery", "Shipping creates Outbound Delivery via VL01N; determines shipping point and route"),
                ("3. Picking & Post Goods Issue", "Warehouse picks items; Post Goods Issue (PGI) triggers inventory reduction (movement 601)"),
                ("4. Billing & Financial Posting", "Billing document created in VF01; auto-generates FI invoice in Accounts Receivable (ACDOCA)")
            ],
            "table_headers": ["O2C Process Phase", "Standard T-Code / Fiori App", "Accounting & Inventory Impact"],
            "table_rows": [
                ("Sales Order", "VA01 / Fiori Manage Sales Orders", "No inventory or FI postings; commits availability ATP and sets credit limit check."),
                ("Outbound Delivery", "VL01N / VL10A", "No financial impact; creates delivery document and staging requirement."),
                ("Post Goods Issue (PGI)", "VL02N (Movement Type 601)", "Debit: Cost of Goods Sold (COGS), Credit: Inventory Account (BSX)."),
                ("Billing Document", "VF01 / Fiori Create Billing Documents", "Debit: Customer Account (AR), Credit: Domestic Revenue (ERL via VKOA), Credit: Tax (MWS).")
            ],
            "sections": [
                ("End-to-End O2C Process Architecture", "Understanding the complete document flow from customer inquiry to cash settlement in S/4HANA."),
                ("Availability Checking (ATP) & Backorder Processing", "How Advanced ATP (aATP) in S/4HANA evaluates product allocation, supply protection, and substitute plants."),
                ("Shipping Point & Route Determination Customizing", "Configuring shipping point determination (Shipping Conditions + Loading Group + Plant) in SPRO."),
                ("Revenue Account Determination (VKOA)", "Connecting SD billing condition types to FI revenue accounts (KOFI/KOFN) in the General Ledger.")
            ],
            "faqs": [
                ("What are the financial accounting entries generated at Post Goods Issue (PGI)?", "Debit Cost of Goods Sold (COGS) account and Credit Inventory (Balance Sheet) account with Movement Type 601."),
                ("How does Shipping Point Determination work in SAP SD?", "SAP determines the shipping point in the sales order using 3 parameters: Shipping Condition (from Customer Master BP) + Loading Group (from Material Master Sales General/Plant view) + Delivering Plant."),
                ("What causes the error 'Account determination for entry XXXX KOFI not possible' during billing?", "This error occurs in transaction VKOA when there is no matching G/L account configured for the billing condition type, Chart of Accounts, Sales Org, Customer Account Assignment Group, or Material Account Assignment Group.")
            ]
        }
    ],
    "fico": [
        {
            "title": "SAP S/4HANA Universal Journal (ACDOCA): Architecture & Configuration Guide",
            "slug": "sap-s4hana-universal-journal-acdoca-guide",
            "badge": "SAP FICO BLUEPRINT",
            "category": "Tutorial",
            "read_time": "14 min read",
            "keyword": "sap s4hana universal journal acdoca configuration fi co integration",
            "meta_desc": "Deep dive into the SAP S/4HANA Universal Journal (Table ACDOCA): Single source of truth, elimination of reconciliation between FI and CO, extension ledgers, and multi-GAAP reporting.",
            "role": "SAP FICO Lead Consultant & Financial Architect",
            "process_title": "Universal Journal (ACDOCA) Data Flow",
            "process_steps": [
                ("1. Operational Event", "Logistics, sales, or financial transaction executed in S/4HANA"),
                ("2. Real-Time Posting", "Engine writes unified header (BKPF) and unified multi-dimensional line item (ACDOCA)"),
                ("3. Multi-GAAP Allocation", "Parallel ledgers (Leading 0L, Non-Leading 2L) evaluate IFRS vs Local GAAP rules"),
                ("4. Instant Analytics", "Eliminates batch reconciliation jobs; enables real-time P&L and balance sheet reporting")
            ],
            "table_headers": ["Legacy ECC Architecture", "S/4HANA Universal Journal (ACDOCA)", "Architectural Benefit"],
            "table_rows": [
                ("Separate FI and CO Tables (BSEG, BSIS, COEP)", "Single Unified Table: ACDOCA (Universal Journal)", "Eliminates reconciliation runs between FI and CO; provides unified reporting."),
                ("Separate Asset Accounting (ANEP, ANLP)", "Direct line-item integration into ACDOCA", "Real-time asset depreciation postings without separate batch settlement."),
                ("Separate Material Ledger (MLCD, MLIT)", "Material Ledger entries written directly to ACDOCA", "Instant multi-currency inventory valuation and actual costing transparency."),
                ("Separate Profitability Analysis (CE1XXXX)", "Margin Analysis (Account-Based CO-PA) in ACDOCA", "Derives profitability segments in real-time with full G/L audit trail.")
            ],
            "sections": [
                ("Why SAP Built the Universal Journal", "The structural shortcomings of classic ECC databases and the revolution of the single table of truth."),
                ("Ledger Architecture: Leading, Non-Leading & Extension Ledgers", "Configuring parallel accounting under multiple valuation frameworks (IFRS, US GAAP, Local GAAP)."),
                ("FI-CO Real-Time Integration & Cost Element Unification", "How Secondary Cost Elements became G/L accounts and eliminated KALC reconciliation."),
                ("Reporting & Universal Journal Performance Tuning", "Optimizing CDS view queries and leveraging SAP Fiori apps for real-time financial close.")
            ],
            "faqs": [
                ("Does Table BSEG still exist in SAP S/4HANA?", "Yes, BSEG still exists for document entry and open-item management, but ACDOCA is the primary reporting and analytics table containing all financial, controlling, asset, and material ledger dimensions."),
                ("What is an Extension Ledger in S/4HANA Finance?", "An Extension Ledger is a ledger that references an underlying base ledger (e.g. Leading Ledger 0L). It stores delta adjustments (such as management forecasts, tax adjustments, or simulated entries) without duplicating base data."),
                ("How does S/4HANA eliminate the need for the FI-CO reconciliation ledger?", "In S/4HANA, every internal controlling posting (such as cost center allocations) is simultaneously written as an ACDOCA entry with unified G/L accounts, ensuring FI and CO are always in 100% real-time balance.")
            ]
        },
        {
            "title": "SAP FICO Document Splitting Configuration: Active, Passive & Zero-Balance Guide",
            "slug": "sap-fico-document-splitting-configuration-guide",
            "badge": "SAP FICO MASTERCLASS",
            "category": "Tutorial",
            "read_time": "15 min read",
            "keyword": "sap fico document splitting configuration active passive zero balance",
            "meta_desc": "Comprehensive guide to configuring Document Splitting in SAP S/4HANA Finance: Active Splitting, Passive Splitting, Zero-Balance Clearing, and Business Segment reporting.",
            "role": "SAP FICO Functional Consultant & General Ledger Lead",
            "process_title": "Document Splitting Processing Sequence",
            "process_steps": [
                ("1. Item Classification", "Classify G/L accounts and Document Types into business categories in SPRO"),
                ("2. Passive Splitting", "System inherits profit center / segment from preceding document reference (e.g. PO/GR)"),
                ("3. Active Splitting", "System applies rule-based splitting proportionally based on expense line allocations"),
                ("4. Zero-Balance Clearing", "Generates balancing clearing lines if debit/credit differs by segment or profit center")
            ],
            "table_headers": ["Splitting Method", "Trigger Mechanism", "Typical Business Use Case"],
            "table_rows": [
                ("Active (Rule-Based) Splitting", "Splitting rules defined in customizing (SPRO)", "Splitting vendor invoice line items proportionally across multiple department expense accounts."),
                ("Passive Splitting", "Inherited from preceding referenced document", "Clearing a vendor payment (F-53) inheriting the profit center from the original vendor invoice."),
                ("Zero-Balance Clearing", "Activated for specific split characteristics (Segment/Profit Center)", "Creates automated balancing debit/credit lines ensuring each segment balances to zero independently.")
            ],
            "sections": [
                ("Why Document Splitting is Mandatory for Segment Reporting", "Meeting IFRS 8 / US GAAP segment reporting mandates without manual reconciliation at period close."),
                ("Step-by-Step Customizing in SPRO", "Classifying G/L Accounts, Classifying Document Types, Defining Splitting Methods, and Assigning Rules."),
                ("Configuring Zero-Balance Clearing Accounts", "Setting up transaction key 000 for automatic balance sheet inter-segment balancing."),
                ("Troubleshooting Document Splitting Errors", "Solving GLT2201 'There is no item category assigned to account XXXX' and activation hazards.")
            ],
            "faqs": [
                ("What is the primary objective of Document Splitting in SAP Finance?", "To generate complete, balanced balance sheet and P&L financial statements at lower organizational levels than Company Code—specifically for Profit Center and Business Segment."),
                ("What does the error 'GLT2201: There is no item category assigned to account XXXX' indicate?", "It means a newly created G/L account involved in a financial posting has not been classified under SPRO > Financial Accounting > General Ledger Accounting > Business Transactions > Document Splitting > Classify G/L Accounts for Document Splitting."),
                ("Can Document Splitting be activated after a system goes live?", "Document splitting can only be activated post go-live via a specialized SAP Migration Service / Migration Cockpit procedure, because all existing historical open items must be enriched with segment characteristics.")
            ]
        }
    ],
    "joule": [
        {
            "title": "SAP Joule AI in S/4HANA Logistics & Procurement: 2026 Architect Blueprint",
            "slug": "sap-joule-ai-s4hana-logistics-procurement-blueprint",
            "badge": "SAP JOULE AI 2026",
            "category": "Technology",
            "read_time": "14 min read",
            "keyword": "sap joule ai s4hana mm ewm generative ai copilot 2026",
            "meta_desc": "Explore how SAP Joule and autonomous AI agents transform S/4HANA 2026: Natural language procurement triage, automated EWM wave replenishment, and Clean Core AI extensibility.",
            "role": "SAP AI Solution Architect & Logistics Transformation Lead",
            "process_title": "SAP Joule Autonomous Agent Execution Cycle",
            "process_steps": [
                ("1. Natural Language Prompt", "User asks Joule in Fiori: 'Analyze overdue purchase orders for Plant 1010 and suggest alternate suppliers'"),
                ("2. Grounded Context Engine", "Joule queries S/4HANA business semantics, supplier scorecards, and open PO status securely"),
                ("3. Agentic Evaluation", "Autonomous procurement agent evaluates supplier capacity and historical delivery reliability"),
                ("4. Actionable Execution", "Joule presents one-click PO amendment with audit trail and Clean Core compliance")
            ],
            "table_headers": ["Operational Area", "Legacy Manual Execution", "Joule AI Agentic Execution (S/4HANA 2026)"],
            "table_rows": [
                ("Procure-to-Pay (P2P)", "Manual review of ME2N / MD04 exception lists across multiple plants.", "Joule triages unassigned requisitions and auto-recommends optimal contracted suppliers."),
                ("Warehouse Management (EWM)", "Supervisors monitor /SCWM/MON manually to identify bottlenecked picking waves.", "Autonomous agents detect warehouse capacity thresholds and trigger dynamic wave replenishment."),
                ("SPRO Configuration Lookup", "Consultants search thousands of IMG nodes to locate customizing tables.", "Consultants ask Joule: 'How do I configure POSC deconsolidation?' and get exact paths with prerequisite checks."),
                ("Variance Resolution (FI/MM)", "Accounts payable manually investigates invoice price/quantity discrepancies.", "Joule inspects 3-way match, flags root cause (freight variance), and drafts supplier resolution note.")
            ],
            "sections": [
                ("The Architecture of SAP Joule", "How SAP's generative and agentic AI operates within the enterprise security context and business data cloud."),
                ("Autonomous Procurement Workflows in S/4HANA MM", "Conversational purchase requisition approvals, supplier risk monitoring, and intelligent contract compliance."),
                ("AI-Driven Warehouse Operations in S/4HANA EWM", "Predictive slotting recommendations, dynamic wave cut-off adjustments, and exception triage in /SCWM/MON."),
                ("Clean Core Alignment & Custom AI Agents", "Extending Joule using SAP Build Code, Generative AI Hub, and Developer Extensibility without modifying the core.")
            ],
            "faqs": [
                ("Is SAP Joule a generic chatbot or grounded in business data?", "Joule is a context-aware enterprise copilot deeply grounded in SAP's semantic data model. It respects user authorizations, role-based access control (RBAC), and enterprise security protocols."),
                ("Can Joule perform transactions or only answer questions?", "In S/4HANA 2026, Joule has evolved from an informational assistant to an Agentic AI capable of executing actions—such as updating delivery dates, releasing purchase orders, or initiating warehouse replenishment tasks—with user confirmation."),
                ("How does Joule adhere to SAP's Clean Core strategy?", "Joule operates via standard SAP APIs, CDS views, and SAP Business Technology Platform (BTP). It does not require custom ABAP modifications to the ERP core, ensuring seamless cloud upgrades.")
            ]
        },
        {
            "title": "SAP Joule Copilot for Financial Close & Variance Analysis (FICO 2026 Guide)",
            "slug": "sap-joule-copilot-financial-close-variance-analysis-guide",
            "badge": "SAP JOULE AI 2026",
            "category": "Technology",
            "read_time": "13 min read",
            "keyword": "sap joule ai fico financial close variance analysis s4hana 2026",
            "meta_desc": "How SAP Joule Copilot and GenAI agents accelerate the financial close in S/4HANA Finance: Real-time P&L variance explanation, automated accruals, and audit trail generation.",
            "role": "SAP Finance Transformation Lead & Financial Controller",
            "process_title": "Joule AI Financial Close Acceleration Flow",
            "process_steps": [
                ("1. Anomaly Detection", "Joule monitors ACDOCA in real-time during period-end close and flags cost center variances exceeding threshold"),
                ("2. Context Synthesis", "Agent analyzes underlying POs, Goods Receipts, and vendor invoices to isolate variance driver"),
                ("3. Executive Narrative", "Generates human-readable variance commentary explaining why budget was exceeded"),
                ("4. Auditor Sign-Off", "Attaches transparent reasoning and evidence trail directly to financial closing cockpit")
            ],
            "table_headers": ["Financial Close Step", "Traditional Close Process", "Joule-Augmented Autonomous Close"],
            "table_rows": [
                ("P&L Variance Analysis", "Controllers export data to Excel; spend days investigating cost center variances.", "Joule auto-generates root cause summaries in seconds linking ACDOCA line items."),
                ("Purchase Order Accruals", "Manual estimation of unbilled goods and services.", "AI agents predict unbilled accruals based on historical patterns and project milestones."),
                ("Intercompany Reconciliation", "Manual matching of intercompany balances across legal entities.", "Automated continuous matching with conversational discrepancy resolution."),
                ("Audit Documentation", "Manual compilation of email threads, PO copies, and approvals for external auditors.", "Audit-ready evidence dossier compiled automatically with complete cryptographic provenance.")
            ],
            "sections": [
                ("The Modern Continuous Financial Close", "Transforming month-end from a high-stress 10-day crunch into an automated, continuous operational rhythm."),
                ("Automating Variance Explanations in S/4HANA Finance", "How Joule interprets complex Multi-GAAP Universal Journal postings and generates board-ready narratives."),
                ("Intelligent Accruals & Payment Run Automation", "Leveraging machine learning models in F110 payment runs and intelligent cash matching."),
                ("Governance, Security & Audit Readiness", "Ensuring AI-generated financial explanations satisfy global compliance standards (SOX, IFRS, GAAP).")
            ],
            "faqs": [
                ("How does Joule explain financial variances to controllers?", "Joule analyzes line items in Table ACDOCA, compares actual postings against planned budget condition records, identifies the primary deviation driver (such as raw material inflation or unpredicted overtime), and summarizes the findings in plain business language."),
                ("Can Joule help with the SAP Financial Closing Cockpit?", "Yes. Joule integrates with SAP S/4HANA Cloud for Advanced Financial Closing, automatically checking task prerequisites, executing unattended batch programs, and alerting controllers only when genuine exceptions occur."),
                ("Is financial data sent to external AI models during Joule queries?", "No. SAP Joule utilizes the SAP Generative AI Hub on SAP BTP with strict enterprise data isolation, ensuring customer financial data is never used to train external public foundation models.")
            ]
        }
    ]
}

def get_published_slugs() -> set:
    """Returns set of all slugs currently published on the website."""
    slugs = set()
    custom_blogs_js = os.path.join(BLOG_DIR, "custom-blogs.js")
    if os.path.exists(custom_blogs_js):
        with open(custom_blogs_js, "r", encoding="utf-8") as f:
            content = f.read()
            for mod_topics in TOPIC_DATABASE.values():
                for t in mod_topics:
                    if t["slug"] in content:
                        slugs.add(t["slug"])
    if os.path.exists(BLOG_DIR):
        for fname in os.listdir(BLOG_DIR):
            if fname.endswith(".html"):
                slugs.add(fname[:-5])
    return slugs

def discover_trending_topic(preferred_module: Optional[str] = None) -> Dict:
    """
    Selects or synthesizes the highest-intent SEO topic across target modules:
    MM, EWM, SD, FICO, and Joule AI.
    Integrates live Google queries and deduplicates against already published blogs.
    """
    published_slugs = get_published_slugs()

    target_modules = [preferred_module] if preferred_module and preferred_module in MODULES else MODULES
    # Prioritize module selection
    selected_module = random.choice(target_modules)
    
    # 1. Check if un-published curated topics exist for this module
    available_curated = [
        t for t in TOPIC_DATABASE.get(selected_module, [])
        if t["slug"] not in published_slugs
    ]

    if available_curated:
        chosen = random.choice(available_curated)
        chosen["module"] = selected_module
        return chosen

    # 2. If curated topics for that module are all published, check other modules
    for mod in MODULES:
        available_curated = [
            t for t in TOPIC_DATABASE.get(mod, [])
            if t["slug"] not in published_slugs
        ]
        if available_curated:
            chosen = random.choice(available_curated)
            chosen["module"] = mod
            return chosen

    # 3. Dynamic Procedural Synthesizer with Live Google Search Suggestions
    return synthesize_live_seo_topic(selected_module, published_slugs)

def synthesize_live_seo_topic(module: str, published_slugs: set) -> Dict:
    """
    Autonomous fallback engine that queries Google Suggest live and procedurally
    synthesizes a high-ranking, technically rigorous SAP article when pools are exhausted.
    """
    meta = MODULE_META.get(module, MODULE_META["mm"])
    
    # Search seeds for Google Suggest
    seed_queries = {
        "mm": ["sap mm configuration guide", "sap mm interview questions scenario", "sap mm p2p troubleshooting", "sap mm valuation class"],
        "ewm": ["sap ewm wave release error", "sap ewm posc vs losc difference", "sap ewm putaway strategy configuration", "sap ewm rfui transaction"],
        "sd": ["sap sd pricing procedure step by step", "sap sd condition technique access sequence", "sap sd order to cash cycle fiori", "sap sd vkoa error"],
        "fico": ["sap fico document splitting configuration", "sap fico universal journal acdoca differences", "sap fico new asset accounting afab", "sap fico mm fi integration obyc"],
        "joule": ["sap joule ai s4hana 2026 use cases", "sap joule generative ai copilot logistics", "sap joule procurement autonomous agents", "sap joule clean core btp"]
    }

    seeds = seed_queries.get(module, seed_queries["mm"])
    selected_seed = random.choice(seeds)
    google_suggestions = fetch_google_suggestions(selected_seed)

    # Use Google suggestion if available, else derive from seed
    best_phrase = google_suggestions[0] if google_suggestions else selected_seed
    clean_title_phrase = best_phrase.title().replace("Sap", "SAP").replace("Fi", "FI").replace("Sd", "SD").replace("Mm", "MM").replace("Ewm", "EWM").replace("Fico", "FICO").replace("Ai", "AI")
    
    year = 2026
    slug_suffix = int(time.time()) % 100000
    slug_base = best_phrase.lower().replace(" ", "-").replace("/", "-")
    slug = f"{slug_base}-{slug_suffix}"
    
    title = f"{clean_title_phrase}: S/4HANA {year} Enterprise Blueprint"

    return {
        "module": module,
        "title": title,
        "slug": slug,
        "badge": meta["badge"],
        "category": meta["category"],
        "read_time": f"{random.randint(12, 16)} min read",
        "keyword": best_phrase.lower(),
        "meta_desc": f"Complete {year} enterprise guide on {best_phrase}: Architectural concepts, SPRO configuration steps, S/4HANA business impact, and consultant troubleshooting blueprints.",
        "role": meta["default_role"],
        "process_title": f"Operational Execution Flow: {clean_title_phrase}",
        "process_steps": [
            ("1. Business Requirements", f"Map enterprise business process parameters into {meta['name']} specifications"),
            ("2. Master Data & SPRO", "Configure condition tables, master parameters, and organizational units in IMG"),
            ("3. Document Execution", "Execute transactional test cycle (Order/Task/Movement/Posting) in sandbox"),
            ("4. Validation & Close", "Verify financial reconciliation, audit logs, and Clean Core compatibility")
        ],
        "table_headers": ["Step / Customizing Node", "T-Code / SPRO Menu Path", "Key Function & Best Practice"],
        "table_rows": [
            ("Customizing Definition", "SPRO Reference IMG", f"Configure primary parameters for {clean_title_phrase}."),
            ("Master Data Realignment", "Master Data Transaction / Fiori", "Align business partner, material, or warehouse master records."),
            ("Transactional Execution", "Document Processing Transaction", "Verify document flow, financial entries, and status updates."),
            ("Monitoring & Audit", "Operational Monitor / Table Analysis", "Verify consistent ledger postings and exception-free logs.")
        ],
        "sections": [
            (f"Core Architecture: {clean_title_phrase}", f"Understanding how {best_phrase} integrates into modern S/4HANA supply chain and financial architecture."),
            ("Step-by-Step Customizing in SPRO", "Detailed configuration paths, prerequisite tables, and parameter settings for implementation leads."),
            ("Integration with Cross-Module Workflows", f"Analyzing how {meta['name']} shares transactional and financial data across enterprise modules."),
            ("Troubleshooting & Real-World Best Practices", "Diagnosing common system errors, missing table entries, and optimization techniques.")
        ],
        "faqs": [
            (f"What is the business purpose of {best_phrase}?", f"It provides structured, automated control over enterprise operations within {meta['name']}, ensuring strict compliance, auditability, and optimal execution speed."),
            (f"How do you troubleshoot errors related to {best_phrase}?", "Inspect configuration settings in SPRO, verify master data integrity, check system error logs in SM21 or qRFC monitor, and validate authorization objects."),
            ("How does this align with S/4HANA Clean Core strategy?", "By utilizing standard SAP BAPIs, released CDS views, and Key User Extensibility rather than modifying standard SAP tables directly.")
        ]
    }

if __name__ == "__main__":
    print("==================================================")
    print("🔍 TESTING LIVE GOOGLE SUGGEST QUESTION RESEARCHER")
    print("==================================================")
    for m in MODULES:
        meta = MODULE_META[m]
        print(f"\n📌 Testing Module: {meta['name']}")
        topic = discover_trending_topic(m)
        print(f"  • Title      : {topic['title']}")
        print(f"  • Slug       : {topic['slug']}")
        print(f"  • Keyword    : {topic['keyword']}")
        print(f"  • Badge      : {topic['badge']}")
        print(f"  • FAQs Count : {len(topic.get('faqs', []))}")
