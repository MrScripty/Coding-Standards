"""Agent-facing projection of value-free contract diagnostics.

The contracts runtime owns validator observations. This boundary supplies the
purpose-appropriate rejection and an explicit installed-input discovery request.
"""
from __future__ import annotations

from dataclasses import asdict

from tools.standards_contracts.standards_contracts import ContractFailure
from . import _generated_contract as c


def feedback_value(operation: str, failure: ContractFailure | None = None) -> dict:
    return {
        'issues': [asdict(item) for item in failure.input_issues] if failure else [],
        'truncated': failure.issues_truncated if failure else False,
        'describe_input': {'operation': operation},
    }


def invalid_input_result(purpose: str, operation: str,
                         failure: ContractFailure | None = None,
                         *, code: str = 'INTERFACE.INVALID_ARGUMENTS') -> dict:
    application = purpose == 'application'
    value = {
        'kind': 'application-rejected-result' if application else 'rejected-result',
        'code': 'APPLICATION.INPUT_INVALID' if application else code,
        'outcome': 'invalid',
        'message': 'Correct the indicated input fields; use describe_input for the exact contract.',
        'next_operations': [],
        'input_feedback': feedback_value(operation, failure),
    }
    if application:
        value['purpose'] = 'application'
    else:
        value['details'] = {}
    result_type = c.ApplicationRejectedResult if application else c.RejectedResult
    return result_type.from_value(value).as_contract()
