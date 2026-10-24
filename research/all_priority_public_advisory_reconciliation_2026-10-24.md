# All-priority public advisory reconciliation — 2026-10-24

## Primary source and exact candidate reconciliation

Primary source: Apple, [About the security content of iOS 26.7 and iPadOS 26.7](https://support.apple.com/en-us/149041), released September 14, 2026. Apple's affected-device scope for the entries below is iPhone 11 and later, which includes iPhone 16 Plus.

The 12 project candidates below are all explicitly present in this Apple bulletin. This closes the earlier source-coverage gap for these candidate IDs. It does **not** establish that a vulnerable path is reachable on target build iOS 26.6.1 (23G83), nor that a usable exploit primitive exists.

| Priority | CVE | Apple component | Apple-published impact | Apple fix summary | Practical implication for Freedom27 |
|---|---|---|---|---|---|
| P1 | CVE-2026-84607 | AVEVideoEncoder | Sandboxed app may execute arbitrary code with kernel privileges | Race condition; improved state management | Highest-impact lead, but no exact-build state transition, patch diff, or reproduction is established |
| P1 | CVE-2026-43689 | Kernel | Malicious app may gain root privileges | Permissions issue; additional restrictions | Root privilege impact does not itself prove kernel code execution or an initial sandbox escape |
| P2 | CVE-2026-84523 | APFS | App may cause unexpected system termination or write kernel memory | Out-of-bounds write; improved bounds checking | Potentially high impact, but exact operation and bounds invariant remain unknown |
| P2 | CVE-2026-84566 | Kernel | Local attacker may cause unexpected system termination or corrupt kernel memory | Improved memory handling | Generic kernel-memory impact; object, caller, and reachable operation remain unknown |
| P2 | CVE-2026-43684 | Kernel | App may cause unexpected system termination or corrupt kernel memory | Use-after-free; improved memory management | Object lifetime and trigger conditions remain unknown |
| P2 | CVE-2026-43686 | Kernel | Connection to malicious NFS server may cause kernel memory corruption | Use-after-free; improved memory management | Requires the relevant NFS path; no target reproduction or patch diff established |
| P2 | CVE-2026-28968 | Kernel | App may cause unexpected system termination or corrupt kernel memory | Out-of-bounds write; improved bounds checking | Structure and arithmetic invariant remain unknown |
| P3 | CVE-2026-86876 | CoreMedia | Sandboxed process may circumvent sandbox restrictions | Out-of-bounds write; improved bounds checking | Sandbox-impact candidate; exact media path and reachable condition remain unknown |
| P3 | CVE-2026-86886 | TCC | App may modify protected system files | Path traversal; improved input validation | File-protection bypass candidate; exact path resolution and authorization path remain unknown |
| P4 | CVE-2026-43687 | Kernel | Connection to malicious NFS server may disclose kernel memory | Improved memory handling | Disclosure alone is not an entry point; NFS preconditions and data source remain unknown |
| P4 | CVE-2026-65405 | Kernel | App may determine kernel memory layout | Memory initialization issue; improved memory handling | Information disclosure only; practical value on this build remains unestablished |
| P4 | CVE-2026-84622 | Kernel | App with root privileges may read uninitialized kernel memory | Memory initialization issue; improved memory handling | Explicit root prerequisite means it is not established as an initial entry point |

## Source verification notes

The entries above were cross-checked by exact CVE identifier against Apple's primary bulletin:

- AVEVideoEncoder CVE-2026-84607: race condition / kernel-privilege code execution, state management.
- Kernel CVE-2026-43689: permissions / root privileges, additional restrictions.
- APFS CVE-2026-84523: out-of-bounds write, bounds checking.
- Kernel CVE-2026-84566: memory handling.
- Kernel CVE-2026-43684 and CVE-2026-43686: use-after-free / memory management, with the latter explicitly tied to a malicious NFS server.
- Kernel CVE-2026-28968: out-of-bounds write / bounds checking.
- CoreMedia CVE-2026-86876: out-of-bounds write / bounds checking, sandbox restrictions.
- TCC CVE-2026-86886: path traversal / input validation, protected system files.
- Kernel CVE-2026-43687: malicious NFS server / kernel memory disclosure.
- Kernel CVE-2026-65405: memory initialization / kernel memory layout disclosure.
- Kernel CVE-2026-84622: root-privileged app / uninitialized kernel memory.

## What the advisory does and does not prove

Apple's advisory provides component, high-level impact, fix class, and affected-product scope. It does not provide source-level patch diffs or establish a vulnerable code path for the exact 23G83 firmware. The target iOS 26.6.1 build is within the release sequence preceding iOS 26.7, but version chronology alone is not sufficient to prove the exact target binary is vulnerable.

## Safe validation properties

| Candidate | Non-weaponized regression property |
|---|---|
| CVE-2026-84607 | Invalid or concurrent lifecycle transitions must not violate authorization/state invariants |
| CVE-2026-43689 | Unauthorized callers remain denied on every entry path |
| CVE-2026-84523 | Bounds and arithmetic checks reject overflow and out-of-range operations |
| CVE-2026-84566 | Ownership and error-path handling preserve memory invariants |
| CVE-2026-43684 | Reference lifetime and cleanup ordering remain valid |
| CVE-2026-43686 | NFS request ownership/lifecycle remains valid on errors and teardown |
| CVE-2026-28968 | Structure bounds and arithmetic validation are enforced |
| CVE-2026-86876 | Media processing cannot bypass sandbox policy; bounds checks hold |
| CVE-2026-86886 | Authorization uses canonical resolved paths and rejects traversal |
| CVE-2026-43687 | NFS responses expose only initialized, authorized bytes |
| CVE-2026-65405 | User-visible outputs do not expose unauthorized kernel addresses/data |
| CVE-2026-84622 | Copyout fields are initialized and root prerequisite is explicitly enforced |

These are test properties for a vendor-controlled model or source-level test harness, not triggers for a live device. No exploit choreography, payload, or real-device malicious server test is proposed.

## Remaining evidence gates

1. **Target and fixed-build firmware inventory:** hash-gated BuildManifest inventories are being generated by CI. These contain metadata only and are not a patch diff.
2. **Exact component comparison:** requires verified component payload bytes and reproducible extraction tooling. BuildManifest digest changes alone do not attribute a CVE.
3. **Patch attribution:** no exact source diff was established in this review. If Apple does not publish one, record that limitation rather than infer a fix from names or strings.
4. **Exact-build applicability and exploitability:** unverified until a code path is evidenced and a safe, reproducible validation establishes reachability. A jailbreak is not verified.

## Safety and scope

This is public-advisory and read-only firmware research. No exploit was executed, no device was accessed or modified, and no jailbreak functionality is claimed.
