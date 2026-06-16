# Legal-Admin AI Automation (GrowingBean)

An AI-powered administrative document intake system designed for in-house legal teams to automate the extraction of metadata from official documents (*công văn*).

## Overview
This project leverages the OpenClaw framework to transform unstructured official PDF documents into structured data. By combining text extraction and predefined processing rules, the system minimizes manual data entry and prepares legal documents for project management and archiving.

## Problem Statement
In-house legal departments often handle a high volume of official administrative documents. Manually extracting the issuer, document number, date, and deadlines for tracking is time-consuming and prone to human error, leading to potential delays in critical legal responses.

## Solution
The project introduces a specialized `legal-admin` skill that implements a strict extraction schema. Instead of full-text OCR, it focuses on "metadata-first" extraction, identifying the core administrative markers of a document to generate a standardized JSON output for downstream integration.

## Current Workflow
1. **Intake:** User uploads a PDF document via Telegram.
2. **Processing:** The `/skill legal-admin` is invoked.
3. **Extraction:** The system applies specific rules (via `parser.py`) to identify the document's header and footer.
4. **Output:** A JSON object is produced containing:
   - File name, Issuing authority, Document number, Date, Main issue, Responsible department, and Deadline.
5. **Archiving:** System state and configurations are backed up as clean checkpoints to S3-compatible vStorage.

## Features Verified
- ✅ **Metadata Extraction:** Successfully extracted schema-v1 data from various official PDF formats.
- ✅ **Telegram Intake:** PDF upload and processing verified via Telegram.
- ✅ **Jira Connectivity:** Jira Draft workflow validated; Owner-controlled Jira issue creation tested (e.g., Issue `OL-1`).
- ✅ **System Recovery:** Automated "Clean Backup" process to vStorage (S3-compatible) for system recovery.
- ✅ **Identity-Based Access Control:** Implementation of Owner vs. Guest roles based on `sender_id` verification.
- ✅ **Security Hardening:** Integrated secret scanning, credential sanitization, and incident recovery protocols.

## Architecture
- **Core Framework:** OpenClaw.
- **Specialized Skill:** `legal-admin` (includes `SKILL.md` and `parser.py`).
- **Operational Infrastructure:** vStorage used for backup and recovery checkpoints.
- **Management:**
Jira draft workflow and owner-controlled issue creation PoC.

## Security Hardening Journey
To ensure the integrity of the legal workspace, the project underwent a comprehensive security hardening process:
- **Incident Response:** Detected a Jira credential leak; immediately revoked exposed Jira token and sanitized credentials.
- **Workspace Sanitization:** Implemented full-workspace secret scanning and cleaned plaintext credentials from all scripts and config files.
- **Quarantine Protocol:** Introduced a security quarantine mechanism to isolate compromised logs.
- **Access Audit:** Completed a full Access Control Audit to verify Owner/Guest boundaries.
- **Clean Checkpoint:** Created a verified "Clean Backup" to vStorage after all sanitization was completed.

## Security Measures
- **Sender-ID Verification:** All sensitive actions are gated by a cross-reference check against `USER.md`.
- **Guest-Isolation Principle:** Restricted mode for non-authorized users to prevent access to `MEMORY.md`, `TOOLS.md`, and system configs.
- **Credential Sanitization:** Use of placeholders (`<ENV:...>`) and environment variables to prevent plaintext secret leakage.

## Current Limitations
- **Guest Mode Validation:** Guest experience has not yet been validated with a real external account.
- **Security Architecture:** Security still relies partly on policy-level controls (LLM prompt) rather than system-level hard-gates.
- **Channel Verification:** Zalo file upload flow has not been fully verified.
- **Jira Workflow:** Guest-specific Jira token workflow is not yet implemented.

## Future Improvements
- **Hardened Security:** Transition from policy-based to system-level hard-gates for sensitive tools.
- **Guest Experience:** Rigorous testing of the Guest mode with multiple external accounts.
- **Expanded Intake:** Implementation of email-to-bot and web upload portals.
- **Enhanced Jira Flow:** Automated task creation and status tracking for Guest users via scoped tokens.

## Tested Documents
The system has been verified against the following document types:
- `3871/TB-KBNN`
- `2256/TTg-KTN`
- `1075/QLCL-CL1`
- `16702/BTC-CĐKT`
- `7366/TCHQ-GSQL`

## Demo Scenario
1. **User:** Uploads a PDF of a government notice via Telegram.
2. **User:** Sends command `/skill legal-admin`.
3. **AI:** Processes the PDF and returns:
   ```json
   {
    "ten_file": "notice_123.pdf",
    "co_quan_ban_hanh": "Ministry of Finance",
    "so_hieu": "123/BTC-TCT",
    "ngay_ban_hanh": "2026-06-10",
    "van_de_chinh": "Instruction on tax reporting for Q2",
    "bo_phan_can_xu_ly": ["Accounting Dept"],
    "deadline": "2026-07-01"
   }
   ```

## Disclaimer
This project is developed for productivity enhancement and research purposes. While security measures are implemented, it is not claimed as "absolutely secure" and should be used in accordance with the defined `USER.md` permission matrix.
