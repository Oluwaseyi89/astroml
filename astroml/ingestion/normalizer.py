"""Transaction normalizer for extracting structured data from Horizon operations."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from astroml.db.schema import NormalizedTransaction
from astroml.ingestion.parsers import (
    _PATH_PAYMENT_TYPES,
    _extract_amount,
    _extract_asset,
    _extract_destination,
    _parse_datetime,
    extract_path_payment_hops,
)


def normalize_operation(data: dict) -> NormalizedTransaction:
    """Transform raw horizon operation data into a NormalizedTransaction.

    For path payments use :func:`normalize_path_payment_hops` instead to
    get one record per hop.
    """
    op_type = data["type"]
    sender = data["source_account"]
    receiver = _extract_destination(data, op_type)

    amount_str = _extract_amount(data)
    amount = float(amount_str) if amount_str is not None else None

    asset_code, asset_issuer = _extract_asset(data)

    if asset_code == "XLM" and asset_issuer is None:
        normalized_asset = "XLM"
    else:
        normalized_asset = (
            f"{asset_code}:{asset_issuer}" if asset_code and asset_issuer else "UNKNOWN"
        )

    timestamp = _parse_datetime(data["created_at"])
    transaction_hash = data["transaction_hash"]

    return NormalizedTransaction(
        transaction_hash=transaction_hash,
        sender=sender,
        receiver=receiver,
        asset=normalized_asset,
        amount=amount,
        timestamp=timestamp,
    )


def normalize_path_payment_hops(data: dict) -> list[NormalizedTransaction]:
    """Return one NormalizedTransaction per hop for a path payment operation.

    Falls back to a single record (via :func:`normalize_operation`) for
    non-path-payment types so callers can use this function uniformly.
    """
    if data.get("type") not in _PATH_PAYMENT_TYPES:
        return [normalize_operation(data)]

    hops = extract_path_payment_hops(data)
    if not hops:
        return [normalize_operation(data)]

    timestamp = _parse_datetime(data["created_at"])
    transaction_hash = data["transaction_hash"]

    return [
        NormalizedTransaction(
            transaction_hash=f"{transaction_hash}_hop{hop['hop_index']}",
            sender=hop["from_account"],
            receiver=hop["to_account"],
            asset=hop["asset"],
            amount=hop["amount"],
            timestamp=timestamp,
        )
        for hop in hops
    ]


_SNAPSHOT_FIELDS = ("transaction_hash", "sender", "receiver", "asset", "amount", "timestamp")


def snapshot_transaction(tx: NormalizedTransaction) -> dict[str, Any]:
    """Serialise a NormalizedTransaction into a JSON-safe snapshot dict (issue #978).

    Args:
        tx: The normalized transaction to snapshot.

    Returns:
        Dict with the normalized fields; ``timestamp`` is ISO-8601 and
        ``amount`` is a float (or None).
    """
    return {
        "transaction_hash": tx.transaction_hash,
        "sender": tx.sender,
        "receiver": tx.receiver,
        "asset": tx.asset,
        "amount": float(tx.amount) if tx.amount is not None else None,
        "timestamp": tx.timestamp.isoformat(),
    }


def restore_transaction(snapshot: dict[str, Any]) -> NormalizedTransaction:
    """Rebuild a NormalizedTransaction from :func:`snapshot_transaction` output (issue #978).

    Args:
        snapshot: Snapshot dict containing every normalized field.

    Returns:
        A new, unpersisted NormalizedTransaction.

    Raises:
        ValueError: if a required field is missing or the timestamp is invalid.
    """
    missing = [f for f in _SNAPSHOT_FIELDS if f not in snapshot]
    if missing:
        raise ValueError(f"snapshot missing fields: {missing}")
    amount = snapshot["amount"]
    return NormalizedTransaction(
        transaction_hash=snapshot["transaction_hash"],
        sender=snapshot["sender"],
        receiver=snapshot["receiver"],
        asset=snapshot["asset"],
        amount=float(amount) if amount is not None else None,
        timestamp=datetime.fromisoformat(snapshot["timestamp"]),
    )
