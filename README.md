# SithScope

**Tool for exfiltrating information through industrial protocols in Operation Technologies environments.**

> **Note:** Confidential operational details have been removed from this public document. This repository is for documentary purposes only. Its use for unauthorised activities is **not** permitted.

---

## Overview

This tool (in an early stage of development) is designed to exfiltrate information through industrial communication protocols present within the target architecture.  
**Version:** v0.3 — **27/10/2025** In this version all the capabilities of the tool are focused on the industrial protocol Modbus. In a future version the tool will have the capabilities to use other industrial protocols with functions to allow the exfiltration.

This release provides the capability to exfiltrate data from a file on an engineering workstation (EWS) in a modular, non-automated fashion.

Below is a detailed explanation of the tool processes and phases.

---

## OBJECTIVES AND SCOPE

The objective of the tool is to exfiltrate information using industrial protocols without being detected or with minimal changes to the security tool notifications. 
To provide initial visual context, the material included an image showing the assets involved and the types of protocols used between them.

<img width="894" height="582" alt="image" src="https://github.com/user-attachments/assets/a51bbbc7-bb2e-42f0-aa80-da9495998e3b" />

It is important to note that the environment in the original assessment was a production environment (motors were running, and any impact to devices could cause process stoppage).  
The stated primary objective was to exfiltrate information from the network, specifically from the engineering station. Other sub-objectives included asset detection, services dedicated to industrial environments, open ports, protocols used, etc.

------

## REFERENCE ARCHITECTURE

The following architecture represents a typical reference architecture in a real industrial environment. The architecture shown below should be taken as an example, but also as the actual environment in which the technical exfiltration tests were performed.

<img width="893" height="502" alt="image" src="https://github.com/user-attachments/assets/40b68a20-daf8-4d7d-a150-6a40e8efb6c0" />

Different networks can be seen including the **IT Network**, the **DMZ IT/OT**, the **Monitoring Network**, the **Control Network** and finally the **Field Network**.

- **The IT Network:** In this example the network was created, and different devices were connected but they are **not relevant** for the purpose of this test.
- **The DMZ IT/OT:** This network has a **Jump Host** for different providers' connections to the industrial networks.
- **The Monitoring Network:** This network represents a virtual **SCADA** configured in **Workstation 2**. As will be seen later, the SCADA was published on Internet what could allow the access to everyone.
- **The Control Network:** One **PLC** with an **HMI** in the laboratory were included. Also, **Workstation 1** was in this network having the software to configure the HMI and the PLC, representing an **Engineering Workstation**.
- **The Field Network:** This network includes two **frequency shifters** and two **motors** controlled by the shifters.

------

## TOOL PHASES

This section originally enumerated the different phases of the "attack" using the tool to demonstrate how exfiltration via an industrial protocol could be performed.

**SithScope tool phases**

1. **PHASE 1: Infection of the engineering workstation** 
2. **PHASE 2: Analysis of the industrial device using Modbus TCP** 
3. **PHASE 3: Prepare the file and information that will be exfiltrated** 
4. **PHASE 4: Exfiltration of information using industrial protocols**

### 1. PHASE 1

In an initial phase, an as initial vector attack, we have chosen a USB infection to the EWS 1 where a malware will be deployed (there are many studies and attacks that demonstrate that this practice from the attackers continues to be used like no other).
As in this study, the infection of this device is not the main point, we have used an external device to simulate the EWS 1 and execute the different phases of our script directly to the network.
In the next picture, the initial architecture of the attack can be seen:

<img width="894" height="581" alt="image" src="https://github.com/user-attachments/assets/6614f948-a371-4847-ab6c-4e211bd9245c" />

At this point, using a tool created by us and called SithScope, different features will be available:
1. Scan of the network looking up for the different industrial devices. This aspect is critical due to knowing what and where are the different devices, their interactions with other industrial devices and with which protocol, is the first stage of the attack. This feature of the tool just implements a simple scan of different TCP and UDP industrial ports but with a slow execution to avoid being detected and using specific industrial protocols requests.
2. The second functionality was implemented to detect if the device where the malware was deployed was an industrial engineering station (to then execute the exfiltration of information on it). 
This functionality of the tool has been developed to analyse different processes and the existence of different software in the device’s objective. If any of them is running, the tool will detect that the device is an engineering workstation. In this case, and as is not the main objective of the analysis, a simple process was executed in parallel to simulate the process.

**From this, the next functionalities are fully related with the exfiltration process using the industrial protocol Modbus TCP.**

### 2. PHASE 2

This second phase of the attack will be focused in analysing the device that has been communicating with the EWS 1. This has been detected thanks to the analysis done with the previous functionalities.
This device had been identified as the PLC M580, which is using the Modbus TCP protocol to control some devices and sending the data to an HMI and to a SCADA solution in other network. The PLC M580 must be analysed to understand its process, Modbus communications and security requirements.
In the next figure, it is possible to see the second phase of the attack to illustrate all the next features:
 
<img width="894" height="616" alt="image" src="https://github.com/user-attachments/assets/1e59c13a-d310-425c-aae7-eafd389595e9" />

Now the next functionalities of the SithScope tool will be described:
1. Detection of the Modbus ID: As it has been possible to detect that the device is using the TCP 502 port related with Modbus TCP, the first thing to interact with the device is to detect the Modbus ID which can be done using a Modbus TCP request (native request) which will not be detected by any security implementation. With the Modbus slave ID detected, different Modbus native request now can be done.
2. The next functionality will analyse the different Modbus registers that the PLC has to know which are static and which are dynamic. This must be remarked due to it is important to exfiltrate information through different Modbus registers that don’t affect the production environment. So, if we write over a dynamic register, the PLC will overwrite our information so we couldn’t exfiltrate it and maybe we are affecting a production variable.

### 3. PHASE 3

In this phase, the files or information that want to be exfiltrated must be processed and prepared with in the SithScope tool. 
 
<img width="894" height="621" alt="image" src="https://github.com/user-attachments/assets/961808bb-6d5e-4905-bc5e-523e44432c02" />

For this research, a specific file has been created (but any of the files or any information that is in the EWS 1 could be exfiltrated). 

1. The use of the functionality number 4 in the SithScope will prepare the text “EXFILTRATED INFO!” to be written in the registers by order. Also, this functionality will encode/sanitize the data, that will be exfiltrated, to be read correctly in the SCADA and at the HMI. With this, the exfiltration can be done using a Modbus TCP native request using the legitimate PLC device and from the EWS 1. This request will be really hard to be detected, as the information will appear in the registry of Modbus which is also being used in the HMI visualization so anyone can see that critical data of the EWS 1 and also in other network, the supervision network, in which the SCADA (with public access on Internet) is configured.

### 4. PHASE 4

As have been said, the industrial protocol Modbus TCP has been used to exfiltrate information. First of all, in the next picture the 4 phases (two exfiltration) can be seen.

<img width="894" height="618" alt="image" src="https://github.com/user-attachments/assets/8c1c13c8-2aee-4ad2-9e1f-e814fc900544" />

The last functionality of the SithScope tool is prepared to send the data using the protocol Modbus TCP over the network to the registries of the PLC that have been detected as modifiable. 
The registries detected and used, are being implemented in the SCADA of the Workstation 2 in the Supervision Network and also by the HMI Magelis in the Control Network. These two data modifications have allowed an attacker to see the data in the HMI Magelis (Which also could be at Internet or that someone without permissions could read it.

---

## CONCLUSIONS

Different conclusion can be taken:
1. All the tool process use (in this, and possibly in many architectures) will be undetectable through the network because all the elements involved in the attack are using native requests of the protocol Modbus TCP with legitimate devices.
2. The firewall couldn’t detect the change in variables due to STRING variables were used, so for it, was a normal traffic sent by the EWS 1.
3. There are many attacks documented of exfiltration at industrial environments. 
4. The Modbus TCP protocol allow sending legitimate packages with STRING, WORD, DWORD data, etc. but also, other protocols like Bacnet, EthernetIP or OPC could be used to exfiltrate data through them.

---


## SAFETY & ETHICS

This content is intended for documentation and (if applicable) for defensive research in controlled, authorised laboratory environments only. Reproduction of operational techniques, vectors, or detailed attack procedures in public repositories is dangerous and irresponsible.

---

---

> © 2025 HackRTU
