# Labeling guide

Gold labels are the ground truth every model is measured against. An
inconsistent label is worse than a missing one: it punishes correct predictions.
When a case is not covered here, decide, **add the rule to this guide**, and
re-check earlier labels.

Labels follow [`LetterExtraction`](../src/bescheid/schema.py). The synthetic
sample [`data/samples/synthetic_mahnung_001.json`](../data/samples/synthetic_mahnung_001.json)
shows a complete label.

## General rules

- Label what the letter **says**, not what you know from elsewhere.
- Missing information is `null` (single values) or `[]` (lists). Never guess.
- Dates are ISO format: `2026-09-14`.
- Copy identifiers exactly as printed, including dots and slashes.
  Evaluation normalizes whitespace and case, nothing else.

## Fields

### `letter_type`
Pick the type that describes the letter's **main purpose**.

| Situation | Type |
|---|---|
| Tax assessment, also with a refund | `tax_assessment` |
| Broadcasting fee, waste fees, street cleaning | `fee_assessment` |
| Speeding ticket, parking fine | `fine` |
| Reminder for an existing debt, announcement of enforcement | `payment_reminder` |
| Approval, rejection or change of benefits | `benefit_decision` |
| Hearing (Anhörung), request to submit documents | `request_for_information` |
| Invitation or summons to an appointment | `appointment` |
| Anything else | `other` |

A fine with an attached hearing form is `fine` if an amount is already set,
`request_for_information` if the letter only asks for a statement.

### `issuing_authority`
The authority from the letterhead, including the sub-unit if printed
(`"Stadt Musterstadt, Stadtkasse"`). Not the clerk's name.

### `letter_date`
The date printed on the letter, not the postmark or the day you received it.

### `reference_number`
The identifier the recipient must quote in correspondence. Priority when several
appear: Aktenzeichen > Kassenzeichen > Steuernummer > Kundennummer.

### `action_required`
`true` if the recipient must pay, reply, submit documents or attend an
appointment. Purely informational letters and refunds without any required step
are `false`.

### `payments`
One entry per amount the recipient must transfer.
- If items and a total are listed, only the **total** is a payment.
- Refunds, credits and amounts already paid are not payments.
- Installment plans: one entry per installment with its own due date.
- `payment_reference` is what must be written in the transfer's reference field.

### `deadlines`
Every obligation with a **concrete calendar date**, including the payment
deadline (yes, it appears both in `payments` and in `deadlines`).
Relative periods ("within one month") are not deadlines; see `legal_remedy`.

`description` is a short German phrase. It is not scored, so keep it brief.

### `legal_remedy`
From the Rechtsbehelfsbelehrung at the end of the letter. `null` if there is none
(typical for reminders).
- `kind`: `einspruch` (tax), `widerspruch` (most other authorities), `klage`
  (when only a lawsuit is possible).
- `period_months`: usually `1`.
- `addressee`: where the remedy has to be filed, as printed.

### `summary`
One or two simple German sentences: what happened and what to do. Not scored
automatically.

## Checklist before committing a label

- [ ] `uv run bescheid validate-labels` passes
- [ ] Every amount and date checked twice against the document
- [ ] Only totals in `payments`
- [ ] IBAN has no spaces
