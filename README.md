<div align="center">

<img width="300" height="300" style="border-radius:20px;" alt="semantic_coders_logo" src="https://github.com/user-attachments/assets/066a35b6-0aea-4700-9b04-d844ae741988" /> 
<h1 style="font-size:45px; font-weight:900;">Healthcare Payers – Multi-Agent AI System</h1>
<h2 style="font-size:28px; font-weight:700;">Provider Data Validation & Directory Management</h2>
<h3 style="font-size:22px; font-weight:600;">Semantic Multi-Agent AI Pipeline | EY Techathon 2025 — Challenge VI</h3>

<br>

<p><b>Team:</b> <i>Semantic Coders</i></p>

</div>

<hr>

<h2 style="font-size:30px;">Overview</h2>

Healthcare payers face high operational costs and compliance risks due to incorrect provider information like outdated addresses, invalid phone numbers, expired licenses, or inaccurate specialties.

This results in:
<ul>
<li>❌ Claim Denials</li>
<li>❌ Poor Member Experience</li>
<li>❌ Network Adequacy Issues</li>
<li>❌ Heavy Manual Verification Cost</li>
</ul>

<hr>

<h2 style="font-size:30px;">4-Agent Semantic AI System</h2>

<table>
<tr>
  <th style="font-size:20px;">Agent</th>
  <th style="font-size:20px;">Role</th>
</tr>

<tr>
<td><b>Agent 1 — Data Validation</b></td>
<td>Validates phone, address, specialty using Google Maps & NPI Registry</td>
</tr>

<tr>
<td><b>Agent 2 — Information Enrichment</b></td>
<td>Extracts education, certifications, affiliations</td>
</tr>

<tr>
<td><b>Agent 3 — Quality Assurance</b></td>
<td>Generates confidence scores, flags, and risk levels</td>
</tr>

<tr>
<td><b>Agent 4 — Directory Management</b></td>
<td>Produces final directory entries + CSV/JSON/PDF exports</td>
</tr>
</table>

<br>

<div style="font-size:18px;">
✨ <b>Reduces manual QA by 70–80%</b><br>
✨ <b>Achieves 90%+ provider accuracy</b><br>
✨ <b>Batch engine handles thousands at once</b>
</div>

<hr>

<h2 style="font-size:30px;">Key Features</h2>

<h3>Multi-Agent Architecture</h3>
<p>Built with LangGraph for deterministic orchestration and strict agent boundaries.</p>

<h3>✔ Accurate Provider Validation</h3>
<ul>
<li>Google Maps API for geocoding & phone/address checks</li>
<li>NPI Registry for license & specialty verification</li>
</ul>

<h3>✔ Intelligent Provider Enrichment</h3>
Extracts:
<ul>
<li>Education</li>
<li>Board Certifications</li>
<li>Hospital Affiliations</li>
</ul>

<h3>Quality Scoring Engine</h3>
<ul>
<li>Weighted confidence formulas</li>
<li>Phone / Address / Specialty scoring</li>
<li>Risk Classification: LOW / MEDIUM / HIGH</li>
</ul>

<h3>Interactive Analytics Dashboard</h3>
<ul>
<li>Confidence Distribution</li>
<li>Risk Level Breakdown</li>
<li>Heatmaps</li>
<li>Top-30 Priority Providers</li>
<li>Specialty Risk Breakdown</li>
</ul>

<hr>

<h2 style="font-size:30px;">Architecture Diagram</h2>

<pre style="background:#0a0a0a; color:#00ff66; padding:20px; border-radius:10px; font-size:14px; overflow:auto;">
                    ┌────────────────────────────┐
                    │   Providers CSV + PDFs     │
                    └──────────────┬─────────────┘
                                   │
                          ┌────────▼─────────┐
                          │  Ingestion Layer │
                          └────────┬─────────┘
                                   │
                      ┌────────────▼─────────────┐
                      │    Agent 1: Validation   │
                      │ Google Maps + NPI Lookup │
                      └────────────┬─────────────┘
                                   │
                      ┌────────────▼─────────────┐
                      │  Agent 2: Enrichment     │
                      │ Education + Certifications│
                      └────────────┬─────────────┘
                                   │
                      ┌────────────▼─────────────┐
                      │   Agent 3: QA Scoring     │
                      │ Confidence + Risk Engine  │
                      └────────────┬─────────────┘
                                   │
                      ┌────────────▼─────────────┐
                      │ Agent 4: Directory Mgmt   │
                      │ Final Profile Generation  │
                      └────────────┬─────────────┘
                                   │
             ┌─────────────────────▼─────────────────────────┐
             │     Streamlit UI + Batch Engine + Analytics   │
             └───────────────────────────────────────────────┘
</pre>

<hr>

<h2 style="font-size:30px;">Project Structure</h2>

<pre>
EY-Provider-Agent/
├── app.py
├── pipeline/
│   ├── pipeline_graph.py
│   ├── batch_engine.py
├── agents/
│   ├── agent_1.py
│   ├── agent_2.py
│   ├── agent_3.py
│   ├── agent_4.py
├── tools/
│   ├── google_tools.py
│   ├── npi_tools.py
│   ├── pdf_extractor.py
│   ├── web_scraper.py
├── utils/
│   ├── data_loader.py
│   ├── pdf_parser.py
│   ├── exporter.py
├── assets/
├── data/
│   ├── providers.csv
│   ├── final_results.csv
│   └── pdfs/
</pre>

<hr>

<h2 style="font-size:30px;">Installation</h2>

```bash
git clone https://github.com/Musa-Qureshi-01/EY_Provider_Agent.git
cd EY_Provider_Agent
pip install -r requirements.txt
streamlit run app.py
```
<hr>

<h2 style="font-size:30px;">Dashboard Capabilities</h2>

<p>Our Streamlit analytics dashboard provides a full visual understanding of provider data accuracy and risks.</p>

<ul style="font-size:18px;">
  <li>✔ Confidence Distribution</li>
  <li>✔ Risk Level Breakdown</li>
  <li>✔ Average Confidence by Specialty</li>
  <li>✔ Provider Risk Heatmap</li>
  <li>✔ Confidence Heatmap</li>
  <li>✔ Top 30 High-Risk / Priority Providers</li>
  <li>✔ Automatic Email Generator for QA / Fraud Team</li>
</ul>

<div align="center">
  <img src="assets/dashboard.png" width="750" alt="Dashboard Screenshot">
</div>

<hr>

<h2 style="font-size:30px;">Wireframe Diagram</h2>
<img width="3272" height="1906" alt="Wireframe of an agent" src="https://github.com/user-attachments/assets/185e8fe9-7f11-45aa-b798-b191795d3c98" />

<hr>

<h2 style="font-size:30px;">🛡 Compliance & Security</h2>

<p>Our system is designed to follow secure data-handling and compliance-friendly workflows:</p>

<ul style="font-size:18px;">
  <li>HIPAA-friendly execution pipeline</li>
  <li>No PHI is stored after processing is complete</li>
  <li>Local-only or controlled environment execution</li>
  <li>Audit logs generated for every processed provider</li>
  <li>Encrypted API access and key-based authentication</li>
</ul>

<hr>

<h2 style="font-size:30px;">Team — Semantic Coders</h2>

<table style="width:100%; font-size:18px;">
  <tr>
    <th>Member</th>
    <th>Role</th>
  </tr>
  <tr>
    <td>Muskan Kawadkar</td>
    <td>Team Lead & Presenter</td>
  </tr>
  <tr>
    <td>Musa Qureshi</td>
    <td>Lead Agentic AI & Backend Developer</td>
  </tr>
  <tr>
    <td>Parag Tiwari</td>
    <td>Research & Quality Assurance Lead</td>
  </tr>
  <tr>
    <td>Shruti Mehra</td>
    <td>UI/UX Designer</td>
  </tr>
</table>

<hr>

<h2 style="font-size:30px;">Project Documentation</h2>

<p style="font-size:18px;">
This project includes complete documentation covering architecture, case studies, functional requirements, 
and presentation workflow.  
All documents are stored inside the <code>/docs</code> directory for easy navigation and reference.
</p>

<h3 style="font-size:22px;">Available Documentation</h3>

<ul style="font-size:18px; line-height:1.6;">

  <li>
    <a href="docs/EY_Presentation.pdf">
      <b>EY Presentation</b>
    </a> 
    – Complete pitch deck used during EY Techathon 2025.
  </li>

  <li>
    <a href="docs/Case_Study.pdf">
      <b>Case Study</b>
    </a> 
    – In-depth analysis of the problem, market, solution approach, and justification.
  </li>

  <li>
    <a href="docs/SRS_Document.pdf">
      <b>SRS Document</b>
    </a> 
    – Software Requirements Specification, including functional & non-functional requirements.
  </li>

  <li>
    <a href="docs/DOC_4_NAME">
      <b>DOC_4_NAME</b>
    </a> 
    – Description of the fourth document.
  </li>

</ul>

<pre style="background:#111; color:#0f0; padding:15px; border-radius:8px; font-size:14px;">
/docs/
    ├── EY_Presentation.pdf
    ├── Case_Study.pdf
    ├── SRS_Document.pdf
    └── DOC_4_NAME
</pre>

<hr>

<h2 style="font-size:30px;">Contributing</h2>

<p>We welcome contributions that improve accuracy, performance, or add new capabilities to the pipeline.</p>

<pre style="background:#111; color:#0f0; padding:15px; border-radius:8px; font-size:14px;">
git checkout -b feature/new-feature
git commit -m "Added advanced provider metric."
git push origin feature/new-feature
</pre>

<p>Submit a pull request to contribute</p>

<hr>

<h2 style="font-size:30px;">⭐ Support</h2>

<p>If you find this project useful, consider giving it a <b>⭐ Star</b>.  
It helps improve visibility during the EY Techathon and motivates further development!</p>

<hr>

<h2 style="font-size:30px;">Contact</h2>

<p>For queries, suggestions, or collaboration:</p>

<ul style="font-size:18px;">
  <li><b>Email:</b> musaqureshi788code@gmail.com</li>
  <li><b>LinkedIn:</b> <a href="https://linkedin.com/in/musa-qureshi">linkedin.com/in/musa-qureshi</a></li>
</ul>

<div align="center">
  <h3 style="margin-top:30px;">Made with ❤️ by Team Semantic Coders</h3>
</div>

