# 📊 PDF Access Log ETL Pipeline

> **Extracts 684K+ badge-to-reader access records from complex PDFs** using Python, transforms them into structured Excel and MySQL tables, and enables security auditing and dashboarding for operations teams.

---

## 🧩 Problem Statement

Our team received access control logs in the form of complex PDFs from the OnGuard system. These included:

* Reader ID blocks (`MC104B AZBio B ...`)
* Timezone & Elevator mappings
* Badge holders with activation/deactivation details
* Inconsistent headers, footers, and multi-line entries

These were not machine-readable and couldn't be loaded into analytics platforms or dashboards.

---

## 🛠️ Tech Stack

| Layer       | Tools / Libraries             |
| ----------- | ----------------------------- |
| Language    | Python                        |
| PDF Parsing | PyMuPDF (`fitz`), `pdftotext` |
| Processing  | `pandas`, `re`, `subprocess`  |
| Output      | Excel (`.xlsx`), MySQL tables |
| Visuals     | Power BI, Excel Dashboards    |

---

## ✅ Features

### 1. Reader Extraction with Suffix Merging

```python
if line in merge_suffixes and merged_lines:
    merged_lines[-1] += f" {line}"
else:
    merged_lines.append(line)
```

* Merges suffix-only lines like `BUTTON`, `SEC-L`, `NORTH DR`
* Filters lines to keep only valid `MCxxxx` entries

### 2. Timezone ↔ Reader Mapping

```python
if "Timezone/Elevator Level" in line:
    reader_queue = []
    timezone_queue = []
    # match them based on order and alignment
```

* Parses timezone blocks and aligns each reader accordingly

### 3. Badge Holder Data Extraction

```python
if re_badge.search(line):
    badge_id = match.group(1)
    ...
    while next_line not in (new reader or header):
        append to current row
```

* Reconstructs multi-line badge records and links them to readers

---

## 📦 Key Outputs

* `final_reader_timezone_corrected.xlsx`
* `only_mc_readers.xlsx`
* `BDC 2nd Floor Lab Cardholders.xlsx`
* `Cardholder Access to Readers 051-100.xlsx`

---

## 📸 Screenshots

### 🔄 Merged Reader Records

<img width="321" height="85" alt="image" src="https://github.com/user-attachments/assets/bb1ae9ac-fd15-4be7-8740-633d631ad269" />


### ✅ Mapping Status Summary

<img width="309" height="80" alt="image" src="https://github.com/user-attachments/assets/c5bbb7b5-6415-4c57-b631-d405d3eaa1bd" />


### 🧾 684,000+ Badge Records Extracted

<img width="1125" height="134" alt="image" src="https://github.com/user-attachments/assets/affaaca0-fb63-40d9-a62d-c3d1092d7b69" />



---

## 🔍 Business Impact & Use Cases

| Use Case                    | Description                                              |
| --------------------------- | -------------------------------------------------------- |
| 🔒 Security Audits          | Match badge access to authorized readers and floors      |
| 👤 Badge Governance         | Flag expired users with active badges                    |
| 🏢 Space Utilization        | Map readers to zones and analyze traffic                 |
| 🧠 Operational Optimization | Detect anomalies in reader assignments or access timings |
| 💾 Data Integrity Fixes     | Filled gaps in badge-to-reader database relationships    |

---

## 📈 Metrics Delivered

* ✅ 684K+ records processed from PDF
* 🧑‍💼 Detected 100s of past employees with active badges
* 📋 Created full audit log in Excel
* 🗃️ Integrated structured reader access into MySQL with updated mappings
* 📊 Enabled Power BI dashboards for Ops & HR

---

## 🧠 Why This Is a Data Engineering Project

✔️ Extract → Clean → Normalize → Serve pipeline with scalable Python tools
✔️ Automated logic to parse semi-structured, multi-line PDF data
✔️ Built new MySQL tables to support integration with HR & Security
✔️ Supported downstream analytics (Power BI) and operational remediation

> ✅ This is end-to-end **data engineering meets physical security analytics**.

---


