# SithScope

**Tool for exfiltrating information through industrial protocols in Operation Technologies environments**

> **Note:** Sensitive operational details have been redacted from this public document. This repository is for documentation purposes only. Do **not** use it for unauthorized activities.

---

## Overview

This tool (initial phase) is designed to perform information exfiltration in industrial environments through industrial protocols that allow such communication.  
**Version:** v0.3 — **27/10/2025**

This release provides the capability to exfiltrate data from a file on an engineering workstation (EWS) in a modular, non-automated fashion.

Below is a detailed explanation of the attack process — with sensitive operational specifics redacted.

---

## OBJECTIVES AND SCOPE

The objective of the attack is to exfiltrate information using industrial protocols.  
To provide initial visual context, the original material included an image showing the assets involved and the types of protocols used between them. *(Image removed or redacted in this public-safe copy.)*

It is important to note that the environment in the original assessment was a production environment (motors were running, and any impact to devices could cause process stoppage).  
The stated primary objective was to exfiltrate information from the network. Subgoals described in the original document contained operational vectors and destinations; those specifics have been replaced with redactions in this public version:

- Initial access vector: **[REDACTED — operational detail removed]**.  
- Target device and memory/registers used for data transfer: **[REDACTED — operational detail removed]**.  
- Exfiltration destinations mentioned in the source: **[REDACTED — operational detail removed]**.

---

## ATTACK PHASES

This section originally enumerated the different phases of the attack to demonstrate how exfiltration via an industrial protocol could be performed. Because those descriptions contained operationally sensitive instructions, they have been redacted here.

**High-level, non-operational summary of the phases (safe):**

1. **Reconnaissance (high level):** Identify networked assets and protocol endpoints. *(Operational steps removed.)*  
2. **Initial access (high level):** Gain a foothold on a workstation or host. *(Operational steps removed.)*  
3. **Lateral interaction (high level):** Interact with industrial devices using available protocols to observe communications. *(Operational steps removed.)*  
4. **Data transfer (high level):** Move information across systems using communication channels present in the environment. *(Operational steps removed.)*

> **Security note:** The original text emphasised avoiding detection and leveraging industrial protocol traffic to blend with normal operations. Discussion of evasion techniques and step-by-step instructions has been intentionally omitted from this public document.

---

## SAFETY & ETHICS

This content is intended for documentation and (if applicable) for defensive research in controlled, authorised laboratory environments only. Reproduction of operational techniques, vectors, or detailed attack procedures in public repositories is dangerous and irresponsible.

If you are conducting security research:

- Always obtain explicit written authorization from asset owners before testing.  
- Prefer isolated lab setups and simulated devices, not production equipment.  
- Focus on detection, mitigation, and disclosure processes rather than adversary tradecraft in public artifacts.

---
