"""Conservative local AArch64 FP self-comparison triage.

No path-sensitive dataflow or numerical safety proof is claimed.
"""
import re

CMP = re.compile(r'^fcmp\s+([sd])(\d+),\s*\1\2$', re.I)
BR = re.compile(r'^b\.(vs|vc)\s+(?:loc_)?(0x[0-9a-f]+|[0-9a-f]+)$', re.I)
CV = re.compile(r'^fcvtzs\s+\S+,\s*([sd])(\d+)$', re.I)


def audit(records):
    """Classify each scalar conversion, failing closed on unverified paths."""
    addresses = {int(r['address'], 16): i for i, r in enumerate(records)}
    out = []
    for i, rec in enumerate(records):
        cv = CV.fullmatch(rec['instruction'].strip())
        if not cv:
            continue
        result = {'address': rec['address'], 'status': 'unknown_no_candidate'}
        for j in range(i - 2, -1, -1):
            cmp = CMP.fullmatch(records[j]['instruction'].strip())
            branch = BR.fullmatch(records[j + 1]['instruction'].strip())
            if not (cmp and branch):
                continue
            result['guard_address'] = records[j + 1]['address']
            if cmp.group(2) != cv.group(2) or cmp.group(1).lower() != cv.group(1).lower():
                result['status'] = 'unknown_different_register_or_width'
            else:
                target = addresses.get(int(branch.group(2), 16))
                if target is None:
                    result['status'] = 'unknown_branch_target'
                else:
                    nan_index = target if branch.group(1).lower() == 'vs' else j + 2
                    if nan_index == i:
                        result['status'] = 'nan_path_enters_conversion'
                    elif j + 2 != i:
                        result['status'] = 'unknown_intervening_instructions'
                    else:
                        result['status'] = 'candidate_local_pair_unverified'
            break
        out.append(result)
    return out
