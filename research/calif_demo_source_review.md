# Calif iOS 27.0.1 demonstration — source review

**Review date:** 2026-10-23  
**Project:** Freedom27  
**Purpose:** Separate public evidence from assumptions before changing compatibility or exploit status.

## Executive result

The public record supports that Calif announced demonstrations at Hexacon on 2026-10-16 and said the work would be released “in due time.” Independent reporting describes an iPhone 18 Pro running iOS 27.0.1 returning to a root SSH session after reboot. However, the reviewed primary material does **not** disclose the jailbreak chain, publish source code or a consumer tool, or establish support for other devices/builds.

**Freedom27 status remains research-only.** This demonstration is not an installable release and does not establish that Freedom27 can reproduce it.

## Sources reviewed

1. **Calif’s own announcement** — https://blog.calif.io/p/iphone  
   Dated 2026-10-16. It lists four demonstrations and says “Everything will be released in due time.” The post is primary evidence that Calif announced demos and its stated release intention; it is not a technical write-up or download.
2. **Decrypt’s on-site report** — https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot  
   Dated 2026-10-16. Reports the iPhone 18 Pro / iOS 27.0.1 demonstration and root access after reboot, based on stage video and researcher Billy Ellis’s post. This is secondary reporting, not source code.
3. **iClarified report** — https://www.iclarified.com/102876/untethered-ios-2701-jailbreak-demonstrated-on-iphone-18-pro-video  
   Dated 2026-10-17. Reports that the demo terminal identified hardware as `iPhone19,2`; this is a reported observation, not an independently reproduced Freedom27 result.
4. **Apple security advisory lead for CVE-2026-28968** — https://support.apple.com/en-us/149036  
   A security issue credited in part to Calif researchers is relevant context, but no reviewed source connects it to the Hexacon jailbreak chain.
5. **Apple security advisory lead for CVE-2026-86886** — https://support.apple.com/en-us/149041  
   Also relevant context only. No reviewed source establishes that this issue was used in the demo.

## Evidence assessment

| Claim | Assessment | What Freedom27 may record |
|---|---|---|
| Calif announced iPhone security demos at Hexacon | Confirmed by Calif’s own post | Primary-source announcement exists |
| An iPhone 18 Pro running iOS 27.0.1 was shown with root access returning after reboot | Reported by multiple outlets based on public video | External demo report; not reproduced by Freedom27 |
| Exact model identifier `iPhone19,2` | Reported by iClarified from terminal output | Treat as reported metadata, not independently verified hardware identification |
| The chain uses CVE-2026-28968 or CVE-2026-86886 | **Unconfirmed** | Keep both as unverified research leads; do not associate either with the chain |
| Other iPhone 18 variants or older iPhones are supported | **Unknown** | No compatibility inference |
| A public jailbreak download, source repository, install guide, or release date exists | **Not found in reviewed sources** | Do not direct users to unofficial downloads or claim it is installable |
| Freedom27 can reproduce the demo | **No evidence** | Remains unimplemented and untested |

## Important limitation on newer claims

A third-party tracker surfaced during this review claims a later interview discusses disclosure after Apple patches and possible changes in a beta release. This review did not verify that interview against a directly accessible primary interview transcript or Calif technical publication, so those claims are **not adopted as project facts**. Re-check the original interview and Apple’s current release/security notes before updating patch status or recommending any firmware decision.

## Evidence required before changing status

- A direct technical publication from Calif or the researchers naming the relevant vulnerabilities and explaining the chain.
- Public source code or a reproducible proof of concept with provenance and a license, if released.
- Exact device model, OS version/build, and explicit limitations from the original researchers.
- Independent reproduction or a documented validation process before marking any Freedom27 capability as verified.
- A separate, clearly documented user-facing installation/bootstrap method before calling anything a usable jailbreak.

## Next action

Monitor Calif’s official post and Apple’s security advisories. Update the evidence ledger only when a new primary source changes a specific claim. Do not infer a tool release from “in due time,” infer broad compatibility from one demonstration, or treat related CVE credits as proof of exploit-chain membership.
