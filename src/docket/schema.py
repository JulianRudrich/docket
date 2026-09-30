"""Target schema for extracting information from German administrative letters.

This schema is the contract of the whole project: labels, model outputs and the
evaluation all use it. Changing a field means relabeling data, so every change
must be recorded in docs/decisions/.

Field descriptions are sent to the model as part of the JSON schema, so they are
written as instructions.
"""

from __future__ import annotations

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

SCHEMA_VERSION = "1.0"


class LetterType(StrEnum):
    TAX_ASSESSMENT = "tax_assessment"
    """Steuerbescheid (income tax, property tax, vehicle tax, ...)."""
    FEE_ASSESSMENT = "fee_assessment"
    """Gebühren-/Beitragsbescheid (broadcasting fee, waste collection, ...)."""
    FINE = "fine"
    """Bußgeldbescheid, Verwarnungsgeld."""
    PAYMENT_REMINDER = "payment_reminder"
    """Mahnung, Zahlungserinnerung, Vollstreckungsankündigung."""
    BENEFIT_DECISION = "benefit_decision"
    """Bewilligungs-, Ablehnungs- or Änderungsbescheid (Bürgergeld, BAföG, Elterngeld, ...)."""
    REQUEST_FOR_INFORMATION = "request_for_information"
    """Anhörung, Aufforderung zur Mitwirkung, request to submit documents."""
    APPOINTMENT = "appointment"
    """Einladung, Vorladung, Termin."""
    OTHER = "other"


class DeadlineKind(StrEnum):
    PAYMENT = "payment"
    RESPONSE = "response"
    DOCUMENT_SUBMISSION = "document_submission"
    APPOINTMENT = "appointment"
    OTHER = "other"


class LegalRemedyKind(StrEnum):
    EINSPRUCH = "einspruch"
    WIDERSPRUCH = "widerspruch"
    KLAGE = "klage"
    OTHER = "other"


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Payment(_Strict):
    amount_eur: float = Field(
        description="Amount the recipient has to pay, in EUR. Use a dot as decimal separator."
    )
    due_date: date | None = Field(description="Date by which the amount must be paid, if stated.")
    iban: str | None = Field(description="IBAN of the receiving account, without spaces.")
    payment_reference: str | None = Field(
        description="Verwendungszweck or Kassenzeichen that must be quoted with the payment."
    )


class Deadline(_Strict):
    kind: DeadlineKind
    due_date: date = Field(description="The concrete calendar date of the deadline.")
    description: str = Field(
        description="Short German description of what must be done by this date."
    )


class LegalRemedy(_Strict):
    kind: LegalRemedyKind
    period_months: int | None = Field(
        description="Length of the period in months (usually 1), counted from notification."
    )
    addressee: str | None = Field(
        description="Authority or court where the remedy has to be filed."
    )


class LetterExtraction(_Strict):
    """Everything a recipient needs to know to act on an administrative letter."""

    letter_type: LetterType
    issuing_authority: str = Field(
        description="Name of the authority as printed in the letterhead, "
        "e.g. 'Finanzamt Köln-Mitte'."
    )
    letter_date: date | None = Field(description="Date printed on the letter.")
    reference_number: str | None = Field(
        description="Primary case identifier (Aktenzeichen, Steuernummer, Beitragsnummer, ...)."
    )
    action_required: bool = Field(
        description="True if the recipient must do something (pay, reply, submit, attend)."
    )
    payments: list[Payment] = Field(
        description="Payments the recipient must make. Empty if nothing has to be paid."
    )
    deadlines: list[Deadline] = Field(
        description="Deadlines with a concrete calendar date. Do not invent dates."
    )
    legal_remedy: LegalRemedy | None = Field(
        description="Rechtsbehelfsbelehrung, if the letter contains one."
    )
    summary: str = Field(
        description="One or two plain-language German sentences: what the letter is about "
        "and what the recipient has to do."
    )
