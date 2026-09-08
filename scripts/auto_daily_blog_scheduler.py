#!/usr/bin/env python3
"""
Fully Automated Twice-Daily Content Research, Generation & SEO Publishing System
theTechMentor (youronementor.com) - SAP MM, EWM & S/4HANA Logistics
Adheres to AGENTS.md Universal Blog Standards
"""

import os
import sys
import json
import time
import datetime
import random
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(BASE_DIR, "blog")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
AUTOMATION_LOG = os.path.join(LOGS_DIR, "daily_automation.log")

# Expansive Master Topic Pool for Autonomous Twice-Daily Publishing
TOPIC_POOL = [
    {
        "title": "SAP MM Batch Management & S/4HANA Batch Determination Masterclass",
        "slug": "sap-mm-batch-management-determination-s4hana-guide",
        "category": "Tutorial",
        "badge": "SAP MM MASTERCLASS",
        "read_time": "13 min read",
        "keyword": "sap mm batch management configuration s4hana",
        "meta_desc": "Comprehensive configuration guide for SAP MM Batch Management, Batch Determination condition tables, S/4HANA classification, and expiration date checks.",
        "role": "SAP MM Functional Consultant / Inventory Specialist",
        "process_title": "End-to-End Batch Management & Determination Workflow",
        "process_steps": [
            ("1. Master Setup", "Activate Batch at Client/Plant/Material level & assign Class (023)"),
            ("2. Strategy Types", "Define Condition Tables & Access Sequences in SPRO"),
            ("3. Batch Inbound", "Post Goods Receipt (101) with Auto Batch Numbering & SLED"),
            ("4. Auto Allocation", "Trigger Auto Batch Determination in Outbound Delivery / Goods Issue")
        ],
        "table_headers": ["Customizing Step", "SPRO Path / Transaction Code", "Key Configuration Details"],
        "table_rows": [
            ("Specify Batch Level", "SPRO > Logistics General > Batch Management > Specify Batch Level", "Set Batch Level to Plant or Material level (Material level recommended in S/4HANA)."),
            ("Batch Class & Characteristics", "Transactions CT04 & CL02 (Class Type 023)", "Create characteristics for SLED, Production Date, and Country of Origin."),
            ("Condition Tables & Access Sequences", "SPRO > Logistics General > Batch Determination > Strategy Types", "Configure strategy type ME01 (Purchasing) or IM01 (Inventory Movements)."),
            ("Search Procedure Determination", "SPRO > Batch Determination > Batch Search Procedure Allocation", "Assign search procedure to movement types (e.g., 201, 261, 311, 541).")
        ],
        "sections": [
            ("Batch Level Architecture", "Understanding Client-Level, Plant-Level, and Material-Level Batch Architecture in S/4HANA"),
            ("Classification Engine", "Configuring Class Type 023, SLED, Manufacturing Date, and Valuation Characteristics"),
            ("Strategy & Condition Technique", "Creating Strategy Types, Access Sequences, and Condition Records for Automatic Allocation"),
            ("Execution & Troubleshooting", "Handling Split Batches in MIGO, Expiry Date Checks, and Solving Missing Batch Search Procedures")
        ]
    },
    {
        "title": "SAP EWM Wave Management & Warehouse Order Creation Rules (WOCR)",
        "slug": "sap-ewm-wave-management-wocr-deep-dive",
        "category": "Tutorial",
        "badge": "SAP EWM BLUEPRINT",
        "read_time": "14 min read",
        "keyword": "sap ewm wave management wocr configuration",
        "meta_desc": "Deep dive into SAP EWM Wave Templates, capacity thresholds, release methods, and Warehouse Order Creation Rules (WOCR) for high-throughput distribution.",
        "role": "SAP EWM Solution Architect & Logistics Lead",
        "process_title": "Automated Wave Planning & Execution Lifecycle",
        "process_steps": [
            ("1. Outbound Request", "Outbound Delivery Order (ODO) created in EWM via ERP Interface"),
            ("2. Wave Assignment", "Condition technique maps ODO items into active Wave Template"),
            ("3. Wave Release", "Automatic or manual release creates picking Warehouse Tasks (WTs)"),
            ("4. WOCR Bundling", "Warehouse Order Creation Rules bundle WTs into optimal Warehouse Orders")
        ],
        "table_headers": ["WOCR Configuration Element", "Customizing Activity", "Warehouse Impact"],
        "table_rows": [
            ("Activity Area Filtering", "/SCWM/WOCR Setup", "Filters tasks by pick area to prevent cross-aisle travel inefficiencies."),
            ("Limit Rules", "Define Limit Values for WO", "Caps order size by maximum weight (kg), volume (m3), or task count."),
            ("Consolidation Group", "Define Consolidation Profile", "Ensures deliveries to the same route or customer are grouped into one WO."),
            ("Packaging Specification", "Assign Pack Spec to WOCR", "Directs pickers to deposit items directly onto target shipping pallets.")
        ],
        "sections": [
            ("Wave Template Customizing", "Defining Cut-off Times, Release Profiles, and Capacity Thresholds in /SCWM/WAVET"),
            ("Condition Technique for Waves", "Configuring Determination Tables (/SCWM/WDGCM) based on Route, Carrier, and Priority"),
            ("WOCR Architecture", "Item Filters, Limit Rules, Consolidation Groups, and Pick-Pack-Pass Logic"),
            ("Production Optimization", "Monitoring Wave Progress in /SCWM/MON and Troubleshooting Unreleased Waves")
        ]
    },
    {
        "title": "SAP S/4HANA Flexible Workflow for Purchase Orders: Modern Approval Architecture",
        "slug": "sap-s4hana-flexible-workflow-purchase-orders-guide",
        "category": "Tutorial",
        "badge": "S/4HANA 2026",
        "read_time": "12 min read",
        "keyword": "sap s4hana flexible workflow purchase orders me21n fiori",
        "meta_desc": "Step-by-step setup of SAP S/4HANA Flexible Workflow for Purchase Orders, replacing legacy Release Strategy (ME28) with Fiori Manage Workflows.",
        "role": "SAP MM Functional Consultant & Workflow Specialist",
        "process_title": "Modern PO Approval Flow with Flexible Workflow",
        "process_steps": [
            ("1. PO Creation", "Buyer creates Purchase Order in ME21N or Fiori Manage Purchase Orders"),
            ("2. Rule Evaluation", "Workflow engine evaluates preconditions (Company Code, Net Amount, Pur Group)"),
            ("3. Step Routing", "Fiori notification dispatched to Approver 1 (Cost Center Manager)"),
            ("4. Final Release", "Approval triggers automatic PO release and output generation (BRFplus)")
        ],
        "table_headers": ["Flexible Workflow Component", "Fiori App / SPRO Node", "Configuration Objective"],
        "table_rows": [
            ("Workflow Scenario Definition", "SWDD_SCENARIO (WS00800238)", "Standard SAP S/4HANA Purchase Order approval workflow template."),
            ("Fiori Configuration App", "Manage Workflows for Purchase Orders (F2874)", "Define start conditions, step approvers, and rejection rules in UI."),
            ("Agent Determination", "BAdI MMPUR_WORKFLOW_AGENTS_V2", "Custom approver routing based on dynamic org hierarchy or cost centers."),
            ("Task Gateway & Notifications", "SAP Task Center / Fiori My Inbox", "Enables mobile push notifications and 1-click approvals on smartphones.")
        ],
        "sections": [
            ("Legacy vs Flexible Workflow", "Why S/4HANA Deprecates NAST & Release Strategy in Favor of Scenario-Driven Workflow"),
            ("Prerequisites in SPRO", "Activating Flexible Workflow for PO Document Types (NB, ZNB) in Customizing"),
            ("Fiori App Configuration", "Setting Up Multi-Level Approval Tiers, Deadlines, and Exception Handling"),
            ("BAdI Enhancements", "Implementing Custom Approver Determination Rules and Managing Rejected Orders")
        ]
    },
    {
        "title": "SAP MM Subcontracting Process with S/4HANA Special Stock 'O' Lifecycle",
        "slug": "sap-mm-subcontracting-cycle-s4hana-step-by-step",
        "category": "Tutorial",
        "badge": "SAP MM BLUEPRINT",
        "read_time": "14 min read",
        "keyword": "sap mm subcontracting process s4hana special stock o",
        "meta_desc": "End-to-end masterclass on SAP MM Subcontracting Cycle (Item Category L), Subcontracting PO, Stock Transfer (541), Goods Receipt (101), and Consumption (543).",
        "role": "SAP MM Lead Consultant / Supply Chain Analyst",
        "process_title": "Complete 5-Step Subcontracting Cycle",
        "process_steps": [
            ("1. Subcontract PO", "Create PO with Item Category 'L' and link BOM Components (ME21N)"),
            ("2. Component Provision", "Transfer raw materials to Subcontractor Special Stock 'O' via MIGO (mvt 541)"),
            ("3. External Processing", "Vendor performs manufacturing or assembly operations off-site"),
            ("4. Goods Receipt", "Receive finished goods (101) + auto-consume components (543) in MIGO"),
            ("5. Subcontract MIRO", "Process vendor service invoice for subcontracting service fees")
        ],
        "table_headers": ["Movement Type", "Description", "Stock Impact & Valuation"],
        "table_rows": [
            ("541", "Transfer raw materials to Vendor Special Stock", "Unrestricted plant stock decreases; Special Stock 'O' increases (Non-valuated transfer)."),
            ("542", "Reversal of Subcontractor stock transfer", "Returns components from Vendor Special Stock 'O' back to plant storage location."),
            ("101", "Goods Receipt of Finished / Assembled Product", "Increases finished goods inventory at plant level with standard/moving price."),
            ("543", "Automatic consumption of components from Stock 'O'", "Reduces Special Stock 'O' and posts expense to Consumption Account (VBR).")
        ],
        "sections": [
            ("Subcontracting Master Data", "Material Master, Subcontracting Info Record, and BOM Construction (CS01)"),
            ("Execution in S/4HANA", "Purchase Order Creation (ME21N Item Category L) and Monitoring via ME2O / ADSUBCON"),
            ("Financial & Inventory Postings", "Double-Entry Accounting Analysis for Finished Good Inbound and Component Write-Down"),
            ("By-Products & Scrap Handling", "Managing Scrap Components (545/544) and Resolving Inventory Discrepancies")
        ]
    },
    {
        "title": "SAP EWM Radio Frequency (RF) Framework: Hardware & /SCWM/RFUI Configuration Guide",
        "slug": "sap-ewm-rf-framework-scwm-rfui-configuration",
        "category": "Tutorial",
        "badge": "SAP EWM ADVANCED",
        "read_time": "15 min read",
        "keyword": "sap ewm rf framework configuration scwm rfui mobile",
        "meta_desc": "Master SAP EWM RF Framework, Screen Manager, Presentation Profiles, Barcode verification, and mobile picking setup in /SCWM/RFUI.",
        "role": "SAP EWM Technical Consultant & Warehouse Systems Lead",
        "process_title": "RF Warehouse Task Processing Sequence",
        "process_steps": [
            ("1. RF Login", "Operator logs into /SCWM/RFUI on mobile handheld with Resource & Device ID"),
            ("2. Queue Assignment", "EWM assigns highest-priority Warehouse Order based on operator qualification"),
            ("3. Scan Verification", "Operator scans Source Bin, Handling Unit, and Product EAN/Barcode"),
            ("4. Confirmation", "Pick confirmed in real time; system guides operator to Target Staging Bay")
        ],
        "table_headers": ["RF Framework Component", "Customizing Node", "Functional Purpose"],
        "table_rows": [
            ("Define Display Profile", "SPRO > Extended Warehouse Management > Mobile Data Entry > RF Framework", "Configures screen dimensions (e.g., 8x40 or 16x20) for rugged scanner screens."),
            ("Presentation Profile", "Define Presentation Profile & Assign Menu", "Controls menu navigation hierarchy (Inbound, Outbound, Internal, Physical Inv)."),
            ("Verification Profile", "Define Verification Profile", "Enforces mandatory barcode scanning of Bin, HU, Quantity, or Serial Number."),
            ("Resource & Device Setup", "Transaction /SCWM/RSRC", "Binds physical terminal ID to Warehouse Resource and assigned Queue.")
        ],
        "sections": [
            ("Architecture of EWM RF", "Decoupled Screen Architecture, Web Dispatcher, and ITSmobile vs Fiori Mobile Client"),
            ("Presentation & Menu Setup", "Configuring Menu Hierarchies, Logical Transactions, and Steps in Customizing"),
            ("Verification & Barcoding", "Enforcing Barcode Scans (GS1-128, 2D DataMatrix) to Eliminate Picking Errors"),
            ("Troubleshooting & Monitoring", "Resolving RF Lockouts, Queue Starvation, and Diagnosing Short Dumps in /SCWM/MON")
        ]
    },
    {
        "title": "SAP MM Consignment Procurement: Info Records, 411 K Movements & MRKO Settlement",
        "slug": "sap-mm-consignment-procurement-mrko-settlement",
        "category": "Tutorial",
        "badge": "SAP MM MASTERCLASS",
        "read_time": "11 min read",
        "keyword": "sap mm consignment procurement mrko settlement 411k",
        "meta_desc": "Configure SAP MM Consignment Procurement from scratch: Consignment Info Records, Goods Receipt without liability, Transfer Posting (411 K), and MRKO Auto-Settlement.",
        "role": "SAP MM Functional Consultant & Procurement Analyst",
        "process_title": "End-to-End Vendor Consignment Cycle",
        "process_steps": [
            ("1. Consignment PO", "Create PO with Item Category 'K'; no financial liability generated"),
            ("2. GR to Special Stock", "Post Goods Receipt (101 K) into Vendor Consignment Stock 'K'"),
            ("3. Stock Withdrawal", "Transfer stock from 'K' to Own Stock (mvt 411 K) or consume to Cost Center (201 K)"),
            ("4. Auto Settlement", "Run Transaction MRKO to automatically generate vendor liability and payment advice")
        ],
        "table_headers": ["Transaction / Key", "Functionality", "Accounting Entry Generated"],
        "table_rows": [
            ("PO Item Cat 'K'", "Identifies Vendor Consignment item", "No financial accounting document created at PO creation."),
            ("MIGO mvt 101 K", "Goods Receipt to Consignment Stock", "No FI document; inventory tracked under Special Stock Indicator 'K'."),
            ("MIGO mvt 411 K", "Transfer Consignment to Own Stock", "Debit: Inventory Account (BSX) / Credit: Consignment Accounts Payable (KON)."),
            ("MRKO Settlement", "Automatic Invoice / Payment Voucher", "Debit: Consignment Payable (KON) / Credit: Vendor Reconciliation (KBS).")
        ],
        "sections": [
            ("Consignment Fundamentals", "Understanding Vendor-Owned Stock on Customer Premises & Zero Working Capital Inbound"),
            ("Master Data Configuration", "Consignment Info Record (ME11), Tax Codes, and OBYC Transaction Key KON Setup"),
            ("Stock Movement Execution", "MIGO 101 K Goods Receipt, 411 K Transfer Postings, and Quality Inspection Handling"),
            ("MRKO Settlement Masterclass", "Automating Periodic Settlement, Generating Credit Memos, and Resolving Price Variances")
        ]
    },
    {
        "title": "SAP S/4HANA Clean Core Architecture: Practical Guide for MM & EWM Consultants",
        "slug": "sap-s4hana-clean-core-architecture-mm-ewm-guide",
        "category": "Guide",
        "badge": "CLEAN CORE 2026",
        "read_time": "12 min read",
        "keyword": "sap s4hana clean core architecture mm ewm extensibility",
        "meta_desc": "How SAP supply chain consultants must adapt to Clean Core in S/4HANA 2026: Key User Extensibility, Developer Extensibility, RAP, and BAdI modernization.",
        "role": "SAP Enterprise Architect & S/4HANA Delivery Lead",
        "process_title": "Clean Core Extensibility Decision Flow",
        "process_steps": [
            ("1. Requirement Ingestion", "Identify custom business process requirement in Sourcing or Warehousing"),
            ("2. Standard Evaluation", "Assess if SAP standard Fiori app or BTP pre-packaged content fulfills scope"),
            ("3. On-Stack Clean Core", "Apply Key User Extensibility (Custom Fields & Logic) or RAP-based Developer Extensibility"),
            ("4. Side-by-Side (BTP)", "Build complex integrations or decoupling logic on SAP Business Technology Platform")
        ],
        "table_headers": ["Extensibility Tier", "Technological Framework", "Best Use Case for MM/EWM"],
        "table_rows": [
            ("Tier 1: Key User", "Custom Fields and Logic Fiori App", "Adding custom header/item fields to Purchase Orders with zero-code upgrade safety."),
            ("Tier 2: Developer", "ABAP Cloud & RAP (RESTful Application Programming)", "Building custom warehouse cockpit or RF transaction on released SAP APIs."),
            ("Tier 3: Side-by-Side", "SAP BTP (Node.js, Java, Kyma, CAP)", "Connecting external 3PL carrier portals or predictive supplier risk dashboards.")
        ],
        "sections": [
            ("Clean Core Principles", "Why SAP S/4HANA Cloud Mandates Separation of Core Business Logic from Custom Code"),
            ("Extensibility Model", "Tier 1 (Key User), Tier 2 (On-Stack Developer), and Tier 3 (Side-by-Side BTP) Explained"),
            ("Customizing Supply Chain", "Replacing Obsolete User Exits & Enhancement Points with Released Clean BAdIs"),
            ("Upgrade Safeguards", "Enforcing ABAP Cloud Language Version Rules and Automated ATC Readiness Checks")
        ]
    },
    {
        "title": "SAP EWM Slotting and Rearrangement: Algorithmic Warehouse Optimization",
        "slug": "sap-ewm-slotting-rearrangement-warehouse-optimization",
        "category": "Tutorial",
        "badge": "SAP EWM ADVANCED",
        "read_time": "13 min read",
        "keyword": "sap ewm slotting rearrangement configuration condition technique",
        "meta_desc": "Configure automated Slotting and Rearrangement in SAP EWM using Condition Technique to dynamically optimize storage bin assignment and reduce picker travel.",
        "role": "SAP EWM Consultant / Warehouse Operations Architect",
        "process_title": "Slotting & Rearrangement Execution Cycle",
        "process_steps": [
            ("1. Velocity Analysis", "System analyzes historical pick frequency, demand velocity, and product dimensions"),
            ("2. Condition Evaluation", "Condition technique matches product attributes against optimal Putaway Strategies"),
            ("3. Master Data Update", "Slotting run writes recommended Putaway Section, Bin Type, and Max Capacity to Product Master"),
            ("4. Rearrangement WTs", "Rearrangement run creates Warehouse Tasks to relocate slow/fast movers to optimal bins")
        ],
        "table_headers": ["Slotting Element", "Configuration Function", "Operational Impact"],
        "table_rows": [
            ("Condition Tables & Access", "SPRO > EWM > Goods Receipt > Slotting", "Determines storage parameters based on Product Group, Temperature, and Turnover Class."),
            ("Requirement Strategy", "Define Requirement Strategy", "Calculates required bin volume and footprint for peak season stock levels."),
            ("Storage Section Determination", "Condition Records via /SCWM/GCM", "Routes fast-moving velocity 'A' items to ground-level ergonomic pick faces."),
            ("Rearrangement Execution", "Transaction /SCWM/REARR", "Generates replenishment and relocation tasks during warehouse low-activity periods.")
        ],
        "sections": [
            ("Business Rationale", "How Dynamic Slotting Reduces Forklift Travel Time by up to 35% in High-Volume DCs"),
            ("Condition Technique for Slotting", "Configuring Field Catalogs, Condition Tables, and Strategy Determination Rules"),
            ("Running Slotting Runs", "Executing Mass Slotting via Transaction /SCWM/SLOT and Evaluating Log Output"),
            ("Automated Rearrangement", "Generating Relocation Tasks and Balancing Warehouse Workload during Night Shifts")
        ]
    },
    {
        "title": "SAP MM Automatic Purchase Order Creation from PR (ME59N) Configuration",
        "slug": "sap-mm-automatic-po-creation-me59n-guide",
        "category": "Tutorial",
        "badge": "SAP MM BLUEPRINT",
        "read_time": "11 min read",
        "keyword": "sap mm automatic po creation me59n purchase requisition",
        "meta_desc": "Step-by-step blueprint to configure automatic PO generation (ME59N) in SAP MM: Material Master, Vendor Master, Source List, and Background Batch Jobs.",
        "role": "SAP MM Functional Lead / Procurement Automation Specialist",
        "process_title": "Automated Requisition-to-PO Conversion Flow",
        "process_steps": [
            ("1. Demand Generation", "MRP Live or plant user creates Purchase Requisition with fixed source of supply"),
            ("2. Flag Verification", "System validates 'Auto PO' check in both Material Master and Business Partner"),
            ("3. Batch Job Run", "Scheduled ME59N background job evaluates approved PRs across plant criteria"),
            ("4. PO Creation", "System groups requisitions by vendor/purchasing org and generates POs with zero touch")
        ],
        "table_headers": ["Configuration Requirement", "Transaction / Location", "Validation Rule"],
        "table_rows": [
            ("Material Master Indicator", "MM02 > Purchasing View", "Checkbox 'Automatic PO' must be ticked for plant-specific material."),
            ("Business Partner Indicator", "BP > Role FLVN01 > Purchasing Data", "Checkbox 'Automatic Purchase Order' must be active in Vendor Pur Org data."),
            ("Fixed Source of Supply", "Transaction ME01 (Source List)", "Source List record must be marked as 'Fixed' and 'MRP Relevant' (Indicator 1)."),
            ("Background Job Scheduling", "Transaction SM36 (Report RM06BB30)", "Schedule ME59N to run every 15-30 minutes with predefined plant selection variant.")
        ],
        "sections": [
            ("Business Value of ME59N", "Eliminating Manual Buyer Intervention for Routine High-Volume Procurement Items"),
            ("The 4 Mandatory Prerequisites", "Material Master, Vendor BP, Source List, and Purchasing Info Record Alignment"),
            ("Grouping & Splitting Logic", "How ME59N Groups Multiple PRs into Single Multi-Line POs or Splits by Plant"),
            ("Production Error Resolution", "Fixing Common Errors: Source Not Determined, Incomplete Pricing, or Account Missing")
        ]
    },
    {
        "title": "Top 30 SAP MM Interview Questions & Scenario-Based Answers for 2026",
        "slug": "top-30-sap-mm-interview-questions-answers-2026",
        "category": "Interview prep",
        "badge": "INTERVIEW PREP 2026",
        "read_time": "16 min read",
        "keyword": "top sap mm interview questions answers 2026 scenario based",
        "meta_desc": "Crack senior SAP MM & S/4HANA procurement interviews with 30 comprehensive scenario questions on P2P, OBYC, Split Valuation, Movement Types, and Troubleshooting.",
        "role": "Senior SAP MM / Sourcing Consultant Candidate",
        "process_title": "Consultant Interview Evaluation Matrix",
        "process_steps": [
            ("Phase 1: Foundations", "Enterprise Structure, Master Data (BP/Material), and Document Types"),
            ("Phase 2: Core P2P", "Pricing Procedure, OBYC Account Determination, and Inventory Movements"),
            ("Phase 3: Special Procurement", "Subcontracting, Consignment, Pipeline, and Stock Transport Orders"),
            ("Phase 4: S/4HANA Delta", "Business Partner, MATDOC, MRP Live, Clean Core, and Fiori Apps")
        ],
        "table_headers": ["Interview Question Topic", "Core Evaluation Criterion", "Key Concept to Mention"],
        "table_rows": [
            ("OBYC Configuration", "Integration with FI and automatic posting", "Valuation Class, BSX, WRX, GBB, PRD, Account Modification BSA/VBR."),
            ("Split Valuation", "Handling multi-cost materials in single plant", "Valuation Categories, Valuation Types, Price Control (V), Accounting 1 view."),
            ("M7021 Error Resolution", "Real-world inventory troubleshooting", "Stock deficit calculation, unconfirmed physical inventory, transfer postings."),
            ("S/4HANA Architecture Changes", "Modern ERP understanding", "MATDOC table consolidation, elimination of BSEG/MKPF redundancy, Fiori Launchpad.")
        ],
        "sections": [
            ("Enterprise Structure & Master Data", "Top 5 Questions on Company Codes, Plants, Storage Locations, and BP Unified Customer/Vendor"),
            ("Procure-to-Pay (P2P) Scenarios", "Real-World Questions on Automatic POs, Price Tolerance Limits, and 3-Way Matching"),
            ("Inventory & Special Procurement", "Subcontracting Loss, Consignment Settlement, and Movement Type Mechanics"),
            ("S/4HANA 2026 Innovations", "Clean Core, Flexible Workflow, MRP Live in Memory, and BAdI Modernization")
        ]
    }
,
    {
    "title": "SAP EWM Inbound POSC: Deconsolidation, Quality & Putaway Blueprint",
    "slug": "sap-ewm-inbound-posc-deconsolidation-blueprint",
    "category": "Tutorial",
    "badge": "SAP EWM MASTERCLASS",
    "read_time": "14 min read",
    "keyword": "sap ewm inbound posc deconsolidation quality putaway",
    "meta_desc": "Configure complex multi-step Inbound POSC in SAP EWM: Unloading (IB01), Deconsolidation (IB02), Quality Inspection (IB03), and Final Putaway (IB04).",
    "role": "SAP EWM Solution Architect & Warehouse Designer",
    "process_title": "4-Step Inbound POSC Process Flow",
    "process_steps": [
        [
            "1. Unloading",
            "Unload mixed pallet from truck to receiving staging area (IB01)"
        ],
        [
            "2. Deconsolidation",
            "Route mixed pallet to decon workstation; pack into product HUs (IB02)"
        ],
        [
            "3. Quality Check",
            "Inspect product samples and record usage decision in QAS bay (IB03)"
        ],
        [
            "4. Final Putaway",
            "System generates destination warehouse task to high-bay storage rack (IB04)"
        ]
    ],
    "table_headers": [
        "Process Step",
        "External Step Code",
        "Internal Process Step / Detail"
    ],
    "table_rows": [
        [
            "Unload",
            "ZUNL",
            "Internal Step IB01: Destination Yard/Staging Bay."
        ],
        [
            "Deconsolidate",
            "ZDEC",
            "Internal Step IB02: Work center routing for mixed HUs."
        ],
        [
            "Quality Inspection",
            "ZQAL",
            "Internal Step IB03: Q-lot creation and sampling."
        ],
        [
            "Putaway",
            "ZPUT",
            "Internal Step IB04: Putaway strategy determination."
        ]
    ],
    "sections": [
        [
            "POSC Customizing Architecture",
            "Storage Process Definition and External Step Mapping in SPRO"
        ],
        [
            "Work Center & Route Rules",
            "Configuring Deconsolidation Work Centers and Routing Groups"
        ],
        [
            "Warehouse Task Automation",
            "Rule-Based Generation of Subsequent Warehouse Tasks in S/4HANA"
        ],
        [
            "Live Execution & Troubleshooting",
            "Monitoring POSC HUs in /SCWM/MON and Fixing Stuck Tasks"
        ]
    ]
},
    {
    "title": "SAP MM Physical Inventory & Cycle Counting: S/4HANA Configuration Guide",
    "slug": "sap-mm-physical-inventory-cycle-counting-guide",
    "category": "Tutorial",
    "badge": "SAP MM MASTERCLASS",
    "read_time": "12 min read",
    "keyword": "sap mm physical inventory cycle counting mi01 mi07",
    "meta_desc": "Master physical inventory in SAP MM: Cycle Counting setup (ABC indicators), tolerance groups, document freeze (MI01), count entry (MI04), and discrepancy posting (MI07).",
    "role": "SAP MM Functional Consultant & Inventory Controller",
    "process_title": "End-to-End Cycle Counting Lifecycle",
    "process_steps": [
        [
            "1. ABC Analysis",
            "Classify materials by movement velocity/value via MIBC"
        ],
        [
            "2. Document Creation",
            "Generate active count documents via MI01 / MICN with book freeze"
        ],
        [
            "3. Physical Count",
            "Warehouse floor counts recorded directly in MI04 / Fiori App"
        ],
        [
            "4. Discrepancy Posting",
            "Post valuation adjustments via MI07 within user tolerance limits"
        ]
    ],
    "table_headers": [
        "Cycle Counting Step",
        "T-Code / SPRO Node",
        "Key Function"
    ],
    "table_rows": [
        [
            "Cycle Counting Indicator",
            "OMCO / SPRO Inventory Management",
            "Set count frequency (e.g., A=12/year, B=6/year, C=2/year)."
        ],
        [
            "User Tolerance Groups",
            "OMC0 / SPRO IM",
            "Enforce maximum currency & percentage limits for variance posting."
        ],
        [
            "Document Generation",
            "MI01 / MICN / LIDC",
            "Generate count sheets with posting block to prevent concurrent goods movements."
        ],
        [
            "Difference Settlement",
            "MI07 / MI20",
            "Trigger inventory adjustments and automatic financial postings (GBB/INV)."
        ]
    ],
    "sections": [
        [
            "Cycle Counting Customizing",
            "Configuring OMCO, ABC Velocity Matrix, and Movement Tolerances in SPRO"
        ],
        [
            "Freeze Book Inventory Mechanics",
            "Preventing Stock Distortions and Phantom Discrepancies During Counting"
        ],
        [
            "Fiori Count Management",
            "Utilizing Fiori Manage Physical Inventory Documents for Mobile Entry"
        ],
        [
            "Financial Reconciliation",
            "Understanding OBYC Valuation Postings and Solving MI07 Authorization Errors"
        ]
    ]
},
    {
    "title": "Stock Transport Orders (STO): Intra-Company vs Inter-Company Configuration Blueprint",
    "slug": "sap-mm-sto-inter-company-intra-company-deep-dive",
    "category": "Tutorial",
    "badge": "SAP LOGISTICS BLUEPRINT",
    "read_time": "15 min read",
    "keyword": "sap mm sto intra company inter company configuration s4hana",
    "meta_desc": "Complete architectural comparison and SPRO configuration guide for Intra-Company (UB) and Inter-Company (NB) Stock Transport Orders with SD Delivery and Billing.",
    "role": "SAP MM / SD Functional Integration Lead",
    "process_title": "STO Execution & Financial Settlement Cycle",
    "process_steps": [
        [
            "1. STO Creation",
            "Receiving plant raises Purchase Order (UB/NB) in ME21N"
        ],
        [
            "2. SD Replenishment",
            "Shipping plant generates Outbound Delivery via VL10B"
        ],
        [
            "3. Goods Issue",
            "Picking & Post Goods Issue (PGI) via VL02N (Mvt 641/643)"
        ],
        [
            "4. Goods Receipt & Bill",
            "MIGO 101 at receiving plant; VF01 Intercompany Invoice for Cross-Company"
        ]
    ],
    "table_headers": [
        "STO Model",
        "Document & Movement Types",
        "Financial & Billing Mechanics"
    ],
    "table_rows": [
        [
            "Intra-Plant One-Step",
            "Movement Type 301 / 311",
            "No SD delivery; direct stock transfer between locations."
        ],
        [
            "Intra-Company Two-Step (UB)",
            "PO Type UB / Delivery NL / Mvt 641 & 101",
            "No intercompany invoice; stock in transit account used."
        ],
        [
            "Cross-Company (NB)",
            "PO Type NB / Delivery NLCC / Mvt 643 & 101",
            "Requires Intercompany Customer, Vendor BP, and VF01 Intercompany Billing (IV)."
        ],
        [
            "Cross-Company with Returns",
            "PO Type NB (Return) / Mvt 673 & 161",
            "Configuring credit memo and reverse in-transit accounting."
        ]
    ],
    "sections": [
        [
            "Architectural Comparison",
            "Contrasting Intra-Company vs Cross-Company Logistics and Financial Flows"
        ],
        [
            "Customer & Vendor BP Setup",
            "Configuring Internal Customer Numbers and Shipping Data for Plants in SPRO"
        ],
        [
            "Checking Rules & Delivery Type",
            "Assigning Delivery Type NL/NLCC and Availability Checking Rules in SPRO"
        ],
        [
            "S/4HANA In-Transit Visibility",
            "Tracking In-Transit Stock in MMBE/MB5T and Resolving Missing Delivery Errors"
        ]
    ]
},
    {
    "title": "SAP EWM Yard Management: Transportation Unit (TU), Dock Door & Check-In Guide",
    "slug": "sap-ewm-yard-management-tu-door-appointment",
    "category": "Tutorial",
    "badge": "SAP EWM ADVANCED",
    "read_time": "13 min read",
    "keyword": "sap ewm yard management transportation unit tu check in",
    "meta_desc": "Configure SAP EWM Yard Management: Yard Structure, Transportation Units (TUs), Check-In, Dock Door scheduling, Yard Movements, and Gate-Out operations.",
    "role": "SAP EWM Solution Architect & Yard Logistics Lead",
    "process_title": "End-to-End EWM Yard Logistics Lifecycle",
    "process_steps": [
        [
            "1. Gate Check-In",
            "Security checkpoint registers truck arrival and creates active TU"
        ],
        [
            "2. Parking Assignment",
            "Yard Task moves TU to designated trailer parking bay"
        ],
        [
            "3. Door Docking",
            "Yard Task moves TU from parking space to active warehouse loading door"
        ],
        [
            "4. Gate-Out",
            "Post Goods Receipt/Issue completes; TU checks out at exit gate"
        ]
    ],
    "table_headers": [
        "Yard Object",
        "Customizing Node / Transaction",
        "Operational Purpose"
    ],
    "table_rows": [
        [
            "Yard Structure",
            "SPRO > EWM > Cross-Process Settings > Yard Management",
            "Defines checkpoints, parking slots, yard bins, and door connections."
        ],
        [
            "Transportation Unit (TU)",
            "/SCWM/TU / /SCWM/YCHECKIN",
            "Tracks physical vehicle container, license plate, driver, and seal numbers."
        ],
        [
            "Yard Movement Task",
            "/SCWM/YM_WT",
            "Generates internal warehouse tasks for vehicle transit across yard zones."
        ],
        [
            "Dock Appointment",
            "SAP DAS / SPRO Dock Scheduling",
            "Integrates driver appointments to level warehouse door workload."
        ]
    ],
    "sections": [
        [
            "Yard Master Data Architecture",
            "Setting Up Checkpoints, Parking Bays, and Linking Warehouse Doors in SPRO"
        ],
        [
            "Transportation Unit Packaging",
            "Configuring Means of Transport and Assigning Deliveries to TUs"
        ],
        [
            "Yard Task Automation",
            "Rule-Based Generation of Vehicle Movements between Yard Bins and Doors"
        ],
        [
            "Yard Monitor & Mobile UI",
            "Tracking Live Fleet Status in /SCWM/MON and Handheld Check-In Workflows"
        ]
    ]
},
    {
    "title": "Source Determination in SAP MM: Info Records, Source Lists & Quota Arrangements",
    "slug": "sap-mm-source-determination-quota-arrangements-guide",
    "category": "Tutorial",
    "badge": "SAP MM BLUEPRINT",
    "read_time": "13 min read",
    "keyword": "sap mm source determination quota arrangement source list me01",
    "meta_desc": "Master the 4-tier Source Determination hierarchy in SAP MM & S/4HANA: Purchase Info Records, Contracts, Source Lists, and Quota Arrangements for automated MRP sourcing.",
    "role": "SAP MM Sourcing Consultant & Procurement Lead",
    "process_title": "Source Determination Evaluation Hierarchy",
    "process_steps": [
        [
            "Tier 1: Quota Rule",
            "Evaluates active Quota Arrangement (MEQ1) to balance procurement share"
        ],
        [
            "Tier 2: Source List",
            "Checks Source List (ME01) for fixed or MRP-relevant preferred suppliers"
        ],
        [
            "Tier 3: Contracts",
            "Selects active Outline Agreement / Value Contract (ME31K)"
        ],
        [
            "Tier 4: Info Record",
            "Falls back to valid Purchasing Info Record (ME11) with regular supplier"
        ]
    ],
    "table_headers": [
        "Sourcing Mechanism",
        "Transaction Code",
        "Key Configuration & Control"
    ],
    "table_rows": [
        [
            "Quota Arrangement",
            "MEQ1",
            "Splits demand across vendors using formula: (Allocated Qty + Quota Base Qty) / Quota."
        ],
        [
            "Source List Requirement",
            "OME5 / Material Master Pur View",
            "Enforces mandatory vendor qualification before PO creation for the plant."
        ],
        [
            "Fixed Vendor Indicator",
            "ME01",
            "Marks a single supplier as automatically determined for manual requisitions."
        ],
        [
            "MRP Relevance",
            "ME01 (MRP Column = 1)",
            "Instructs MRP Live to automatically assign this vendor to planned orders."
        ]
    ],
    "sections": [
        [
            "Determination Priority Engine",
            "In-Depth Evaluation of the 4-Tier Hierarchy During PR and PO Creation"
        ],
        [
            "Quota Calculation Mechanics",
            "Configuring Quota Ratings, Minimum Splitting Quantities, and Max Capacity Limits"
        ],
        [
            "Source List Customizing",
            "Enforcing Mandatory Source Lists at Plant Level and Setting Validity Windows"
        ],
        [
            "Automated MRP Allocation",
            "Troubleshooting Unassigned Purchase Requisitions in S/4HANA MRP Runs"
        ]
    ]
},
    {
    "title": "Cross-Docking in SAP S/4HANA EWM: Opportunistic vs Planned Fulfillment",
    "slug": "sap-ewm-cross-docking-opportunistic-planned-blueprint",
    "category": "Tutorial",
    "badge": "SAP EWM 2026",
    "read_time": "13 min read",
    "keyword": "cross docking sap ewm opportunistic planned configuration",
    "meta_desc": "Eliminate warehouse putaway and picking touches with SAP EWM Cross-Docking: Opportunistic Cross-Docking and Transportation Cross-Docking (TCD) in S/4HANA.",
    "role": "SAP EWM Functional Lead & Fulfillment Architect",
    "process_title": "EWM Cross-Docking Execution Lifecycle",
    "process_steps": [
        [
            "1. Inbound Arrival",
            "Goods receipt posted for inbound delivery at receiving door"
        ],
        [
            "2. Demand Match",
            "System detects matching open outbound delivery demand in real time"
        ],
        [
            "3. Direct Route WT",
            "System creates direct warehouse task bypassing high-bay storage racks"
        ],
        [
            "4. Outbound Staging",
            "Goods move immediately to outbound shipping lane for truck loading"
        ]
    ],
    "table_headers": [
        "Cross-Docking Model",
        "Activation Node in SPRO",
        "Operational Benefit"
    ],
    "table_rows": [
        [
            "Opportunistic Inbound",
            "Cross-Process Settings > Cross-Docking > Opportunistic",
            "Redirects inbound pallets directly to open outbound deliveries at GR."
        ],
        [
            "Opportunistic Outbound",
            "Cross-Process Settings > Cross-Docking > Opportunistic",
            "Searches receiving staging area before triggering picking tasks in warehouse."
        ],
        [
            "Transportation Cross-Docking (TCD)",
            "Integration with SAP TM & ERP Routing",
            "Cross-docks full containers across intermediate logistics distribution hubs."
        ],
        [
            "Merchandise Distribution (Retail)",
            "Push/Pull Distribution via SAP Retail",
            "Direct store allocation for fast-moving consumer packaged goods."
        ]
    ],
    "sections": [
        [
            "Cross-Docking Architecture",
            "Contrasting Opportunistic Cross-Docking and Transportation Cross-Docking (TCD)"
        ],
        [
            "Customizing SPRO Rules",
            "Configuring Determination Sequences, Relevance Profiles, and Storage Types"
        ],
        [
            "Warehouse Task Automation",
            "Rule-Based Generation of Direct Stage-to-Dock Warehouse Tasks"
        ],
        [
            "KPIs & Exception Monitoring",
            "Tracking Touch-Reduction Metrics and Resolving Cancelled Outbound Matches"
        ]
    ]
},
    {
    "title": "SAP S/4HANA Material Ledger & Actual Costing: Valuation Masterclass",
    "slug": "sap-s4hana-material-ledger-actual-costing-valuation-guide",
    "category": "Tutorial",
    "badge": "SAP MM ADVANCED",
    "read_time": "14 min read",
    "keyword": "sap s4hana material ledger actual costing ckm3n valuation",
    "meta_desc": "Comprehensive guide to mandatory Material Ledger in S/4HANA: Actual Costing (CKMLCP), multi-currency valuation, price variance settlement (PRD), and CKM3N analysis.",
    "role": "SAP MM / CO Functional Consultant & Product Costing Specialist",
    "process_title": "Period-End Material Ledger Settlement Flow",
    "process_steps": [
        [
            "1. Daily Postings",
            "Material movements posted at Standard Price (S) with price variances to PRD"
        ],
        [
            "2. Period Closing",
            "Execute Cockpit CKMLCP: Determine single-level price differences"
        ],
        [
            "3. Multilevel Settlement",
            "Roll price variances up from components to semi-finished/finished goods"
        ],
        [
            "4. Actual Revaluation",
            "Calculate periodic unit price (PUP) and revalue ending inventory balance"
        ]
    ],
    "table_headers": [
        "Valuation Element",
        "Transaction / SPRO Path",
        "Significance in S/4HANA"
    ],
    "table_rows": [
        [
            "Mandatory Activation",
            "SPRO > Controlling > Product Cost Controlling > Actual Costing",
            "Material Ledger is technically mandatory in S/4HANA; activates universal journal (ACDOCA)."
        ],
        [
            "Currency Types",
            "OMX2 / OMX3",
            "Enables 3 parallel currencies (Company Code, Group, Hard Currency)."
        ],
        [
            "Price Determination",
            "Material Master Accounting 1 (Indicator 2 vs 3)",
            "Indicator 2 = Transaction-Based; Indicator 3 = Single/Multilevel Actual Costing."
        ],
        [
            "Material Price Analysis",
            "Transaction CKM3N",
            "Real-time interactive audit trail of receipts, consumption, and variances."
        ]
    ],
    "sections": [
        [
            "S/4HANA Material Ledger Mandate",
            "Why S/4HANA Replaced Classic Valuation with Universal Journal Material Ledger"
        ],
        [
            "Price Determination: 2 vs 3",
            "Choosing between Transaction-Based Valuation and Single/Multilevel Actual Costing"
        ],
        [
            "Period-End Settlement (CKMLCP)",
            "Step-by-step Cockpit Execution: Selection, Sequence, Costing, and Closing Postings"
        ],
        [
            "CKM3N Troubleshooting",
            "Diagnosing Unallocated Price Variances, Not-Distributed Warnings, and Inventory Adjustments"
        ]
    ]
},
    {
    "title": "EWM Internal Replenishment: Planned, Order-Related & Crate Strategies",
    "slug": "sap-ewm-internal-replenishment-strategies-deep-dive",
    "category": "Tutorial",
    "badge": "SAP EWM MASTERCLASS",
    "read_time": "12 min read",
    "keyword": "sap ewm internal replenishment planned order related crate",
    "meta_desc": "Configure SAP EWM Internal Replenishment: Planned Replenishment, Order-Related Replenishment for picking waves, and Crate Replenishment with /SCWM/REPL.",
    "role": "SAP EWM Solution Architect & Picking Optimization Lead",
    "process_title": "EWM Pick Bin Replenishment Cycle",
    "process_steps": [
        [
            "1. Threshold Trigger",
            "Stock in fast-pick bin drops below minimum threshold parameter"
        ],
        [
            "2. Replenishment Run",
            "Background job evaluates replenishment strategy via /SCWM/REPL"
        ],
        [
            "3. WT Creation",
            "Warehouse task created from high-bay reserve storage to active pick face"
        ],
        [
            "4. Confirmation",
            "Forklift confirms drop-off; pick bin available for wave picking"
        ]
    ],
    "table_headers": [
        "Replenishment Type",
        "Trigger Mechanism",
        "Typical Business Application"
    ],
    "table_rows": [
        [
            "Planned Replenishment",
            "Scheduled background batch job checking Min/Max bin quantities",
            "Overnight restocking of forward pick faces for high-velocity SKUs."
        ],
        [
            "Order-Related Replenishment",
            "Triggered dynamically during Outbound Wave Release",
            "Replenishes pick bins specifically when open order demand exceeds on-hand pick stock."
        ],
        [
            "Crate Replenishment",
            "Manual or RF barcode scan of empty production supply bin",
            "Restocks small parts containers (Kanban) at shop-floor production work centers."
        ],
        [
            "Direct Replenishment",
            "Triggered instantly when a picker confirms a pick that zeroes stock",
            "Prevents next picker in same wave from encountering an empty bin."
        ]
    ],
    "sections": [
        [
            "Replenishment Types & Strategies",
            "Contrasting Planned, Order-Related, Crate, and Direct Replenishment Logic"
        ],
        [
            "Customizing Master Data & Bins",
            "Configuring Min/Max Quantities and Replenishment Control in Storage Type Customizing"
        ],
        [
            "Condition Technique for Replenishment",
            "Setting Up Strategies and Determination Tables in /SCWM/REPL"
        ],
        [
            "Execution & RF Mobile Confirmation",
            "Operator Workflows on Handheld Devices (/SCWM/RFUI) and Stock Exception Handling"
        ]
    ]
},
    {
    "title": "Service Procurement in SAP S/4HANA: Lean Services Architecture Guide",
    "slug": "sap-s4hana-service-procurement-lean-services-guide",
    "category": "Tutorial",
    "badge": "S/4HANA 2026",
    "read_time": "11 min read",
    "keyword": "sap s4hana service procurement lean services item category e ml81n",
    "meta_desc": "Modernize service purchasing in S/4HANA: Replacing legacy Service Master (AC03) & Service Entry Sheets (ML81N) with Lean Services (Product Type SERV) and Fiori Manage Service Entry Sheets.",
    "role": "SAP MM / Sourcing Functional Consultant",
    "process_title": "Modern Lean Services Procurement Flow",
    "process_steps": [
        [
            "1. PR / PO Creation",
            "Create Service PO with Item Category E (Enhanced) and Product Type SERV"
        ],
        [
            "2. Service Delivery",
            "Vendor executes consulting, maintenance, or engineering service on site"
        ],
        [
            "3. Fiori Service Entry",
            "Contractor records hours in Fiori App Manage Service Entry Sheets - Lean"
        ],
        [
            "4. Approval & 3-Way Match",
            "Department manager approves sheet; automatic GR (101) posted to trigger MIRO"
        ]
    ],
    "table_headers": [
        "Legacy vs Lean Feature",
        "Legacy Service Procurement (ECC)",
        "Modern Lean Services (S/4HANA 2026)"
    ],
    "table_rows": [
        [
            "Item Category",
            "Item Category D (Service)",
            "Item Category E (Enhanced Limit / Lean Service) or Standard."
        ],
        [
            "Master Data",
            "Service Master Record (AC03)",
            "Material Master with Product Type SERV (Clean Core aligned)."
        ],
        [
            "Entry Sheet Interface",
            "SAP GUI ML81N (complex hierarchy)",
            "Fiori App Manage Service Entry Sheets (intuitive mobile UI)."
        ],
        [
            "Unplanned Limits",
            "Overall Limit in PO line item",
            "Enhanced Limit Items with simplified budget consumption."
        ]
    ],
    "sections": [
        [
            "Why SAP Redesigned Service Purchasing",
            "Shortcomings of Legacy Service Master and Advantages of Lean Services Architecture"
        ],
        [
            "Product Type SERV Configuration",
            "Maintaining Material Master Views, Valuation Classes, and Account Determination for Services"
        ],
        [
            "Item Category E & Enhanced Limits",
            "Managing CapEx and OpEx Service Contracts with Flexible Preconditions"
        ],
        [
            "Fiori Execution & Invoice Verification",
            "Step-by-Step Approval Workflow and 3-Way Invoicing Matching in S/4HANA"
        ]
    ]
},
    {
    "title": "Top 30 SAP EWM Real-Time Scenario Interview Questions (2026 Architect Guide)",
    "slug": "top-30-sap-ewm-scenario-interview-questions-2026",
    "category": "Interview prep",
    "badge": "INTERVIEW BLUEPRINT",
    "read_time": "16 min read",
    "keyword": "top sap ewm interview questions scenario based 2026 answers",
    "meta_desc": "Crack senior SAP EWM consultant and architect interviews with 30 in-depth scenario questions covering POSC/LOSC, Wave Management, WOCR, RF Framework, and Yard Operations.",
    "role": "Senior SAP EWM Consultant & Architect Candidate",
    "process_title": "EWM Technical Interview Preparation Structure",
    "process_steps": [
        [
            "Module 1: Inbound Logistics",
            "Inbound POSC, Deconsolidation, Quality Inspection, and Slotting rules"
        ],
        [
            "Module 2: Storage & Inventory",
            "Handling Units, Physical Inventory, Internal Replenishment, and Rearrangement"
        ],
        [
            "Module 3: Outbound Fulfillment",
            "Wave Management, WOCR, Two-Step Picking, and Packing Stations"
        ],
        [
            "Module 4: Technical & S/4HANA",
            "qRFC Interfaces, /SCWM/MON BAdIs, Embedded vs Decentral, and Clean Core"
        ]
    ],
    "table_headers": [
        "Interview Focus Area",
        "Complex Scenario Topic",
        "Target Architectural Answer"
    ],
    "table_rows": [
        [
            "POSC vs LOSC Combination",
            "Can a warehouse task have both POSC and LOSC active simultaneously?",
            "Yes. POSC determines the business sequence (e.g. Unload > Decon > Putaway); LOSC controls intermediate transport routing (e.g. Conveyor system)."
        ],
        [
            "Wave Release Bottlenecks",
            "What causes a wave to fail release with zero warehouse tasks generated?",
            "Missing storage bin capacity, unmet replenishment thresholds, stock locked by physical inventory, or failing stock determination rules."
        ],
        [
            "qRFC Stuck Queues",
            "How do you troubleshoot stuck SMQ1/SMQ2 queues between S/4HANA ERP and EWM?",
            "Inspect queue error logs, check material/batch CIF replication, verify number range buffering, and reprocess via /SCWM/ERP_STOCK_CHECK."
        ],
        [
            "Pick-Pack-Pass Logic",
            "How is activity area routing enforced in high-throughput fulfillment centers?",
            "Configure WOCR with Activity Area assignment and Pick-Pack-Pass consolidation profiles."
        ]
    ],
    "sections": [
        [
            "Inbound & Storage Control Scenarios",
            "Complex Interview Questions on POSC, Deconsolidation Routing, and HU Tracking"
        ],
        [
            "Outbound Picking & Wave Scenarios",
            "High-Throughput Warehouse Scenarios on WOCR Bundling, Limits, and Cut-off Management"
        ],
        [
            "Mobile & RF Framework Scenarios",
            "Handling Disconnected Barcode Scanners, Verification Profiles, and Custom Menu Flows"
        ],
        [
            "Architecture & Troubleshooting Scenarios",
            "qRFC Integration, S/4HANA 2026 Embedded EWM Sizing, and Performance Tuning"
        ]
    ]
}
]

def log_msg(msg: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    with open(AUTOMATION_LOG, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def generate_dynamic_sap_topic() -> dict:
    """
    Autonomous fallback generator that procedurally synthesizes fresh,
    unique, enterprise-grade SAP MM/EWM topics when predefined pools are exhausted.
    Ensures the twice-daily scheduler NEVER halts.
    """
    modules = ["SAP MM", "SAP EWM", "SAP S/4HANA Supply Chain"]
    focus_areas = [
        ("Physical Inventory & Cycle Counting", "physical-inventory-cycle-counting", "Tutorial", "SAP MM MASTERCLASS",
         "Master physical inventory cycle counting, continuous inventory, difference posting (MI07), and tolerance groups in SAP S/4HANA.",
         "SAP MM Functional Lead / Inventory Auditor",
         [("Inventory Types", "Annual, Continuous, Cycle Counting & Sampling Procedures"),
          ("Customizing Setup", "Defining Tolerance Groups for Difference Posting in SPRO"),
          ("Execution Flow", "MI01 Create Document, MI04 Enter Count, and MI07 Post Differences"),
          ("Audit Compliance", "Handling Book Inventory Freezes and Physical Inventory Valuation")]),

        ("Stock Transport Orders (STO): Intra vs Inter-Company Blueprint", "sto-intra-inter-company-blueprint", "Tutorial", "SAP LOGISTICS BLUEPRINT",
         "Comprehensive guide to configuring Intra-Company (UB) and Cross-Company (NB) Stock Transport Orders with Outbound SD Delivery and Billing.",
         "SAP MM / SD Functional Consultant & Integration Specialist",
         [("STO Models", "One-Step vs Two-Step and Intra-Company vs Inter-Company Mechanics"),
          ("Master Data Setup", "Customer Master for Plant, Vendor BP, and Shipping Data Assignment"),
          ("Customizing SPRO", "Assigning Delivery Types, Checking Rules, and PO Document Types"),
          ("Billing & Invoicing", "Inter-Company Invoicing (IV) and Clearing in S/4HANA")]),

        ("Yard Management (YM): Check-In to Gate-Out Operations", "yard-management-ym-checkin-gateout-guide", "Tutorial", "SAP EWM ADVANCED",
         "Configure SAP EWM Yard Management: Transportation Units (TU), Parking Bays, Check-in, Door Assignment, and Gate-Out flows.",
         "SAP EWM Architect & Yard Logistics Specialist",
         [("Yard Architecture", "Yard Structure, Checkpoints, Parking Spaces, and Doors in SPRO"),
          ("Transportation Units", "Creating and Managing TUs for Inbound and Outbound Shipments"),
          ("Yard Task Execution", "Moving Vehicles from Parking Bay to Warehouse Dock Door"),
          ("Integration with TM", "Direct Integration with SAP Transportation Management (TM)")]),

        ("Cross-Docking in S/4HANA EWM: Opportunistic vs Planned", "cross-docking-s4hana-ewm-deep-dive", "Tutorial", "SAP EWM 2026",
         "Implement Opportunistic and Planned Cross-Docking in SAP S/4HANA EWM to bypass putaway and fulfill outbound orders instantly.",
         "SAP EWM Senior Consultant / Fulfillment Architect",
         [("Cross-Docking Types", "Understanding Opportunistic Cross-Docking vs Transportation Cross-Docking"),
          ("Configuration Framework", "Setting Up Cross-Docking Determination Rules and Relevance Checks"),
          ("Execution Lifecycle", "Directing Inbound Pallets Directly to Outbound Staging Areas"),
          ("Performance Metrics", "Measuring Dock-to-Stock Reduction and Operational Cost Savings")]),

        ("Source Determination: Source List, Quota & Info Records", "source-determination-source-list-quota-arrangement", "Tutorial", "SAP MM BLUEPRINT",
         "Master Source Determination hierarchy in SAP MM: Purchase Info Records, Source Lists, Quota Arrangements, and Outline Agreements.",
         "SAP MM Sourcing Consultant & Procurement Analyst",
         [("Hierarchy of Determination", "Evaluation Order: Quota Arrangement > Source List > Contracts > Info Records"),
          ("Quota Calculation", "Configuring Quota Rating Formula and Splitting Quotations"),
          ("Source List Control", "Blocking and Fixing Vendors for Specific Plant Validity Periods"),
          ("Troubleshooting", "Resolving Unassigned Requisitions during Automated MRP Runs")]),

        ("EWM Handling Unit Management (HUM) & Packing Architecture", "ewm-handling-unit-management-hum-packing", "Tutorial", "SAP EWM MASTERCLASS",
         "Deep dive into Packaging Materials, Packaging Specifications, Storage Unit Types, and Nested Handling Units in SAP EWM.",
         "SAP EWM Functional Consultant / Packaging Specialist",
         [("HUM Foundations", "Packaging Materials, Pack Material Types, and HU Number Ranges"),
          ("Packaging Specifications", "Constructing Multi-Level Pack Specs for Single-Item vs Master Cartons"),
          ("Work Center Packing", "Deconsolidation and Repacking at Packing Station (/SCWM/PACK)"),
          ("Label Printing", "Generating GS1 Barcode Shipping Labels for Pallet Identification")])
    ]

    selected_module = random.choice(modules)
    focus = random.choice(focus_areas)
    year = datetime.datetime.now().year
    slug_suffix = int(time.time()) % 10000
    
    slug = f"{focus[1]}-{slug_suffix}"
    title = f"{focus[0]}: {selected_module} Complete Guide ({year})"
    
    return {
        "title": title,
        "slug": slug,
        "category": focus[2],
        "badge": focus[3],
        "read_time": f"{random.randint(11, 15)} min read",
        "keyword": f"{focus[1].replace('-', ' ')} {selected_module.lower()}",
        "meta_desc": focus[4],
        "role": focus[5],
        "process_title": f"{focus[0]} Operational Process Flow",
        "process_steps": [
            ("1. Requirement Identification", f"Identify operational scope and prerequisite configurations in {selected_module}"),
            ("2. Master Data & SPRO", "Maintain core tables, condition records, and organizational assignments"),
            ("3. Execution & Validation", "Execute end-to-end transaction test cycle in sandbox environment"),
            ("4. Go-Live & Monitoring", "Deploy transport requests and activate operational monitoring dashboards")
        ],
        "table_headers": ["Step / Object", "T-Code / SPRO Node", "Configuration Function"],
        "table_rows": [
            ("Customizing Definition", "SPRO Reference IMG", f"Configure primary parameters for {focus[0]}."),
            ("Master Data Maintenance", "Transaction Maintenance", "Align material, business partner, and warehouse master data."),
            ("Execution Testing", "Front-End Execution", "Test complete document flow and verify financial/inventory updates.")
        ],
        "sections": focus[6]
    }

def render_article_html(topic: dict) -> str:
    """Renders high-fidelity SEO web article adhering strictly to AGENTS.md & website design system."""
    date_str = datetime.datetime.now().strftime('%b %d, %Y')
    iso_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Render Table of Contents
    toc_items = "".join([
        f'<li><a href="#sec-{idx+1}" style="color:#38bdf8; text-decoration:none; font-weight:600;">{idx+1}. {s[0]}</a></li>'
        for idx, s in enumerate(topic['sections'])
    ])
    
    # Render Process Steps if available
    process_html = ""
    if "process_steps" in topic and topic["process_steps"]:
        steps_boxes = []
        for idx, step in enumerate(topic["process_steps"]):
            steps_boxes.append(f"""
              <div style="background:#0284c7; color:#fff; padding:1.1rem 0.85rem; border-radius:8px; width:155px; text-align:center;">
                <strong style="display:block; font-size:0.95rem; margin-bottom:0.2rem;">{step[0]}</strong>
                <span style="font-size:0.75rem; opacity:0.9; display:block;">{step[1]}</span>
              </div>
            """)
            if idx < len(topic["process_steps"]) - 1:
                steps_boxes.append('<span style="color:#94a3b8; font-size:1.25rem;">►</span>')
        
        process_html = f"""
        <!-- PROCESS FLOW COMPONENT -->
        <div style="background: #080d14; border: 1px solid #1e293b; border-radius: 12px; padding: 2rem 1.5rem; text-align: center; margin: 2.5rem 0;">
          <span style="color: #f1f5f9; font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">
            {topic.get('process_title', 'OPERATIONAL PROCESS FLOW')}
          </span>
          <div style="display: flex; justify-content: center; align-items: center; gap: 0.6rem; flex-wrap: wrap; margin-top: 1.5rem;">
            {"".join(steps_boxes)}
          </div>
        </div>
        """

    # Render Table if available
    table_html = ""
    if "table_headers" in topic and "table_rows" in topic and topic["table_rows"]:
        th_elements = "".join([f'<th style="padding: 1rem; color: #fff; border-bottom: 1px solid #1e293b;">{h}</th>' for h in topic["table_headers"]])
        tr_elements = "".join([
            f'<tr><td style="padding: 0.9rem 1rem; border-bottom: 1px solid #1e293b; color: #fff; font-weight: 600;">{r[0]}</td><td style="padding: 0.9rem 1rem; border-bottom: 1px solid #1e293b;"><code style="background:#1e293b; color:#38bdf8; padding:0.15rem 0.4rem; border-radius:4px;">{r[1]}</code></td><td style="padding: 0.9rem 1rem; border-bottom: 1px solid #1e293b; color: #94a3b8;">{r[2]}</td></tr>'
            for r in topic["table_rows"]
        ])
        table_html = f"""
        <!-- RESPONSIVE CONFIGURATION TABLE -->
        <div class="table-responsive" style="margin: 2.5rem 0;">
          <table style="width: 100%; border-collapse: collapse; background: #080d14; border: 1px solid #1e293b; border-radius: 10px; overflow: hidden; font-size: 0.9rem;">
            <thead>
              <tr style="background: #0f172a; text-align: left;">
                {th_elements}
              </tr>
            </thead>
            <tbody>
              {tr_elements}
            </tbody>
          </table>
        </div>
        """

    # Render Sections
    sections_html = ""
    for idx, s in enumerate(topic['sections']):
        sections_html += f"""
        <h2 id="sec-{idx+1}" style="color: #fff; font-size: 1.5rem; font-weight: 700; margin: 2.25rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 1px solid #1e293b;">
          {idx+1}. {s[0]}
        </h2>
        <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.75; margin-bottom: 1.25rem;">
          {s[1]}. Understanding this configuration logic is essential for designing resilient enterprise supply chains and ensuring upgrade compatibility with Clean Core standards.
        </p>
        <div style="background: #080d14; border: 1px solid #1e293b; border-left: 3px solid #38bdf8; border-radius: 8px; padding: 1.25rem; margin: 1.5rem 0;">
          <strong style="color: #fff; display: block; margin-bottom: 0.35rem; font-size: 0.95rem;">📌 Implementation Note for Consultants</strong>
          <p style="color: #94a3b8; font-size: 0.9rem; margin: 0; line-height: 1.6;">
            Always verify that transport requests for {s[0]} are tested end-to-end in the Quality (QAS) environment with active stock transactions before scheduling production deployment.
          </p>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{topic['title']} | theTechMentor</title>
  <meta name="description" content="{topic['meta_desc']}" />
  <link rel="canonical" href="https://youronementor.com/blog/{topic['slug']}.html" />
  <meta property="og:title" content="{topic['title']}" />
  <meta property="og:description" content="{topic['meta_desc']}" />
  <meta property="og:image" content="https://youronementor.com/images/og-cover.svg" />
  <link rel="stylesheet" href="../styles.css" />
  <link rel="stylesheet" href="blog.css" />
  <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
</head>
<body>
  <div class="reading-progress" id="reading-progress-bar"></div>

  <header class="header">
    <nav class="nav container">
      <a href="../index.html" class="logo">
        <span class="logo-mark">SAP</span>
        <span class="logo-text">theTechMentor</span>
      </a>
      <ul class="nav-links">
        <li><a href="../index.html#courses">Live Batches</a></li>
        <li><a href="../index.html#self-paced">Self-Paced</a></li>
        <li><a href="index.html" style="color:var(--blog-accent-light); font-weight:600;">Blog Hub</a></li>
        <li><a href="../index.html#pricing">Pricing</a></li>
        <li><a href="../index.html#enroll" class="btn btn-sm">Enroll Now</a></li>
      </ul>
    </nav>
  </header>

  <main class="blog-article-wrap">
    <div class="blog-breadcrumb">
      <a href="../index.html">Home</a> &gt; <a href="index.html">Blog</a> &gt; <span>{topic['category']}</span>
    </div>

    <header class="blog-header">
      <span class="sp-badge sp-badge--teal" style="margin-bottom:1rem; display:inline-block;">{topic['badge']}</span>
      <h1 class="blog-title">{topic['title']}</h1>
      
      <div class="blog-meta">
        <div class="author-chip">
          <div class="author-avatar-ph">AB</div>
          <div class="author-info">
            <strong>Anshuman Behuria</strong>
            <span>Lead SAP S/4HANA Trainer</span>
          </div>
        </div>
        <span>•</span>
        <span>{date_str}</span>
        <span>•</span>
        <span>⏱️ {topic['read_time']}</span>
      </div>
    </header>

    <article class="article-content">

      <!-- TOP PDF DOWNLOAD CARD -->
      <div style="background:#080d14; border:1px solid #1e293b; border-left:4px solid #38bdf8; padding:1.25rem; border-radius:10px; margin:1.5rem 0; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
        <div>
          <strong style="color:#fff; font-size:1.05rem; display:block;">📄 Download Original PDF Guide</strong>
          <span style="color:#94a3b8; font-size:0.85rem;">Prefer reading offline? Access the full technical documentation of this guide.</span>
        </div>
        <a href="{topic['slug']}.html" class="btn btn-sm btn-primary" style="padding:0.6rem 1.25rem; font-weight:700; text-decoration:none; background:linear-gradient(135deg,#0284c7,#7c3aed); border:none; color:#fff; border-radius:6px;">Download PDF Guide ↗</a>
      </div>

      <!-- TARGET METADATA GRID -->
      <div style="background: #080d14; border: 1px solid #1e293b; border-radius: 10px; padding: 1.5rem; margin-bottom: 2rem; display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem;">
        <div style="border-left: 3px solid #0284c7; padding-left: 0.85rem;">
          <span style="color: #94a3b8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; display: block;">Target Role:</span>
          <strong style="color: #fff; font-size: 0.95rem;">{topic['role']}</strong>
        </div>
        <div style="border-left: 3px solid #0284c7; padding-left: 0.85rem;">
          <span style="color: #94a3b8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; display: block;">Primary Keyword:</span>
          <code style="background: #1e293b; color: #38bdf8; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.85rem;">{topic['keyword']}</code>
        </div>
        <div style="border-left: 3px solid #0284c7; padding-left: 0.85rem;">
          <span style="color: #94a3b8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; display: block;">Platform:</span>
          <strong style="color: #fff; font-size: 0.95rem;">SAP S/4HANA (Private Cloud &amp; On-Premise)</strong>
        </div>
        <div style="border-left: 3px solid #0284c7; padding-left: 0.85rem;">
          <span style="color: #94a3b8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; display: block;">Prerequisites:</span>
          <strong style="color: #fff; font-size: 0.95rem;">Core understanding of SAP Logistics &amp; SPRO Menu Navigation</strong>
        </div>
      </div>

      <!-- TABLE OF CONTENTS -->
      <div style="background:#080d14; border:1px solid #1e293b; border-radius:10px; padding:1.5rem; margin:1.75rem 0;">
        <h3 style="color:#fff; font-size:1.15rem; font-weight:700; margin:0 0 0.85rem 0; border-bottom:1px solid #1e293b; padding-bottom:0.5rem;">📑 In This Guide</h3>
        <ul style="padding-left:1.25rem; margin:0; display:flex; flex-direction:column; gap:0.4rem;">
          {toc_items}
        </ul>
      </div>

      <p style="font-size: 1.05rem; line-height: 1.75; color: #cbd5e1; margin-bottom: 2rem;">
        Enterprise logistics transformation requires a deep understanding of standard business processes, customizing controls, and modern Clean Core architecture. In this hands-on technical masterclass, we break down <strong>{topic['title']}</strong> with actionable configuration blueprints and real-world project troubleshooting advice.
      </p>

      {process_html}

      {table_html}

      {sections_html}

      <!-- CALLOUT CARD -->
      <div style="background:rgba(2,132,199,0.1); border-left:4px solid #38bdf8; padding:1.25rem; border-radius:8px; margin:2rem 0;">
        <strong style="color:#fff; display:block; margin-bottom:0.4rem;">🎯 KEY CONSULTANT TAKEAWAYS</strong>
        <p style="margin-bottom:0; font-size:0.95rem; color:#cbd5e1;">
          Mastering {topic['keyword']} prepares you to handle mission-critical logistics challenges, lead client workshops, and design scalable supply chains for global enterprise implementations.
        </p>
      </div>

      <!-- FOOTER PDF DOWNLOAD CARD -->
      <div style="background:#080d14; border:1px solid #1e293b; border-radius:10px; padding:1.5rem; margin:2.5rem 0; text-align:center;">
        <h4 style="color:#fff; font-size:1.15rem; font-weight:700; margin-bottom:0.4rem;">📄 Prefer Reading Offline?</h4>
        <p style="color:#94a3b8; font-size:0.9rem; margin-bottom:1rem;">Download the full PDF blueprint and implementation checklist for this guide.</p>
        <a href="{topic['slug']}.html" class="btn btn-primary" style="padding:0.75rem 1.75rem; font-weight:700; text-decoration:none; background:linear-gradient(135deg,#0284c7,#7c3aed); border:none; color:#fff; border-radius:6px;">Download Offline PDF Version ↗</a>
      </div>

      <!-- COURSE CTA CARD -->
      <div class="blog-course-cta">
        <span class="tier-badge" style="background:#f59e0b; color:#000; font-weight:700; padding:0.2rem 0.6rem; border-radius:4px; font-size:0.75rem; text-transform:uppercase;">Accelerate Your Career</span>
        <h3>Master SAP MM &amp; EWM S/4HANA Live with Anshuman Behuria</h3>
        <p>Get 24/7 server access, real project blueprints, and 1-on-1 interview preparation.</p>
        <div class="blog-cta-actions">
          <button type="button" class="btn btn-primary razorpay-link" data-amount="10999" data-program="MM + EWM Self-Paced Bundle">
            Get Complete Bundle — ₹10,999 ↗
          </button>
          <a href="../index.html#courses" class="btn btn-outline">View Batches</a>
        </div>
      </div>

    </article>
  </main>
</body>
</html>"""

def run_daily_publisher():
    log_msg("🚀 Starting Autonomous Twice-Daily Blog Publishing Routine...")
    
    # 1. Check already published slugs from repository and custom-blogs.js
    published_slugs = set()
    custom_blogs_js = os.path.join(BLOG_DIR, "custom-blogs.js")
    if os.path.exists(custom_blogs_js):
        with open(custom_blogs_js, "r", encoding="utf-8") as f:
            content = f.read()
            for t in TOPIC_POOL:
                if t['slug'] in content:
                    published_slugs.add(t['slug'])

    # Also check html files in blog/
    for fname in os.listdir(BLOG_DIR):
        if fname.endswith(".html"):
            published_slugs.add(fname[:-5])

    # 2. Filter un-published topics from pool
    available_topics = [t for t in TOPIC_POOL if t['slug'] not in published_slugs]
    
    # If all predefined topics are published, invoke dynamic generator
    if not available_topics:
        log_msg("ℹ️ All predefined topics have been published. Invoking Autonomous Dynamic Topic Synthesizer...")
        topic = generate_dynamic_sap_topic()
        while topic['slug'] in published_slugs:
            topic = generate_dynamic_sap_topic()
    else:
        topic = random.choice(available_topics)

    log_msg(f"📌 Selected Trending Topic: {topic['title']}")
    log_msg(f"📌 Primary SEO Keyword : {topic['keyword']}")
    log_msg(f"📌 Target Article Slug  : {topic['slug']}")

    # 3. Build HTML article
    article_path = os.path.join(BLOG_DIR, f"{topic['slug']}.html")
    html_content = render_article_html(topic)

    with open(article_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    log_msg(f"✅ Generated Article Page: {article_path}")

    current_date_str = datetime.datetime.now().strftime('%b %d, %Y')
    current_iso_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # 4. Update blog/custom-blogs.js
    if os.path.exists(custom_blogs_js):
        with open(custom_blogs_js, "r", encoding="utf-8") as f:
            js_data = f.read()
        
        if topic['slug'] not in js_data:
            new_entry = f""",
  {{
    id: "post_{int(time.time()*1000)}",
    title: "{topic['title']}",
    slug: "{topic['slug']}",
    category: "{topic['category']}",
    readTime: "{topic['read_time']}",
    date: "{current_date_str}",
    isoDate: "{current_iso_date}",
    excerpt: "{topic['meta_desc']}",
    imageUrl: "https://youronementor.com/images/og-cover.svg"
  }}
];"""
            js_data = js_data.rstrip().rstrip(";").rstrip("]").rstrip() + new_entry
            with open(custom_blogs_js, "w", encoding="utf-8") as f:
                f.write(js_data)
            log_msg("✅ Updated blog/custom-blogs.js repository file")

    # 5. Update homepage index.html
    home_html = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(home_html):
        with open(home_html, "r", encoding="utf-8") as f:
            h_data = f.read()
        
        if topic['slug'] not in h_data:
            cat_badge_class = "blog-post-badge--teal"
            if "interview" in topic['category'].lower():
                cat_badge_class = "blog-post-badge--blue"
            elif "career" in topic['category'].lower():
                cat_badge_class = "blog-post-badge--amber"

            card_html = f"""
          <!-- Auto-Published on {current_date_str} -->
          <article class="blog-card" data-cat="tutorial" data-date="{current_iso_date}">
            <div class="blog-thumb" style="background:#ccfbf1;">📰</div>
            <div class="blog-body">
              <span class="blog-post-badge {cat_badge_class}">{topic['badge'].upper()}</span>
              <div class="blog-post-title">{topic['title']}</div>
              <div class="blog-meta-line">By Anshuman Behuria &middot; {topic['read_time']} &middot; {current_date_str}</div>
              <a href="blog/{topic['slug']}.html" class="blog-read-link">Read article &amp; join Q&amp;A &rarr;</a>
            </div>
          </article>"""
            target_str = '<div class="blog-grid" id="blog-grid">'
            if target_str in h_data:
                h_data = h_data.replace(target_str, target_str + "\n" + card_html)
                with open(home_html, "w", encoding="utf-8") as f:
                    f.write(h_data)
                log_msg("✅ Updated homepage index.html with new blog card")

    # 6. Update blog/index.html hub
    hub_html = os.path.join(BLOG_DIR, "index.html")
    if os.path.exists(hub_html):
        with open(hub_html, "r", encoding="utf-8") as f:
            hb_data = f.read()
        
        if topic['slug'] not in hb_data:
            cat_badge_class = "blog-post-badge--teal"
            if "interview" in topic['category'].lower():
                cat_badge_class = "blog-post-badge--blue"
            elif "career" in topic['category'].lower():
                cat_badge_class = "blog-post-badge--amber"

            hub_card = f"""
        <!-- Auto-Published on {current_date_str} -->
        <article class="blog-card" data-cat="tutorial" data-date="{current_iso_date}">
          <div class="blog-thumb" style="background:#ccfbf1;">📰</div>
          <div class="blog-body">
            <span class="blog-post-badge {cat_badge_class}">{topic['badge'].upper()}</span>
            <h2 class="blog-post-title" style="font-size:1.15rem; margin:0.5rem 0;">{topic['title']}</h2>
            <div class="blog-meta-line">By Anshuman Behuria &middot; {topic['read_time']} &middot; {current_date_str}</div>
            <a href="{topic['slug']}.html" class="blog-read-link">Read article &amp; join discussion &rarr;</a>
          </div>
        </article>"""
            hub_target = '<div class="blog-grid" id="hub-blog-grid">'
            if hub_target in hb_data:
                hb_data = hb_data.replace(hub_target, hub_target + "\n" + hub_card)
                with open(hub_html, "w", encoding="utf-8") as f:
                    f.write(hb_data)
                log_msg("✅ Updated blog/index.html hub with new blog card")

    # 7. Invoke publish_blog.py with dynamic payload
    pub_script = os.path.join(BASE_DIR, "scripts", "publish_blog.py")
    payload = {
        "title": topic['title'],
        "slug": topic['slug'],
        "category": topic['category'],
        "tags": ["SAP MM", "SAP EWM", "S/4HANA 2026", topic.get('badge', 'SAP'), "Clean Core"],
        "status": "publish",
        "meta_title": f"{topic['title']} | theTechMentor",
        "meta_description": topic['meta_desc'],
        "focus_keyword": topic['keyword'],
        "live_url": f"https://youronementor.com/blog/{topic['slug']}.html"
    }
    res = subprocess.run([sys.executable, pub_script, json.dumps(payload)], check=False)
    if res.returncode == 0:
        log_msg(f"🎉 Successfully published article '{topic['title']}'!")
    else:
        log_msg(f"⚠️ Publishing returned non-zero code {res.returncode}.")

if __name__ == "__main__":
    run_daily_publisher()
