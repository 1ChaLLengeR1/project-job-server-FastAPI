from decimal import ROUND_HALF_UP, Decimal

from api.response import ApiErrorData
from core.service.rental.family.response import (
    AllocationRuleInput,
    AllocationSettlementInput,
    BeneficiaryAllocationItemResponse,
    BeneficiaryAllocationResponse,
    FamilyAllocationResponse,
)

VALID_COMPONENTS = ("rent", "electricity", "water", "cost_type", "recurring")
VALID_MODES = ("fixed_amount", "full")

_COMPONENT_LABELS = {
    "rent": "czynsz",
    "electricity": "prąd",
    "water": "woda",
    "cost_type": "koszt",
    "recurring": "kwota stała",
}


def _round_grosze(value: float) -> float:
    return float(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _validate_rule(rule: AllocationRuleInput) -> str | None:
    if rule.component not in VALID_COMPONENTS:
        return f"Nieznany składnik reguły: '{rule.component}' (reguła {rule.rule_id})"
    if rule.mode not in VALID_MODES:
        return f"Nieznany tryb reguły: '{rule.mode}' (reguła {rule.rule_id})"
    if rule.component == "recurring" and rule.amount is None:
        return f"Reguła 'recurring' wymaga kwoty (reguła {rule.rule_id})"
    if rule.mode == "fixed_amount" and rule.component != "recurring" and rule.amount is None:
        return f"Reguła 'fixed_amount' wymaga kwoty (reguła {rule.rule_id})"
    if rule.component == "cost_type" and rule.cost_type_id is None:
        return f"Reguła 'cost_type' wymaga cost_type_id (reguła {rule.rule_id})"
    return None


def _matching_settlements(
    rule: AllocationRuleInput, settlements: list[AllocationSettlementInput]
) -> list[AllocationSettlementInput]:
    if rule.apartment_id is None:
        return settlements
    return [settlement for settlement in settlements if settlement.apartment_id == rule.apartment_id]


def _component_amount(rule: AllocationRuleInput, settlement: AllocationSettlementInput) -> float:
    if rule.component == "rent":
        return settlement.rent_amount
    if rule.component == "electricity":
        return settlement.electricity_cost
    if rule.component == "water":
        return settlement.water_cost
    # cost_type — suma pozycji rozliczenia z danym rodzajem kosztu (0, gdy mieszkanie go nie ma)
    return sum(item.amount for item in settlement.items if item.cost_type_id == rule.cost_type_id)


def _rule_label(rule: AllocationRuleInput) -> str:
    return rule.description or _COMPONENT_LABELS[rule.component]


def calculation_family_allocation(
    rules: list[AllocationRuleInput],
    settlements: list[AllocationSettlementInput],
) -> tuple[FamilyAllocationResponse | None, ApiErrorData | None, bool]:
    """Podział rozliczeń okresu na beneficjentów (sekcje "Ja / Ojciec / Mama" z notatek).

    - recurring: stała kwota niezależna od mieszkań (podatek -270, telefon +25),
    - fixed_amount: kwota reguły (czynsz Dudzik -> Ojciec 1100),
    - full: pełna kwota składnika z pasujących rozliczeń (cały prąd -> Ja,
      woda/śmieci/internet -> Mama), pozycja per mieszkanie jak w notatkach.
    """
    try:
        for rule in rules:
            validation_error = _validate_rule(rule)
            if validation_error:
                return (
                    None,
                    ApiErrorData(
                        message=validation_error,
                        type_module="calculation_family_allocation",
                        type_error="exception",
                        key_type_error="Exception",
                    ),
                    False,
                )

        items_by_beneficiary: dict[str, list[BeneficiaryAllocationItemResponse]] = {}
        for rule in rules:
            items_by_beneficiary.setdefault(rule.beneficiary_id, [])
            label = _rule_label(rule)

            if rule.component == "recurring":
                items_by_beneficiary[rule.beneficiary_id].append(
                    BeneficiaryAllocationItemResponse(
                        description=label,
                        amount=_round_grosze(rule.amount),
                        rule_id=rule.rule_id,
                    )
                )
                continue

            matching = _matching_settlements(rule, settlements)

            if rule.mode == "fixed_amount":
                if rule.apartment_id is not None and matching:
                    description = f"{label} - {matching[0].apartment_name}"
                    settlement_id = matching[0].settlement_id
                else:
                    description = label
                    settlement_id = None
                items_by_beneficiary[rule.beneficiary_id].append(
                    BeneficiaryAllocationItemResponse(
                        description=description,
                        amount=_round_grosze(rule.amount),
                        rule_id=rule.rule_id,
                        settlement_id=settlement_id,
                    )
                )
                continue

            # mode == "full" — pozycja per pasujące mieszkanie (jak "woda-dudzik: 64" w notatkach)
            for settlement in matching:
                items_by_beneficiary[rule.beneficiary_id].append(
                    BeneficiaryAllocationItemResponse(
                        description=f"{label} - {settlement.apartment_name}",
                        amount=_round_grosze(_component_amount(rule, settlement)),
                        rule_id=rule.rule_id,
                        settlement_id=settlement.settlement_id,
                    )
                )

        warnings = []
        for settlement in settlements:
            allocated = 0.0
            for rule in rules:
                if rule.component != "rent":
                    continue
                if rule.apartment_id is not None and rule.apartment_id != settlement.apartment_id:
                    continue
                allocated += settlement.rent_amount if rule.mode == "full" else (rule.amount or 0.0)
            allocated = _round_grosze(allocated)
            if allocated != _round_grosze(settlement.rent_amount):
                warnings.append(
                    f"Czynsz '{settlement.apartment_name}': rozdzielono {allocated} zł "
                    f"z {_round_grosze(settlement.rent_amount)} zł"
                )

        beneficiaries = [
            BeneficiaryAllocationResponse(
                beneficiary_id=beneficiary_id,
                total_amount=_round_grosze(sum(item.amount for item in items)),
                items=items,
            )
            for beneficiary_id, items in items_by_beneficiary.items()
        ]

        return FamilyAllocationResponse(beneficiaries=beneficiaries, warnings=warnings), None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="calculation_family_allocation",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
